"use client";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import LoadingSpinner from "@/components/LoadingSpinner";
import ReactMarkdown from "react-markdown";
import { researchAPI } from "@/lib/api";

export default function GapFinderPage() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await researchAPI.identifyGaps(topic);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">🔬 Research Gap Finder</h1>
          <p className="text-slate-400 mb-6">Identify under-explored research areas and opportunities using AI analysis</p>

          <div className="flex gap-3 mb-6">
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
              placeholder="e.g., NLP for low-resource languages"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <button
              onClick={handleAnalyze}
              disabled={loading || !topic.trim()}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors whitespace-nowrap"
            >
              {loading ? "Analyzing..." : "Find Gaps"}
            </button>
          </div>

          {error && <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-4 text-red-300 text-sm">{error}</div>}
          {loading && <LoadingSpinner message="Analyzing research coverage and identifying gaps..." />}

          {result && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-slate-100 mb-4">Research Gaps: {result.topic}</h2>
              <div className="prose prose-invert max-w-none text-sm">
                <ReactMarkdown>{result.gaps}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
