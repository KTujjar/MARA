import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { StreamState } from "../types";

export function StreamingAnswerPanel({ state }: { state: StreamState }) {
  const { status, report, errorMessage, updates } = state;

  if (status === "idle") {
    return <div className="answer-panel empty">Ask a question to get started.</div>;
  }
  if (status === "error") {
    return <div className="answer-panel error">Something went wrong: {errorMessage}</div>;
  }
  if (report) {
    return (
      <div className="answer-panel">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{report}</ReactMarkdown>
      </div>
    );
  }

  const preview = extractPreviewText(updates);
  return (
    <div className="answer-panel streaming">
      <h2>Working…</h2>
      <div className="report-body">{preview ?? "Gathering information…"}</div>
    </div>
  );
}

function extractPreviewText(updates: StreamState["updates"]): string | null {
  const last = [...updates].reverse().find((u) => u.output.plan || u.output.findings?.length);
  if (!last) return null;
  const { findings, plan } = last.output;
  if (findings?.length) return findings[findings.length - 1];
  return plan ?? null;
}
