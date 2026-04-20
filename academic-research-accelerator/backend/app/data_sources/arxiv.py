import httpx
import feedparser
from typing import List, Optional
from app.models.paper import Paper
import hashlib

ARXIV_BASE_URL = "http://export.arxiv.org/api/query"

async def search_arxiv(query: str, max_results: int = 10) -> List[Paper]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(ARXIV_BASE_URL, params=params)
            response.raise_for_status()
        except httpx.RequestError:
            return []
    
    feed = feedparser.parse(response.text)
    papers = []
    
    for entry in feed.entries:
        arxiv_id = entry.get("id", "").split("/abs/")[-1]
        paper_id = f"arxiv_{hashlib.md5(arxiv_id.encode()).hexdigest()[:12]}"
        
        authors = [author.name for author in entry.get("authors", [])]
        
        pdf_url = None
        for link in entry.get("links", []):
            if link.get("type") == "application/pdf":
                pdf_url = link.href
                break
        
        year = None
        published = entry.get("published", "")
        if published:
            try:
                year = int(published[:4])
            except (ValueError, IndexError):
                pass
        
        keywords = [tag.term for tag in entry.get("tags", [])]
        
        paper = Paper(
            id=paper_id,
            title=entry.get("title", "").replace("\n", " ").strip(),
            abstract=entry.get("summary", "").replace("\n", " ").strip(),
            authors=authors,
            year=year,
            keywords=keywords,
            pdf_url=pdf_url,
            source="arxiv",
            url=entry.get("id", ""),
            doi=entry.get("arxiv_doi", None)
        )
        papers.append(paper)
    
    return papers
