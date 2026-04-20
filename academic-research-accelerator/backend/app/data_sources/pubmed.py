import httpx
from typing import List
from app.models.paper import Paper
from app.config import settings
import hashlib
import json

PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

async def search_pubmed(query: str, max_results: int = 10) -> List[Paper]:
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": min(max_results, 100),
        "retmode": "json",
        "sort": "relevance"
    }
    if settings.ncbi_api_key:
        search_params["api_key"] = settings.ncbi_api_key
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            search_resp = await client.get(f"{PUBMED_BASE_URL}/esearch.fcgi", params=search_params)
            search_resp.raise_for_status()
            search_data = search_resp.json()
            pmids = search_data.get("esearchresult", {}).get("idlist", [])
        except (httpx.RequestError, Exception):
            return []
        
        if not pmids:
            return []
        
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
            "rettype": "abstract"
        }
        if settings.ncbi_api_key:
            fetch_params["api_key"] = settings.ncbi_api_key
        
        try:
            fetch_resp = await client.get(f"{PUBMED_BASE_URL}/efetch.fcgi", params=fetch_params)
            fetch_resp.raise_for_status()
        except (httpx.RequestError, Exception):
            return []
    
    # PubMed efetch with JSON returns complex structure; use summary instead
    summary_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json"
    }
    if settings.ncbi_api_key:
        summary_params["api_key"] = settings.ncbi_api_key
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            summary_resp = await client.get(f"{PUBMED_BASE_URL}/esummary.fcgi", params=summary_params)
            summary_resp.raise_for_status()
            summary_data = summary_resp.json()
        except (httpx.RequestError, Exception):
            return []
    
    papers = []
    result = summary_data.get("result", {})
    
    for pmid in pmids:
        item = result.get(pmid, {})
        if not item or "error" in item:
            continue
        
        paper_id = f"pubmed_{hashlib.md5(pmid.encode()).hexdigest()[:12]}"
        
        authors = [a.get("name", "") for a in item.get("authors", []) if a.get("authtype") == "Author"]
        
        pub_date = item.get("pubdate", "")
        year = None
        if pub_date:
            try:
                year = int(pub_date[:4])
            except (ValueError, IndexError):
                pass
        
        doi = None
        for article_id in item.get("articleids", []):
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value")
                break
        
        paper = Paper(
            id=paper_id,
            title=item.get("title", ""),
            abstract=item.get("source", ""),
            authors=authors,
            year=year,
            citations=0,
            keywords=[],
            journal=item.get("fulljournalname") or item.get("source"),
            doi=doi,
            source="pubmed",
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        )
        papers.append(paper)
    
    return papers
