import { useRef, useState } from 'react';
import { cn } from '@/lib/cn';
import { useTerminal } from '@/store/terminal';

interface CommandBarProps {
  onExecute: (ticker: string, functionCode: string) => void;
}

const SECTORS = [
  { key: 'F2', label: 'GOVT', color: 'bg-blue-600' },
  { key: 'F3', label: 'CORP', color: 'bg-blue-500' },
  { key: 'F4', label: 'MTGE', color: 'bg-blue-400' },
  { key: 'F5', label: 'M-Mkt', color: 'bg-cyan-500' },
  { key: 'F6', label: 'MUNI', color: 'bg-cyan-400' },
  { key: 'F7', label: 'PFD', color: 'bg-emerald-500' },
  { key: 'F8', label: 'EQUITY', color: 'bg-green-500' },
  { key: 'F9', label: 'COMDTY', color: 'bg-amber-500' },
  { key: 'F10', label: 'INDEX', color: 'bg-yellow-500' },
  { key: 'F11', label: 'CURNCY', color: 'bg-orange-500' },
  { key: 'F12', label: 'ALPHA', color: 'bg-red-500' },
];

export function CommandBar({ onExecute }: CommandBarProps) {
  const { commandTicker, setCommandTicker } = useTerminal();
  const inputRef = useRef<HTMLInputElement>(null);
  const [func, setFunc] = useState('');

  function execute() {
    const ticker = commandTicker.trim().toUpperCase();
    const fn = func.trim().toUpperCase() || 'CG';
    if (ticker) {
      onExecute(ticker, fn);
    } else if (fn !== 'CG') {
      onExecute('', fn);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter') {
      execute();
    }
  }

  return (
    <div className="flex items-center gap-1 px-2 py-1.5 bg-bbg-bg-elevated border-t border-bbg-border">
      {/* Ticker input */}
      <span className="text-bbg-text-dim text-[10px] mr-1">TKR</span>
      <input
        ref={inputRef}
        value={commandTicker}
        onChange={(e) => setCommandTicker(e.target.value.toUpperCase())}
        onKeyDown={handleKeyDown}
        placeholder="TICKER"
        className="flex-1 bg-bbg-bg border border-bbg-border text-bbg-green text-xs font-mono px-2 py-1 rounded focus:border-bbg-green focus:outline-none min-w-[100px]"
      />

      {/* Function input */}
      <span className="text-bbg-text-dim text-[10px] ml-2 mr-1">FN</span>
      <input
        value={func}
        onChange={(e) => setFunc(e.target.value.toUpperCase())}
        onKeyDown={handleKeyDown}
        placeholder="CG"
        className="w-16 bg-bbg-bg border border-bbg-border text-bbg-green text-xs font-mono px-2 py-1 rounded focus:border-bbg-green focus:outline-none"
      />

      {/* GO button */}
      <button
        onClick={execute}
        className="ml-2 px-4 py-1 bg-bbg-green text-bbg-bg font-bold text-xs font-mono rounded hover:bg-bbg-green-dim transition-colors"
      >
        GO
      </button>

      <div className="flex-1" />

      {/* Sector hotkeys */}
      <div className="flex items-center gap-0.5 ml-4">
        {SECTORS.map((s) => (
          <button
            key={s.key}
            className={cn(
              'px-1.5 py-0.5 text-[9px] font-bold text-white rounded transition-colors hover:opacity-80',
              s.color,
            )}
            title={s.label}
          >
            {s.key}
          </button>
        ))}
      </div>
    </div>
  );
}
