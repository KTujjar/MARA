import { ChatInput } from "./components/ChatInput";
import { StreamingAnswerPanel } from "./components/StreamingAnswerPanel";
import { AgentActivitySidebar } from "./components/AgentActivitySidebar";
import { useAgentStream } from "./hooks/useAgentStream";
import "./App.css";

export default function App() {
  const stream = useAgentStream();
  const isBusy = stream.status === "streaming";

  return (
    <div className="app-layout">
      <header>
        <h1>Research Assistant</h1>
      </header>
      <main>
        <ChatInput onSubmit={stream.run} disabled={isBusy} />
        <StreamingAnswerPanel state={stream} />
      </main>
      <AgentActivitySidebar updates={stream.updates} status={stream.status} />
    </div>
  );
}
