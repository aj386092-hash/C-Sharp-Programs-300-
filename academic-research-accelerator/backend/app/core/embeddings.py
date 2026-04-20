from sentence_transformers import SentenceTransformer
from app.config import settings
import numpy as np
from typing import List

_model = None

def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model

def generate_embeddings(texts: List[str]) -> np.ndarray:
    model = get_embedding_model()
    return model.encode(texts, show_progress_bar=False, normalize_embeddings=True)

def generate_embedding(text: str) -> np.ndarray:
    return generate_embeddings([text])[0]
