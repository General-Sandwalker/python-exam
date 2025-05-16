import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Get API URL from environment variable
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Set page title and configuration
st.set_page_config(
    page_title="Movie Explorer",
    page_icon="🎬",
    layout="wide"
)

# App title and description
st.title("🎬 Movie & Actor Explorer")
st.markdown("Click the button below to discover a random movie and its actors.")

# Initialize session state if not already initialized
if "movie" not in st.session_state:
    st.session_state.movie = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# Function to fetch a random movie from the API
def get_random_movie():
    try:
        response = requests.get(f"{API_URL}/movies/random/")
        if response.status_code == 200:
            st.session_state.movie = response.json()
            # Clear the previous summary when loading a new movie
            st.session_state.summary = None
            return True
        else:
            st.error(f"Error fetching movie: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return False

# Function to get a summary for the current movie
def get_movie_summary():
    if st.session_state.movie:
        try:
            movie_id = st.session_state.movie["id"]
            response = requests.post(
                f"{API_URL}/generate_summary/",
                json={"movie_id": movie_id}
            )
            if response.status_code == 200:
                st.session_state.summary = response.json()["summary_text"]
                return True
            else:
                st.error(f"Error getting summary: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            st.error(f"Error connecting to the API: {e}")
            return False

# UI Components
col1, col2, col3 = st.columns([1, 1, 1])

# Random Movie Button in the first column
with col1:
    if st.button("Show Random Movie", use_container_width=True):
        get_random_movie()

# Get Summary Button in the second column (only enabled if a movie is loaded)
with col2:
    if st.session_state.movie:
        if st.button("Get Summary", use_container_width=True):
            get_movie_summary()
    else:
        st.button("Get Summary", use_container_width=True, disabled=True)

# Display movie information
if st.session_state.movie:
    movie = st.session_state.movie
    
    st.header(f"{movie['title']} ({movie['year']})")
    
    # Movie details
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Movie Details")
        st.write(f"**Director:** {movie['director']}")
        st.write(f"**Year:** {movie['year']}")
    
    # Actors
    with col2:
        st.subheader("Starring")
        for actor in movie['actors']:
            st.write(f"• {actor['actor_name']}")
    
    # Display summary if available
    if st.session_state.summary:
        st.subheader("Movie Summary")
        st.info(st.session_state.summary)
else:
    st.info("Click 'Show Random Movie' to get started!")

# Add information about how to add movies
st.markdown("---")
st.write("ℹ️ Note: Make sure to add movies via the FastAPI backend API first using the `/movies/` POST endpoint.")
st.write("You can access the API documentation at http://localhost:8000/docs")