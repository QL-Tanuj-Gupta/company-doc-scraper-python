from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Project
from app.database.dependencies import get_db
from app.schemas import ProjectCreate
from app.services.markdown import to_markdown_list, create_project_markdown

app = FastAPI()

@app.get("/")
def home():
  return {
    "message":"Company Doc Scraper API"
  }

@app.post("/api/projects/add")
def create_project(
  project:ProjectCreate,
  db:Session = Depends(get_db)
  ):

  project_name = project.projectName.strip()
  if not project_name:
    raise HTTPException(
      status_code=400,
      detail="Project name is required"
    )

  if not project.overview.strip():
    raise HTTPException(
      status_code=400,
      detail="Project overview is required"
    )

  existing_project = db.query(Project).filter(
    func.lower(Project.name) == project_name.lower()
  ).first()

  if (existing_project):
    raise HTTPException(
      status_code=409,
      detail="Project already exists"
    )

  markdown = create_project_markdown(project)

  new_project = Project(
    name=project_name,
    overview=project.overview.strip(),
    technologies=to_markdown_list(project.technologies),
    team=to_markdown_list(project.team),
    features=to_markdown_list(project.features)
  )

  db.add(new_project)
  db.commit()
  db.refresh(new_project)

  return {
    "success": True,
    "message": "Project prepared successfully",
    "data": {
        "project": project.model_dump(),
        "markdown": markdown
    }
  }