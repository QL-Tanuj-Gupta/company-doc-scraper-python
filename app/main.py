from fastapi import Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Project
from app.database.dependencies import get_db
from app.schemas import ProjectCreate, ChatRequest
from app.services.markdown import to_markdown_list, create_project_markdown
from app.services.indexing import index_project_markdown
from app.services.chat import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return JSONResponse(
      status_code=400,
      content={
          "success": False,
          "message": "Project name is required"
      }
    )

  if not project.overview.strip():
    return JSONResponse(
        status_code=400,
        content={
          "success": False,
          "message": "Project overview is required"
        }
    )

  existing_project = db.query(Project).filter(
    func.lower(Project.name) == project_name.lower()
  ).first()

  if existing_project:
    return JSONResponse(
        status_code=409,
        content={
          "success": False,
          "message": "Project already exists"
        }
      )

  markdown = create_project_markdown(project)

  index_project_markdown(markdown, project_name)

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

@app.post("/chat")
def chat(request:ChatRequest):
  if not request.question.strip():
    return JSONResponse(
      status_code=400,
      content={
        "success":False,
        "message":"Question is required"
      }
    )
  
  result = generate_answer(
    question=request.question,
    history=request.history
  )

  return{
    "success":True,
    "message":"Answer generated successfully",
    "data":result
  }