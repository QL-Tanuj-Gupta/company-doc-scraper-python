import os

from dotenv import load_dotenv
from llama_index.core import Document
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

load_dotenv()

EMBEDDING_DIMENSIONS = 768

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