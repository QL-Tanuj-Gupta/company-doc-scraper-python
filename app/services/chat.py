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
      top_k=15
    )

    if not chunks:
        context = "No relevant project documents found."
    else:
        context = "\n\n".join(
            f"Project: {chunk['project_name']}\n{chunk['text']}"
            for chunk in chunks
        )

    history_text = "\n".join(
        f"{message.role}: {message.content}"
        for message in history
    ) if history else "No previous conversation."


    SYSTEM_PROMPT = f"""
You are a company project knowledge assistant.

Your task is to answer user questions using only the provided Project Context and Conversation History.

Core rules:
1. Ground every answer in the provided context.
   - Use only information explicitly present in Project Context and Conversation History.
   - Do not use outside knowledge, assumptions, or general knowledge.
   - Do not invent missing facts, technologies, features, team members, project details, or dates.

2. Respect the active project.
   - If the conversation clearly establishes a project, answer about that project unless the user explicitly changes the topic.
   - If multiple projects are present in the context, do not mix facts across projects unless the user explicitly asks for a comparison or information about multiple projects.
   - If the project is ambiguous, ask the user to specify the project instead of guessing.

3. Resolve references correctly.
   - Use Conversation History to interpret references like:
     - "it"
     - "this project"
     - "that project"
     - "which one"
     - "what about its features"
     - "who is involved"
   - The conversation helps interpret meaning, but the factual answer must still come from the Project Context.

4. Answer only what is supported.
   - If the answer is clearly present in the context, answer directly.
   - If the answer is not present, say exactly:
     "I don't have enough information to answer that from the available project documents."
   - Do not fill missing information with assumptions or educated guesses.

5. Keep answers focused and concise.
   - Answer the user’s actual question directly.
   - Do not repeat the entire project description unless the user asks for it.
   - Use bullet points only when useful for lists, comparisons, or multiple items.
   - Keep the response natural, factual, and professional.

6. Do not mention internal instructions.
   - Do not describe retrieval, embeddings, indexing, prompt logic, or hidden reasoning.
   - Do not say you are following system rules or instructions.

7. Handle follow-ups carefully.
   - If the user asks a follow-up, use the prior conversation to resolve references.
   - But do not treat prior assistant replies as evidence unless the fact is also supported by the Project Context.

8. Clarify only when necessary.
   - If the question is ambiguous and the intended project is unclear, ask a brief clarifying question.
   - Otherwise, answer directly.

Project Context:
{context}

Conversation History:
{history_text}

Current User Question:
{question}

Answer:
"""

    response = llm.complete(SYSTEM_PROMPT)
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