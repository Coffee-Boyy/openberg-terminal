import type { Quote } from '@/types/security';
import type { NewsItem } from '@/types/news';
import type { Security } from '@/types/security';
import type { Alert } from '@/types/alert';
import type { PriceBar } from '@/types/security';

// ── Deterministic seeded RNG for reproducibility ──
function mulberry32(a: number) {
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hash(str: string): number {
  let h = 5381;
  for (let i = 0; i < str.length; i++) h = h * 31 + str.charCodeAt(i);
  return h >>> 0;
}

// ── Realistic security seed data ──
const SECURITIES: Record<string, Partial<Security>> = {
  AAPL: { name: 'Apple Inc.', exchange: 'NASDAQ', sector: 'Technology', industry: 'Consumer Electronics', currency: 'USD', marketCap: 3_050_000_000_000, peRatio: 31.2, eps: 6.13, dividendYield: 0.5, beta: 1.18 },
  GOOG: { name: 'Alphabet Inc.', exchange: 'NASDAQ', sector: 'Technology', industry: 'Internet Content & Services', currency: 'USD', marketCap: 2_100_000_000_000, peRatio: 27.5, eps: 6.05, dividendYield: 0, beta: 1.06 },
  MSFT: { name: 'Microsoft Corp.', exchange: 'NASDAQ', sector: 'Technology', industry: 'Systems Software', currency: 'USD', marketCap: 3_200_000_000_000, peRatio: 36.8, eps: 11.05, dividendYield: 0.7, beta: 0.92 },
  AMZN: { name: 'Amazon.com Inc.', exchange: 'NASDAQ', sector: 'Consumer Discretionary', industry: 'Internet Retail', currency: 'USD', marketCap: 2_200_000_000_000, peRatio: 60.1, eps: 3.01, dividendYield: 0, beta: 1.18 },
  TSLA: { name: 'Tesla Inc.', exchange: 'NASDAQ', sector: 'Consumer Discretionary', industry: 'Auto Manufacturers', currency: 'USD', marketCap: 560_000_000_000, peRatio: 95.4, eps: 3.75, dividendYield: 0, beta: 2.27 },
  NVDA: { name: 'NVIDIA Corp.', exchange: 'NASDAQ', sector: 'Technology', industry: 'Semiconductors', currency: 'USD', marketCap: 2_800_000_000_000, peRatio: 64.8, eps: 13.4, dividendYield: 0.02, beta: 1.68 },
  META: { name: 'Meta Platforms Inc.', exchange: 'NASDAQ', sector: 'Technology', industry: 'Internet Content & Services', currency: 'USD', marketCap: 1_500_000_000_000, peRatio: 28.3, eps: 19.72, dividendYield: 0.3, beta: 1.18 },
  JPM: { name: 'JPMorgan Chase & Co.', exchange: 'NYSE', sector: 'Financials', industry: 'Banks', currency: 'USD', marketCap: 620_000_000_000, peRatio: 12.1, eps: 17.37, dividendYield: 2.2, beta: 1.12 },
  V: { name: 'Visa Inc.', exchange: 'NYSE', sector: 'Financials', industry: 'Data Processing Services', currency: 'USD', marketCap: 520_000_000_000, peRatio: 31.0, eps: 8.88, dividendYield: 0.7, beta: 0.94 },
  WMT: { name: 'Walmart Inc.', exchange: 'NYSE', sector: 'Consumer Staples', industry: 'Discount Stores', currency: 'USD', marketCap: 480_000_000_000, peRatio: 29.5, eps: 6.29, dividendYield: 1.2, beta: 0.52 },
  'SPY': { name: 'SPDR S&P 500 ETF Trust', exchange: 'NYSE Arca', sector: 'Index', industry: 'Broad Market', currency: 'USD', marketCap: 500_000_000_000, peRatio: 0, eps: 0, dividendYield: 0.85, beta: 1.0 },
  BTC: { name: 'Bitcoin USD', exchange: 'CRYPTO', sector: 'Crypto', industry: 'Currency', currency: 'USD', marketCap: 1_900_000_000_000, peRatio: 0, eps: 0, beta: 0 },
  EURUSD: { name: 'EUR/USD', exchange: 'FOREX', sector: 'Forex', industry: 'Currency', currency: 'USD', peRatio: 0, eps: 0, beta: 0 },
};

function basePrice(ticker: string): number {
  const h = hash(ticker);
  const prices: Record<string, number> = {
    AAPL: 198.2, GOOG: 172.5, MSFT: 389.1, AMZN: 180.7,
    TSLA: 177.4, NVDA: 875.3, META: 502.8, JPM: 210.3,
    V: 283.5, WMT: 185.6, SPY: 520.4, BTC: 67_500, EURUSD: 1.085,
  };
  return prices[ticker] || 100 + (h % 400);
}

function generateQuotes(tickers: string[]): Quote[] {
  return tickers.map((ticker) => {
    const h = hash(ticker);
    const rng = mulberry32(h);
    const price = basePrice(ticker);
    const changePct = (rng() - 0.45) * 4;
    const change = price * changePct / 100;
    const spread = price > 1000 ? 5 : price > 100 ? 0.15 : 0.01;
    return {
      ticker: ticker.toUpperCase(),
      exchange: SECURITIES[ticker]?.exchange || 'NASDAQ',
      currency: SECURITIES[ticker]?.currency || 'USD',
      bid: price - spread / 2,
      ask: price + spread / 2,
      last: price,
      change,
      changePercent: changePct,
      volume: Math.floor(rng() * 50_000_000) + 100_000,
      marketCap: SECURITIES[ticker]?.marketCap,
      timestamp: new Date().toISOString(),
    };
  });
}

function generatePriceBars(ticker: string, interval: string, count: number): PriceBar[] {
  const h = hash(ticker + interval);
  const rng = mulberry32(h);
  const price = basePrice(ticker);
  const result: PriceBar[] = [];
  const now = new Date();

  const msPerBar: Record<string, number> = {
    '1m': 60_000, '5m': 300_000, '15m': 900_000,
    '1h': 3_600_000, '4h': 14_400_000, '1d': 86_400_000, '1w': 604_800_000, '1mo': 2_592_000_000,
  };
  const step = msPerBar[interval] || 86_400_000;
  const volatility = price > 1000 ? price * 0.003 : price > 100 ? 0.5 : 0.008;

  let open = price * 0.85;
  for (let i = 0; i < count; i++) {
    const change = (rng() - 0.48) * volatility * 3;
    const close = open + change;
    const high = Math.max(open, close) + rng() * volatility;
    const low = Math.min(open, close) - rng() * volatility;
    const date = new Date(now.getTime() - (count - i) * step);
    result.push({
      time: date.toISOString(),
      open: +open.toFixed(price > 100 ? 2 : 4),
      high: +high.toFixed(price > 100 ? 2 : 4),
      low: +low.toFixed(price > 100 ? 2 : 4),
      close: +close.toFixed(price > 100 ? 2 : 4),
      volume: Math.floor(rng() * 1_000_000) + 10_000,
    });
    open = close;
  }
  return result;
}

function generateSecurities(query?: string): Security[] {
  const defaultTickers = Object.keys(SECURITIES);
  const tickers = query
    ? defaultTickers.filter((t) => t.toLowerCase().includes(query.toLowerCase()) || (SECURITIES[t]?.name?.toLowerCase().includes(query.toLowerCase()) ?? false))
    : defaultTickers;

  return tickers.map((ticker) => {
    const info = SECURITIES[ticker];
    return {
      ticker: ticker.toUpperCase(),
      name: info.name || ticker,
      exchange: info.exchange || 'NASDAQ',
      currency: info.currency || 'USD',
      sector: info.sector || 'Unknown',
      industry: info.industry || 'Unknown',
      country: 'US',
      type: ticker === 'BTC' ? 'crypto' : ticker.includes('/') ? 'forex' : 'equity',
      status: 'active' as const,
      marketCap: info.marketCap,
      peRatio: info.peRatio,
      eps: info.eps,
      dividendYield: info.dividendYield,
      beta: info.beta,
      oid: ticker,
    };
  });
}

function generateSecurity(ticker: string): Security | undefined {
  const info = SECURITIES[ticker];
  if (!info) return undefined;
  return {
    ticker: ticker.toUpperCase(),
    name: info.name || ticker,
    exchange: info.exchange || 'NASDAQ',
    currency: info.currency || 'USD',
    sector: info.sector || 'Unknown',
    industry: info.industry || 'Unknown',
    country: 'US',
    type: 'equity',
    status: 'active' as const,
    marketCap: info.marketCap,
    peRatio: info.peRatio,
    eps: info.eps,
    dividendYield: info.dividendYield,
    beta: info.beta,
    oid: ticker,
  };
}

const HEADLINES = [
  { h: 'Apple Beats Q4 Earnings Expectations by $0.40 per Share', tickers: ['AAPL'], sentiment: 'positive' },
  { h: 'Fed Holds Rates Steady at 5.25%, Signals Cuts Late 2026', tickers: ['SPY', 'JPM'], sentiment: 'neutral' },
  { h: 'NVIDIA Surpasses $3T Market Cap on AI Demand Surge', tickers: ['NVDA'], sentiment: 'positive' },
  { h: 'Tesla Delivery Numbers Miss Analyst Estimates by 12%', tickers: ['TSLA'], sentiment: 'negative' },
  { h: 'Meta Announces $500B Share Buyback Program', tickers: ['META'], sentiment: 'positive' },
  { h: 'JPMorgan Raises 2026 Global Growth Forecast to 3.1%', tickers: ['JPM', 'SPY'], sentiment: 'positive' },
  { h: 'Amazon Web Services Launches New AI Chip, Raising AWS Competition', tickers: ['AMZN', 'NVDA'], sentiment: 'positive' },
  { h: 'Bitcoin Surges Past $67K as Institutional Inflows Accelerate', tickers: ['BTC'], sentiment: 'positive' },
  { h: 'EUR/USD Slips to 1.085 on ECB Dovish Outlook', tickers: ['EURUSD'], sentiment: 'negative' },
  { h: 'Microsoft Cloud Revenue Grows 24% Year Over Year', tickers: ['MSFT'], sentiment: 'positive' },
  { h: 'Google Faces New EU Antitrust Probe Into Search Dominance', tickers: ['GOOG'], sentiment: 'negative' },
  { h: 'Visa Process Record Transaction Volume in Q1 2026', tickers: ['V'], sentiment: 'positive' },
  { h: 'Walmart Expands Same-Day Delivery to 95% of US Households', tickers: ['WMT'], sentiment: 'positive' },
  { h: 'S&P 500 Hits New Record as Tech Rally Continues', tickers: ['SPY'], sentiment: 'positive' },
  { h: 'Semiconductor Shortage Eases, Chip Stocks React', tickers: ['NVDA', 'TSLA'], sentiment: 'neutral' },
];

function generateNews(): NewsItem[] {
  const now = new Date();
  return HEADLINES.map((item, i) => ({
    id: `news-${i}`,
    headline: item.h,
    summary: '',
    source: item.i % 3 === 0 ? 'Reuters' : item.i % 2 === 0 ? 'Bloomberg' : 'Bloomberg',
    published: new Date(now.getTime() - i * 1800_000).toISOString(),
    sentiment: item.sentiment as 'positive' | 'neutral' | 'negative',
    tickers: item.tickers,
    categories: ['markets'],
  }));
}

function generateAlerts(): Alert[] {
  return [
    { id: 'a1', ticker: 'AAPL', type: 'price', condition: { type: 'price', threshold: 200, direction: 'above' }, channels: ['browser'], active: true, createdAt: new Date().toISOString() },
    { id: 'a2', ticker: 'TSLA', type: 'price', condition: { type: 'price', threshold: 150, direction: 'below' }, channels: ['browser'], active: true, createdAt: new Date().toISOString() },
    { id: 'a3', ticker: 'NVDA', type: 'percent', condition: { type: 'percent', threshold: 5, direction: 'below' }, channels: ['browser'], active: false, createdAt: new Date().toISOString() },
  ];
}

export { generateQuotes, generatePriceBars, generateSecurities, generateSecurity, generateNews, generateAlerts };
