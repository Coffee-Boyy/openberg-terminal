export type AlertType = 'price' | 'percent' | 'volume' | 'news' | 'technical';

export interface Alert {
  id: string;
  ticker: string;
  type: AlertType;
  condition: AlertCondition;
  channels: ('browser' | 'email' | 'webhook')[];
  active: boolean;
  triggered?: string;
  createdAt: string;
}

export interface AlertCondition {
  type: AlertType;
  threshold: number;
  direction?: 'above' | 'below';
}
