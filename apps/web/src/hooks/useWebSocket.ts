/** WebSocket hook for live quotes. */

import { useState, useEffect, useRef, useCallback } from 'react';
import { API_URL } from '@/config';
import type { Quote } from '@/types/security';

function wsUrl(): string {
  const base = API_URL.replace(/\/api$/, '');
  return `${base.replace(/^http/, 'ws')}/ws/quotes`;
}

export function useWebSocketQuotes(tickers: string[], pollInterval = 30_000) {
  const [quotes, setQuotes] = useState<Quote[] | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const quotesRef = useRef<Quote[]>([]);

  const poll = useCallback(async () => {
    if (!tickers.length) return;
    try {
      const url = `${API_URL}/api/quotes?tickers=${tickers.join(',')}`;
      const resp = await fetch(url);
      if (resp.ok) {
        const data: Quote[] = await resp.json();
        setQuotes(data);
        quotesRef.current = data;
      }
    } catch {
      // ignore polling failures
    }
  }, [tickers]);

  useEffect(() => {
    if (!tickers.length) return;
    const qs = new URLSearchParams({ tickers: tickers.join(',') });
    const url = `${wsUrl()}?${qs}`;
    let cancelled = false;
    let alive = true;

    function connect() {
      if (cancelled || !alive) return;
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.type === 'quotes') {
            setQuotes(msg.quotes);
            quotesRef.current = msg.quotes;
          }
        } catch {
          // ignore malformed messages
        }
      };

      ws.onopen = () => {
        setConnected(true);
        retryRef.current = 0;
      };

      ws.onclose = () => {
        setConnected(false);
        if (!alive) return;
        const delay = Math.min(1000 * Math.pow(2, retryRef.current), 10_000);
        retryRef.current += 1;
        setTimeout(connect, delay);
      };

      ws.onerror = () => ws.close();
    }

    connect();

    // Fallback to polling after 5 failed reconnection attempts
    const fallbackTimer = setTimeout(() => {
      if (retryRef.current >= 5) {
        wsRef.current?.close();
        wsRef.current = null;
        setConnected(false);
        timerRef.current = setInterval(poll, pollInterval);
      }
    }, 15_000);

    return () => {
      cancelled = true;
      alive = false;
      wsRef.current?.close();
      clearTimeout(fallbackTimer);
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [tickers.join(','), poll, pollInterval]);

  return { quotes, connected, latest: quotesRef.current };
}
