import os

from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from app.schemas import ChatMessage
from app.services.indexing import retrieve_relevant_chunks

load_dotenv()

llm = GoogleGenAI(
  model="gemini-3.5-flash-lite",
  api_key=os.getenv("GOOGLE_API_KEY")
)

def condense_question(question:str,history:list[ChatMessage]) -> str:
  if not history:
    return question.strip()
  
  conversation = "\n".join(
    f"{message.role}: {message.content}"
    for message in history
  )

  prompt = f"""Rewrite the latest question as a standalone question
using the conversation history.

Do not answer the question. Only return the rewritten question.

Conversation history:
{conversation}

Latest question:
{question}

Standalone question:"""

  return response.text.strip() or question.strip()

def generate_answer(question: str, history: list[ChatMessage]):
    standalone_question = condense_question(question, history)

    chunks = retrieve_relevant_chunks(standalone_question, top_k=3)

    if not chunks:
        return {
            "answer": "I couldn't find relevant information in the project documents.",
            "condensed_question": standalone_question,
            "sources": []
        }

    context = "\n\n".join(
        f"Project: {chunk['project_name']}\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""You are a company project knowledge assistant.

Answer the question using only the provided project context.
If the context does not contain the answer, say that you
could not find the information in the available project documents.
Do not invent facts.

Project context:
{context}

Question:
{standalone_question}

Answer:"""

    response = llm.complete(prompt)

    return {
        "answer": response.text.strip(),
        "condensed_question": standalone_question,
        "sources": chunks
    }