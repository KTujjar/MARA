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
