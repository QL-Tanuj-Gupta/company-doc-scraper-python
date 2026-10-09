from pydantic import BaseModel

class ProjectCreate(BaseModel):
  projectName: str
  overview: str
  technologies: list[str] | None = None
  team: list[str] | None = None
  features: list[str] | None = None

class ChatMessage(BaseModel):
  role:str
  content:str

class ChatRequest(BaseModel):
  question:str
  sessionId:str | None = None