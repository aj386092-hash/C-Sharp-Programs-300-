from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.paper import SearchQuery, Paper
from app.agents.research_agent import ingest_papers
from app.core.vector_store import get_vector_store
from typing import List

router = APIRouter(prefix="/api/papers", tags=["papers"])

@router.post("/ingest", response_model=dict)
async def ingest_research_papers(query: SearchQuery):
    try:
        papers = await ingest_papers(query)
        return {
            "status": "success",
            "papers_ingested": len(papers),
            "papers": [p.model_dump() for p in papers[:10]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=dict)
async def get_stats():
    vector_store = get_vector_store()
    return {
        "total_chunks": vector_store.total_documents,
        "status": "operational"
    }
