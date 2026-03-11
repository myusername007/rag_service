import chromadb
import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv() 

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("documents")

def split_into_chunks(text: str, chunk_size: int = 200) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

async def upload_document(doc_id: str, text: str) -> int:
    chunks = split_into_chunks(text)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc_id} for _ in chunks]  # додаємо metadata
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    return len(chunks)

async def ask_document(question: str, doc_id: str | None = None, n_results: int = 3) -> str:
    where = {"doc_id": doc_id} if doc_id else None
    results = collection.query(
    query_texts=[question],
    n_results=n_results,
    where=where  # не where_document, а where
)
    relevant_chunks = results["documents"][0]
    context = "\n\n".join(relevant_chunks)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="Answer questions based only on the provided context. If the answer is not in the context, say so.",
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return message.content[0].text


async def list_documents() -> list[str]:
    results = collection.get()
    doc_ids = list(set(
        m["doc_id"] for m in results["metadatas"]
    ))
    return doc_ids

async def delete_document(doc_id: str) -> int:
    results = collection.get(where={"doc_id": doc_id})
    ids = results["ids"]
    if ids:
        collection.delete(ids=ids)
    return len(ids)