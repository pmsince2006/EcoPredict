import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Sparkles } from 'lucide-react';
import { MOCK_FORECAST_24H } from '../../services/mockData';
import { DemoBadge } from '../../components/common/DemoBadge';

export const ForecastChart: React.FC = () => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <h3 className="text-base font-bold text-white">24h AQI Forecast</h3>
            <DemoBadge label="ML Model Preview" />
          </div>
          <div className="flex items-center space-x-2 text-xs text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded bg-cyan-500 inline-block" />
              Predicted Mean
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded bg-cyan-500/20 inline-block border border-cyan-500/40" />
              85% Confidence Interval
            </span>
          </div>
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Time-series model projection with diurnal meteorological and traffic features
        </p>

        {/* Chart */}
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={MOCK_FORECAST_24H}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <defs>
                <linearGradient id="forecastFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="boundsFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0891b2" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#0891b2" stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="time"
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
              />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
                domain={[100, 350]}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-950/95 border border-slate-700/80 p-2.5 rounded-lg text-xs shadow-xl backdrop-blur">
                        <div className="font-semibold text-slate-200 mb-1">{label}</div>
                        <div className="text-cyan-400 font-mono font-bold">
                          Predicted AQI: {data.predictedAqi}
                        </div>
                        <div className="text-slate-400 text-[11px] mt-0.5">
                          Range: {data.lowerBound} - {data.upperBound}
                        </div>
                        <div className="text-amber-400 font-medium text-[11px] mt-1">
                          Category: {data.category}
                        </div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              {/* Severe Threshold line */}
              <ReferenceLine
                y={300}
                stroke="#ef4444"
                strokeDasharray="3 3"
                label={{
                  value: 'Severe (300)',
                  fill: '#ef4444',
                  fontSize: 10,
                  position: 'insideTopRight',
                }}
              />
              {/* Very Poor Threshold line */}
              <ReferenceLine
                y={200}
                stroke="#f97316"
                strokeDasharray="3 3"
                label={{
                  value: 'Poor (200)',
                  fill: '#f97316',
                  fontSize: 10,
                  position: 'insideTopRight',
                }}
              />
              <Area
                type="monotone"
                dataKey="upperBound"
                stroke="transparent"
                fill="url(#boundsFill)"
              />
              <Area
                type="monotone"
                dataKey="predictedAqi"
                stroke="#06b6d4"
                strokeWidth={2.5}
                fill="url(#forecastFill)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800/60 mt-4 flex items-center justify-between">
        <span>Model: Random Forest / Gradient Boosting (Planned Checkpoint 2)</span>
        <span>Forecast Horizon: +24h</span>
      </div>
    </div>
  );
};
