from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, Float, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class PaperDB(Base):
    __tablename__ = "papers"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text)
    authors = Column(JSON)
    year = Column(Integer)
    citations = Column(Integer, default=0)
    references = Column(JSON)
    keywords = Column(JSON)
    journal = Column(String)
    doi = Column(String)
    pdf_url = Column(String)
    source = Column(String)
    url = Column(String)
    embedding_stored = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Paper(BaseModel):
    id: str
    title: str
    abstract: Optional[str] = ""
    authors: List[str] = []
    year: Optional[int] = None
    citations: int = 0
    references: List[str] = []
    keywords: List[str] = []
    journal: Optional[str] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    source: str
    url: Optional[str] = None

class PaperChunk(BaseModel):
    paper_id: str
    chunk_index: int
    text: str
    metadata: dict = {}

class SearchQuery(BaseModel):
    query: str
    max_results: int = Field(default=10, le=50)
    sources: List[str] = ["semantic_scholar", "arxiv", "pubmed", "openalex"]

class LiteratureReviewRequest(BaseModel):
    topic: str
    max_papers: int = Field(default=20, le=50)

class GapAnalysisRequest(BaseModel):
    topic: str
    papers: Optional[List[str]] = None

class MethodologyRequest(BaseModel):
    research_question: str
    domain: Optional[str] = None

class ContradictionRequest(BaseModel):
    topic: str
    paper_ids: Optional[List[str]] = None

class DraftReviewRequest(BaseModel):
    draft_text: str
    title: Optional[str] = None

class HypothesisRequest(BaseModel):
    topic: str
    context: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    topic: Optional[str] = None
