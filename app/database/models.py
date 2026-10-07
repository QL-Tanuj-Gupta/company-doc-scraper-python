from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

class Project(Base):
  __tablename__ = "projects"

  id: Mapped[int] = mapped_column(Integer,primary_key=True)
  name: Mapped[str] = mapped_column(String(255))
  overview: Mapped[str] = mapped_column(Text)
  technologies: Mapped[str] = mapped_column(Text)
  team: Mapped[str] = mapped_column(Text)
  features: Mapped[str] = mapped_column(Text)