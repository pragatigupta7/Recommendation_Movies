import pickle
import streamlit as st
import requests
import os
import base64


# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=74b97bfa205303a9ed126ff4e1c62c16&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json() 
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w780/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters
st.markdown("<h1 style='color: red;'>Movie Recommender System</h1>", unsafe_allow_html=True)
# st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

# Custom label using HTML & CSS
st.markdown("""
    <style>
        .custom-label {
            font-size: 18px;  /* Change font size */
            font-weight: bold; /* Make it bold */
            color: white; /* Change text color */
        }
    </style>
    <p class="custom-label">Type or select a movie from the dropdown:</p>
""", unsafe_allow_html=True)


selected_movie = st.selectbox("",movie_list
)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

def set_bg_local(image_path):
    abs_path = os.path.abspath(image_path)  # Get absolute path
    with open(abs_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_local(r"D:\Movie Recommendation Project\image\background.jpg")  # Make sure the path is correct