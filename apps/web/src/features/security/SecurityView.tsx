import { cn } from '@/lib/cn';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import type { Security } from '@/types/security';
import { formatCurrency, formatMarketCap, formatPrice } from '@/utils/format';
import { generateSecurity } from '@/services/demo-data';

interface SecurityViewProps {
  ticker: string;
}

export function SecurityView({ ticker }: SecurityViewProps) {
  const security = generateSecurity(ticker);

  if (!security) {
    return (
      <div className="p-8 text-center">
        <p className="text-bbg-text-dim text-xs">Security not found: {ticker}</p>
      </div>
    );
  }

  return (
    <div className="p-4 overflow-y-auto max-h-full">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="text-2xl font-bold text-bbg-green font-mono">{security.ticker}</div>
        <Badge variant="blue">{security.exchange}</Badge>
        <Badge variant={security.status === 'active' ? 'green' : 'red'}>{security.status}</Badge>
      </div>
      <div className="text-bbg-text-dim text-sm mb-6">{security.name}</div>

      {/* Price and key stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <StatCard label="Market Cap" value={formatMarketCap(security.marketCap || 0)} />
        <StatCard label="P/E Ratio" value={security.peRatio ? security.peRatio.toFixed(2) : 'N/A'} />
        <StatCard label="EPS" value={security.eps ? formatCurrency(security.eps) : 'N/A'} />
        <StatCard label="Dividend Yield" value={security.dividendYield ? `${security.dividendYield.toFixed(2)}%` : 'N/A'} />
        <StatCard label="Beta" value={security.beta?.toFixed(2) || 'N/A'} />
        <StatCard label="Sector" value={security.sector} />
        <StatCard label="Industry" value={security.industry} />
        <StatCard label="Currency" value={security.currency} />
      </div>

      {/* Identifiers */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">IDENTIFIERS</span>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-2 gap-x-8 gap-y-2">
            <IdentifierRow label="Ticker" value={security.ticker} />
            <IdentifierRow label="OID" value={security.oid} />
            <IdentifierRow label="Exchange" value={security.exchange} />
            <IdentifierRow label="Country" value={security.country} />
          </div>
        </CardBody>
      </Card>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <button className="px-4 py-1.5 bg-bbg-green text-bbg-bg font-bold text-xs font-mono rounded hover:bg-bbg-green-dim transition-colors">
          CG CHART
        </button>
        <button className="px-4 py-1.5 bg-bbg-border text-bbg-text font-bold text-xs font-mono rounded hover:bg-bbg-border/80 transition-colors">
          CN NEWS
        </button>
        <button className="px-4 py-1.5 bg-bbg-border text-bbg-text font-bold text-xs font-mono rounded hover:bg-bbg-border/80 transition-colors">
          DVDF DIVIDENDS
        </button>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <Card>
      <CardBody className="py-2">
        <div className="text-bbg-text-dim text-[10px] uppercase tracking-wider">{label}</div>
        <div className="text-bbg-green text-sm font-bold mt-0.5">{value}</div>
      </CardBody>
    </Card>
  );
}

function IdentifierRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-bbg-text-dim text-[10px]">{label}</span>
      <span className="text-bbg-text text-xs font-mono">{value}</span>
    </div>
  );
}
