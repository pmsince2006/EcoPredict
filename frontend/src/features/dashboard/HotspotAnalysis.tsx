import React from 'react';
import { Flame, AlertTriangle } from 'lucide-react';
import { MOCK_POLLUTION_SOURCES } from '../../services/mockData';
import { DemoBadge } from '../../components/common/DemoBadge';

export const HotspotAnalysis: React.FC = () => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-1">
          <div className="flex items-center space-x-2">
            <Flame className="w-4 h-4 text-amber-400" />
            <h3 className="text-base font-bold text-white">Hotspot Analysis</h3>
          </div>
          <DemoBadge label="Source Apportionment" />
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Estimated primary pollution contributors for the Delhi NCR basin
        </p>

        {/* Source breakdown bars */}
        <div className="space-y-3.5">
          {MOCK_POLLUTION_SOURCES.map((source) => (
            <div key={source.name} className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300 font-medium">{source.name}</span>
                <span className="font-mono font-bold text-slate-200">{source.percentage}%</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${source.percentage}%`,
                    backgroundColor: source.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Localized Alert Note */}
        <div className="mt-5 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold text-amber-300 block mb-0.5">
                Alert for Okhla Area
              </strong>
              <p className="text-amber-200/90 text-[11px] leading-relaxed">
                Heavy freight traffic near Okhla Phase III combined with stagnant planetary boundary layer conditions is driving localized AQI spikes above 300.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800/60 mt-4 flex items-center justify-between">
        <span>Attribution Model: Prototype Emission Inventory</span>
        <span>Simulated</span>
      </div>
    </div>
  );
};
