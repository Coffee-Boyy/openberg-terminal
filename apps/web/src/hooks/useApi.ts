/** TanStack Query hooks for the OpenBerg Terminal API. */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';
import type { Security } from '@/types/security';
import type { Quote, PriceBar } from '@/types/security';
import type { NewsItem } from '@/types/news';

// ── Market data ───────────────────────────────────────────────

export function useQuotes(tickers: string[], refetchMs = 30_000) {
  return useQuery({
    queryKey: ['quotes', tickers],
    queryFn: () => api.getQuotes(tickers),
    refetchInterval: tickers.length > 0 ? refetchMs : false,
    staleTime: 10_000,
  });
}

export function usePriceHistory(ticker: string, interval: string, count = 200) {
  return useQuery({
    queryKey: ['prices', ticker, interval],
    queryFn: () => api.getPrices(ticker, interval, count),
    staleTime: 5 * 60_000,
  });
}

export function useSecurity(ticker: string) {
  return useQuery<Security | undefined>({
    queryKey: ['security', ticker],
    queryFn: () => api.getSecurity(ticker),
    staleTime: Infinity,
  });
}

export function useSearch(query: string, enabled: boolean) {
  return useQuery<Security[]>({
    queryKey: ['search', query],
    queryFn: () => api.searchSecurities(query),
    enabled,
    staleTime: 30_000,
  });
}

export function useNews(ticker?: string, limit = 50) {
  return useQuery({
    queryKey: ['news', ticker],
    queryFn: () => api.getNews(ticker, limit),
    refetchInterval: 5 * 60_000,
    staleTime: 5 * 60_000,
  });
}

export function useDividends(ticker: string) {
  return useQuery({
    queryKey: ['dividends', ticker],
    queryFn: () => api.getDividends(ticker),
    staleTime: Infinity,
  });
}

// ── Watchlist ─────────────────────────────────────────────────

export function useWatchlist() {
  return useQuery({
    queryKey: ['watchlist'],
    queryFn: () => api.getWatchlist(),
    staleTime: 30_000,
  });
}

// ── Portfolio ─────────────────────────────────────────────────

export function usePortfolio() {
  return useQuery({
    queryKey: ['portfolio'],
    queryFn: () => api.getPortfolio(),
    staleTime: 10_000,
  });
}

export function usePortfolioSummary() {
  return useQuery({
    queryKey: ['portfolio-summary'],
    queryFn: () => api.getPortfolioSummary(),
    staleTime: 10_000,
  });
}

// ── Alerts ────────────────────────────────────────────────────

export function useAlerts() {
  return useQuery({
    queryKey: ['alerts'],
    queryFn: () => api.getAlerts(),
    staleTime: 30_000,
  });
}

// ── Mutations ─────────────────────────────────────────────────

export function useMutationApi() {
  const qc = useQueryClient();
  return {
    addWatchlist: async (ticker: string, name?: string) => {
      await api.addWatchlist(ticker, name);
      await qc.invalidateQueries({ queryKey: ['watchlist'] });
    },
    removeWatchlist: async (ticker: string) => {
      await api.removeWatchlist(ticker);
      await qc.invalidateQueries({ queryKey: ['watchlist'] });
    },
    addPortfolio: async (ticker: string, shares: number, cost: number) => {
      await api.addPortfolio(ticker, shares, cost);
      await qc.invalidateQueries({ queryKey: ['portfolio'] });
      await qc.invalidateQueries({ queryKey: ['portfolio-summary'] });
    },
    removePortfolio: async (ticker: string) => {
      await api.removePortfolio(ticker);
      await qc.invalidateQueries({ queryKey: ['portfolio'] });
      await qc.invalidateQueries({ queryKey: ['portfolio-summary'] });
    },
    createAlert: async (ticker: string, alert_type: string, threshold: number) => {
      await api.createAlert(ticker, alert_type, threshold);
      await qc.invalidateQueries({ queryKey: ['alerts'] });
    },
    removeAlert: async (alertId: number) => {
      await api.removeAlert(alertId);
      await qc.invalidateQueries({ queryKey: ['alerts'] });
    },
  };
}
