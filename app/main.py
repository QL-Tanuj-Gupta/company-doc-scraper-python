from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session

from app.database.models import Project
from app.database.dependencies import get_db
from app.schemas import ProjectCreate
from app.services.markdown import to_markdown_list

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

  exisint_project = db.query(Project).filter(
    Project.name == project.name
  ).first()

  if (exisint_project):
    raise HTTPException(
      status_code=409,
      detail="Project already exists"
    )

  new_project = Project(
    name=project.name,
    overview=project.overview,
    technologies=to_markdown_list(project.technologies),
    team=to_markdown_list(project.team),
    features=to_markdown_list(project.features)
  )
  
  db.add(new_project)
  db.commit()
  db.refresh(new_project)

  return new_project