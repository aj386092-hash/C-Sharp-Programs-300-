import { Paper } from "@/lib/api";

interface PaperCardProps {
  paper: Paper;
}

const sourceColors: Record<string, string> = {
  arxiv: "bg-red-900/30 text-red-300",
  semantic_scholar: "bg-purple-900/30 text-purple-300",
  openalex: "bg-green-900/30 text-green-300",
  pubmed: "bg-blue-900/30 text-blue-300",
};

export default function PaperCard({ paper }: PaperCardProps) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-blue-500/50 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-sm leading-tight line-clamp-2">
            {paper.url ? (
              <a href={paper.url} target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 transition-colors">
                {paper.title}
              </a>
            ) : paper.title}
          </h3>
          {paper.authors && paper.authors.length > 0 && (
            <p className="text-xs text-slate-400 mt-1">
              {paper.authors.slice(0, 3).join(", ")}
              {paper.authors.length > 3 && " et al."}
            </p>
          )}
        </div>
        <span className={`text-xs px-2 py-0.5 rounded-full whitespace-nowrap flex-shrink-0 ${sourceColors[paper.source] || "bg-slate-700 text-slate-300"}`}>
          {paper.source?.replace("_", " ")}
        </span>
      </div>
      
      <div className="flex items-center gap-4 mt-3">
        {paper.year && <span className="text-xs text-slate-500">📅 {paper.year}</span>}
        {paper.citations != null && paper.citations > 0 && (
          <span className="text-xs text-slate-500">📊 {paper.citations} citations</span>
        )}
        {paper.relevance_score != null && (
          <span className="text-xs text-slate-500">🎯 {(paper.relevance_score * 100).toFixed(0)}% match</span>
        )}
      </div>
      
      {paper.snippet && (
        <p className="mt-2 text-xs text-slate-500 line-clamp-2">{paper.snippet}</p>
      )}
    </div>
  );
}
