"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard", icon: "🏠" },
  { href: "/search", label: "Paper Search", icon: "🔍" },
  { href: "/literature-review", label: "Literature Review", icon: "📚" },
  { href: "/gap-finder", label: "Gap Finder", icon: "🔬" },
  { href: "/citation-network", label: "Citation Network", icon: "🕸️" },
  { href: "/hypothesis", label: "Hypothesis Generator", icon: "💡" },
  { href: "/draft-analyzer", label: "Draft Analyzer", icon: "📝" },
  { href: "/chat", label: "AI Assistant", icon: "🤖" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-slate-800 border-r border-slate-700 z-10">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-lg font-bold text-blue-400">🎓 Research</h1>
        <p className="text-xs text-slate-400 mt-1">Academic Research Accelerator</p>
      </div>
      <nav className="p-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
              pathname === item.href
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-700 hover:text-white"
            }`}
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
