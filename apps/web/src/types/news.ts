export interface NewsItem {
  id: string;
  headline: string;
  summary: string;
  source: string;
  published: string;
  updated?: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  tickers: string[];
  categories: string[];
  url?: string;
}
