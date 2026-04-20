from fastapi import APIRouter, HTTPException
from app.models.paper import ChatRequest
from app.core.rag_pipeline import rag_query

router = APIRouter(prefix="/api/chat", tags=["chat"])

CHAT_PROMPT = """You are an intelligent academic research assistant with deep knowledge across scientific disciplines. 

You help researchers by:
- Answering questions about research papers and findings
- Explaining complex concepts clearly
- Suggesting research directions
- Analyzing methodologies
- Identifying connections between papers

Always:
- Base your responses on the provided research context
- Cite specific papers when possible
- Be accurate and acknowledge uncertainty
- Provide actionable insights
- Use academic but accessible language"""

@router.post("/", response_model=dict)
async def chat_with_assistant(request: ChatRequest):
    try:
        last_message = request.messages[-1].content if request.messages else ""
        
        result = await rag_query(
            query=last_message,
            system_prompt=CHAT_PROMPT,
            k=8,
            conversation_history=request.messages[:-1] if len(request.messages) > 1 else None
        )
        
        return {
            "response": result["response"],
            "sources": result["sources"],
            "num_sources": result["num_sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
