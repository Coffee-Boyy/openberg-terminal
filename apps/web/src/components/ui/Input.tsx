import { forwardRef } from 'react';
import { cn } from '@/lib/cn';

const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        'w-full bg-bbg-bg border border-bbg-border text-bbg-text text-xs font-mono px-2 py-1 rounded',
        'focus:border-bbg-cyan focus:outline-none transition-colors',
        'placeholder:text-bbg-text-dim',
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = 'Input';

export { Input };
