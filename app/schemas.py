from pydantic import BaseModel

class ProjectCreate(BaseModel):
  projectName: str
  overview: str
  technologies: list[str] | None = None
  team: list[str] | None = None
  features: list[str] | None = None