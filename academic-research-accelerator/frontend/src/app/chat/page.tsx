import Sidebar from "@/components/Sidebar";
import ChatAssistant from "@/components/ChatAssistant";

export default function ChatPage() {
  return (
    <div className="flex min-h-screen bg-slate-900">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-100 mb-2">🤖 AI Research Assistant</h1>
          <p className="text-slate-400 mb-6">
            Chat with an AI assistant powered by your research corpus. Ask questions, get insights, and explore the literature.
          </p>
          <ChatAssistant />
        </div>
      </main>
    </div>
  );
}
