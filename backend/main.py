import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from api.routes import router
from db.metadata_store import init_db
import sys
import os

# Set logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger("faiss").setLevel(logging.ERROR)

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize any DBs
init_db()

# FastAPI app
app = FastAPI(title="🧠 RAG Pipeline")

# Include all API routes under /api
app.include_router(router, prefix="/api")


# Optional: handle root path (avoid 404 on /)
@app.get("/")
def root():
    return JSONResponse(content={
        "message": "✅ Backend is running! Use /api/upload/ to upload PDFs and /api/query/ to ask questions."
    })


# Optional: suppress favicon.ico errors
@app.get("/favicon.ico")
def favicon():
    return JSONResponse(content={}, status_code=204)


# Run locally (if needed)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
