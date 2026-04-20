"use client";
import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import { researchAPI } from "@/lib/api";
import Link from "next/link";

const features = [
  { href: "/search", icon: "🔍", title: "Paper Search", desc: "Search across Semantic Scholar, arXiv, PubMed, and OpenAlex" },
  { href: "/literature-review", icon: "📚", title: "Literature Review", desc: "Auto-generate structured literature reviews with AI" },
  { href: "/gap-finder", icon: "🔬", title: "Research Gap Finder", desc: "Identify unexplored research areas and opportunities" },
  { href: "/citation-network", icon: "🕸️", title: "Citation Network", desc: "Visualize paper relationships and citation clusters" },
  { href: "/hypothesis", icon: "💡", title: "Hypothesis Generator", desc: "Generate novel testable research hypotheses" },
  { href: "/draft-analyzer", icon: "📝", title: "Draft Analyzer", desc: "Get AI critique of your research paper or thesis" },
  { href: "/chat", icon: "🤖", title: "AI Research Assistant", desc: "Conversational AI powered by your research corpus" },
];

export default function Dashboard() {
  const [stats, setStats] = useState<{ total_chunks?: number; status?: string } | null>(null);

  useEffect(() => {
    researchAPI.getStats().then((r) => setStats(r.data)).catch(() => {});
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-5xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-100">
              🎓 Academic Research Accelerator
            </h1>
            <p className="text-slate-400 mt-2 text-lg">
              AI-powered research assistant with RAG, multi-agent system, and semantic search
            </p>
          </div>

          {stats && (
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-blue-400">{stats.total_chunks?.toLocaleString() || 0}</div>
                <div className="text-xs text-slate-400 mt-1">Document Chunks Indexed</div>
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-green-400">4</div>
                <div className="text-xs text-slate-400 mt-1">Research APIs Connected</div>
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-purple-400">6</div>
                <div className="text-xs text-slate-400 mt-1">AI Agents Active</div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {features.map((f) => (
              <Link
                key={f.href}
                href={f.href}
                className="bg-slate-800 border border-slate-700 hover:border-blue-500/50 rounded-xl p-5 transition-all hover:shadow-lg hover:shadow-blue-500/5 group"
              >
                <div className="text-3xl mb-3">{f.icon}</div>
                <h3 className="font-semibold text-slate-100 group-hover:text-blue-400 transition-colors">{f.title}</h3>
                <p className="text-sm text-slate-400 mt-1">{f.desc}</p>
              </Link>
            ))}
          </div>

          <div className="mt-8 bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h2 className="font-semibold text-slate-100 mb-3">🚀 Quick Start</h2>
            <ol className="space-y-2 text-sm text-slate-400">
              <li className="flex gap-2"><span className="text-blue-400 font-bold">1.</span> Configure your API keys in <code className="bg-slate-700 px-1.5 py-0.5 rounded text-xs">backend/.env</code></li>
              <li className="flex gap-2"><span className="text-blue-400 font-bold">2.</span> Go to <strong className="text-slate-300">Paper Search</strong> to search and ingest research papers</li>
              <li className="flex gap-2"><span className="text-blue-400 font-bold">3.</span> Use <strong className="text-slate-300">Literature Review</strong> to auto-generate a review on any topic</li>
              <li className="flex gap-2"><span className="text-blue-400 font-bold">4.</span> Explore <strong className="text-slate-300">Research Gaps</strong> and <strong className="text-slate-300">Hypotheses</strong> for research opportunities</li>
              <li className="flex gap-2"><span className="text-blue-400 font-bold">5.</span> Upload your draft to <strong className="text-slate-300">Draft Analyzer</strong> for AI critique</li>
            </ol>
          </div>
        </div>
      </main>
    </div>
  );
}
