"use client";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import LoadingSpinner from "@/components/LoadingSpinner";
import CitationGraph from "@/components/CitationGraph";
import { researchAPI, CitationNetwork } from "@/lib/api";

export default function CitationNetworkPage() {
  const [topic, setTopic] = useState("");
  const [network, setNetwork] = useState<CitationNetwork | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleVisualize = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setNetwork(null);
    try {
      const res = await researchAPI.getCitationNetwork(topic, 50);
      setNetwork(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to build citation network.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">🕸️ Citation Network Visualization</h1>
          <p className="text-slate-400 mb-6">Visualize citation relationships and research clusters using D3.js force graphs</p>

          <div className="flex gap-3 mb-6">
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleVisualize()}
              placeholder="e.g., BERT language model"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <button
              onClick={handleVisualize}
              disabled={loading || !topic.trim()}
              className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors whitespace-nowrap"
            >
              {loading ? "Building..." : "Visualize Network"}
            </button>
          </div>

          {error && <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-4 text-red-300 text-sm">{error}</div>}
          {loading && <LoadingSpinner message="Building citation network..." />}

          {network && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 text-sm text-slate-400">
                <span>📄 {network.total_papers} papers</span>
                <span>🔗 {network.edges.length} connections</span>
              </div>
              {network.nodes.length === 0 ? (
                <div className="bg-slate-800 border border-slate-700 rounded-xl p-8 text-center text-slate-400">
                  No papers found for this topic. Try searching and indexing papers first.
                </div>
              ) : (
                <CitationGraph nodes={network.nodes} edges={network.edges} />
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
