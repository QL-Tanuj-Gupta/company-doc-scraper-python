import os

from uuid import uuid4
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from app.schemas import ChatMessage
from app.services.indexing import retrieve_relevant_chunks

load_dotenv()

llm = GoogleGenAI(
  model="gemini-3.5-flash-lite",
  api_key=os.getenv("GOOGLE_API_KEY")
)

chat_sessions : dict[str, list[ChatMessage]] = {}

def condense_question(question:str,history:list[ChatMessage]) -> str:
  if not history:
    return question.strip()
  
  conversation = "\n".join(
    f"{message.role}: {message.content}"
    for message in history
  )

  prompt = f"""Rewrite the latest question as a standalone question using the conversation history.

  Do not answer the question. Only return the rewritten question.

  Conversation history:
  {conversation}

  Latest question:
  {question}

  Standalone question:"""

  response = llm.complete(prompt)
  
  return response.text.strip() or question.strip()

def generate_answer(question: str, session_id: str | None = None):
    if not session_id:
      session_id = str(uuid4())

    history = chat_sessions.setdefault(session_id,[])

    standalone_question = condense_question(question, history)

    chunks = retrieve_relevant_chunks(
      standalone_question,
      top_k=3
    )

    if not chunks:
        answer = "I couldn't find relevant information in the project documents."
    else:
        context = "\n\n".join(
            f"Project: {chunk['project_name']}\n{chunk['text']}"
            for chunk in chunks
        )

    prompt = f"""You are a friendly assistant for the company's internal project knowledge base.

    Follow these rules:

    1. Be natural, polite, and concise.
    2. For greetings like "Hi", "Hello", or "Hey", respond with a short, friendly greeting. Do not mention a specific project unless the user mentioned it.
    3. For thanks or other simple pleasantries, respond naturally without retrieving or summarizing project information.
    4. For project-related questions, answer using only relevant information from the provided context.
    5. The retrieved context may contain unrelated information. Ignore anything that does not help answer the question.
    6. If the answer is not supported by the relevant context, say that you could not find the information in the available project documents.
    7. Never invent project details or make unsupported assumptions.
    8. For follow-up questions, use the standalone question and relevant context to understand what the user means.
    9. Use clear language and include only the details needed to answer the question.

    Relevant project context:
    {context}

    User question:
    {standalone_question}

    Answer:"""

    response = llm.complete(prompt)
    answer = response.text.strip()

    history.append(
        ChatMessage(role="user", content=question)
    )

    history.append(
        ChatMessage(role="assistant", content=answer)
    )

    return {
      "sessionId":session_id,
      "answer": answer,
      "condensed_question": standalone_question,
      "sources": chunks
    }