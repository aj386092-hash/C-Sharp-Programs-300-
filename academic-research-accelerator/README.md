# 🎓 Academic Research Accelerator

An AI-powered full-stack academic research assistant that accelerates every stage of the research workflow — from literature discovery to manuscript review — using Retrieval-Augmented Generation (RAG), a multi-agent system, and semantic vector search.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Academic Research Accelerator                │
├─────────────────────────────┬───────────────────────────────────┤
│        Frontend (Next.js)   │         Backend (FastAPI)         │
│  ┌─────────────────────┐    │   ┌───────────────────────────┐   │
│  │  Dashboard          │    │   │  RAG Pipeline             │   │
│  │  Paper Search       │◄───┼──►│  FAISS Vector Store       │   │
│  │  Literature Review  │    │   │  Embedding Model          │   │
│  │  Gap Finder         │    │   └───────────────────────────┘   │
│  │  Citation Network   │    │   ┌───────────────────────────┐   │
│  │  Hypothesis Gen.    │    │   │  Multi-Agent System       │   │
│  │  Draft Analyzer     │    │   │  ├─ Literature Review     │   │
│  │  AI Chat            │    │   │  ├─ Gap Detection         │   │
│  └─────────────────────┘    │   │  ├─ Methodology Advisor   │   │
│                             │   │  ├─ Contradiction Finder   │   │
│  ┌─────────────────────┐    │   │  └─ Draft Reviewer        │   │
│  │  D3.js Force Graph  │    │   └───────────────────────────┘   │
│  │  React Markdown     │    │   ┌───────────────────────────┐   │
│  │  Tailwind CSS       │    │   │  Data Sources             │   │
│  └─────────────────────┘    │   │  ├─ Semantic Scholar API  │   │
│                             │   │  ├─ arXiv API             │   │
│                             │   │  ├─ PubMed (NCBI)         │   │
│                             │   │  └─ OpenAlex API          │   │
│                             │   └───────────────────────────┘   │
└─────────────────────────────┴───────────────────────────────────┘
```

---

## Features

1. **🔍 Paper Search** — Semantic search across Semantic Scholar, arXiv, PubMed, and OpenAlex simultaneously. Results are ranked by relevance using FAISS vector similarity.

2. **📚 Literature Review Generator** — Auto-generates structured, 7-section literature reviews using GPT models + RAG. Includes introduction, key contributions, methodologies, comparative analysis, trends, and limitations.

3. **🔬 Research Gap Finder** — Analyzes the ingested corpus to surface under-explored areas, methodological gaps, population/context gaps, and temporal gaps with actionable research directions.

4. **🕸️ Citation Network Visualization** — Interactive D3.js force-directed graph showing paper relationships, citation counts, and research clusters. Supports zoom, pan, and drag interactions.

5. **💡 Hypothesis Generator** — Generates 5–7 novel, testable research hypotheses with rationale, proposed methodology, and expected impact — grounded in the literature.

6. **📝 Draft Analyzer** — AI-powered peer review of research drafts (paste text or upload PDF/TXT). Assesses methodology, unsupported claims, missing citations, writing quality, and novelty.

7. **🤖 AI Research Assistant** — Conversational chat interface with multi-turn memory, powered by your indexed research corpus via RAG.

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional, for containerized deployment)
- OpenAI API key (optional — demo mode available without it)

---

## Local Development Setup

### Backend

```bash
cd academic-research-accelerator/backend

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys (OpenAI required for AI features)

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd academic-research-accelerator/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

---

## Docker Deployment

```bash
cd academic-research-accelerator

# Set your API keys
export OPENAI_API_KEY=your_key_here
export SEMANTIC_SCHOLAR_API_KEY=your_key_here  # optional

# Build and start all services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## API Documentation

All endpoints are documented interactively at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/papers/ingest` | Fetch papers from APIs and index in vector store |
| GET | `/api/papers/stats` | Get vector store statistics |
| POST | `/api/search/papers` | Semantic search over indexed papers |
| POST | `/api/review/literature` | Generate literature review |
| POST | `/api/review/draft` | Review a research draft (text) |
| POST | `/api/review/draft/upload` | Review a research draft (file upload) |
| POST | `/api/analysis/gaps` | Identify research gaps |
| POST | `/api/analysis/methodology` | Suggest research methodology |
| POST | `/api/analysis/contradictions` | Find contradicting findings |
| POST | `/api/analysis/hypotheses` | Generate research hypotheses |
| GET | `/api/analysis/citation-network` | Build citation network graph |
| POST | `/api/chat/` | Chat with AI research assistant |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | `""` (demo mode) |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar API key (increases rate limits) | `""` |
| `NCBI_API_KEY` | NCBI API key for PubMed (increases rate limits) | `""` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite+aiosqlite:///./research.db` |
| `FAISS_INDEX_PATH` | Path to store FAISS index files | `./faiss_index` |
| `EMBEDDING_MODEL` | Sentence transformer model name | `all-MiniLM-L6-v2` |
| `LLM_MODEL` | OpenAI model for generation | `gpt-4o-mini` |
| `MAX_PAPERS_PER_QUERY` | Max papers fetched per API source | `20` |
| `CHUNK_SIZE` | Text chunk size in words | `512` |
| `CHUNK_OVERLAP` | Overlap between chunks in words | `50` |

---

## Usage Guide

### Getting Started (5 minutes)

1. **Start both servers** (see Local Development Setup above)
2. **Navigate to Paper Search** (`/search`)
3. **Enter a research topic** (e.g., *"transformer models in medical imaging"*)
4. **Click "Fetch & Index"** to retrieve papers from all 4 APIs and index them
5. **Go to Literature Review** (`/literature-review`) and enter the same topic
6. **Click "Generate Review"** — the AI will synthesize a structured review
7. **Explore Research Gaps**, **Hypotheses**, and **Citation Network** for the topic
8. **Upload a draft** at `/draft-analyzer` to get AI-powered peer review
9. **Use the AI Chat** at `/chat` for interactive Q&A about the literature

### Demo Mode (No API Keys)

Without an OpenAI API key, the system still:
- Fetches and indexes papers from all 4 research databases
- Performs semantic vector search (FAISS)
- Returns structured mock responses showing what AI-powered analysis would look like
- Builds citation network visualizations

Configure `OPENAI_API_KEY` in `backend/.env` to unlock full AI-powered analysis.
