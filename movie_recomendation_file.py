#!/usr/bin/env python
# coding: utf-8
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# In[1]:
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[2]:


movies = pd.read_csv("tmdb_5000_movies.csv.zip")
credits = pd.read_csv('tmdb_5000_credits.csv.zip')


# In[3]:


movies = movies.merge(credits,on='title')


# In[4]:


movies.head()


# In[5]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.head()


# In[6]:


import ast


# In[7]:


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 


# In[8]:


movies.dropna(inplace=True)


# In[9]:


movies['genres'] = movies['genres'].apply(convert)
movies.head()


# In[10]:


movies['keywords'] = movies['keywords'].apply(convert)
movies.head()


# In[11]:


ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[12]:


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 


# In[13]:


movies['cast'] = movies['cast'].apply(convert)
movies.head()


# In[14]:


movies['cast'] = movies['cast'].apply(lambda x:x[0:3])


# In[15]:


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


# In[16]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[17]:


movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.sample(5)


# In[18]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[19]:


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


# In[20]:


movies.head()


# In[36]:


movies['title']


# In[21]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[22]:


new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
new.head()


# In[23]:


new['tags'] = new['tags'].apply(lambda x: " ".join(x))
new.head()


# In[24]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[25]:


vector = cv.fit_transform(new['tags']).toarray()
vector.shape


# In[26]:


from sklearn.metrics.pairwise import cosine_similarity


# In[27]:


similarity = cosine_similarity(vector)


# In[28]:


similarity


# In[29]:


new[new['title'] == 'The Lego Movie'].index[0]


# In[30]:


def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)


# In[31]:


recommend('Avatar')


# In[32]:


recommend('Gandhi')


# In[33]:


recommend('John Carter')


# In[38]:


recommend('Avengers: Age of Ultron')


import pickle

pickle.dump(new,open('movies_dict.pkl','wb'))
pickle.dump(new.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))




