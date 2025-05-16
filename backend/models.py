from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional
from database import Base

# SQLAlchemy Models
class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    director = Column(String)
    
    # Relationship with Actors model
    actors = relationship("Actors", back_populates="movie")

class Actors(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    actor_name = Column(String, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    
    # Relationship with Movies model
    movie = relationship("Movies", back_populates="actors")

# Pydantic Models
class ActorBase(BaseModel):
    actor_name: str

class ActorPublic(ActorBase):
    id: int
    
    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorBase]

class MoviePublic(BaseModel):
    id: int
    title: str
    year: int
    director: str
    actors: List[ActorPublic]
    
    class Config:
        orm_mode = True

# Models for Summary functionality
class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str