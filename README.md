# LLM-Powered Movie & Actor Explorer

This application consists of a FastAPI backend that manages movie and actor data stored in PostgreSQL and a Streamlit frontend for exploring movies and requesting AI-generated summaries.

## Project Structure

```
.
├── backend/
│   ├── database.py        # PostgreSQL connection setup
│   ├── main_fastapi.py    # FastAPI application with endpoints
│   ├── models.py          # SQLAlchemy models and Pydantic schemas
│   ├── requirements.txt   # Backend dependencies
│   └── .env               # Backend environment variables
└── frontend/
  ├── main_streamlit.py  # Streamlit UI application
  ├── requirements.txt   # Frontend dependencies
  └── .env               # Frontend environment variables
```

## Setup Instructions

### Prerequisites

- PostgreSQL installed and running
- Python 3.x installed

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with your PostgreSQL connection details:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/moviedb
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Start the FastAPI server:
   ```
   uvicorn main_fastapi:app --reload
   ```

6. Access the API documentation at http://localhost:8000/docs

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Streamlit app:
   ```
   streamlit run main_streamlit.py
   ```

5. Access the Streamlit app at http://localhost:8501

## Backend API Endpoints

### Create Movie
```
POST /movies/
```
Creates a new movie with associated actors.

**Request Body Example (for "Inception"):**
```json
{
  "title": "Inception",
  "year": 2010,
  "director": "Christopher Nolan",
  "actors": [
    {
      "actor_name": "Leonardo DiCaprio"
    },
    {
      "actor_name": "Joseph Gordon-Levitt"
    },
    {
      "actor_name": "Elliot Page"
    },
    {
      "actor_name": "Tom Hardy"
    }
  ]
}
```

### Get Random Movie
```
GET /movies/random/
```
Retrieves a random movie with its associated actors.

### Generate Movie Summary
```
POST /generate_summary/
```
Generates a summary for a movie using the Groq API.

**Request Body Example:**
```json
{
  "movie_id": 1
}
```

## Answers to Questions

### Question 1: Why is it often necessary to commit the primary record (Movies) before creating the related records (Actors) that depend on its foreign key?

It's necessary to commit the primary record (Movies) before creating related records (Actors) because:

1. The primary record needs to be persisted in the database first to generate its primary key (ID).
2. This ID is then used as a foreign key in the related records (Actors).
3. Without committing the primary record first, the ID might not be available (depending on the database and ORM settings), making it impossible to establish the relationship correctly.
4. In SQLAlchemy, the `refresh()` method is used after committing to ensure the generated ID is available in the object before creating related records.

### Question 2: What is the difference between lazy loading and eager loading (like joinedload) for relationships in SQLAlchemy?

**Lazy Loading:**
- Relationships are loaded only when they are explicitly accessed (on-demand).
- This means related data is fetched with separate database queries when the relationship attribute is accessed.
- Can lead to the N+1 query problem, where accessing relationships for multiple parent objects results in many individual queries.
- Default behavior in SQLAlchemy.

**Eager Loading (joinedload):**
- Related data is loaded in the same query as the parent objects.
- Reduces the number of database queries by fetching parent and related entities in one go.
- More efficient when you know in advance that you'll need the related data.
- Implemented in SQLAlchemy using strategies like `joinedload()`, `selectinload()`, or `subqueryload()`.

### Question 3: How would you format the list of actors fetched from the database into a simple string suitable for inclusion in the LLM prompt?

To format the list of actors into a string for the LLM prompt:

```python
# Extract actor names from the actors relationship
actor_names = [actor.actor_name for actor in movie.actors]

# Join them with commas
actor_list = ", ".join(actor_names)

# Now actor_list can be used in the prompt
# e.g., "Generate a summary for movie X starring {actor_list}"
```

This creates a comma-separated string of actor names that can be seamlessly integrated into the LLM prompt template.
