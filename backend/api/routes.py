from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from core.chunker import chunk_pdf
from core.retriever import vector_store
from db.metadata_store import insert_metadata
from fastapi import Request
from core.llm import generate_answer 
from core.retriever import vector_store
from core.llm import generate_answer

router = APIRouter()

@router.get("/")
def root():
    return {"message": "✅ RAG Backend is Running. Use /api/upload/ to POST PDFs."}

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    try:
        # Log file upload info (replace print with logger in real apps)
        print(f"[UPLOAD] Received file: {file.filename}")

        chunks = chunk_pdf(content)
        if not chunks:
            raise HTTPException(status_code=422, detail="No valid text extracted.")

        vector_store.add_documents(chunks)
        insert_metadata(file.filename, len(chunks))

        # Return minimal JSON response (no large data)
        return JSONResponse(
            status_code=201,
            content={"message": f"PDF '{file.filename}' processed successfully.",
                     "chunk_count": len(chunks)}
        )

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/query/")
async def handle_query(request: Request):
    try:
        body = await request.json()
        question = body.get("question")

        if not question:
            raise HTTPException(status_code=400, detail="Question is required.")

        context_chunks = vector_store.similarity_search(question, k=3)
        context = "\n".join(context_chunks)

        answer = generate_answer(question, context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))