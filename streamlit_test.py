import streamlit as st
import pickle
import pandas as pd
import requests



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    
    for i in movie_list:
        # fetch the movie poster
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names


st.header('Movie Recommender System')
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Show Recommendation'):
    recommendations=recommend(selected_movie)
    for i in recommendations:
        st.write(i)
