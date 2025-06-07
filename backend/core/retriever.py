import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384
        self.index = faiss.IndexFlatIP(self.dim)
        self.chunks = []
        self.load_from_disk()

    def load_from_disk(self):
        if os.path.exists("faiss_index.bin"):
            self.index = faiss.read_index("faiss_index.bin")
        if os.path.exists("chunks.json"):
            with open("chunks.json", "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def save_to_disk(self):
        faiss.write_index(self.index, "faiss_index.bin")
        with open("chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f)

    def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        embeddings = self.model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings

    def add_documents(self, chunks: List[str]):
        embeddings = self.embed_chunks(chunks)
        self.index.add(embeddings)
        self.chunks.extend(chunks)
        self.save_to_disk()

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        if self.index.ntotal == 0:
            return []
        query_embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        distances, indices = self.index.search(query_embedding, k)
        return [(self.chunks[i], float(dist)) for i, dist in zip(indices[0], distances[0]) if i < len(self.chunks)]

vector_store = VectorStore()
