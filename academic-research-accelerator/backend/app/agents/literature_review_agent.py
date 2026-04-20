from app.core.rag_pipeline import rag_query

LITERATURE_REVIEW_PROMPT = """You are an expert academic research assistant specializing in generating comprehensive literature reviews.

Generate a structured literature review in the following format:

## 1. Introduction
Brief overview of the research domain.

## 2. Key Studies and Contributions
Major papers and their contributions, citing authors and years.

## 3. Methodologies Used
Common research methods and approaches in the field.

## 4. Comparative Analysis
Compare findings, similarities and differences between studies.

## 5. Current Trends
Emerging patterns and directions in the research.

## 6. Limitations of Existing Research
Gaps, weaknesses, and unaddressed questions.

## 7. Summary
Concise summary of the state of the field.

Always cite papers from the provided context. Be academic, precise, and comprehensive."""

async def generate_literature_review(topic: str, max_papers: int = 20) -> dict:
    result = await rag_query(
        query=f"comprehensive literature review on {topic}",
        system_prompt=LITERATURE_REVIEW_PROMPT,
        k=max_papers
    )
    return {
        "topic": topic,
        "review": result["response"],
        "sources": result["sources"],
        "num_papers_analyzed": result["num_sources"]
    }
