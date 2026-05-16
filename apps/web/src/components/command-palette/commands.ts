import type { Command, CommandCategory } from '@/types/command';

const commands: Command[] = [
  // Security
  { id: 'AP', label: 'Security Description', description: 'Full security fact sheet', category: 'security', requiresTicker: true, icon: 'file-text' },
  { id: 'SD', label: 'Security Descrip', description: 'Quick security ID and fact sheet', category: 'security', requiresTicker: true, icon: 'file-text' },
  { id: 'GL', label: 'Global List', description: 'Security master search', category: 'security', icon: 'search' },

  // Chart
  { id: 'CG', label: 'Chart', description: 'Interactive price chart', category: 'chart', requiresTicker: true, icon: 'bar-chart-3' },
  { id: 'CAG', label: 'Chart Advanced', description: 'Multi-chart analysis', category: 'chart', requiresTicker: true, icon: 'bar-chart-3' },

  // Data
  { id: 'HP', label: 'Historical Pricing', description: 'End-of-day or intraday history', category: 'data', requiresTicker: true, icon: 'history' },
  { id: 'WM', label: 'Where Moved', description: 'Price change analysis', category: 'data', requiresTicker: true, icon: 'trending-up' },

  // News
  { id: 'BN', label: 'Bloomberg News', description: 'Headline news feed', category: 'news', icon: 'newspaper' },
  { id: 'CN', label: 'Corporate News', description: 'Security-specific news', category: 'news', requiresTicker: true, icon: 'newspaper' },
  { id: 'NLS', label: 'News Search', description: 'Full-text news search', category: 'news', icon: 'search' },

  // Portfolio
  { id: 'PP', label: 'Portfolio', description: 'Portfolio tracker', category: 'portfolio', icon: 'pie-chart' },
  { id: 'PB', label: 'Portfolio Builder', description: 'Portfolio construction', category: 'portfolio', icon: 'plus' },
  { id: 'PAA', label: 'Portfolio Analysis', description: 'Factor exposure & peer comparison', category: 'portfolio', icon: 'pie-chart' },

  // Alerts
  { id: 'PA', label: 'Price Alert', description: 'Set price alerts', category: 'alerts', icon: 'bell' },

  // Watchlist
  { id: 'WC', label: 'Watchlist', description: 'Custom watchlists', category: 'watchlist', icon: 'eye' },

  // Analytics
  { id: 'DVDF', label: 'Dividends', description: 'Dividend history', category: 'analytics', requiresTicker: true, icon: 'dollar-sign' },
  { id: 'CALC', label: 'Calculator', description: 'Financial calculator', category: 'analytics', icon: 'calculator' },
  { id: 'EFP', label: 'Earnings Calendar', description: 'Upcoming earnings', category: 'analytics', icon: 'calendar' },
  { id: 'RAT', label: 'Ratios', description: 'Fundamental ratios', category: 'analytics', requiresTicker: true, icon: 'percent' },
  { id: 'RC', label: 'Correlation', description: 'Return correlation matrix', category: 'analytics', icon: 'git-merge' },
  { id: 'SPC', label: 'Peer Comparison', description: 'Compare peers', category: 'analytics', icon: 'git-merge' },

  // System
  { id: 'SETTINGS', label: 'Settings', description: 'User preferences', category: 'system', icon: 'settings' },
  { id: 'HELP', label: 'Help', description: 'Terminal help & keyboard shortcuts', category: 'system', icon: 'circle-help' },
  { id: 'THEME', label: 'Toggle Theme', description: 'Switch dark/light mode', category: 'system', icon: 'moon' },
  { id: 'TOGGLE_SIDEBAR', label: 'Toggle Sidebar', description: 'Show/hide left sidebar', category: 'system', icon: 'panel-left' },
  { id: 'TOGGLE_NEWS', label: 'Toggle News Panel', description: 'Show/hide news panel', category: 'system', icon: 'panel-right' },
];

const categoryLabels: Record<CommandCategory, string> = {
  security: 'Security',
  chart: 'Chart',
  data: 'Data',
  news: 'News',
  portfolio: 'Portfolio',
  alerts: 'Alerts',
  watchlist: 'Watchlist',
  analytics: 'Analytics',
  system: 'System',
};

const sectorMap: Record<string, Command> = {
  GOVT: { id: 'GOVT', label: 'Government', description: 'Government bonds', category: 'security', icon: 'landmark' },
  CORP: { id: 'CORP', label: 'Corporate', description: 'Corporate bonds', category: 'security', icon: 'building-2' },
  EQUITY: { id: 'EQUITY', label: 'Equity', description: 'Common stocks', category: 'security', icon: 'trending-up' },
  COMDTY: { id: 'COMDTY', label: 'Commodity', description: 'Raw materials', category: 'security', icon: 'package' },
  CURNCY: { id: 'CURNCY', label: 'Currency', description: 'Forex pairs', category: 'security', icon: 'banknote' },
  INDEX: { id: 'INDEX', label: 'Index', description: 'Market indices', category: 'security', icon: 'bar-chart' },
};

export { commands, categoryLabels, sectorMap };
export type { Command, CommandCategory };
