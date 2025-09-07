import streamlit as st
import pickle
import pandas as pd
import requests


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])[1:6]
    recomended_movies=[]
    for i in distances:
        movie_id=i[0]
        recomended_movies.append(movies.iloc[i[0]].title)
    return recomended_movies

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
st.title('movie recomendation system')

similarity=pickle.load(open('similarity.pkl','rb'))


option = st.selectbox(
    "select movies", movies['title'].values)

if st.button('recommend'):
    recomendations=recommend(option)