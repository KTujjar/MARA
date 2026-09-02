const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export function streamQuery(query: string, signal?: AbortSignal): Promise<Response> {
  return fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal,
  });
}
