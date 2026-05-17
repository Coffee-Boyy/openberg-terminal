import { useState } from 'react';
import { useTheme } from '@/store/theme';
import { useAuth } from '@/store/auth';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { LoginDialog } from '@/components/auth/LoginDialog';

export function SettingsView() {
  const { theme, toggle } = useTheme();
  const { isAuthenticated, user, logout } = useAuth();
  const [yahooKey, setYahooKey] = useState('');
  const [finnhubKey, setFinnhubKey] = useState('');
  const [polygonKey, setPolygonKey] = useState('');
  const [showLogin, setShowLogin] = useState(false);

  return (
    <div className="p-4 overflow-y-auto max-h-full">
      <h2 className="text-bbg-amber font-bold text-xs font-mono mb-4">SETTINGS</h2>

      {/* Session */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">SESSION</span>
        </CardHeader>
        <CardBody>
          {isAuthenticated && user ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {user.avatar && (
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="w-8 h-8 rounded-full bg-bbg-border"
                  />
                )}
                <div>
                  <div className="text-bbg-text text-xs font-mono font-bold">{user.name}</div>
                  <div className="text-bbg-text-dim text-[10px] font-mono">{user.email}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="green">ONLINE</Badge>
                <button
                  onClick={logout}
                  className="px-3 py-1.5 bg-bbg-border text-bbg-text font-bold text-xs font-mono rounded hover:bg-bbg-border/80 transition-colors"
                >
                  SIGN OUT
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <div>
                <div className="text-bbg-text text-xs font-mono">Not signed in</div>
                <div className="text-bbg-text-dim text-[10px] font-mono">
                  Sign in to sync watchlists and settings
                </div>
              </div>
              <button
                onClick={() => setShowLogin(true)}
                className="px-3 py-1.5 bg-bbg-green/20 text-bbg-green border border-bbg-green/40 font-bold text-xs font-mono rounded hover:bg-bbg-green/30 transition-colors"
              >
                SIGN IN
              </button>
            </div>
          )}
        </CardBody>
      </Card>

      {/* Theme */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">APPEARANCE</span>
        </CardHeader>
        <CardBody>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-bbg-text text-xs">Theme</div>
              <div className="text-bbg-text-dim text-[10px]">Switch between dark and light mode</div>
            </div>
            <button
              onClick={toggle}
              className="px-3 py-1.5 bg-bbg-border text-bbg-text font-bold text-xs font-mono rounded hover:bg-bbg-border/80 transition-colors"
            >
              {theme === 'dark' ? '🌙 DARK' : '☀️ LIGHT'}
            </button>
          </div>
        </CardBody>
      </Card>

      {/* API Keys */}
      <Card className="mb-4">
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">DATA CONNECTORS</span>
        </CardHeader>
        <CardBody>
          <div className="space-y-3">
            <ApiKeyRow
              label="Yahoo Finance"
              placeholder="Enter API key..."
              value={yahooKey}
              onChange={setYahooKey}
              enabled={!!yahooKey}
            />
            <ApiKeyRow
              label="Finnhub"
              placeholder="Enter API key..."
              value={finnhubKey}
              onChange={setFinnhubKey}
              enabled={!!finnhubKey}
            />
            <ApiKeyRow
              label="Polygon.io"
              placeholder="Enter API key..."
              value={polygonKey}
              onChange={setPolygonKey}
              enabled={!!polygonKey}
            />
          </div>
        </CardBody>
      </Card>

      {/* About */}
      <Card>
        <CardHeader>
          <span className="text-bbg-text font-bold text-xs font-mono">ABOUT</span>
        </CardHeader>
        <CardBody>
          <div className="flex items-center gap-3">
            <div className="text-bbg-green font-bold text-lg font-mono">OPENBERG</div>
            <Badge variant="gray">v0.1.0</Badge>
          </div>
          <div className="text-bbg-text-dim text-xs mt-2">
            Open-source financial terminal for retail traders.
            <br />
            Built with React, Vite, TypeScript, and FastAPI.
          </div>
        </CardBody>
      </Card>

      {/* Login Dialog */}
      <LoginDialog open={showLogin} onClose={() => setShowLogin(false)} />
    </div>
  );
}

function ApiKeyRow({
  label,
  placeholder,
  value,
  onChange,
  enabled,
}: {
  label: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
  enabled: boolean;
}) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div>
        <div className="text-bbg-text text-xs">{label}</div>
        <div className="text-bbg-text-dim text-[10px]">API key for data connector</div>
      </div>
      <div className="flex items-center gap-2">
        <Input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          type="password"
          className="w-48"
        />
        <Badge variant={enabled ? 'green' : 'gray'}>{enabled ? 'ACTIVE' : 'OFF'}</Badge>
      </div>
    </div>
  );
}
