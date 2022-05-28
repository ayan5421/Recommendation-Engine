from pathlib import Path
import streamlit as st
import pickle as pk
import pandas as pd
import requests as req

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

movie_list = ['Select Movie']
for i in range(0,len(movies)):
    movie_list.append(movies['original_title'][i])

with st.sidebar:
    st.title('Remsik Movie Recommender')
    option = st.selectbox(
        'Select a movie you like',
        movie_list)
    if option =='Select Movie':
        st.write('No movie selected')
    else:
        st.write('You selected:')
        st.header(option)
        poster(movies.iloc[movies[movies['original_title'] == option].index[0]].id)

col1, col2 = st.columns([3,1])
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