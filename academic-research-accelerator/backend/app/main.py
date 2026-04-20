from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import papers, search, review, analysis, chat

app = FastAPI(
    title="Academic Research Accelerator API",
    description="AI-powered academic research assistant with RAG and multi-agent system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(papers.router)
app.include_router(search.router)
app.include_router(review.router)
app.include_router(analysis.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "name": "Academic Research Accelerator",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "papers": "/api/papers",
            "search": "/api/search",
            "review": "/api/review",
            "analysis": "/api/analysis",
            "chat": "/api/chat",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
