import { useState } from 'react';
import { cn } from '@/lib/cn';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { useTerminal } from '@/store/terminal';
import type { Alert, AlertCondition } from '@/types/alert';
import { formatPrice } from '@/utils/format';

type AlertDirection = 'above' | 'below';

const ALERT_TEMPLATES: { label: string; type: 'price' | 'percent'; direction: AlertDirection }[] = [
  { label: 'Price Above', type: 'price', direction: 'above' },
  { label: 'Price Below', type: 'price', direction: 'below' },
  { label: 'Down %', type: 'percent', direction: 'below' },
  { label: 'Up %', type: 'percent', direction: 'above' },
];

export function AlertsView() {
  const { alerts, removeAlert, toggleAlert } = useTerminal();
  const [newTicker, setNewTicker] = useState('');
  const [threshold, setThreshold] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<typeof ALERT_TEMPLATES[0]>(ALERT_TEMPLATES[0]);

  function handleAdd() {
    if (!newTicker || !threshold) return;
    const alert: Alert = {
      id: `alert-${Date.now()}`,
      ticker: newTicker.toUpperCase(),
      type: selectedTemplate.type,
      condition: {
        type: selectedTemplate.type,
        threshold: parseFloat(threshold),
        direction: selectedTemplate.direction,
      },
      channels: ['browser'],
      active: true,
      createdAt: new Date().toISOString(),
    };
    // In a real app, this would persist to backend
    toggleAlert(alert.id);
    toggleAlert(alert.id);
  }

  return (
    <div className="p-4 overflow-y-auto max-h-full">
      <h2 className="text-bbg-amber font-bold text-xs font-mono mb-4">PRICE ALERTS</h2>

      {/* New alert form */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">CREATE ALERT</span>
        </CardHeader>
        <CardBody>
          <div className="flex items-center gap-2">
            <Input
              value={newTicker}
              onChange={(e) => setNewTicker(e.target.value.toUpperCase())}
              placeholder="TICKER"
              className="w-24"
            />
            <select
              value={selectedTemplate.label}
              onChange={(e) => {
                const t = ALERT_TEMPLATES.find((t) => t.label === e.target.value);
                if (t) setSelectedTemplate(t);
              }}
              className="bg-bbg-bg border border-bbg-border text-bbg-text text-xs px-2 py-1 rounded"
            >
              {ALERT_TEMPLATES.map((t) => (
                <option key={t.label} value={t.label}>{t.label}</option>
              ))}
            </select>
            <Input
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              placeholder="VALUE"
              className="w-24"
            />
            <button
              onClick={handleAdd}
              className="px-3 py-1 bg-bbg-green text-bbg-bg font-bold text-xs font-mono rounded"
            >
              CREATE
            </button>
          </div>
        </CardBody>
      </Card>

      {/* Alert list */}
      <div className="space-y-2">
        {alerts.map((alert) => (
          <Card key={alert.id}>
            <CardBody className="py-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Badge variant="blue">{alert.ticker}</Badge>
                  <span className="text-bbg-text text-xs font-mono">
                    {alert.condition.direction === 'above' ? '↑' : '↓'} {formatPrice(alert.condition.threshold)}
                  </span>
                  <Badge variant={alert.active ? 'green' : 'gray'}>
                    {alert.active ? 'ACTIVE' : 'INACTIVE'}
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleAlert(alert.id)}
                    className="text-bbg-text-dim hover:text-bbg-text text-[10px]"
                  >
                    {alert.active ? 'PAUSE' : 'RESUME'}
                  </button>
                  <button
                    onClick={() => removeAlert(alert.id)}
                    className="text-bbg-text-dim hover:text-bbg-red text-[10px]"
                  >
                    DEL
                  </button>
                </div>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>
    </div>
  );
}
