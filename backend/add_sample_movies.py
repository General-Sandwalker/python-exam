#!/usr/bin/env python3

from sqlalchemy.orm import Session
import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our database models
from database import engine, SessionLocal, Base
from models import Movies, Actors

# Load environment variables
load_dotenv()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Sample movie data
sample_movies = [
    {
        "title": "Inception",
        "year": 2010,
        "director": "Christopher Nolan",
        "actors": [
            "Leonardo DiCaprio",
            "Joseph Gordon-Levitt",
            "Elliot Page",
            "Tom Hardy"
        ]
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "director": "Quentin Tarantino",
        "actors": [
            "John Travolta",
            "Samuel L. Jackson",
            "Uma Thurman",
            "Bruce Willis"
        ]
    },
    {
        "title": "Al-Risalah (The Message)",
        "year": 1976,
        "director": "Moustapha Akkad",
        "actors": [
            "Abdullah Gaith (عبد الله غيث)",
            "Muna Wassef (منى واصف)",
            "Hamdi Ghaith (حمدي غيث)",
            "Ahmad Marey (أحمد مرعي)"
        ]
    },
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "director": "Frank Darabont",
        "actors": [
            "Tim Robbins",
            "Morgan Freeman",
            "Bob Gunton",
            "William Sadler"
        ]
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "director": "Francis Ford Coppola",
        "actors": [
            "Marlon Brando",
            "Al Pacino",
            "James Caan",
            "Richard S. Castellano"
        ]
    },
    {
        "title": "Parasite",
        "year": 2019,
        "director": "Bong Joon-ho",
        "actors": [
            "Song Kang-ho",
            "Lee Sun-kyun",
            "Cho Yeo-jeong",
            "Choi Woo-shik"
        ]
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "director": "Lana Wachowski, Lilly Wachowski",
        "actors": [
            "Keanu Reeves",
            "Laurence Fishburne",
            "Carrie-Anne Moss",
            "Hugo Weaving"
        ]
    },
    {
        "title": "Back to the Future",
        "year": 1985,
        "director": "Robert Zemeckis",
        "actors": [
            "Michael J. Fox",
            "Christopher Lloyd",
            "Lea Thompson",
            "Crispin Glover"
        ]
    },
    {
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "director": "Bob Persichetti, Peter Ramsey, Rodney Rothman",
        "actors": [
            "Shameik Moore",
            "Jake Johnson",
            "Hailee Steinfeld",
            "Mahershala Ali"
        ]
    },
    {
        "title": "Spirited Away",
        "year": 2001,
        "director": "Hayao Miyazaki",
        "actors": [
            "Rumi Hiiragi",
            "Miyu Irino",
            "Mari Natsuki",
            "Takashi Naitô"
        ]
    }
]

def add_movies():
    """Add sample movies to the database"""
    # Create a new session
    db = SessionLocal()
    
    try:
        # Check if movies already exist
        existing_count = db.query(Movies).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} movies. Do you want to add more? (y/n)")
            response = input().lower()
            if response != 'y':
                print("Operation cancelled.")
                return
        
        # Add each movie and its actors
        for movie_data in sample_movies:
            # Create the movie record
            movie = Movies(
                title=movie_data["title"],
                year=movie_data["year"],
                director=movie_data["director"]
            )
            
            # Add the movie to the session
            db.add(movie)
            # Commit to get the movie ID
            db.commit()
            db.refresh(movie)
            
            # Add the actors for this movie
            for actor_name in movie_data["actors"]:
                actor = Actors(
                    actor_name=actor_name,
                    movie_id=movie.id
                )
                db.add(actor)
            
            # Commit the actors
            db.commit()
            
            print(f"Added movie: {movie.title} with {len(movie_data['actors'])} actors")
        
        # Print the total count of movies
        movie_count = db.query(Movies).count()
        print(f"Total movies in database: {movie_count}")
        
    except Exception as e:
        print(f"Error adding movies: {e}")
        db.rollback()
    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    print("Adding sample movies to database...")
    add_movies()
    print("Done!")