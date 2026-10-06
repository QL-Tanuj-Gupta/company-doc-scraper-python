from fastapi import FastAPI
from app.schemas import Project

app = FastAPI()

projects: list[Project] = []

@app.get("/")
def home():
  return {
    "message":"Company Doc Scraper API"
  }

@app.post("/projects")
def create_project(project:Project):
  projects.append(project)
  return {
    "message":"Project created successfully",
    "project":project
  }

@app.get("/projects")
def get_projects():
  return projects