import React, { useState } from 'react';
import { Header } from '../components/common/Header';
import { Shield } from 'lucide-react';

interface MainLayoutProps {
  children: (props: { selectedLocation: string }) => React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [selectedLocation, setSelectedLocation] = useState<string>('Delhi NCR');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation & Alerts Header */}
      <Header
        selectedLocation={selectedLocation}
        onLocationChange={setSelectedLocation}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {children({ selectedLocation })}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-900/60 mt-12 py-6 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-300">EcoPredict</span>
            <span>—</span>
            <span>Air Quality Monitoring & Forecasting Platform (Checkpoint 1 Foundation)</span>
          </div>

          <div className="flex items-center space-x-4 text-slate-400">
            <span className="flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-emerald-400" />
              Demo Data Mode
            </span>
            <span>•</span>
            <span>Built by Team of 4 Students</span>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-2 text-[11px] text-slate-400">
          Disclaimer: Visualizations, forecasts, and hotspot attributions shown on this dashboard are illustrative mock previews prepared for Checkpoint 1 submission. Live API integrations and trained ML models will be connected in subsequent phases.
        </div>
      </footer>
    </div>
  );
};
