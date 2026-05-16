import { create } from 'zustand';
import { generateQuotes } from '@/services/demo-data';

interface WatchlistState {
  items: ReturnType<typeof generateQuotes>;
  addTicker: (ticker: string) => void;
  removeTicker: (ticker: string) => void;
  refresh: () => void;
}

export const useWatchlist = create<WatchlistState>((set, get) => ({
  items: generateQuotes(['AAPL', 'GOOG', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'META', 'JPM']),
  addTicker: (ticker) => {
    const items = get().items;
    if (items.find((i) => i.ticker === ticker.toUpperCase())) return;
    set({ items: [...items, ...generateQuotes([ticker])] });
  },
  removeTicker: (ticker) => {
    set({ items: get().items.filter((i) => i.ticker !== ticker.toUpperCase()) });
  },
  refresh: () => {
    const tickers = get().items.map((i) => i.ticker);
    set({ items: generateQuotes(tickers) });
  },
}));
