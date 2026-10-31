import React from 'react';
import { Wind, AlertTriangle, MapPin, Server } from 'lucide-react';
import { LOCATIONS, MOCK_ANOMALY_ALERT } from '../../services/mockData';
import { DemoBadge } from './DemoBadge';
import { HealthResponse } from '../../types/aqi';

interface HeaderProps {
  selectedLocation: string;
  onLocationChange: (loc: string) => void;
  healthStatus?: HealthResponse | null;
}

export const Header: React.FC<HeaderProps> = ({
  selectedLocation,
  onLocationChange,
  healthStatus,
}) => {
  const isOnline = healthStatus?.status === 'healthy';

  return (
    <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        {/* Left: Brand & Tagline */}
        <div className="flex items-center space-x-3.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-sm">
            <Wind className="w-6 h-6 stroke-[2.2]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
                EcoPredict
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 font-medium">
                  v0.3 Checkpoint
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400">
              AI-Powered AQI Forecasting & Clean Routing Intelligence
            </p>
          </div>
        </div>

        {/* Center / Right: Location selector & Anomaly banner */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Backend Connection Status Pill */}
          <div
            className={`flex items-center px-2.5 py-1 rounded text-xs border font-medium ${
              isOnline
                ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                : 'bg-slate-800/80 text-slate-400 border-slate-700/60'
            }`}
            title={
              isOnline
                ? `Backend Online (Model Provenance: ${healthStatus?.model_provenance || 'loaded'})`
                : 'Backend unreachable. Running in local preview mode.'
            }
          >
            <Server className={`w-3.5 h-3.5 mr-1.5 ${isOnline ? 'text-emerald-400' : 'text-slate-500'}`} />
            <span>{isOnline ? 'API Connected' : 'Local Preview'}</span>
          </div>

          {/* Location Selector */}
          <div className="flex items-center bg-slate-800/80 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-300">
            <MapPin className="w-3.5 h-3.5 text-emerald-400 mr-1.5 shrink-0" />
            <select
              value={selectedLocation}
              onChange={(e) => onLocationChange(e.target.value)}
              className="bg-transparent border-none text-slate-200 text-xs font-medium focus:ring-0 focus:outline-none cursor-pointer pr-2"
              aria-label="Select Monitoring Location"
            >
              {LOCATIONS.map((loc) => (
                <option key={loc} value={loc} className="bg-slate-900 text-slate-200">
                  {loc}
                </option>
              ))}
            </select>
          </div>

          {/* Anomaly Notification Pill matching design reference */}
          <div className="flex items-center bg-rose-950/40 border border-rose-800/40 rounded-lg px-3 py-1.5 text-xs text-rose-200 max-w-md shadow-sm">
            <AlertTriangle className="w-4 h-4 text-rose-400 mr-2 shrink-0 animate-pulse" />
            <div className="truncate">
              <span className="font-semibold text-rose-300">Anomaly Detected:</span>{' '}
              <span className="text-rose-200/90">{MOCK_ANOMALY_ALERT.description}</span>
            </div>
          </div>

          <DemoBadge label="Demo Preview" />
        </div>
      </div>
    </header>
  );
};
