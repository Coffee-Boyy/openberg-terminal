export interface Security {
  oid: string;
  ticker: string;
  name: string;
  exchange: string;
  currency: string;
  sector: string;
  industry: string;
  country: string;
  type: SecurityType;
  status: 'active' | 'suspended' | 'delisted';
  marketCap?: number;
  peRatio?: number;
  eps?: number;
  dividendYield?: number;
  beta?: number;
  high52w?: number;
  low52w?: number;
}

export type SecurityType =
  | 'equity'
  | 'bond'
  | 'etf'
  | 'index'
  | 'forex'
  | 'crypto'
  | 'commodity'
  | 'future'
  | 'option';

export interface Quote {
  ticker: string;
  exchange: string;
  currency: string;
  bid: number;
  ask: number;
  last: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap?: number;
  timestamp: string;
}

export interface PriceBar {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
