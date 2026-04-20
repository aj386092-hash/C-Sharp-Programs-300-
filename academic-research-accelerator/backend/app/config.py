from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: str = ""
    semantic_scholar_api_key: str = ""
    ncbi_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./research.db"
    faiss_index_path: str = "./faiss_index"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gpt-4o-mini"
    max_papers_per_query: int = 20
    chunk_size: int = 512
    chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()
