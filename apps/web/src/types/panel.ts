export type PanelType =
  | 'security'
  | 'chart'
  | 'news'
  | 'portfolio'
  | 'history'
  | 'alerts'
  | 'watchlist'
  | 'settings';

export interface PanelConfig {
  ticker?: string;
  [key: string]: unknown;
}

export interface Panel {
  id: string;
  type: PanelType;
  config: PanelConfig;
}

export type ActiveFunction = {
  type: PanelType;
  config: PanelConfig;
};
