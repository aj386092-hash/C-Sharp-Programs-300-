"use client";
import { useState, useRef } from "react";
import Sidebar from "@/components/Sidebar";
import LoadingSpinner from "@/components/LoadingSpinner";
import ReactMarkdown from "react-markdown";
import { researchAPI } from "@/lib/api";

export default function DraftAnalyzerPage() {
  const [draftText, setDraftText] = useState("");
  const [title, setTitle] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"text" | "upload">("text");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleReview = async () => {
    if (!draftText.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await researchAPI.reviewDraft(draftText, title || undefined);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Review failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await researchAPI.uploadDraft(file);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Upload review failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">📝 Research Draft Analyzer</h1>
          <p className="text-slate-400 mb-6">Get AI-powered critique of your research paper, thesis, or proposal</p>

          <div className="flex gap-2 mb-4">
            {(["text", "upload"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === tab ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-100"
                }`}
              >
                {tab === "text" ? "Paste Text" : "Upload PDF/Text"}
              </button>
            ))}
          </div>

          {activeTab === "text" ? (
            <div className="space-y-3 mb-6">
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Paper title (optional)"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm"
              />
              <textarea
                value={draftText}
                onChange={(e) => setDraftText(e.target.value)}
                placeholder="Paste your research paper, thesis, or proposal text here..."
                rows={12}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm resize-none"
              />
              <button
                onClick={handleReview}
                disabled={loading || !draftText.trim()}
                className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                {loading ? "Analyzing..." : "Analyze Draft"}
              </button>
            </div>
          ) : (
            <div className="mb-6">
              <div
                className="border-2 border-dashed border-slate-700 hover:border-blue-500/50 rounded-xl p-12 text-center cursor-pointer transition-colors"
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="text-4xl mb-3">📄</div>
                <p className="text-slate-400 text-sm">Click to upload PDF or text file</p>
                <p className="text-slate-500 text-xs mt-1">PDF, TXT supported</p>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.txt"
                className="hidden"
                onChange={handleFileUpload}
              />
            </div>
          )}

          {error && <div className="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-4 text-red-300 text-sm">{error}</div>}
          {loading && <LoadingSpinner message="AI is reviewing your draft..." />}

          {result && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
              <h2 className="text-lg font-semibold text-slate-100 mb-4">
                Review: {result.title || "Your Draft"}
              </h2>
              <div className="prose prose-invert max-w-none text-sm">
                <ReactMarkdown>{result.review}</ReactMarkdown>
              </div>
              {result.related_papers && result.related_papers.length > 0 && (
                <div className="mt-6 pt-4 border-t border-slate-700">
                  <h3 className="text-sm font-semibold text-slate-300 mb-2">📚 Related Papers from Knowledge Base</h3>
                  <div className="space-y-1">
                    {result.related_papers.slice(0, 5).map((p: any, i: number) => (
                      <div key={i} className="text-xs text-slate-400">
                        • {p.title || "Unknown"}{p.year && ` (${p.year})`}
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
