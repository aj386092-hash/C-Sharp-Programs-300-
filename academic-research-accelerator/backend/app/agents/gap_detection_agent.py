from app.core.rag_pipeline import rag_query

GAP_DETECTION_PROMPT = """You are a research gap analysis expert. Your task is to identify under-explored areas and research opportunities in the given field.

Analyze the provided research papers and identify:

## Research Gaps Identified

### 1. Unexplored Areas
Topics and questions that have received little to no research attention.

### 2. Methodological Gaps
Research methods or approaches not yet applied to this domain.

### 3. Population/Context Gaps
Under-represented populations, contexts, or settings in existing research.

### 4. Temporal Gaps
Recent developments not yet studied academically.

### 5. Contradiction Opportunities
Areas where conflicting findings need resolution through new research.

## Suggested Research Directions
Specific, actionable research questions and directions.

Be specific and provide justification for each identified gap based on the literature."""

async def detect_research_gaps(topic: str) -> dict:
    result = await rag_query(
        query=f"research gaps and unexplored areas in {topic}",
        system_prompt=GAP_DETECTION_PROMPT,
        k=15
    )
    return {
        "topic": topic,
        "gaps": result["response"],
        "sources": result["sources"]
    }
