import { useState } from 'react';
import { cn } from '@/lib/cn';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import type { PositionPnl } from '@/types/portfolio';
import { formatCurrency, formatChange, formatPercent, formatMarketCap } from '@/utils/format';
import { generateQuotes } from '@/services/demo-data';

const DEMO_HOLDINGS = [
  { ticker: 'AAPL', quantity: 100, costBasis: 175.5 },
  { ticker: 'GOOG', quantity: 50, costBasis: 155.2 },
  { ticker: 'MSFT', quantity: 30, costBasis: 350.0 },
  { ticker: 'NVDA', quantity: 20, costBasis: 720.0 },
  { ticker: 'JPM', quantity: 75, costBasis: 195.0 },
  { ticker: 'V', quantity: 40, costBasis: 260.0 },
];

export function PortfolioView() {
  const [newTicker, setNewTicker] = useState('');
  const [quantity, setQuantity] = useState('');
  const [costBasis, setCostBasis] = useState('');
  const [holdings, setHoldings] = useState(DEMO_HOLDINGS);

  const quotes = generateQuotes(holdings.map((h) => h.ticker));
  const positions: PositionPnl[] = holdings.map((h) => {
    const q = quotes.find((q) => q.ticker === h.ticker);
    if (!q) return { ...h, currentPrice: 0, currentValue: 0, unrealizedPnl: 0, unrealizedPnlPercent: 0 };
    return {
      ticker: h.ticker,
      quantity: h.quantity,
      costBasis: h.costBasis,
      currentPrice: q.last,
      currentValue: q.last * h.quantity,
      unrealizedPnl: (q.last - h.costBasis) * h.quantity,
      unrealizedPnlPercent: ((q.last - h.costBasis) / h.costBasis) * 100,
    };
  });

  const totalCost = holdings.reduce((sum, h) => sum + h.costBasis * h.quantity, 0);
  const totalCurrent = positions.reduce((sum, p) => sum + p.currentValue, 0);
  const totalPnl = totalCurrent - totalCost;
  const totalPnlPercent = totalCost > 0 ? (totalPnl / totalCost) * 100 : 0;

  function handleAdd() {
    if (!newTicker || !quantity || !costBasis) return;
    setHoldings([...holdings, {
      ticker: newTicker.toUpperCase(),
      quantity: parseFloat(quantity),
      costBasis: parseFloat(costBasis),
    }]);
    setNewTicker('');
    setQuantity('');
    setCostBasis('');
  }

  return (
    <div className="p-4 overflow-y-auto max-h-full">
      <h2 className="text-bbg-amber font-bold text-xs font-mono mb-4">PORTFOLIO</h2>
      {/* P&L Summary */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        <SummaryCard label="Total Cost" value={formatCurrency(totalCost)} />
        <SummaryCard label="Current Value" value={formatCurrency(totalCurrent)} />
        <SummaryCard label="Unrealized P&L" value={formatCurrency(totalPnl)} positive={totalPnl >= 0} />
        <SummaryCard label="P&L %" value={formatPercent(totalPnlPercent)} positive={totalPnlPercent >= 0} />
      </div>

      {/* Holdings table */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">HOLDINGS</span>
        </CardHeader>
        <CardBody>
          <div className="overflow-x-auto">
            <table className="w-full text-xs font-mono">
              <thead>
                <tr className="border-b border-bbg-border text-bbg-text-dim text-[10px]">
                  <th className="text-left py-1.5 px-2">TICKER</th>
                  <th className="text-right py-1.5 px-2">QTY</th>
                  <th className="text-right py-1.5 px-2">COST BASIS</th>
                  <th className="text-right py-1.5 px-2">CURRENT</th>
                  <th className="text-right py-1.5 px-2">P&L</th>
                  <th className="text-right py-1.5 px-2">P&L %</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((p) => (
                  <tr key={p.ticker} className="border-b border-bbg-border/30 hover:bg-bbg-border">
                    <td className="py-1.5 px-2 text-bbg-text font-bold">{p.ticker}</td>
                    <td className="py-1.5 px-2 text-right text-bbg-text-dim">{p.quantity}</td>
                    <td className="py-1.5 px-2 text-right text-bbg-text-dim">{formatCurrency(p.costBasis)}</td>
                    <td className="py-1.5 px-2 text-right text-bbg-green">{formatCurrency(p.currentPrice)}</td>
                    <td className={cn(
                      'py-1.5 px-2 text-right font-bold',
                      p.unrealizedPnl >= 0 ? 'text-bbg-green' : 'text-bbg-red',
                    )}>
                      {formatCurrency(p.unrealizedPnl)}
                    </td>
                    <td className={cn(
                      'py-1.5 px-2 text-right',
                      p.unrealizedPnlPercent >= 0 ? 'text-bbg-green' : 'text-bbg-red',
                    )}>
                      {formatChange(p.unrealizedPnlPercent, false)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardBody>
      </Card>

      {/* Add holding form */}
      <Card>
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">ADD HOLDING</span>
        </CardHeader>
        <CardBody>
          <div className="flex items-center gap-2">
            <Input value={newTicker} onChange={(e) => setNewTicker(e.target.value.toUpperCase())} placeholder="TICKER" className="w-24" />
            <Input value={quantity} onChange={(e) => setQuantity(e.target.value)} placeholder="QTY" className="w-20" />
            <Input value={costBasis} onChange={(e) => setCostBasis(e.target.value)} placeholder="COST BASIS" className="w-28" />
            <button
              onClick={handleAdd}
              className="px-3 py-1 bg-bbg-green text-bbg-bg font-bold text-xs font-mono rounded"
            >
              ADD
            </button>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

function SummaryCard({ label, value, positive }: { label: string; value: string; positive?: boolean }) {
  return (
    <Card>
      <CardBody className="py-2">
        <div className="text-bbg-text-dim text-[10px] uppercase tracking-wider">{label}</div>
        <div className={cn(
          'text-sm font-bold mt-0.5',
          positive !== undefined ? (positive ? 'text-bbg-green' : 'text-bbg-red') : 'text-bbg-text',
        )}>
          {value}
        </div>
      </CardBody>
    </Card>
  );
}
