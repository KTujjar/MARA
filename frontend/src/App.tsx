import { useState } from "react";
import { ChatInput } from "./components/ChatInput";
import { StreamingAnswerPanel } from "./components/StreamingAnswerPanel";
import { AgentActivitySidebar } from "./components/AgentActivitySidebar";
import { HistoryPanel } from "./components/HistoryPanel";
import { ReportView } from "./components/ReportView";
import { useAgentStream } from "./hooks/useAgentStream";
import "./App.css";

type View = "chat" | "history";

export default function App() {
  const stream = useAgentStream();
  const isBusy = stream.status === "streaming";

  const [view, setView] = useState<View>("chat");
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <div className="app-layout">
      <header>
        <h1>Research Assistant</h1>
        <nav className="view-tabs">
          <button
            className={view === "chat" ? "active" : undefined}
            onClick={() => setView("chat")}
          >
            New Query
          </button>
          <button
            className={view === "history" ? "active" : undefined}
            onClick={() => setView("history")}
          >
            History
          </button>
        </nav>
      </header>

      <main>
        {view === "chat" ? (
          <>
            <ChatInput onSubmit={stream.run} disabled={isBusy} />
            <StreamingAnswerPanel state={stream} />
          </>
        ) : selectedId !== null ? (
          <ReportView queryId={selectedId} />
        ) : (
          <div className="answer-panel empty">Select a past query to view its report.</div>
        )}
      </main>

      {view === "chat" ? (
        <AgentActivitySidebar updates={stream.updates} status={stream.status} />
      ) : (
        <HistoryPanel onSelect={setSelectedId} selectedId={selectedId} />
      )}
    </div>
  );
}
