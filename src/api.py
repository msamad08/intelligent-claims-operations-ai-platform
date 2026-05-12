from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_pipeline import answer_question

app = FastAPI(
    title="Intelligent Claims & Operations AI API",
    description="Enterprise RAG API for claims intelligence, SOP retrieval, and operational decision support.",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Intelligent Claims & Operations AI API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = answer_question(request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {e}"
        )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }