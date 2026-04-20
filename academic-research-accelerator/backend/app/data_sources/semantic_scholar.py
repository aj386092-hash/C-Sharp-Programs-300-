import httpx
from typing import List, Optional
from app.models.paper import Paper
from app.config import settings
import hashlib

SS_BASE_URL = "https://api.semanticscholar.org/graph/v1"

async def search_semantic_scholar(query: str, max_results: int = 10) -> List[Paper]:
    fields = "title,abstract,authors,year,citationCount,references,externalIds,fieldsOfStudy,publicationVenue,openAccessPdf"
    
    headers = {}
    if settings.semantic_scholar_api_key:
        headers["x-api-key"] = settings.semantic_scholar_api_key
    
    params = {
        "query": query,
        "limit": min(max_results, 100),
        "fields": fields
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{SS_BASE_URL}/paper/search",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.RequestError, Exception):
            return []
    
    papers = []
    for item in data.get("data", []):
        ss_id = item.get("paperId", "")
        paper_id = f"ss_{hashlib.md5(ss_id.encode()).hexdigest()[:12]}"
        
        authors = [a.get("name", "") for a in item.get("authors", [])]
        
        refs = [r.get("paperId", "") for r in item.get("references", []) if r.get("paperId")]
        
        doi = None
        external_ids = item.get("externalIds", {}) or {}
        if "DOI" in external_ids:
            doi = external_ids["DOI"]
        
        pdf_url = None
        open_access = item.get("openAccessPdf")
        if open_access and isinstance(open_access, dict):
            pdf_url = open_access.get("url")
        
        venue = item.get("publicationVenue") or {}
        journal = venue.get("name") if isinstance(venue, dict) else None
        
        paper = Paper(
            id=paper_id,
            title=item.get("title", ""),
            abstract=item.get("abstract", "") or "",
            authors=authors,
            year=item.get("year"),
            citations=item.get("citationCount", 0) or 0,
            references=refs[:20],
            keywords=item.get("fieldsOfStudy", []) or [],
            journal=journal,
            doi=doi,
            pdf_url=pdf_url,
            source="semantic_scholar",
            url=f"https://www.semanticscholar.org/paper/{ss_id}"
        )
        papers.append(paper)
    
    return papers
