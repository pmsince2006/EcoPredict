import React from 'react';
import { MOCK_CURRENT_SUMMARY } from '../services/mockData';
import { KpiCards } from '../features/dashboard/KpiCards';
import { InteractiveMap } from '../features/dashboard/InteractiveMap';
import { RoutePlanner } from '../features/dashboard/RoutePlanner';
import { HotspotAnalysis } from '../features/dashboard/HotspotAnalysis';
import { ForecastChart } from '../features/dashboard/ForecastChart';
import { HistoricalTrendChart } from '../features/dashboard/HistoricalTrendChart';
import { PollutantCards } from '../features/dashboard/PollutantCards';
import { SourceBreakdownChart } from '../features/dashboard/SourceBreakdownChart';

interface DashboardPageProps {
  selectedLocation: string;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ selectedLocation }) => {
  // Update location name for demo summary if location changes
  const summary = {
    ...MOCK_CURRENT_SUMMARY,
    locationName: selectedLocation,
  };

  return (
    <div className="space-y-6">
      {/* 1. Top KPI Summary Cards */}
      <section aria-label="Key Performance Indicators">
        <KpiCards summary={summary} />
      </section>

      {/* 2. Middle Section: Map + Route Planner & Hotspot Analysis */}
      <section
        aria-label="Geospatial Hotspots and Route Planning"
        className="grid grid-cols-1 lg:grid-cols-12 gap-6"
      >
        {/* Interactive Map (8 cols on large screens) */}
        <div className="lg:col-span-8 h-[480px]">
          <InteractiveMap />
        </div>

        {/* Route Planner & Hotspot Side Panel (4 cols on large screens) */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <RoutePlanner />
          <HotspotAnalysis />
        </div>
      </section>

      {/* 3. Predictive Forecast & Historical Telemetry Trend */}
      <section
        aria-label="Forecast and Historical Trends"
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        <ForecastChart />
        <HistoricalTrendChart />
      </section>

      {/* 4. Pollutant Granularity & Source Attribution */}
      <section
        aria-label="Pollutant Breakdown and Emission Sources"
        className="grid grid-cols-1 lg:grid-cols-12 gap-6"
      >
        <div className="lg:col-span-7">
          <PollutantCards pollutants={summary.pollutants} />
        </div>
        <div className="lg:col-span-5">
          <SourceBreakdownChart />
        </div>
      </section>
    </div>
  );
};
