from fastapi import APIRouter, HTTPException
from app.models.paper import GapAnalysisRequest, MethodologyRequest, ContradictionRequest, HypothesisRequest
from app.agents.gap_detection_agent import detect_research_gaps
from app.agents.methodology_agent import recommend_methodology
from app.agents.contradiction_agent import detect_contradictions
from app.core.rag_pipeline import rag_query
from app.core.vector_store import get_vector_store
import networkx as nx

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

HYPOTHESIS_PROMPT = """You are a creative research scientist. Generate novel, testable research hypotheses.

Format your response as:

## Research Hypotheses

### Hypothesis 1: [Brief Title]
**Statement:** [Clear, testable hypothesis]
**Rationale:** [Why this hypothesis is worth testing]
**Methodology:** [How to test it]
**Expected Impact:** [Potential significance]

[Repeat for each hypothesis]

## Most Promising Directions
Which hypotheses have the highest potential for significant contributions.

Generate 5-7 distinct, novel hypotheses based on the research context."""

@router.post("/gaps", response_model=dict)
async def identify_gaps(request: GapAnalysisRequest):
    try:
        return await detect_research_gaps(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/methodology", response_model=dict)
async def suggest_methodology(request: MethodologyRequest):
    try:
        return await recommend_methodology(request.research_question, request.domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contradictions", response_model=dict)
async def find_contradictions(request: ContradictionRequest):
    try:
        return await detect_contradictions(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hypotheses", response_model=dict)
async def generate_hypotheses(request: HypothesisRequest):
    try:
        result = await rag_query(
            query=f"research hypotheses for {request.topic}",
            system_prompt=HYPOTHESIS_PROMPT,
            k=10
        )
        return {
            "topic": request.topic,
            "hypotheses": result["response"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/citation-network", response_model=dict)
async def get_citation_network(topic: str, limit: int = 50):
    try:
        vector_store = get_vector_store()
        results = vector_store.search(topic, k=limit)
        
        G = nx.DiGraph()
        seen_nodes = set()
        
        for text, metadata, score in results:
            paper_id = metadata.get("paper_id", "")
            if not paper_id or paper_id in seen_nodes:
                continue
            seen_nodes.add(paper_id)
            
            G.add_node(paper_id, 
                       title=metadata.get("title", "Unknown"),
                       year=metadata.get("year"),
                       citations=metadata.get("citations", 0),
                       source=metadata.get("source", ""),
                       score=round(score, 3))
        
        nodes = [
            {
                "id": n,
                "title": G.nodes[n].get("title", ""),
                "year": G.nodes[n].get("year"),
                "citations": G.nodes[n].get("citations", 0),
                "source": G.nodes[n].get("source", ""),
                "score": G.nodes[n].get("score", 0)
            }
            for n in G.nodes()
        ]
        
        edges = [{"source": u, "target": v} for u, v in G.edges()]
        
        return {
            "topic": topic,
            "nodes": nodes,
            "edges": edges,
            "total_papers": len(nodes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
