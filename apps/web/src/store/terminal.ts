import { create } from 'zustand';
import type { ActiveFunction, PanelType } from '@/types/panel';
import type { Alert } from '@/types/alert';
import { generateAlerts, generateNews, generateSecurities } from '@/services/demo-data';

interface TerminalState {
  // Active function
  activeFunction: ActiveFunction;
  setCurrentFunction: (fn: ActiveFunction) => void;

  // Ticker search
  commandTicker: string;
  setCommandTicker: (ticker: string) => void;

  // News
  newsItems: ReturnType<typeof generateNews>;
  refreshNews: () => void;

  // Alerts
  alerts: Alert[];
  addAlert: (alert: Alert) => void;
  removeAlert: (id: string) => void;
  toggleAlert: (id: string) => void;
  refreshDemoAlerts: () => void;

  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;

  // News panel
  newsPanelOpen: boolean;
  toggleNewsPanel: () => void;

  // Security search results
  searchResults: ReturnType<typeof generateSecurities>;
  setSearchResults: (results: ReturnType<typeof generateSecurities>) => void;

  // Demo mode
  demoMode: boolean;
}

export const useTerminal = create<TerminalState>((set, get) => ({
  activeFunction: { type: 'chart', config: { ticker: 'AAPL' } },
  setCurrentFunction: (fn) => set({ activeFunction: fn }),

  commandTicker: '',
  setCommandTicker: (ticker) => set({ commandTicker: ticker }),

  newsItems: generateNews(),
  refreshNews: () => set({ newsItems: generateNews() }),

  alerts: generateAlerts(),
  addAlert: (alert) => set((s) => ({ alerts: [...s.alerts, alert] })),
  removeAlert: (id) => set((s) => ({ alerts: s.alerts.filter((a) => a.id !== id) })),
  toggleAlert: (id) =>
    set((s) => ({
      alerts: s.alerts.map((a) => (a.id === id ? { ...a, active: !a.active } : a)),
    })),
  refreshDemoAlerts: () => set({ alerts: generateAlerts() }),

  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  newsPanelOpen: true,
  toggleNewsPanel: () => set((s) => ({ newsPanelOpen: !s.newsPanelOpen })),

  searchResults: [],
  setSearchResults: (results) => set({ searchResults: results }),

  demoMode: true,
}));
