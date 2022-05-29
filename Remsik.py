from operator import index
from pathlib import Path
from streamlit_option_menu import option_menu
import streamlit as st
import streamlit_authenticator as sa
import pickle as pk
import pandas as pd
import requests as req
import sqlite3
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///user_data.db')

#opening files
movies_dictionary = pk.load(open(Path(__file__).parent/'movies_dictionary.pkl','rb'))
movies = pd.DataFrame(movies_dictionary)
sim = pk.load(open(Path(__file__).parent/'sim.pkl','rb'))


#function to fetch poster from tmdb database using movie id
def poster(id):
    poster_json = (req.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(id))).json()
    st.image('https://image.tmdb.org/t/p/original' + str(poster_json['poster_path']), caption=movies.iloc[movies[movies['id'] == id].index[0]].tagline)


#function to recommend movie ids on given movie id
def recommend(mov,count):
    a = 6 + count*5
    mov_index = movies[movies['original_title'] == mov].index[0]
    mov_list = sorted(list(enumerate(sim[mov_index])), reverse=True, key=lambda x: x[1])[a-5:a]
    movie_id = []
    for i in mov_list:
        movie_id.append(movies['id'][i[0]])
    return movie_id


#creating the login and signup menu
with st.sidebar:
    st.title('Remsik Movie Recommender')
    status = option_menu(menu_title=None,options=['SignUp','Login'],icons=['person-plus-fill','person-check-fill'],orientation='horizontal')

#creating the signup form and storing the given data in the database
if status == 'SignUp':
    authentication_status=None
    with st.form(key='signup_form',clear_on_submit=True):
        st.subheader('REMSIK MOVIE RECOMMENDER SIGNUP')
        name = st.text_input('Enter your Name')
        username = st.text_input('Enter a Username (This will be used during Login)')
        password = st.text_input('Password',type='password')
        confirm_password = st.text_input('Confirm Password',type='password')
        submit = st.form_submit_button("SignUp")
        if submit == True and password == confirm_password:
            hashed_password = sa.Hasher([password]).generate()
            user_details = pd.read_sql('user_details',engine)
            duplicate =0
            for i in range(0,len(user_details)):
                if user_details['username'][i]==username:
                    duplicate =1
                    break
            if duplicate==0:
                data = pd.DataFrame([{'name':name,'username':username,'hashed_password':hashed_password[0]}])
                data.to_sql('user_details',engine,if_exists='append',index=False)
                st.info('Go to Login menu to login')
            else:
                st.warning('The username is already taken... Create another username')
        elif submit == True and password != confirm_password:
            st.warning("Password and Confirm Password doesn't match")
#for login
elif status == 'Login':
    user_details = pd.read_sql('user_details',engine)
    authenticator = sa.Authenticate(user_details['name'].values,user_details['username'].values,user_details['hashed_password'].values,'remsik_recommender','abc123',cookie_expiry_days=7)
    name, authentication_status, username = authenticator.login('REMSIK MOVIE RECOMMENDER LOGIN')


#user authentication
if authentication_status==False:
    st.error('Username/Password Incorrect')
#after authentication the interface
elif authentication_status == True:
    movie_list = ['Select Movie']
    for i in range(0,len(movies)):
        movie_list.append(movies['original_title'][i])

    with st.sidebar:
        st.subheader('Welcome ' + name + ' !!')
        authenticator.logout('LOGOUT')
        option = st.selectbox('Select a movie you like',options = movie_list)
        if option =='Select Movie':
            st.write('No movie selected')
        else:
            st.write('You selected:')
            st.header(option)
            poster(movies.iloc[movies[movies['original_title'] == option].index[0]].id)
        if option !=  'Select Movie':
            user_movie = pd.DataFrame([{'id':str(movies.iloc[movies[movies['original_title'] == option].index[0]].id)}])
            user_movie.to_sql('user_movies_'+username,engine,if_exists='append',index=False)

    menu = option_menu(menu_title=None,options=['Recommendations','Profile'],icons=['book-half','person-bounding-box'],orientation='horizontal')

    if menu=='Recommendations':
        col1, col2, = st.columns([3,1])
        with col1:
            st.header('Your Suggesions:')
        with col2:
            count = st.number_input('Page number', min_value=1, step=1) - 1

        if option == 'Select Movie':
            st.write('Select a movie first !')
        else:
            recommended = recommend(option,count)
            for i in range(0,5):
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.header('')
                        poster(recommended[i])
                        st.caption('Released : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].release_date)
                        st.caption('Run Time : ' + str(movies.iloc[movies[movies['id'] == recommended[i]].index[0]].runtime) + ' mins')
                    with col2:
                        st.header(movies.iloc[movies[movies['id'] == recommended[i]].index[0]].original_title)
                        st.caption('Genres : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].genres)
                        st.caption('Overview : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].overview)
                        st.caption('Director : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].director)
                        st.caption('Producer : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].producer)
                        st.caption('Cast : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].cast)
                        st.caption('Produced By : ' + movies.iloc[movies[movies['id'] == recommended[i]].index[0]].production_companies)
                        st.caption('Homepage : ' + str(movies.iloc[movies[movies['id'] == recommended[i]].index[0]].homepage))
    elif menu=='Profile':
        st.subheader('Pleasure to have you back '+ name)
        st.write('Want to change password ?')
        with st.form(key='password_change_form',clear_on_submit=True):
            new_password = st.text_input('Enter new Password',type='password')
            if st.form_submit_button('Change Password'):
                user_details = pd.read_sql('user_details',engine)
                hashed_new_password = sa.Hasher([new_password]).generate()
                user_details.loc[user_details[user_details['username']==username].index[0],'hashed_password'] = hashed_new_password[0]
                user_details.to_sql('user_details',engine,if_exists='replace',index=False)
                st.success('Password Changed Successfully')
        with st.container():
            st.subheader('You searched for these movies back :')
            try:
                movie_record = pd.read_sql('user_movies_' + username,engine)
                length = len(movie_record)
                new = pd.DataFrame([{'id':movie_record['id'][0]}])
                for i in range(0,len(movie_record)-1):
                    if movie_record['id'][i] != movie_record['id'][i+1]:
                        new = new.append({'id':movie_record['id'][i+1]},ignore_index=True)
                new.to_sql('user_movies_' + username,engine,if_exists='replace',index=False)
                if len(new)<=5:
                    effective = len(new)
                else:
                    effective = 5
                col = st.columns(effective)
                for i in range(0,effective):
                    with col[i]:
                        st.text(movies.iloc[movies[movies['id'] == int(new['id'][len(new) -1 -i])].index[0]].original_title)
                        poster(int(new['id'][len(new) -1 -i]))
            except:
                st.caption('Everything seems so quiet here... Search for movies first')