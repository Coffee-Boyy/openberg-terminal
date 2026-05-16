import { useState, useMemo, useRef } from 'react';
import { cn } from '@/lib/cn';
import { commands } from './commands';
import { Input } from '@/components/ui/Input';

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
  onSelect: (commandId: string, ticker?: string) => void;
  defaultTicker?: string;
}

export function CommandPalette({ open, onClose, onSelect, defaultTicker }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = useMemo(() => {
    if (!query) return commands;
    const q = query.toLowerCase();
    return commands.filter(
      (c) => c.label.toLowerCase().includes(q) || c.id.toLowerCase().includes(q) || c.description.toLowerCase().includes(q),
    );
  }, [query]);

  const handleSelect = (cmd: (typeof commands)[0]) => {
    onSelect(cmd.id, defaultTicker);
    setQuery('');
  };

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Escape') {
      onClose();
    }
    if (e.key === 'Enter' && filtered.length > 0) {
      handleSelect(filtered[0]);
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20" onClick={onClose}>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />
      <div
        className="relative w-[600px] max-w-[90vw] bg-bbg-bg-elevated border border-bbg-border rounded-lg shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-2 px-3 py-2 border-b border-bbg-border">
          <span className="text-bbg-text-dim text-xs">⌘</span>
          <Input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or search..."
            className="bg-transparent border-none text-sm placeholder:text-bbg-text-dim"
            autoFocus
          />
        </div>
        <div className="max-h-[400px] overflow-y-auto p-1">
          {filtered.map((cmd) => (
            <button
              key={cmd.id}
              className="w-full flex items-center gap-3 px-3 py-2 rounded hover:bg-bbg-border text-left group"
              onClick={() => handleSelect(cmd)}
            >
              <span className="text-bbg-amber font-bold text-xs w-16 truncate">{cmd.id}</span>
              <span className="text-bbg-text text-xs flex-1 truncate">{cmd.label}</span>
              <span className="text-bbg-text-dim text-[10px] hidden group-hover:block">{cmd.description}</span>
            </button>
          ))}
          {filtered.length === 0 && (
            <div className="px-3 py-6 text-center text-bbg-text-dim text-xs">No commands found</div>
          )}
        </div>
      </div>
    </div>
  );
}
