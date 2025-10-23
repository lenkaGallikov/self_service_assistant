# self_service_assistant
My POC for an AI bot that can talk to policy documents of an organisation to anwers customer queries

# Open-Source Stack (Local or Cloud-hosted)
-	LLM via Ollama (e.g., llama3.1:8b-instruct-q4_K_M)
-	RAG API using FastAPI
-	ChromaDB for document search
-	Sentence Transformers for embeddings
-	Mounted KB (/app/local_kb) with your PDFs/articles

## This stack handles:
-	Natural language Q&A
-	Citations from your documents
-	Fast response times
-	Easy customization

# SnapLogic Cloud Integration
SnapLogic will act as the orchestrator and frontend connector:
What SnapLogic will do:
-	Call your RAG API via REST (e.g., /ask, /seed_kb)
-	Route user queries from Teams/Web to your assistant
-	Mock OMS/CIS APIs using JSON datasets or dummy endpoints
-	Log analytics (containment rate, top intents, latency)
-	Trigger escalation flows (e.g., handoff to human agent)

# How It All Fits Together
Component	                        Role
FastAPI RAG API	            Core engine for answering questions
ChromaDB + Embeddings	    Finds relevant info from your KB
Ollama (LLM)	            Generates grounded, natural answers
SnapLogic Cloud	            Connects users, mocks APIs, logs analytics
Teams/Web Bot	            User-facing interface
Mock OMS/CIS APIs	        Simulated backend for demo purposes

# Deliverables
-	Web/Teams bot interface
-	Citations in answers
-	Analytics dashboard (containment, latency, top intents)
-	“Golden questions” test set
-	Quality report (≥70% accuracy, <2.5s latency)

# To start working with this code follow the below steps:
## Start Your Virtual Environment
-	Open Terminal and run:
-	cd path/to/self_service_assistant
-	source rag-env/bin/activate
-	This activates your Python environment with all dependencies.

## Start FastAPI Server
-	The FastAPI contains the below endpoints:
        /ask — for answering questions
        /seed_kb — for loading documents
        /health — for status checks
-	Run:
        uvicorn main:app --reload
-	This launches your assistant backend.
-	The n test your API: curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the late payment fee?"}'

## Start ngrok Tunnel
-	In a separate terminal:
        ngrok http 8000
-	Copy the new public URL (e.g., https://unscabbed-unwarrantably-dyan.ngrok-free.dev) and update it in:
        streamlit_app.py

## Test SnapLogic Pipelines
-	Open SnapLogic Designer
-	Import the Intent-Based Query Router with Logging_2025_10_23.slp file from snaplogic_pipeline_export folder
-	Run your pipeline manually or via Triggered Task
-	Make sure the HTTP Client Snap uses the updated ngrok URL
-	Build the GET, PUT, DELETE worker pipelines to make it more interactive

## Run Streamlit UI
-	In the same virtual environment:
-	streamlit run streamlit_app.py
-	This opens your assistant UI in the browser.




