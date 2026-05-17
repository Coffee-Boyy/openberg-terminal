import { useState } from 'react';
import { cn } from '@/lib/cn';
import { useAuth } from '@/store/auth';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';

type Tab = 'signin' | 'signup';

interface LoginDialogProps {
  open: boolean;
  onClose: () => void;
}

export function LoginDialog({ open, onClose }: LoginDialogProps) {
  const { login, signup } = useAuth();
  const [tab, setTab] = useState<Tab>('signin');

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');

    if (!email.trim()) {
      setError('Email is required');
      return;
    }
    if (tab === 'signup' && !name.trim()) {
      setError('Name is required');
      return;
    }
    if (!password.trim()) {
      setError('Password is required');
      return;
    }

    if (tab === 'signin') {
      login(email, password);
    } else {
      signup(email, name, password);
    }
    clearForm();
    onClose();
  }

  function clearForm() {
    setName('');
    setEmail('');
    setPassword('');
    setError('');
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Escape') onClose();
  }

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      onClick={onClose}
      onKeyDown={handleKeyDown}
    >
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />

      {/* Dialog */}
      <div
        className={cn(
          'relative w-[420px] max-w-[90vw] bg-bbg-bg-elevated border border-bbg-border rounded-lg shadow-2xl overflow-hidden',
          'flex flex-col',
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-bbg-border">
          <div className="flex items-center gap-2">
            <span className="text-bbg-green font-bold text-xs font-mono">OPENBERG</span>
            <Badge variant="green">DEMO</Badge>
          </div>
          <button
            onClick={onClose}
            className="text-bbg-text-dim text-sm hover:text-bbg-text transition-colors font-mono"
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-bbg-border">
          {(['signin', 'signup'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => {
                setTab(t);
                setError('');
              }}
              className={cn(
                'flex-1 py-2 text-xs font-mono font-bold uppercase tracking-wider transition-colors',
                t === tab
                  ? 'text-bbg-green border-b-2 border-bbg-green bg-bbg-green/5'
                  : 'text-bbg-text-dim hover:text-bbg-text',
              )}
            >
              {t === 'signin' ? 'Sign In' : 'Sign Up'}
            </button>
          ))}
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-4 space-y-3">
          {tab === 'signup' && (
            <div>
              <label className="text-bbg-text-dim text-[10px] font-mono uppercase tracking-wider mb-1 block">
                Name
              </label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Trader McTerson"
                autoComplete="name"
              />
            </div>
          )}

          <div>
            <label className="text-bbg-text-dim text-[10px] font-mono uppercase tracking-wider mb-1 block">
              Email
            </label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="trader@example.com"
              autoComplete="email"
            />
          </div>

          <div>
            <label className="text-bbg-text-dim text-[10px] font-mono uppercase tracking-wider mb-1 block">
              Password
            </label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete={tab === 'signin' ? 'current-password' : 'new-password'}
            />
          </div>

          {error && (
            <div className="text-red-400 text-xs font-mono">{error}</div>
          )}

          <div className="pt-1">
            <button
              type="submit"
              className="w-full py-2 bg-bbg-green/20 text-bbg-green border border-bbg-green/40 rounded font-bold text-xs font-mono uppercase tracking-wider hover:bg-bbg-green/30 transition-colors"
            >
              {tab === 'signin' ? 'Sign In' : 'Create Account'}
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="px-4 pb-3">
          <div className="text-bbg-text-dim text-[10px] font-mono text-center">
            Demo mode — any credentials work
          </div>
        </div>
      </div>
    </div>
  );
}
