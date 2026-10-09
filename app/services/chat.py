import os

from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

llm = GoogleGenAI(
  model="gemini-3.5-flash-lite",
  api_key=os.getenv("GOOGLE_API_KEY")
)