from pydantic import BaseModel

class ProjectCreate(BaseModel):
  name:str
  overview:str
  technologies: str
  team:str
  features:str