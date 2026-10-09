import os

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Document
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

load_dotenv()

EMBEDDING_DIMENSIONS = 768
VECTOR_TABLE = "project_vectors"

embed_model = GoogleGenAIEmbedding(
  model_name = "gemini-embedding-2",
  api_key = os.getenv("GOOGLE_API_KEY"),
  embedding_config = {
    "output_dimensionality" : EMBEDDING_DIMENSIONS
  }
)

def create_document(markdown:str, project_name:str):
  document = Document(
    text=markdown,
    metadata={
      "project_name": project_name
    }
  )

  return document

def get_vector_store():
  database_url = os.getenv("DATABASE_URL")

  if not database_url:
    return{
      "message":"DATABASE_URL is not configured"
    }

  db_url = make_url(database_url)

  vector_store = PGVectorStore.from_params(
    database=db_url.database,
    host=db_url.host,
    port=db_url.port,
    user=db_url.username,
    password=db_url.password,
    table_name=VECTOR_TABLE,
    embed_dim=EMBEDDING_DIMENSIONS
  )

  return vector_store