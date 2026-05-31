current_pdf = None
from fastapi import FastAPI, UploadFile, File
import os
from pdf_utils import extract_text_from_pdf
from text_splitter_utils import create_chunks
from embedding_utils import create_embeddings
from faiss_utils import create_faiss_index
from answer_generator import generate_answer
from pydantic import BaseModel
from embedding_utils import (
    create_embeddings,
    create_query_embedding
)
from faiss_utils import (
    create_faiss_index,
    search_chunks
)
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
class QuestionRequest(BaseModel):
    question: str



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "SmartDoc QA Backend Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global current_pdf


    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    current_pdf = file_path

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully"
    }
@app.get("/test-pdf")
def test_pdf():

    text = extract_text_from_pdf(
        current_pdf
    )

    return {
        "text": text[:1000]
    }



@app.get("/test-chunks")
def test_chunks():

    text = extract_text_from_pdf(
        current_pdf
    )

    chunks = create_chunks(text)

    return {
        "total_chunks": len(chunks),
        "first_chunk": chunks[0]
    }
@app.get("/test-embeddings")
def test_embeddings():

    text = extract_text_from_pdf(
        current_pdf
    )

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    return {
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0])
    }
@app.get("/test-faiss")
def test_faiss():

    text = extract_text_from_pdf(
        current_pdf
    )

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return {
        "total_chunks": len(chunks),
        "vectors_in_index": index.ntotal
    }
@app.get("/test-llm")
def test_llm():

    answer = generate_answer(
        "Python is a programming language.",
        "What is Python?"
    )

    return {
        "answer": answer
    }
@app.post("/ask")
def ask_question(request: QuestionRequest):
    if current_pdf is None:
        return {
            "error": "Please upload a PDF first"
    }

    text = extract_text_from_pdf(
        current_pdf
    )

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(
        embeddings
    )

    query_embedding = create_query_embedding(
        request.question
    )

    indices = search_chunks(
        query_embedding,
        index,
        k=2
    )

    context = ""

    for idx in indices:
        context += chunks[idx] + "\n"

    answer = generate_answer(
        context,
        request.question
    )
    log_entry = {
        "question": request.question,
        "answer": answer,
        "timestamp": str(datetime.now())
    }

    try:
        with open("logs.json", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(log_entry)

    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=4)

    return {
        "question": request.question,
        "answer": answer
    }

    
    

    

