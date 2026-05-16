import { useEffect } from 'react';
import { useTerminal } from '@/store/terminal';
import { useTheme } from '@/store/theme';
import { commands } from '@/components/command-palette/commands';

interface UseKeyboardShortcutsOptions {
  onOpenCommandPalette?: () => void;
  onExecuteCommand?: (commandId: string, ticker?: string) => void;
  commandTicker?: string;
}

export function useKeyboardShortcuts({
  onOpenCommandPalette,
  onExecuteCommand,
  commandTicker,
}: UseKeyboardShortcutsOptions) {
  const toggleSidebar = useTerminal((s) => s.toggleSidebar);
  const toggleNewsPanel = useTerminal((s) => s.toggleNewsPanel);
  const setCurrentFunction = useTerminal((s) => s.setCurrentFunction);
  const { toggle: toggleTheme } = useTheme();

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      const mod = (e.ctrlKey || e.metaKey);

      // Cmd+K — command palette
      if (mod && e.key === 'k') {
        e.preventDefault();
        onOpenCommandPalette?.();
        return;
      }

      // Cmd+B — toggle sidebar
      if (mod && e.key === 'b') {
        e.preventDefault();
        toggleSidebar();
        return;
      }

      // Cmd+N — toggle news panel
      if (mod && e.key === 'n') {
        e.preventDefault();
        toggleNewsPanel();
        return;
      }

      // F2-F12 — sector hotkeys
      if (e.key.startsWith('F') && !e.ctrlKey && !e.metaKey) {
        const fMap: Record<string, string> = {
          F2: 'GOVT', F3: 'CORP', F4: 'MTGE', F5: 'M-Mkt',
          F6: 'MUNI', F7: 'PFD', F8: 'EQUITY', F9: 'COMDTY',
          F10: 'INDEX', F11: 'CURNCY', F12: 'CLIENT',
        };
        const sector = fMap[e.key];
        if (sector && onExecuteCommand) {
          e.preventDefault();
          onExecuteCommand('AP', commandTicker);
        }
        return;
      }

      // Escape — close panels or command bar
      if (e.key === 'Escape') {
        e.preventDefault();
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onOpenCommandPalette, onExecuteCommand, commandTicker, toggleSidebar, toggleNewsPanel, toggleTheme]);
}
