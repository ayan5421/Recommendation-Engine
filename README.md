# Recommendation-Engine
Recommendation Engine for Microsoft Engage Project
Using TMDB 5000 movies dataset
Using Content based Filtering
# TMDB 5000 Movie Dataset Analysis

### Data
The Movie Database provides two datasets:
tmdb_5000_movies.csv (Movie credits data):
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

* tmdb_5000_credits.csv:
- movie_id
- title
- cast
- crew
We will merge the two datasets in order to get all the informations about the actors and the directors of their relative movie.

### The files
- Write A Data Science Blog Postipynb: code notebook
- Write A Data Science Blog Post.html

### The libraries used 
- NumPy
- pandas
- Sklearn / scikit-learn
- Matplotlib (for data visualization)

### A summary of the results: 
Through clustering , we have noticed that, revenue, profit, vote count, budget, popularity, Adventure genre , Action genre have a positive correlation, that mean this attribute tend to increase together.
We can say that Adventure and Action genre tend to Increase revenue, profit, vote count, budget, popularity.

runtime, Drama, History, vote average, War genre, France country , United Kingdom country , Italy country , Sweden country , Denmark country and Germany country have a positive correlation, that mean this attribute tend to increase together. And they have a negative correlation with Comedy genre, United States of America country , Family genre and Animation genre.
We can say that Europe countries tend to watch Drama, History, and War films. While America tends to watch Comedy, Family and Animation films.
## Introduction

This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
- Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe (|) characters.
- There are some odd characters in the ‘cast’ column. Don’t worry about cleaning them. You can leave them as is.
- The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.


## Objectives:

- Know all the steps involved in a typical data analysis process
- Be comfortable posing questions that can be answered with a given dataset and then answering those questions
- Investigate problems in a dataset and wrangle the data into a format that can be used
- Communicating the results of your analysis


## **Softwares needed:**
*You will need an installation of Python, plus the following libraries:
1. pandas
2. NumPy
3. Matplotlib
4. csv

* A text editor, like _VS Code_ or _Atom_.
* A terminal application (_Terminal_ on _Mac_ and _Linux_ or _Cygwin_ on _Windows_).


## **Installation links for softwares:**
* [Git for windows - for terminal application using Git Bash](https://gitforwindows.org/)
* [Python using Anaconda (latest version for windows)](https://www.anaconda.com/distribution/)
* [Visual Studio Code Editor (for windows)](https://code.visualstudio.com/docs/setup/windows)


## References:
1. [TMDB Movies Datasets](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
2. [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
3. [Matplotlib Documentation](https://matplotlib.org/)
