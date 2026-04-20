from app.core.rag_pipeline import rag_query

CONTRADICTION_PROMPT = """You are an expert at analyzing research papers and identifying contradictions, inconsistencies, and conflicting findings.

Analyze the provided research papers and identify:

## Contradiction Analysis

### 1. Direct Contradictions
Papers with directly opposing findings or conclusions.

### 2. Methodological Inconsistencies
Different methodologies leading to conflicting results.

### 3. Context-Dependent Findings
Results that only hold in specific contexts, potentially conflicting across contexts.

### 4. Temporal Contradictions
Earlier findings contradicted by more recent research.

### 5. Sample/Population Conflicts
Contradictions arising from different study populations.

## Possible Explanations
Plausible reasons for the identified contradictions.

## Recommendations
How future research could resolve these contradictions.

Be specific, cite the papers involved, and provide nuanced analysis."""

async def detect_contradictions(topic: str) -> dict:
    result = await rag_query(
        query=f"contradictions and conflicting findings in research about {topic}",
        system_prompt=CONTRADICTION_PROMPT,
        k=15
    )
    return {
        "topic": topic,
        "analysis": result["response"],
        "sources": result["sources"]
    }
