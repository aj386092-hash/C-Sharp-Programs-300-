from fastapi import APIRouter, HTTPException
from app.models.paper import SearchQuery
from app.core.vector_store import get_vector_store
from app.agents.research_agent import ingest_papers
from typing import List

router = APIRouter(prefix="/api/search", tags=["search"])

@router.post("/papers", response_model=dict)
async def search_papers(query: SearchQuery):
    try:
        # Search vector store first
        vector_store = get_vector_store()
        results = vector_store.search(query.query, k=query.max_results)
        
        if not results:
            # If no results in vector store, fetch from APIs
            papers = await ingest_papers(query)
            results = vector_store.search(query.query, k=min(len(papers), query.max_results))
        
        seen_paper_ids = set()
        papers_data = []
        for text, metadata, score in results:
            pid = metadata.get("paper_id")
            if pid and pid not in seen_paper_ids:
                seen_paper_ids.add(pid)
                papers_data.append({
                    "paper_id": pid,
                    "title": metadata.get("title", ""),
                    "authors": metadata.get("authors", []),
                    "year": metadata.get("year"),
                    "source": metadata.get("source", ""),
                    "url": metadata.get("url", ""),
                    "citations": metadata.get("citations", 0),
                    "relevance_score": round(score, 4),
                    "snippet": text[:300]
                })
        
        return {
            "query": query.query,
            "total_results": len(papers_data),
            "papers": papers_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
