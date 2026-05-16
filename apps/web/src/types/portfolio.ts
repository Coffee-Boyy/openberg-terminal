export interface Holding {
  ticker: string;
  quantity: number;
  costBasis: number;
  acquired: string;
}

export interface Portfolio {
  id: string;
  name: string;
  holdings: Holding[];
  currency: string;
  inception: string;
}

export interface PositionPnl {
  ticker: string;
  quantity: number;
  costBasis: number;
  currentPrice: number;
  currentValue: number;
  unrealizedPnl: number;
  unrealizedPnlPercent: number;
}
