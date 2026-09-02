import { useCallback, useRef, useState } from "react";
import {streamQuery} from "../api/client";
import type { AgentUpdate, StreamState } from "../types";

const initialState: StreamState = {
  status: "idle",
  updates: [],
  report: null,
  errorMessage: null,
};

export function useAgentStream() {
  const [state, setState] = useState<StreamState>(initialState);
  const abortRef = useRef<AbortController | null>(null);

  const run = useCallback(async (query: string) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setState({status: "streaming", updates: [], report: null, errorMessage: null});

    try {
      const res = await streamQuery(query, controller.signal);
      if(!res.ok || !res.body) throw new Error('Request failed: ${res.status}');

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while(true) {
        const {value, done} = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, {stream: true});

        const events = buffer.split("\n\n")
        buffer = events.pop() ?? "";

        for (const rawEvent of events){
          let eventType = "message";
          let dataLine = "";

          for (const line of rawEvent.split("\n")){
            if (line.startsWith("event:")) eventType = line.slice(6).trim();
            else if (line.startsWith("data:")) dataLine += line.slice(5).trim();
          }

          if (eventType === "done") {
            setState((prev) => ({ ...prev, status: "done"}));
            continue;
          }
          if(eventType === "error"){
            const parsed = safeParse(dataLine);
            setState((prev) => ({
              ...prev,
              status: "error",
              errorMessage: parsed?.message ?? "Unknown error",
            }));
            continue
          }
          
          const update = safeParse(dataLine) as AgentUpdate | null;
          if(!update) continue;

          setState((prev) => ({
            ...prev,
            updates: [...prev.updates, update],
            report: update.output?.report ?? prev.report,
          }));
        }
      }
      setState((prev) => (prev.status === "streaming" ? {...prev, status:"done"} : prev));
    } catch (err) {
      if ((err as Error).name === "AbortError") return;
      setState((prev) => ({...prev, status:"error", errorMessage: (err as Error).message }));
    }

  }, []);

  const cancel  = useCallback(() => abortRef.current?.abort(), []);

  return {...state, run, cancel};
}

function safeParse(text: string) {
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

