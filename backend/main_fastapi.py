from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
import os
from dotenv import load_dotenv
import requests
import json

from database import get_db, engine
import models
from models import Movies, Actors, MovieBase, MoviePublic, SummaryRequest, SummaryResponse

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Movie Explorer API")

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/movies/", response_model=MoviePublic)
def create_movie(movie: MovieBase, db: Session = Depends(get_db)):
    """
    Create a new movie with associated actors.
    
    First, we create the movie record, then we commit it to get the movie ID,
    after which we create the actor records associated with that movie ID.
    """
    # Create the movie record first
    db_movie = Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    
    # Now create the actor records using the movie's ID
    for actor in movie.actors:
        db_actor = Actors(
            actor_name=actor.actor_name,
            movie_id=db_movie.id
        )
        db.add(db_actor)
    
    # Commit all the actor records
    db.commit()
    # Refresh the movie to load the actors relationship
    db.refresh(db_movie)
    
    return db_movie

@app.get("/movies/random/", response_model=MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    """
    Get a random movie with its associated actors.
    
    We use SQLAlchemy's func.random() to select a random record,
    and use joinedload to eagerly load the actors relationship.
    """
    # Get a random movie with eagerly loaded actors
    movie = db.query(Movies).options(joinedload(Movies.actors)).order_by(func.random()).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail="No movies found in database")
        
    return movie

@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_movie_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    """
    Generate a Groq-based summary for a movie.
    
    We retrieve the movie by ID, format the actor names into a string,
    create a prompt with the movie details, and use Groq's API to generate a summary.
    """
    # Get the movie with its actors
    movie = db.query(Movies).options(joinedload(Movies.actors)).filter(Movies.id == request.movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie with ID {request.movie_id} not found")
    
    # Format the list of actors into a comma-separated string
    actor_names = [actor.actor_name for actor in movie.actors]
    actor_list = ", ".join(actor_names)
    
    # Create the prompt for Groq
    user_message = f"Generate a short, engaging summary for the movie '{movie.title}' ({movie.year}), directed by {movie.director} and starring {actor_list}."
    
    # Prepare the payload for Groq API
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    try:
        # Make the API call to Groq
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract the summary from the response
        result = response.json()
        summary = result["choices"][0]["message"]["content"]
        
        # Return the generated summary
        return SummaryResponse(summary_text=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

# Startup event to check database connection
@app.on_event("startup")
async def startup_db_client():
    try:
        # Just create the tables to verify the connection works
        models.Base.metadata.create_all(bind=engine)
        print("Successfully connected to the database")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)