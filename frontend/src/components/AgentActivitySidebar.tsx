import type {AgentUpdate, StreamStatus} from "../types";
import { summarizeUpdate } from "../utils";

const NODE_ORDER = ["orchestrator", "research", "critique", "writer"];
const NODE_LABELS: Record<string, string> = {
  orchestrator: "Planning",
  research: "Researching",
  critique: "Fact-checking",
  writer: "Writing report",
};

interface AgentActivitySidebarProps{
  updates: AgentUpdate[];
  status: StreamStatus;
}

export function AgentActivitySidebar({updates, status}: AgentActivitySidebarProps){
  const lastNode = updates[updates.length - 1]?.node;
  const visited = new Set(updates.map((u) => u.node));

  return (
    <aside className="agent-activity">
      <h3>Pipeline</h3>
      <ul className="pipeline">
        {NODE_ORDER.map((node) => {
          const isActive = status === "streaming" && node === lastNode;
          const isDone = visited.has(node) && !isActive;
          return (
            <li key={node} className={isActive ? "active" : isDone ? "done" : "pending"}>
              <span className="dot" />
              {NODE_LABELS[node] ?? node}
              {isActive ? " …" : ""}
            </li>
          );
        })}
      </ul>

      <h3>Activity Log</h3>
      <ol className="activity-log">
        {status === "idle" && <li className="muted">Waiting for a query…</li>}
        {updates.map((update, i) => (
          <li key={i}>{summarizeUpdate(update)}</li>
        ))}
      </ol>
    </aside>
  );
}
