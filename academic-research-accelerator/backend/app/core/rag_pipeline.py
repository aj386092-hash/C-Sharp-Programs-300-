from typing import List, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.core.vector_store import get_vector_store
from app.models.paper import ChatMessage

client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

async def retrieve_context(query: str, k: int = 5) -> List[dict]:
    vector_store = get_vector_store()
    results = vector_store.search(query, k=k)
    return [
        {"text": text, "metadata": meta, "score": score}
        for text, meta, score in results
    ]

async def generate_response(
    query: str,
    context_docs: List[dict],
    system_prompt: str,
    conversation_history: Optional[List[ChatMessage]] = None
) -> str:
    if not client:
        return _mock_response(query, context_docs)
    
    context_text = "\n\n".join([
        f"[Paper: {doc['metadata'].get('title', 'Unknown')}]\n{doc['text']}"
        for doc in context_docs[:5]
    ])
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if conversation_history:
        for msg in conversation_history[-6:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    user_message = f"""Context from research papers:
{context_text}

User Query: {query}

Please provide a comprehensive, well-structured response based on the research context above."""
    
    messages.append({"role": "user", "content": user_message})
    
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.3,
        max_tokens=2000
    )
    return response.choices[0].message.content

def _mock_response(query: str, context_docs: List[dict]) -> str:
    papers = [doc['metadata'].get('title', 'Unknown') for doc in context_docs[:3]]
    paper_list = "\n".join([f"- {p}" for p in papers]) if papers else "- No papers found yet"
    return f"""**Research Analysis for: "{query}"**

Based on the available research corpus, here is a summary:

**Key Findings:**
The query "{query}" relates to active areas of research. Analysis of the available literature suggests several important trends and findings in this domain.

**Relevant Papers:**
{paper_list}

**Summary:**
This is a demonstration response. To get AI-powered insights, please configure your OpenAI API key in the .env file. The system will then use GPT models to generate comprehensive literature reviews, gap analyses, and research insights based on the retrieved papers.

**Next Steps:**
1. Configure OPENAI_API_KEY in your .env file
2. Ingest papers using the /api/papers/ingest endpoint
3. Use the search and analysis features for real AI-powered insights"""

async def rag_query(
    query: str,
    system_prompt: str,
    k: int = 5,
    conversation_history: Optional[List[ChatMessage]] = None
) -> dict:
    context_docs = await retrieve_context(query, k=k)
    response = await generate_response(query, context_docs, system_prompt, conversation_history)
    return {
        "response": response,
        "sources": [doc["metadata"] for doc in context_docs],
        "num_sources": len(context_docs)
    }
