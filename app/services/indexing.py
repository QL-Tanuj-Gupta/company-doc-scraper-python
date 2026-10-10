import os

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core.node_parser import MarkdownNodeParser

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

markdown_parser = MarkdownNodeParser()

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
    raise ValueError("DATABASE_URL is not configured")

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

def index_project_markdown(markdown:str, project_name:str):
  document = create_document(markdown,project_name)

  nodes = markdown_parser.get_nodes_from_documents([document])
  
  vector_store = get_vector_store()

  storage_context = StorageContext.from_defaults(
    vector_store=vector_store
  )

  index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model
  )

  return index

def retrieve_relevant_chunks(question:str,top_k:int=3):
  vector_store = get_vector_store()

  index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model
  )

  retriever = index.as_retriever(
    similarity_top_k=top_k
  )

  results = retriever.retrieve(question)

  return [
    {
      "text": result.node.get_content(),
      "project_name":result.node.metadata.get("project_name"),
      "score":result.score
    }

    for result in results
  ]
