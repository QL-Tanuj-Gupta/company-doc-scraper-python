from fastapi import Depends,FastAPI
from sqlalchemy.orm import Session

from app.database.models import Project
from app.database.dependencies import get_db
from app.schemas import ProjectCreate

app = FastAPI()

@app.get("/")
def home():
  return {
    "message":"Company Doc Scraper API"
  }

@app.post("/projects")
def create_project(
  project:ProjectCreate,
  db:Session = Depends(get_db)
  ):

  new_project = Project(
    name=project.name,
    overview=project.overview,
    technologies=project.technologies,
    team=project.team,
    features=project.features
  )
  
  db.add(new_project)
  db.commit()
  db.refresh(new_project)

  return new_project
  
@app.get("/projects")
def get_projects(db:Session = Depends(get_db)):
  projects = db.query(Project).all()
  
  return projects