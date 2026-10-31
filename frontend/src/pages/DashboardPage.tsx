import React, { useEffect, useState } from 'react';
import { MOCK_CURRENT_SUMMARY, MOCK_STATIONS, MOCK_FORECAST_24H } from '../services/mockData';
import {
  getAqiSummary,
  getMonitoringStations,
  getForecast,
  getHealthStatus,
  transformForecastToChartData,
} from '../services/api';
import {
  AQISummary,
  Station,
  ForecastDataPoint,
  ForecastResponse,
  HealthResponse,
} from '../types/aqi';
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
  onHealthStatusUpdate?: (status: HealthResponse) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  selectedLocation,
  onHealthStatusUpdate,
}) => {
  const [summary, setSummary] = useState<AQISummary>({
    ...MOCK_CURRENT_SUMMARY,
    locationName: selectedLocation,
  });
  const [stations, setStations] = useState<Station[]>(MOCK_STATIONS);
  const [forecastData, setForecastData] = useState<ForecastDataPoint[]>(MOCK_FORECAST_24H);
  const [forecastMeta, setForecastMeta] = useState<ForecastResponse | null>(null);
  const [isLoadingForecast, setIsLoadingForecast] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;

    async function loadBackendData() {
      // 1. Fetch Health
      try {
        const health = await getHealthStatus();
        if (isMounted && onHealthStatusUpdate) {
          onHealthStatusUpdate(health);
        }
      } catch (e) {
        // Handled in api client
      }

      // 2. Fetch Summary
      try {
        const sum = await getAqiSummary(selectedLocation);
        if (isMounted) setSummary(sum);
      } catch (e) {
        // Handled in api client
      }

      // 3. Fetch Stations
      try {
        const stList = await getMonitoringStations();
        if (isMounted) setStations(stList);
      } catch (e) {
        // Handled in api client
      }

      // 4. Fetch Forecast from backend model service
      setIsLoadingForecast(true);
      try {
        const fc = await getForecast(selectedLocation, 24, true);
        if (isMounted) {
          setForecastMeta(fc);
          const chartPoints = transformForecastToChartData(fc);
          setForecastData(chartPoints);
        }
      } catch (e) {
        // Handled in api client
      } finally {
        if (isMounted) setIsLoadingForecast(false);
      }
    }

    loadBackendData();

    return () => {
      isMounted = false;
    };
  }, [selectedLocation, onHealthStatusUpdate]);

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
          <InteractiveMap stations={stations} />
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
        <ForecastChart
          forecastData={forecastData}
          forecastMeta={forecastMeta}
          isLoading={isLoadingForecast}
        />
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
