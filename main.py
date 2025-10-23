from kb_loader import seed_kb, embed_local, retrieve_context
from fastapi import FastAPI, Request
from llm_client import query_llm
from kb_loader import seed_kb, embed_local
from rag_engine import format_prompt

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/seed_kb")
def seed_kb_endpoint():
    return seed_kb()

@app.post("/embed_local")
def embed_local_endpoint():
    return embed_local()


@app.post("/ask")
async def ask_endpoint(request: Request):
    data = await request.json()
    question = data.get("query", "")

    # Retrieve context from ChromaDB
    context_chunks = retrieve_context(question)

    # Format the prompt using rag_engine
    prompt = format_prompt(context_chunks, question)

    # Query the LLM
    llm_response = query_llm(prompt)  #This line must be present

    # Return only the answer text
    return {"answer": llm_response.get("response", "No answer returned")}


@app.get("/debug")
def debug():
    return {"debug": "info"}