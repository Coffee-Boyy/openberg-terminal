import { useState } from 'react';
import { cn } from '@/lib/cn';
import { useWatchlist } from '@/store/watchlist';
import { useTerminal } from '@/store/terminal';
import { formatChange, formatPrice } from '@/utils/format';
import { Badge } from '@/components/ui/Badge';

interface SidebarProps {
  onSelectSecurity: (ticker: string) => void;
}

export function Sidebar({ onSelectSecurity }: SidebarProps) {
  const { items, addTicker, removeTicker } = useWatchlist();
  const { sidebarOpen, toggleSidebar } = useTerminal();
  const [newTicker, setNewTicker] = useState('');

  function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    const t = newTicker.trim().toUpperCase();
    if (t) {
      addTicker(t);
      setNewTicker('');
    }
  }

  if (!sidebarOpen) return null;

  return (
    <div className="w-64 bg-bbg-bg-elevated border-r border-bbg-border flex flex-col flex-shrink-0">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-bbg-border">
        <h2 className="text-bbg-green font-bold text-xs font-mono">WATCHLIST</h2>
        <button
          onClick={toggleSidebar}
          className="text-bbg-text-dim hover:text-bbg-text"
          title="Close sidebar"
        >
          ✕
        </button>
      </div>

      {/* Watchlist items */}
      <div className="flex-1 overflow-y-auto">
        {items.map((item) => (
          <div
            key={item.ticker}
            className="group flex items-center justify-between px-3 py-2 border-b border-bbg-border/50 hover:bg-bbg-border cursor-pointer"
            onClick={() => onSelectSecurity(item.ticker)}
          >
            <div>
              <div className="text-bbg-text font-bold text-xs font-mono">{item.ticker}</div>
              <div className="text-bbg-text-dim text-[10px]">{formatPrice(item.last)}</div>
            </div>
            <div className="flex items-center gap-2">
              <Badge
                variant={item.changePercent >= 0 ? 'green' : 'red'}
              >
                {formatChange(item.changePercent, false)}
              </Badge>
              <button
                className="text-bbg-text-dim opacity-0 group-hover:opacity-100 hover:text-bbg-red text-[10px]"
                onClick={(e) => {
                  e.stopPropagation();
                  removeTicker(item.ticker);
                }}
              >
                ✕
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Add ticker form */}
      <form onSubmit={handleAdd} className="flex items-center gap-1 p-2 border-t border-bbg-border">
        <input
          value={newTicker}
          onChange={(e) => setNewTicker(e.target.value.toUpperCase())}
          placeholder="Add ticker..."
          className="flex-1 bg-bbg-bg border border-bbg-border text-bbg-text text-xs font-mono px-2 py-1 rounded focus:border-bbg-green focus:outline-none"
        />
        <button
          type="submit"
          className="px-2 py-1 bg-bbg-green text-bbg-bg font-bold text-[10px] font-mono rounded"
        >
          ADD
        </button>
      </form>

      {/* Quick search */}
      <div className="p-2 border-t border-bbg-border">
        <h3 className="text-bbg-text-dim text-[10px] font-bold mb-1">QUICK ACCESS</h3>
        <div className="grid grid-cols-4 gap-1">
          {['SPY', 'QQQ', 'DIA', 'IWM'].map((t) => (
            <button
              key={t}
              onClick={() => onSelectSecurity(t)}
              className="px-1 py-0.5 text-[10px] font-mono bg-bbg-border text-bbg-text-dim rounded hover:bg-bbg-green hover:text-bbg-bg transition-colors"
            >
              {t}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
