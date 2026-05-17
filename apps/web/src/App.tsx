import { useState } from 'react';
import { StatusBar } from '@/components/layout/StatusBar';
import { Sidebar } from '@/components/layout/Sidebar';
import { NewsPanel } from '@/components/layout/NewsPanel';
import { CommandBar } from '@/components/layout/CommandBar';
import { CommandPalette } from '@/components/command-palette/CommandPalette';
import { ChartView } from '@/components/charts/ChartView';
import { SecurityView } from '@/features/security/SecurityView';
import { PortfolioView } from '@/features/portfolio/PortfolioView';
import { AlertsView } from '@/features/alerts/AlertsView';
import { SettingsView } from '@/features/settings/SettingsView';
import { useTerminal } from '@/store/terminal';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import type { ActiveFunction, PanelType } from '@/types/panel';

export default function App() {
  const {
    activeFunction,
    setCurrentFunction,
    sidebarOpen,
    newsPanelOpen,
    newsItems,
  } = useTerminal();

  const [showCommandPalette, setShowCommandPalette] = useState(false);

  useKeyboardShortcuts({
    onOpenCommandPalette: () => setShowCommandPalette(true),
    onExecuteCommand: handleExecuteCommand,
    commandTicker: '',
  });

  function handleExecuteCommand(commandId: string, ticker?: string) {
    setShowCommandPalette(false);
    const fnMap: Record<string, PanelType> = {
      AP: 'security', CG: 'chart', HP: 'history', BN: 'news',
      CN: 'news', PP: 'portfolio', PB: 'portfolio', PAA: 'portfolio',
      PA: 'alerts', WC: 'watchlist', DVDF: 'data', CALC: 'data',
      EFP: 'data', RAT: 'data', RC: 'data', SPC: 'data',
      SETTINGS: 'settings', THEME: 'settings',
    };
    const type = fnMap[commandId] || 'chart';
    setCurrentFunction({ type, config: { ticker: ticker || activeFunction.config.ticker } });
  }

  function handleCommandBarExecute(ticker: string, funcCode: string) {
    handleExecuteCommand(funcCode, ticker || activeFunction.config.ticker);
  }

  function handleSelectSecurity(ticker: string) {
    setCurrentFunction({ type: 'chart', config: { ticker } });
  }

  // Render the main panel content based on active function
  const ticker = (activeFunction.config.ticker as string) || 'AAPL';

  let panelContent: React.ReactNode;
  switch (activeFunction.type) {
    case 'chart':
      panelContent = (
        <div className="flex flex-col h-full">
          <ChartView ticker={ticker} />
        </div>
      );
      break;
    case 'security':
      panelContent = <SecurityView ticker={ticker} />;
      break;
    case 'portfolio':
      panelContent = <PortfolioView />;
      break;
    case 'alerts':
      panelContent = <AlertsView />;
      break;
    case 'settings':
      panelContent = <SettingsView />;
      break;
    case 'news':
      panelContent = (
        <div className="p-4">
          <h2 className="text-bbg-amber font-bold text-xs font-mono mb-3">NEWS: {ticker}</h2>
          <div className="space-y-2">
            {newsItems
              .filter((n) => n.tickers.includes(ticker))
              .map((item) => (
                <div key={item.id} className="p-2 border-b border-bbg-border/50">
                  <p className="text-bbg-text text-xs">{item.headline}</p>
                  <div className="text-bbg-text-dim text-[10px] mt-1">{item.source}</div>
                </div>
              ))}
          </div>
        </div>
      );
      break;
    default:
      panelContent = <ChartView ticker={ticker} />;
  }

  return (
    <div className="flex flex-col h-screen bg-bbg-bg text-bbg-text overflow-hidden">
      {/* Status bar */}
      <StatusBar demoMode />

      {/* Main terminal area */}
      <div className="flex flex-1 min-h-0">
        {/* Left sidebar */}
        <Sidebar onSelectSecurity={handleSelectSecurity} />

        {/* Main panel */}
        <div className="flex-1 min-w-0 overflow-hidden flex flex-col">
          {/* Panel header */}
          <div className="flex items-center justify-between px-3 py-1.5 border-b border-bbg-border">
            <div className="flex items-center gap-2">
              <span className="text-bbg-text-dim text-[10px] font-mono">
                {activeFunction.type.toUpperCase()}
              </span>
              {activeFunction.config.ticker && (
                <span className="text-bbg-green font-bold text-xs font-mono">
                  {activeFunction.config.ticker}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1 text-bbg-text-dim">
              <button
                onClick={() => setShowCommandPalette(true)}
                className="px-2 py-0.5 text-[10px] bg-bbg-border rounded hover:bg-bbg-border/80 transition-colors"
                title="Command Palette (Cmd+K)"
              >
                ⌘K
              </button>
            </div>
          </div>

          {/* Panel content */}
          <div className="flex-1 overflow-hidden">
            {panelContent}
          </div>
        </div>

        {/* Right news panel */}
        <NewsPanel ticker={ticker} />
      </div>

      {/* Command bar */}
      <CommandBar onExecute={handleCommandBarExecute} />

      {/* Command palette overlay */}
      <CommandPalette
        open={showCommandPalette}
        onClose={() => setShowCommandPalette(false)}
        onSelect={handleExecuteCommand}
        defaultTicker={activeFunction.config.ticker as string | undefined}
      />
    </div>
  );
}
