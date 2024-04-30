from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Create a SQLite database
DATABASE_URL = "sqlite:///./podcast.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Model for Podcast
class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    file_path = Column(String)
    duration = Column(Integer)

app = FastAPI()

class PodcastCreate(BaseModel):
    title: str
    description: str
    duration: int

@app.post("/podcasts/")
def create_podcast(podcast: PodcastCreate):
    db = SessionLocal()
    db_podcast = Podcast(**podcast.dict())
    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast

@app.get("/podcasts/{podcast_id}")
def read_podcast(podcast_id: int):
    db = SessionLocal()
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return podcast

@app.get("/podcasts/")
def list_podcasts():
    db = SessionLocal()
    return db.query(Podcast).all()

@app.delete("/podcasts/{podcast_id}")
def delete_podcast(podcast_id: int):
    db = SessionLocal()
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if podcast is None:
        raise HTTPException(status_code=404, detail="Podcast not found")
    db.delete(podcast)
    db.commit()
    return {"message": "Podcast deleted successfully"}
