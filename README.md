# Recommendation-Engine
Recommendation Engine for Microsoft Engage Project, using [TMDB 5000 movies datasets](https://www.kaggle.com/tmdb/tmdb-movie-metadata),using Content based Filtering
## Link to the web application
[Remsik Movie Recommender](https://remsik-movie-recommender.herokuapp.com/)
## Data
The Movie Database provides two datasets:
### tmdb_5000_movies.csv:
- budget
- genres
- homepage
- id
- keywords
- original_language
- original_title
- overview
- popularity
- production_companies
- production_countries
- release_date
- revenue
- runtime
- spoken_languages
- status
- tagline
- title
- vote_average
- vote_count

### tmdb_5000_credits.csv:
- movie_id
- title
- cast
- crew
We merged the two datasets in order to get all the informations about the actors and the directors of their relative movie.

## The libraries used 
- numpy
- pandas
- Sklearn / scikit-learn
- ast module
- nltk (Natural Language Toolkit)
- pickle
- streamlit
- requests

## Process:
We are using the 2 files of the dataset in pre-processing (using Movie Recommender.ipynb) and then generating 2 new files 'movies_dictionary.pkl' and 'sim.pkl'. These 2 files are then used by Remsik.py to predict the recommendations for a given movie by the user. Content based Filtering is used here, so the steps in pre-processing involve creating tags for each and every movie and after that vectorizing each movie and then creating a matrix containig the cosine distances (similarity score) between each and every movie. That similarity score is used to recommend movies by Remsik.py (more the score, similar are the movies).
