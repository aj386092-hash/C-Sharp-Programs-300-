"use client";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import PaperCard from "@/components/PaperCard";
import LoadingSpinner from "@/components/LoadingSpinner";
import { researchAPI, Paper } from "@/lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    setPapers([]);
    try {
      const res = await researchAPI.searchPapers(query, 20);
      setPapers(res.data.papers);
      setSearched(true);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Search failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    if (!query.trim()) return;
    setIngesting(true);
    setError("");
    try {
      const res = await researchAPI.ingestPapers(query, 20);
      const ingested = res.data.papers || [];
      if (ingested.length > 0) {
        setPapers(ingested.map((p: any) => ({
          paper_id: p.id,
          title: p.title,
          authors: p.authors || [],
          year: p.year,
          source: p.source,
          url: p.url,
          citations: p.citations,
        })));
      }
      setSearched(true);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Ingestion failed.");
    } finally {
      setIngesting(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">🔍 Research Paper Search</h1>
          <p className="text-slate-400 mb-6">Search across Semantic Scholar, arXiv, PubMed, and OpenAlex</p>

          <div className="flex gap-3 mb-6">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder="e.g., transformer models in medical imaging"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="px-5 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
            >
              {loading ? "Searching..." : "Search"}
            </button>
            <button
              onClick={handleIngest}
              disabled={ingesting || !query.trim()}
              title="Fetch from APIs and add to knowledge base"
              className="px-5 py-3 bg-green-700 hover:bg-green-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
            >
              {ingesting ? "Fetching..." : "Fetch & Index"}
            </button>
          </div>

          {error && (
            <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-4 text-red-300 text-sm">{error}</div>
          )}

          {loading && <LoadingSpinner message="Searching knowledge base..." />}
          {ingesting && <LoadingSpinner message="Fetching papers from APIs and indexing..." />}

          {!loading && !ingesting && searched && (
            <>
              <p className="text-sm text-slate-400 mb-4">{papers.length} papers found</p>
              {papers.length === 0 ? (
                <div className="text-center py-12 text-slate-500">
                  <p>No papers found. Try clicking "Fetch & Index" to retrieve papers from research APIs.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {papers.map((p) => <PaperCard key={p.paper_id} paper={p} />)}
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
