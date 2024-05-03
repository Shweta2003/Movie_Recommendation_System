import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

st.set_page_config(layout='wide')

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=631b4cb3c7491ba88ecea1f3fa154198&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        #TMDB credentials
        #username : blossomshweta2003
        #password : 1234
        #fetch movie posters
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommendation System')
option = st.selectbox(
    'Select a movie?',
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    with col1:
        st.image(posters[0])
        st.markdown("<h3 style='position:relative;font-size: 25px;height: 125px;width: 100%;text-align: center;padding: 0px;'>{}</h1>".format(names[0]), unsafe_allow_html = True)

    with col2:
        st.image(posters[1])
        st.markdown("<h3 style='position:relative;font-size: 25px;height: 125px;width: 100%;text-align: center;padding: 0px;'>{}</h1>".format(names[1]), unsafe_allow_html=True)

    with col3:
        st.image(posters[2])
        st.markdown("<h3 style='position:relative;font-size: 25px;height: 125px;width: 100%;text-align: center;padding: 0px;'>{}</h1>".format(names[2]), unsafe_allow_html=True)

    with col4:
        st.image(posters[3])
        st.markdown("<h3 style='position:relative;font-size: 25px;height: 125px;width: 100%;text-align: center;padding: 0px;'>{}</h1>".format(names[3]), unsafe_allow_html=True)

    with col5:
        st.image(posters[4])
        st.markdown("<h3 style='position:relative;font-size: 25px;height: 125px;width: 100%;text-align: center;padding: 0px;'>{}</h1>".format(names[4]), unsafe_allow_html=True)

