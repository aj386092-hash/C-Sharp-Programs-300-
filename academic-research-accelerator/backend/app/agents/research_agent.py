from typing import List
from app.models.paper import Paper, SearchQuery
from app.data_sources.arxiv import search_arxiv
from app.data_sources.semantic_scholar import search_semantic_scholar
from app.data_sources.openalex import search_openalex
from app.data_sources.pubmed import search_pubmed
from app.core.vector_store import get_vector_store
from app.utils.text_processor import clean_text, chunk_text
import asyncio

async def ingest_papers(query: SearchQuery) -> List[Paper]:
    tasks = []
    if "arxiv" in query.sources:
        tasks.append(search_arxiv(query.query, query.max_results))
    if "semantic_scholar" in query.sources:
        tasks.append(search_semantic_scholar(query.query, query.max_results))
    if "openalex" in query.sources:
        tasks.append(search_openalex(query.query, query.max_results))
    if "pubmed" in query.sources:
        tasks.append(search_pubmed(query.query, query.max_results))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_papers: List[Paper] = []
    seen_titles = set()
    
    for result in results:
        if isinstance(result, list):
            for paper in result:
                title_key = paper.title.lower().strip()[:80]
                if title_key and title_key not in seen_titles:
                    seen_titles.add(title_key)
                    all_papers.append(paper)
    
    # Store in vector database
    await store_papers_in_vector_db(all_papers)
    
    return all_papers

async def store_papers_in_vector_db(papers: List[Paper]) -> None:
    vector_store = get_vector_store()
    texts = []
    metadatas = []
    
    for paper in papers:
        content = f"{paper.title}\n\n{paper.abstract or ''}"
        content = clean_text(content)
        if len(content) < 50:
            continue
        
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({
                "paper_id": paper.id,
                "title": paper.title,
                "authors": paper.authors[:3],
                "year": paper.year,
                "source": paper.source,
                "url": paper.url,
                "chunk_index": i,
                "citations": paper.citations
            })
    
    if texts:
        vector_store.add_documents(texts, metadatas)
