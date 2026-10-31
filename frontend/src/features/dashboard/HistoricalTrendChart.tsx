import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { History } from 'lucide-react';
import { MOCK_HISTORICAL_24H } from '../../services/mockData';
import { DemoBadge } from '../../components/common/DemoBadge';

export const HistoricalTrendChart: React.FC = () => {
  const [viewMetric, setViewMetric] = useState<'aqi' | 'particulates'>('aqi');

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
          <div className="flex items-center space-x-2">
            <History className="w-4 h-4 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Historical AQI Trend</h3>
            <DemoBadge label="Telemetry Preview" />
          </div>

          {/* Metric Toggle */}
          <div className="flex bg-slate-950 p-0.5 rounded-lg border border-slate-800 text-xs">
            <button
              onClick={() => setViewMetric('aqi')}
              className={`px-2.5 py-1 rounded font-medium transition-colors ${
                viewMetric === 'aqi'
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Overall AQI
            </button>
            <button
              onClick={() => setViewMetric('particulates')}
              className={`px-2.5 py-1 rounded font-medium transition-colors ${
                viewMetric === 'particulates'
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              PM2.5 vs PM10
            </button>
          </div>
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Observed ambient air telemetry over the previous 24 hours
        </p>

        {/* Chart */}
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={MOCK_HISTORICAL_24H}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
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
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-slate-950/95 border border-slate-700/80 p-2.5 rounded-lg text-xs shadow-xl backdrop-blur">
                        <div className="font-semibold text-slate-200 mb-1">{label}</div>
                        {payload.map((item, idx) => (
                          <div
                            key={idx}
                            className="font-mono text-[11px]"
                            style={{ color: item.color }}
                          >
                            {item.name}: {item.value}
                          </div>
                        ))}
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Legend
                verticalAlign="top"
                align="right"
                iconType="circle"
                wrapperStyle={{ fontSize: '11px', paddingBottom: '8px' }}
              />
              {viewMetric === 'aqi' ? (
                <Line
                  type="monotone"
                  dataKey="aqi"
                  name="Air Quality Index (AQI)"
                  stroke="#10b981"
                  strokeWidth={2.5}
                  dot={{ fill: '#10b981', r: 3 }}
                  activeDot={{ r: 5 }}
                />
              ) : (
                <>
                  <Line
                    type="monotone"
                    dataKey="pm25"
                    name="PM 2.5 (µg/m³)"
                    stroke="#ef4444"
                    strokeWidth={2}
                    dot={{ fill: '#ef4444', r: 3 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="pm10"
                    name="PM 10 (µg/m³)"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    dot={{ fill: '#f59e0b', r: 3 }}
                  />
                </>
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800/60 mt-4 flex items-center justify-between">
        <span>Source: Central Pollution Control Board (CPCB) Standard Emulation</span>
        <span>Sampling interval: 3h</span>
      </div>
    </div>
  );
};
