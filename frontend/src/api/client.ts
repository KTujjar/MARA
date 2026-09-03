import type { HistoryItem, ReportDetail } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export function streamQuery(query: string, signal?: AbortSignal): Promise<Response> {
  return fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal,
  });
}

export async function fetchHistory(limit = 20): Promise<HistoryItem[]> {
  const res = await fetch(`${API_BASE}/history?limit=${limit}`);
  if (!res.ok) throw new Error(`Failed to load history: ${res.status}`);
  return res.json();
}

export async function fetchReport(id: number): Promise<ReportDetail> {
  const res = await fetch(`${API_BASE}/reports/${id}`);
  if (!res.ok) throw new Error(`Failed to load report: ${res.status}`);
  return res.json();
}
