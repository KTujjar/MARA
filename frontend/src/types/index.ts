export type AgentNode = "orchestrator" | "research" | "critique" | "writer";

export interface AgentNodeOutput {
  plan?: string;
  findings?: string[];
  research_rounds?: number;
  critique_notes?: string;
  needs_more_research?: boolean;
  report?: string;
}

export interface AgentUpdate {
  node: AgentNode | string;
  output: AgentNodeOutput;
}

export type StreamStatus = "idle" | "streaming" | "done" | "error";

export interface StreamState {
  status: StreamStatus;
  updates: AgentUpdate[];
  report: string | null;
  errorMessage: string | null;
}

// Matches GET /history — one row per past query, no findings/report body.
export interface HistoryItem {
  id: number;
  query: string;
  status: string;
  created_at: string;
  completed_at: string | null;
}

// Matches GET /reports/{id} — the full record for one past query.
export interface ReportDetail {
  id: number;
  query: string;
  status: string;
  critique_notes: string | null;
  research_rounds: number;
  findings: string[];
  report: string | null;
  created_at: string;
  completed_at: string | null;
}
