import React, { useState } from 'react';
import { Navigation, Compass, CheckCircle2 } from 'lucide-react';
import { DemoBadge } from '../../components/common/DemoBadge';

export const RoutePlanner: React.FC = () => {
  const [startPoint, setStartPoint] = useState('Connaught Place');
  const [endPoint, setEndPoint] = useState('Okhla Industrial Estate');
  const [isCalculated, setIsCalculated] = useState(true);

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-1">
          <div className="flex items-center space-x-2">
            <Compass className="w-4 h-4 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Route Planner</h3>
          </div>
          <DemoBadge label="Experimental" />
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Compare cumulative pollution exposure across transit routes
        </p>

        {/* Inputs */}
        <div className="space-y-3">
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Start
            </label>
            <div className="flex items-center bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus-within:border-emerald-500/50">
              <span className="w-2 h-2 rounded-full bg-emerald-400 mr-2.5 shrink-0" />
              <input
                type="text"
                value={startPoint}
                onChange={(e) => setStartPoint(e.target.value)}
                className="bg-transparent border-none text-slate-100 text-xs w-full focus:outline-none"
                placeholder="Starting landmark or coordinates"
              />
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Destination
            </label>
            <div className="flex items-center bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus-within:border-emerald-500/50">
              <span className="w-2 h-2 rounded-full bg-rose-400 mr-2.5 shrink-0" />
              <input
                type="text"
                value={endPoint}
                onChange={(e) => setEndPoint(e.target.value)}
                className="bg-transparent border-none text-slate-100 text-xs w-full focus:outline-none"
                placeholder="Destination landmark or coordinates"
              />
            </div>
          </div>

          <button
            type="button"
            onClick={() => setIsCalculated(true)}
            className="w-full mt-2 py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 text-white text-xs font-semibold rounded-lg flex items-center justify-center space-x-2 transition-colors shadow-sm"
          >
            <Navigation className="w-3.5 h-3.5" />
            <span>Calculate Cleanest Route</span>
          </button>
        </div>

        {/* Route Exposure Recommendation Card */}
        {isCalculated && (
          <div className="mt-4 p-3 bg-slate-950/70 border border-slate-800/80 rounded-lg space-y-2 text-xs">
            <div className="flex items-center justify-between text-slate-300">
              <span className="font-semibold text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Recommended: Barapullah Bypass
              </span>
              <span className="text-[11px] font-mono text-emerald-300 bg-emerald-500/10 px-1.5 py-0.5 rounded">
                -28% PM2.5
              </span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Direct Mathura Rd has severe particulate congestion (AQI ~310). The bypass route adds 4 mins but reduces inhaled toxic exposure significantly.
            </p>
          </div>
        )}
      </div>

      <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800/60 mt-4 flex items-center justify-between">
        <span>Routing Engine: Simulated Graph Prototype</span>
        <span>Checkpoint 1</span>
      </div>
    </div>
  );
};
