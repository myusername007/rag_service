from fastapi import FastAPI, HTTPException
from schemas import AskRequest, AskResponse, UploadRequest, UploadResponse
from services.rag_service import upload_document, ask_document

app = FastAPI()

@app.post("/upload", response_model= UploadResponse)
async def upload_doc(request: UploadRequest):
    result = await upload_document(doc_id=request.doc_id, text=request.text)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )
    return UploadResponse(doc_id=request.doc_id, chunks_count=result)

@app.post("/ask", response_model=AskResponse)
async def ask_doc(request: AskRequest):
    result = await ask_document(question=request.question, doc_id=request.doc_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )
    return AskResponse(answear=result)