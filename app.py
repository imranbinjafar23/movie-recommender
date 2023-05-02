import streamlit as st
import pickle
import pandas as pd
import requests

movies_df = pickle.load(open('movies.pkl','rb'))
movies_list_df = pd.DataFrame(movies_df)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=f8ab1aaaa1f0dbd6f5e2f1667bebd153&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def recommend(movie):
    movie_index = movies_list_df[movies_list_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_list_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_list_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('!~ Movie Recommender System ~!')
st.write('Hi, welcome to the Movie Recommender System!')
st.subheader('About this app')
description = "This app recommends English movies based on the similarity between the selected movie and 5000 other movies in the TMDB database. The similarity between movies is calculated using a machine learning algorithm trained on movie features such as cast, crew, genres, and keywords. Simply select a movie from the dropdown menu and click the 'Recommend' button to see the top five recommended movies!"
st.text_area(label='', value=description, height=150)

selected_movie_name = st.selectbox(
    'Please select a movie from the following list & click Recommend button:',
    movies_list_df['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# Add footer text and link
st.markdown("""
            [Developed By: Imran Bin Jafar (GitHub Repository)](https://github.com/imranbinjafar23/movie-recommender.git)
            """)