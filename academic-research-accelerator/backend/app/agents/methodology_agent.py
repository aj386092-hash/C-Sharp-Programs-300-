from app.core.rag_pipeline import rag_query

METHODOLOGY_PROMPT = """You are a research methodology expert. Based on the existing literature, recommend appropriate research methodologies.

Structure your recommendations as follows:

## Recommended Research Methodologies

### 1. Quantitative Approaches
Specific quantitative methods suitable for this research question.

### 2. Qualitative Approaches  
Qualitative methods that could provide valuable insights.

### 3. Mixed Methods
How combining approaches could strengthen research.

### 4. Data Collection Methods
Recommended data sources and collection strategies.

### 5. Analysis Techniques
Statistical and analytical methods to apply.

### 6. Validation Strategies
How to validate findings and ensure rigor.

### 7. Existing Successful Methodologies
What methods have worked well in similar studies.

Justify each recommendation with reference to the literature."""

async def recommend_methodology(research_question: str, domain: str = None) -> dict:
    query = f"research methodology for: {research_question}"
    if domain:
        query += f" in {domain}"
    
    result = await rag_query(
        query=query,
        system_prompt=METHODOLOGY_PROMPT,
        k=10
    )
    return {
        "research_question": research_question,
        "recommendations": result["response"],
        "sources": result["sources"]
    }
