import { useEffect, useState } from "react";
import { fetchHistory } from "../api/client";
import type { HistoryItem } from "../types";

interface HistoryPanelProps {
  onSelect: (id: number) => void;
  selectedId: number | null;
}

export function HistoryPanel({ onSelect, selectedId }: HistoryPanelProps) {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory()
      .then(setItems)
      .catch((e) => setError((e as Error).message));
  }, []);

  return (
    <aside className="history-panel">
      <h3>Past Queries</h3>

      {error && <p className="history-error">Couldn't load history: {error}</p>}
      {!error && items.length === 0 && <p className="muted">No past queries yet.</p>}

      <ul className="history-list">
        {items.map((item) => (
          <li
            key={item.id}
            className={item.id === selectedId ? "selected" : undefined}
            onClick={() => onSelect(item.id)}
          >
            <span className={`status-dot status-${item.status}`} />
            <span className="history-query">{item.query}</span>
            <span className="history-date">{new Date(item.created_at).toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </aside>
  );
}

