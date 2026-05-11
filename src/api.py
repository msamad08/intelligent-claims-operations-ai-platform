from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_pipeline import answer_question

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

    result = answer_question(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }