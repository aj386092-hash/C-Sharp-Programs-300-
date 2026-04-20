import httpx
from typing import List
from app.models.paper import Paper
import hashlib

OPENALEX_BASE_URL = "https://api.openalex.org"

async def search_openalex(query: str, max_results: int = 10) -> List[Paper]:
    params = {
        "search": query,
        "per-page": min(max_results, 25),
        "select": "id,title,abstract_inverted_index,authorships,publication_year,cited_by_count,primary_location,keywords,doi,open_access,referenced_works",
        "mailto": "research@example.com"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{OPENALEX_BASE_URL}/works", params=params)
            response.raise_for_status()
            data = response.json()
        except (httpx.RequestError, Exception):
            return []
    
    papers = []
    for item in data.get("results", []):
        oa_id = item.get("id", "")
        paper_id = f"oa_{hashlib.md5(oa_id.encode()).hexdigest()[:12]}"
        
        # Reconstruct abstract from inverted index
        abstract = ""
        inv_index = item.get("abstract_inverted_index") or {}
        if inv_index:
            word_positions = {}
            for word, positions in inv_index.items():
                for pos in positions:
                    word_positions[pos] = word
            abstract = " ".join(word_positions[k] for k in sorted(word_positions.keys()))
        
        authors = []
        for authorship in item.get("authorships", []):
            author = authorship.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])
        
        location = item.get("primary_location") or {}
        source = location.get("source") or {}
        journal = source.get("display_name") if isinstance(source, dict) else None
        
        pdf_url = None
        open_access = item.get("open_access") or {}
        if isinstance(open_access, dict):
            pdf_url = open_access.get("oa_url")
        
        keywords = [kw.get("display_name", "") for kw in (item.get("keywords") or [])]
        
        refs = [(r.split("/")[-1]) for r in (item.get("referenced_works") or [])[:20]]
        
        paper = Paper(
            id=paper_id,
            title=item.get("title", "") or "",
            abstract=abstract,
            authors=authors,
            year=item.get("publication_year"),
            citations=item.get("cited_by_count", 0) or 0,
            references=refs,
            keywords=keywords,
            journal=journal,
            doi=item.get("doi"),
            pdf_url=pdf_url,
            source="openalex",
            url=oa_id
        )
        papers.append(paper)
    
    return papers
