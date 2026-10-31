import React from 'react';

interface DemoBadgeProps {
  label?: string;
  className?: string;
}

export const DemoBadge: React.FC<DemoBadgeProps> = ({
  label = 'Demo Data',
  className = '',
}) => {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium tracking-wide uppercase bg-amber-500/10 text-amber-400 border border-amber-500/30 ${className}`}
      title="This reading or metric is representative sample data for Checkpoint 1."
    >
      <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mr-1.5 animate-pulse" />
      {label}
    </span>
  );
};
