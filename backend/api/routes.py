from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from core.chunker import chunk_pdf
from core.retriever import vector_store
from db.metadata_store import insert_metadata
from core.llm import generate_answer

router = APIRouter()


@router.get("/")
def root():
    return {"message": "✅ RAG Backend is Running. Use /api/upload/ to POST PDFs."}


# Accept both /upload and /upload/
@router.post("/upload")
@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    try:
        chunks = chunk_pdf(content)
        if not chunks:
            raise HTTPException(status_code=422, detail="No valid text extracted.")

        vector_store.add_documents(chunks)
        insert_metadata(file.filename, len(chunks))

        return JSONResponse(
            status_code=201,
            content={"message": "PDF processed", "chunks": len(chunks)}
        )

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/")
async def query_document(question: str = Form(...)):
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        print(f"[QUERY] Incoming question: {question}")
        docs_and_scores = vector_store.similarity_search_with_score(question, k=5)
        
        print(f"[QUERY] Retrieved top chunks (w/ scores):")
        for i, (chunk, score) in enumerate(docs_and_scores):
            print(f"{i+1}: Score={score:.4f}\n{chunk[:200]}...\n")

        threshold = 0.3
        relevant_docs = [doc for doc, score in docs_and_scores if score >= threshold]

        if not relevant_docs:
            return {
                "answer": "Sorry, no relevant content found. Try rephrasing or uploading more detailed docs."
            }

        context = "\n\n".join(relevant_docs)
        answer = generate_answer(question, context)

        print(f"[QUERY] Final generated answer: {answer}")
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
