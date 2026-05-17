import { useEffect, useState } from 'react';
import { cn } from '@/lib/cn';

export function StatusBar({ demoMode }: { demoMode?: boolean }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center justify-between px-3 py-1 bg-bbg-bg-elevated border-b border-bbg-border text-[10px] font-mono">
      <div className="flex items-center gap-4">
        <span className="text-bbg-green font-bold">● CONNECTED</span>
        {demoMode && <span className="text-bbg-amber">● DEMO MODE</span>}
        <span className="text-bbg-text-dim">SESSION: TERMINAL-01</span>
      </div>
      <div className="flex items-center gap-4 text-bbg-text-dim">
        <span>
          UTC {time.toISOString().slice(11, 19)}
        </span>
        <span>
          LOCAL {time.toLocaleTimeString('en-US', { hour12: true })}
        </span>
        <span className="text-bbg-cyan">OPENBERG TERMINAL v0.1.0</span>
      </div>
    </div>
  );
}
