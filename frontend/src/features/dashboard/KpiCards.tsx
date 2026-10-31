import React from 'react';
import { TrendingUp, Zap, Info, ShieldCheck } from 'lucide-react';
import { AQISummary } from '../../types/aqi';
import { getAqiBadgeClasses } from '../../utils/aqiUtils';

interface KpiCardsProps {
  summary: AQISummary;
}

export const KpiCards: React.FC<KpiCardsProps> = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Current Avg AQI */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Current Avg AQI
          </span>
          <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline space-x-3 mb-2">
          <span className="text-4xl font-extrabold tracking-tight text-white font-mono">
            {summary.aqi}
          </span>
          <span
            className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${getAqiBadgeClasses(
              summary.category
            )}`}
          >
            {summary.category}
          </span>
        </div>
        <div className="text-xs text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800/60">
          <span className="text-amber-400/90 font-medium">{summary.changeRate}</span>
          <span className="text-[11px] text-slate-500 font-mono">Simulated</span>
        </div>
      </div>

      {/* 2. 12h Prediction */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            12h Prediction
          </span>
          <div className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400">
            <Zap className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline space-x-3 mb-2">
          <span className="text-4xl font-extrabold tracking-tight text-white font-mono">
            {summary.twelveHourPrediction}
          </span>
          <span
            className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${getAqiBadgeClasses(
              summary.twelveHourCategory
            )}`}
          >
            {summary.twelveHourCategory}
          </span>
        </div>
        <div className="text-xs text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800/60">
          <span>Confidence: <strong className="text-slate-200">{summary.predictionConfidence}</strong></span>
          <span className="text-[11px] text-slate-500 font-mono">ML Forecast</span>
        </div>
      </div>

      {/* 3. Main Pollutant */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Main Pollutant
          </span>
          <div className="p-1.5 rounded-lg bg-amber-500/10 text-amber-400">
            <Info className="w-4 h-4" />
          </div>
        </div>
        <div className="mb-2">
          <div className="text-3xl font-extrabold tracking-tight text-white">
            {summary.primaryPollutant}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            {summary.primaryConcentration}
          </p>
        </div>
        <div className="text-xs text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800/60">
          <span className="text-slate-400">Primary Health Risk</span>
          <span className="text-[11px] text-slate-500 font-mono">Telemetry</span>
        </div>
      </div>

      {/* 4. Health Advice */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Health Advice
          </span>
          <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
        </div>
        <div className="mb-2">
          <p className="text-sm font-medium text-slate-200 leading-snug">
            {summary.healthAdvice}
          </p>
        </div>
        <div className="text-xs text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800/60">
          <span className="text-emerald-400 font-medium">Public Health Advisory</span>
          <span className="text-[11px] text-slate-500 font-mono">CPCB Scale</span>
        </div>
      </div>
    </div>
  );
};
