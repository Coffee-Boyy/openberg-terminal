import { cn } from '@/lib/cn';
import { useTerminal } from '@/store/terminal';
import type { NewsItem } from '@/types/news';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/utils/format';

const sentimentColors: Record<string, 'green' | 'yellow' | 'red'> = {
  positive: 'green',
  neutral: 'yellow',
  negative: 'red',
};

export function NewsPanel({ ticker }: { ticker?: string }) {
  const { newsItems, newsPanelOpen, toggleNewsPanel } = useTerminal();
  const filtered = ticker
    ? newsItems.filter((n) => n.tickers.includes(ticker.toUpperCase()))
    : newsItems;

  if (!newsPanelOpen) return null;

  return (
    <div className="w-72 bg-bbg-bg-elevated border-l border-bbg-border flex flex-col flex-shrink-0">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-bbg-border">
        <h2 className="text-bbg-amber font-bold text-xs font-mono">NEWS FEED</h2>
        <button
          onClick={toggleNewsPanel}
          className="text-bbg-text-dim hover:text-bbg-text"
          title="Close news panel"
        >
          ✕
        </button>
      </div>

      {/* News items */}
      <div className="flex-1 overflow-y-auto">
        {filtered.map((item) => (
          <NewsItemCard key={item.id} item={item} />
        ))}
        {filtered.length === 0 && (
          <div className="p-4 text-center text-bbg-text-dim text-xs">
            No news for {ticker || 'any ticker'}
          </div>
        )}
      </div>
    </div>
  );
}

function NewsItemCard({ item }: { item: NewsItem }) {
  return (
    <div className="px-3 py-2 border-b border-bbg-border/50 hover:bg-bbg-border transition-colors">
      <div className="flex items-start gap-2">
        <Badge variant={sentimentColors[item.sentiment]}>
          {item.sentiment}
        </Badge>
        <div className="flex-1 min-w-0">
          <p className="text-bbg-text text-[11px] leading-relaxed">{item.headline}</p>
          <div className="flex items-center gap-2 mt-1 text-[10px] text-bbg-text-dim">
            <span>{item.source}</span>
            <span>•</span>
            <span>{formatDate(item.published)}</span>
          </div>
          <div className="flex gap-1 mt-1">
            {item.tickers.slice(0, 3).map((t) => (
              <span key={t} className="text-[9px] font-mono text-bbg-cyan bg-bbg-cyan/10 px-1 rounded">
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
