import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Suppress faiss warning logs below ERROR level
logging.getLogger("faiss").setLevel(logging.ERROR)
from fastapi import FastAPI
from api.routes import router
from db.metadata_store import init_db
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

init_db()

app = FastAPI(title="RAG Pipeline")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    # Since you run from inside backend, this should be:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
