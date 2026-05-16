import { cn } from '@/lib/cn';

type BadgeVariant = 'green' | 'red' | 'yellow' | 'blue' | 'gray' | 'amber';

export function Badge({
  children,
  variant = 'gray',
  className,
}: {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}) {
  const colors: Record<BadgeVariant, string> = {
    green: 'bg-green-500/20 text-green-400',
    red: 'bg-red-500/20 text-red-400',
    yellow: 'bg-yellow-500/20 text-yellow-400',
    blue: 'bg-blue-500/20 text-blue-400',
    gray: 'bg-slate-500/20 text-slate-400',
    amber: 'bg-amber-500/20 text-amber-400',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-sm',
        colors[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
