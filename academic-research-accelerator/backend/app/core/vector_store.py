import faiss
import numpy as np
import json
import os
import pickle
from typing import List, Tuple, Optional
from app.config import settings
from app.core.embeddings import generate_embedding, generate_embeddings

class FAISSVectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.metadata: List[dict] = []
        self.texts: List[str] = []
        self.index_path = settings.faiss_index_path
        os.makedirs(self.index_path, exist_ok=True)
        self._load()

    def add_documents(self, texts: List[str], metadatas: List[dict]) -> None:
        if not texts:
            return
        embeddings = generate_embeddings(texts).astype(np.float32)
        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadata.extend(metadatas)
        self._save()

    def search(self, query: str, k: int = 5) -> List[Tuple[str, dict, float]]:
        if self.index.ntotal == 0:
            return []
        query_embedding = generate_embedding(query).astype(np.float32).reshape(1, -1)
        k = min(k, self.index.ntotal)
        scores, indices = self.index.search(query_embedding, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append((self.texts[idx], self.metadata[idx], float(score)))
        return results

    def _save(self) -> None:
        faiss.write_index(self.index, os.path.join(self.index_path, "index.faiss"))
        with open(os.path.join(self.index_path, "metadata.pkl"), "wb") as f:
            pickle.dump({"texts": self.texts, "metadata": self.metadata}, f)

    def _load(self) -> None:
        index_file = os.path.join(self.index_path, "index.faiss")
        meta_file = os.path.join(self.index_path, "metadata.pkl")
        if os.path.exists(index_file) and os.path.exists(meta_file):
            self.index = faiss.read_index(index_file)
            with open(meta_file, "rb") as f:
                data = pickle.load(f)
                self.texts = data["texts"]
                self.metadata = data["metadata"]

    @property
    def total_documents(self) -> int:
        return self.index.ntotal

_vector_store: Optional[FAISSVectorStore] = None

def get_vector_store() -> FAISSVectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = FAISSVectorStore()
    return _vector_store
