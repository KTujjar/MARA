import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { fetchReport } from "../api/client";
import type { ReportDetail } from "../types";

export function ReportView({ queryId }: { queryId: number }) {
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setReport(null);
    setError(null);
    fetchReport(queryId)
      .then(setReport)
      .catch((e) => setError((e as Error).message));
  }, [queryId]);

  if (error) {
    return <div className="answer-panel error">Couldn't load report: {error}</div>;
  }
  if (!report) {
    return <div className="answer-panel">Loading…</div>;
  }

  return (
    <div className="answer-panel">
      <h2>{report.query}</h2>

      {report.report ? (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{report.report}</ReactMarkdown>
      ) : (
        <p className="muted">No report was generated for this query (status: {report.status}).</p>
      )}

      {report.critique_notes && (
        <details>
          <summary>Critique notes</summary>
          <p>{report.critique_notes}</p>
        </details>
      )}

      {report.findings.length > 0 && (
        <details>
          <summary>Findings ({report.findings.length})</summary>
          <ul>
            {report.findings.map((finding, i) => (
              <li key={i}>{finding}</li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
