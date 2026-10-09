from llama_index.core import Document

def create_document(markdown:str, project_name:str):
  document = Document(
    text=markdown,
    metadata={
      "project_name": project_name
    }
  )

  return document