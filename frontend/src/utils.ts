import type { AgentUpdate } from "./types";

export function summarizeUpdate(update: AgentUpdate): string {
  const { node, output } = update;
  switch (node) {
    case "orchestrator":
      return "Drafted a research plan";
    case "research":
      return `Completed research round ${output.research_rounds ?? "?"}`;
    case "critique":
      return output.needs_more_research
        ? `Found gaps — looping back to research${output.critique_notes ? `: ${output.critique_notes}` : ""}`
        : "Findings look solid — moving to write-up";
    case "writer":
      return "Synthesized the final report";
    default:
      return `Update from ${node}`;
  }
}
