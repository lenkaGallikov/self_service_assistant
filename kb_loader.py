import os
from sentence_transformers import SentenceTransformer
import chromadb
from PyPDF2 import PdfReader

# Initialize embedding model and ChromaDB client
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_or_create_collection(name="kb_collection")


def retrieve_context(query: str, top_k: int = 3):
    # Embed the query
    query_embedding = model.encode(query)

    # Query ChromaDB for top_k relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['documents', 'metadatas']
    )

    # Format the results with source and content
    context_chunks = []
    for doc, meta_list in zip(results['documents'], results.get('metadatas', [{}]*top_k)):
        meta = meta_list[0] if isinstance(meta_list, list) and meta_list else {}
        context_chunks.append({
            "source": meta.get("source", "unknown_source"),
            "content": doc
        })

    return context_chunks


def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def seed_kb():
    docs = []
    ids = []
    folder_path = "data/kb"
    file_list = os.listdir(folder_path)
    success_count = 0

    for i, filename in enumerate(file_list):
        file_path = os.path.join(folder_path, filename)
        content = ""

        if filename.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading TXT {filename}: {e}")
                continue

        elif filename.endswith(".pdf"):
            content = extract_text_from_pdf(file_path)

        else:
            print(f"Skipping unsupported file type: {filename}")
            continue

        if content.strip():
            docs.append(content)
            ids.append(str(i))
            success_count += 1
        else:
            print(f"No content extracted from {filename}, skipping.")

    if docs:
        embeddings = model.encode(docs)
        collection.add(documents=docs, embeddings=embeddings, ids=ids)

    return {
        "status": "completed",
        "embedded_documents": success_count,
        "total_files": len(file_list)
    }

def embed_local():
    return seed_kb()