from app.core.rag_pipeline import rag_query, retrieve_context
from app.config import settings
from openai import AsyncOpenAI

DRAFT_REVIEW_PROMPT = """You are an expert academic reviewer and research mentor. Critically analyze the submitted research draft.

Provide a comprehensive review covering:

## Research Draft Review

### 1. Overall Assessment
Overall quality and significance of the work (score out of 10).

### 2. Strengths
What the paper does well.

### 3. Critical Issues

#### Methodology Weaknesses
Problems with research design and methods.

#### Unsupported Claims
Claims lacking adequate evidence or citations.

#### Missing Citations
Important works that should be cited.

#### Logical Gaps
Flaws in reasoning or argumentation.

### 4. Writing Quality
Clarity, organization, grammar, and academic style.

### 5. Novelty Assessment
How original and innovative is the contribution (score out of 10)?

### 6. Specific Suggestions for Improvement
Actionable, specific recommendations.

### 7. Missing Sections or Elements
Important components that should be added.

Be constructive, specific, and detailed."""

async def review_draft(draft_text: str, title: str = None) -> dict:
    context_docs = await retrieve_context(draft_text[:500], k=8)
    
    client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    if not client:
        context_text = "\n\n".join([
            f"[Related Paper: {doc['metadata'].get('title', 'Unknown')}]"
            for doc in context_docs[:5]
        ])
        return {
            "title": title,
            "review": f"**Draft Review**\n\nTo get AI-powered draft review, please configure your OpenAI API key.\n\nRelated papers found in knowledge base:\n{context_text or 'None found yet'}",
            "related_papers": [doc["metadata"] for doc in context_docs],
            "overall_score": None,
            "novelty_score": None
        }
    
    context_text = "\n\n".join([
        f"[Related Paper: {doc['metadata'].get('title', 'Unknown')}]\n{doc['text']}"
        for doc in context_docs[:5]
    ])
    
    messages = [
        {"role": "system", "content": DRAFT_REVIEW_PROMPT},
        {"role": "user", "content": f"""Related papers from knowledge base:
{context_text}

Research Draft to Review:
Title: {title or 'Untitled'}

{draft_text[:6000]}

Please provide a comprehensive review of this research draft."""}
    ]
    
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.3,
        max_tokens=2500
    )
    
    review_text = response.choices[0].message.content
    
    return {
        "title": title,
        "review": review_text,
        "related_papers": [doc["metadata"] for doc in context_docs],
        "overall_score": None,
        "novelty_score": None
    }
