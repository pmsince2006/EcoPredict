import React from 'react';
import { Activity } from 'lucide-react';
import { PollutantValues } from '../../types/aqi';
import { DemoBadge } from '../../components/common/DemoBadge';

interface PollutantCardsProps {
  pollutants: PollutantValues;
}

interface PollutantItem {
  id: string;
  name: string;
  label: string;
  value: number;
  unit: string;
  standardLimit: number;
  description: string;
}

export const PollutantCards: React.FC<PollutantCardsProps> = ({ pollutants }) => {
  const items: PollutantItem[] = [
    {
      id: 'pm25',
      name: 'PM 2.5',
      label: 'Fine Particles',
      value: pollutants.pm25,
      unit: 'µg/m³',
      standardLimit: 60,
      description: 'Penetrates deep into alveolar lung tissues',
    },
    {
      id: 'pm10',
      name: 'PM 10',
      label: 'Coarse Dust',
      value: pollutants.pm10,
      unit: 'µg/m³',
      standardLimit: 100,
      description: 'Suspended road dust and construction debris',
    },
    {
      id: 'no2',
      name: 'NO₂',
      label: 'Nitrogen Dioxide',
      value: pollutants.no2,
      unit: 'µg/m³',
      standardLimit: 80,
      description: 'Vehicle combustion and power generation',
    },
    {
      id: 'so2',
      name: 'SO₂',
      label: 'Sulfur Dioxide',
      value: pollutants.so2,
      unit: 'µg/m³',
      standardLimit: 80,
      description: 'Thermal power plants and fossil refining',
    },
    {
      id: 'co',
      name: 'CO',
      label: 'Carbon Monoxide',
      value: pollutants.co,
      unit: 'mg/m³',
      standardLimit: 2.0,
      description: 'Incomplete vehicular exhaust combustion',
    },
    {
      id: 'o3',
      name: 'O₃',
      label: 'Ground-level Ozone',
      value: pollutants.o3,
      unit: 'µg/m³',
      standardLimit: 100,
      description: 'Photochemical reaction under solar radiation',
    },
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Specific Pollutant Concentrations</h3>
            <DemoBadge label="Telemetry Grid" />
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Individual pollutant readings compared against Indian NAAQS 24h standards
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {items.map((item) => {
          const isExceeded = item.value > item.standardLimit;
          return (
            <div
              key={item.id}
              className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-3.5 flex flex-col justify-between hover:border-slate-700 transition-colors"
            >
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-200 text-sm">{item.name}</span>
                  {isExceeded ? (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-medium">
                      Exceeded
                    </span>
                  ) : (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                      Safe
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-slate-500 truncate mb-2">{item.label}</div>
                <div className="flex items-baseline space-x-1">
                  <span className="text-xl font-bold font-mono text-white">{item.value}</span>
                  <span className="text-[11px] text-slate-400">{item.unit}</span>
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-800/60 text-[10px] text-slate-400 flex justify-between">
                <span>Std Limit:</span>
                <span className="font-mono text-slate-300">
                  {item.standardLimit} {item.unit}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
