from fastapi import FastAPI
from pydantic import BaseModel

from rag import (
    load_and_chunk,
    embed_chunks,
    build_index,
    search,
    generate_answer,
)


app = FastAPI(title="EFG HR Policy QA API")


# Load policies and build the search index
POLICIES_DIR = "../data/policies"

chunks = load_and_chunk(POLICIES_DIR)
chunks = embed_chunks(chunks)
index = build_index(chunks)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "EFG HR Policy QA API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question

    results = search(
        question,
        chunks,
        index
    )

    answer = generate_answer(
        question,
        results
    )

    # Return only the best matching source
    sources = []

    if results:
        best_result = results[0]

        sources.append(
            {
                "document": best_result["doc_title"],
                "section": best_result["section"],
                "document_id": best_result["doc_id"],
            }
        )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }