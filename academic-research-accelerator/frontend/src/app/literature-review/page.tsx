"use client";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import LoadingSpinner from "@/components/LoadingSpinner";
import ReactMarkdown from "react-markdown";
import { researchAPI, LiteratureReview, Source } from "@/lib/api";

export default function LiteratureReviewPage() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState<LiteratureReview | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await researchAPI.generateLiteratureReview(topic, 20);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to generate review.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">📚 Literature Review Generator</h1>
          <p className="text-slate-400 mb-6">Auto-generate comprehensive, structured literature reviews powered by AI + RAG</p>

          <div className="flex gap-3 mb-6">
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
              placeholder="e.g., deep learning in medical imaging"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
            <button
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors whitespace-nowrap"
            >
              {loading ? "Generating..." : "Generate Review"}
            </button>
          </div>

          {error && <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-4 text-red-300 text-sm">{error}</div>}
          {loading && <LoadingSpinner message="Generating literature review with AI..." />}

          {result && (
            <div className="space-y-6">
              <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-slate-100">Literature Review: {result.topic}</h2>
                  <span className="text-xs bg-blue-900/30 text-blue-300 px-3 py-1 rounded-full">
                    {result.num_papers_analyzed} papers analyzed
                  </span>
                </div>
                <div className="prose prose-invert max-w-none text-sm">
                  <ReactMarkdown>{result.review}</ReactMarkdown>
                </div>
              </div>

              {result.sources && result.sources.length > 0 && (
                <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
                  <h3 className="font-semibold text-slate-100 mb-3">📎 Sources Used</h3>
                  <div className="space-y-2">
                    {result.sources.slice(0, 10).map((s: Source, i) => (
                      <div key={i} className="text-xs text-slate-400 flex gap-2">
                        <span className="text-blue-400 font-bold">[{i + 1}]</span>
                        <span>
                          {s.title || "Unknown"}{s.authors && s.authors.length > 0 && ` — ${s.authors.slice(0, 2).join(", ")}`}{s.year && ` (${s.year})`}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
