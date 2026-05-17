/** Typed HTTP client for the OpenBerg Terminal backend. */

import { API_URL } from '@/config';

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public error: unknown,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export interface Health {
  status: string;
  version: string;
  adapters?: string[];
}

export interface WatchlistItem {
  id: number;
  ticker: string;
  name: string | null;
  added_at: string;
}

export interface PortfolioPosition {
  id: number;
  ticker: string;
  shares: number;
  avg_cost: number;
  current_price: number;
  added_at: string;
  updated_at: string;
}

export interface PortfolioSummary {
  total_value: number;
  total_cost: number;
  total_pnl: number;
  pnl_percent: number;
  position_count: number;
}

export interface AlertItem {
  id: number;
  ticker: string;
  alert_type: string;
  threshold: number;
  triggered: number;
  created_at: string;
  resolved_at: string | null;
}

import type { Quote, PriceBar, Security } from '@/types/security';
import type { NewsItem } from '@/types/news';

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const url = `${API_URL}${path}`;
  const resp = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!resp.ok) {
    const body = await resp.text().catch(() => '');
    throw new ApiError(`${resp.status} ${resp.statusText}: ${body}`, resp.status, body);
  }
  if (resp.status === 204) return undefined as T;
  return resp.json();
}

export const api = {
  // ── Market data ────────────────────────────────────────────

  health: (): Promise<Health> => request('/api/health'),

  searchSecurities: (q: string): Promise<Security[]> =>
    request(`/api/securities?q=${encodeURIComponent(q)}`),

  getSecurity: (ticker: string): Promise<Security> =>
    request(`/api/securities/${ticker}`),

  getQuotes: (tickers: string[]): Promise<Quote[]> =>
    request(`/api/quotes?tickers=${tickers.join(',')}`),

  getPrices: (ticker: string, interval: string, count: number = 200): Promise<PriceBar[]> =>
    request(`/api/prices/${ticker}?interval=${interval}&count=${count}`),

  getNews: (ticker?: string, limit: number = 50): Promise<NewsItem[]> => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (ticker) params.set('ticker', ticker);
    return request(`/api/news?${params}`);
  },

  getDividends: (ticker: string): Promise<{ date: string; amount: number | null }[]> =>
    request(`/api/dividends/${ticker}`),

  // ── Watchlist ──────────────────────────────────────────────

  getWatchlist: (): Promise<WatchlistItem[]> => request('/api/watchlist'),

  addWatchlist: (ticker: string, name?: string): Promise<WatchlistItem> =>
    request('/api/watchlist', {
      method: 'POST',
      body: JSON.stringify({ ticker, name }),
    }),

  removeWatchlist: (ticker: string): Promise<void> =>
    request(`/api/watchlist?ticker=${ticker}`, { method: 'DELETE' }),

  // ── Portfolio ─────────────────────────────────────────────

  getPortfolio: (): Promise<PortfolioPosition[]> => request('/api/portfolio'),

  getPortfolioSummary: (): Promise<PortfolioSummary> => request('/api/portfolio/summary'),

  addPortfolio: (ticker: string, shares: number, cost: number): Promise<PortfolioPosition> =>
    request('/api/portfolio', {
      method: 'POST',
      body: JSON.stringify({ ticker, shares, cost }),
    }),

  updatePortfolioPrice: (ticker: string, price: number): Promise<PortfolioPosition> =>
    request(`/api/portfolio/${ticker}/price`, {
      method: 'PATCH',
      body: JSON.stringify({ price }),
    }),

  removePortfolio: (ticker: string): Promise<void> =>
    request(`/api/portfolio?ticker=${ticker}`, { method: 'DELETE' }),

  // ── Alerts ─────────────────────────────────────────────────

  getAlerts: (): Promise<AlertItem[]> => request('/api/alerts'),

  createAlert: (ticker: string, alert_type: string, threshold: number): Promise<AlertItem> =>
    request('/api/alerts', {
      method: 'POST',
      body: JSON.stringify({ ticker, alert_type, threshold }),
    }),

  removeAlert: (alertId: number): Promise<void> =>
    request(`/api/alerts?id=${alertId}`, { method: 'DELETE' }),
};
