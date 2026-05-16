export type CommandCategory =
  | 'security'
  | 'chart'
  | 'data'
  | 'news'
  | 'portfolio'
  | 'alerts'
  | 'watchlist'
  | 'analytics'
  | 'system';

export interface Command {
  id: string;
  label: string;
  description: string;
  keystrokes?: string;
  category: CommandCategory;
  requiresTicker?: boolean;
  icon: string;
}

export interface CommandArgs {
  ticker?: string;
  params?: Record<string, unknown>;
}
