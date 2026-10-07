from app.database.connection import engine
from app.database.models import Base

# containing info about tables
Base.metadata.create_all(bind=engine)