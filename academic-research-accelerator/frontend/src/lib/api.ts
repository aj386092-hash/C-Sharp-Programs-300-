import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 60000,
});

export interface Paper {
  paper_id: string;
  title: string;
  authors: string[];
  year?: number;
  source: string;
  url?: string;
  citations?: number;
  relevance_score?: number;
  snippet?: string;
}

export interface Source {
  title?: string;
  authors?: string[];
  year?: number;
  source?: string;
  url?: string;
}

export interface SearchResult {
  query: string;
  total_results: number;
  papers: Paper[];
}

export interface LiteratureReview {
  topic: string;
  review: string;
  sources: Source[];
  num_papers_analyzed: number;
}

export interface GapAnalysis {
  topic: string;
  gaps: string;
  sources: Source[];
}

export interface CitationNode {
  id: string;
  title: string;
  year?: number;
  citations: number;
  source: string;
  score: number;
}

export interface CitationNetwork {
  topic: string;
  nodes: CitationNode[];
  edges: { source: string; target: string }[];
  total_papers: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export const researchAPI = {
  searchPapers: (query: string, maxResults = 10, sources?: string[]) =>
    api.post<SearchResult>("/api/search/papers", {
      query,
      max_results: maxResults,
      sources: sources || ["semantic_scholar", "arxiv", "openalex", "pubmed"],
    }),

  ingestPapers: (query: string, maxResults = 20) =>
    api.post("/api/papers/ingest", {
      query,
      max_results: maxResults,
      sources: ["semantic_scholar", "arxiv", "openalex"],
    }),

  getStats: () => api.get("/api/papers/stats"),

  generateLiteratureReview: (topic: string, maxPapers = 20) =>
    api.post<LiteratureReview>("/api/review/literature", {
      topic,
      max_papers: maxPapers,
    }),

  identifyGaps: (topic: string) =>
    api.post<GapAnalysis>("/api/analysis/gaps", { topic }),

  suggestMethodology: (researchQuestion: string, domain?: string) =>
    api.post("/api/analysis/methodology", { research_question: researchQuestion, domain }),

  findContradictions: (topic: string) =>
    api.post("/api/analysis/contradictions", { topic }),

  generateHypotheses: (topic: string) =>
    api.post("/api/analysis/hypotheses", { topic }),

  getCitationNetwork: (topic: string, limit = 50) =>
    api.get<CitationNetwork>(`/api/analysis/citation-network?topic=${encodeURIComponent(topic)}&limit=${limit}`),

  reviewDraft: (draftText: string, title?: string) =>
    api.post("/api/review/draft", { draft_text: draftText, title }),

  uploadDraft: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/api/review/draft/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  chat: (messages: ChatMessage[]) =>
    api.post("/api/chat/", { messages }),
};

export default researchAPI;
