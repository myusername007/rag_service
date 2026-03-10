from pydantic import BaseModel

class UploadRequest(BaseModel):
    doc_id: str
    text: str

class UploadResponse(BaseModel):
    doc_id: str
    chunks_count: int

class AskRequest(BaseModel):
    question: str
    doc_id: str | None = None

class AskResponse(BaseModel):
    answear: str

    