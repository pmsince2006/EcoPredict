import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { PieChart as PieIcon } from 'lucide-react';
import { MOCK_POLLUTION_SOURCES } from '../../services/mockData';
import { DemoBadge } from '../../components/common/DemoBadge';

export const SourceBreakdownChart: React.FC = () => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
          <div className="flex items-center space-x-2">
            <PieIcon className="w-4 h-4 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Pollution Source Contribution</h3>
            <DemoBadge label="Apportionment" />
          </div>
        </div>
        <p className="text-xs text-slate-400 mb-3">
          Relative sectoral contributions to urban particulate accumulation
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <div className="h-52 w-52 shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={MOCK_POLLUTION_SOURCES}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="percentage"
                >
                  {MOCK_POLLUTION_SOURCES.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-slate-950/95 border border-slate-700/80 p-2 rounded-lg text-xs shadow-xl backdrop-blur">
                          <div className="font-semibold text-slate-200">{data.name}</div>
                          <div className="text-emerald-400 font-mono font-bold">
                            {data.percentage}% Share
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-2 text-xs w-full max-w-xs">
            {MOCK_POLLUTION_SOURCES.map((item) => (
              <div
                key={item.name}
                className="flex items-center justify-between p-2 rounded bg-slate-950/50 border border-slate-800/60"
              >
                <div className="flex items-center space-x-2">
                  <span
                    className="w-3 h-3 rounded-full shrink-0"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-slate-300 truncate">{item.name}</span>
                </div>
                <span className="font-mono font-bold text-white">{item.percentage}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800/60 mt-4 flex items-center justify-between">
        <span>Model Source: Chemical Mass Balance (CMB) Simulation</span>
        <span>Receptor Modeling</span>
      </div>
    </div>
  );
};
