/**
 * EcoPredict Frontend API Client
 *
 * Handles HTTP requests to the FastAPI backend with:
 * - Configurable base URL via VITE_API_BASE_URL
 * - Type-safe response mapping from backend snake_case to frontend camelCase
 * - Graceful fallback to verified mock fixtures when backend is offline
 * - Explicit preservation of data_status ("demo_preview", "real_observation", "unavailable")
 */

import {
  AQISummary,
  Station,
  StationResponse,
  ForecastResponse,
  HealthResponse,
  ForecastDataPoint,
} from '../types/aqi';
import {
  MOCK_CURRENT_SUMMARY,
  MOCK_STATIONS,
  MOCK_FORECAST_24H,
} from './mockData';

const BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Checks system health and model loading status from the backend.
 */
export async function getHealthStatus(): Promise<HealthResponse> {
  try {
    const res = await fetch(`${BASE_URL}/health`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    // Return fallback offline state
    return {
      status: 'offline',
      service: 'EcoPredict Backend API (Offline)',
      version: '0.3.0',
      checkpoint: 'Checkpoint 3 — Safe Backend Inference & Integration',
      data_status: 'demo_preview',
      model_loaded: false,
      real_data_validated: false,
      environment: 'development',
    };
  }
}

/**
 * Fetches the current AQI summary for a given monitoring location.
 */
export async function getAqiSummary(location: string = 'Delhi NCR'): Promise<AQISummary> {
  try {
    const url = `${BASE_URL}/aqi/summary?location=${encodeURIComponent(location)}`;
    const res = await fetch(url, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    const data = await res.json();

    // Map backend response safely
    return {
      locationName: data.location_name || location,
      aqi: data.aqi,
      category: data.category,
      severityColor: data.severity_color || '#f97316',
      primaryPollutant: data.primary_pollutant || 'PM 2.5',
      primaryConcentration: data.primary_concentration || '92 µg/m³',
      twelveHourPrediction: data.twelve_hour_prediction || 164,
      twelveHourCategory: data.twelve_hour_category || 'Poor',
      predictionConfidence: data.prediction_confidence || '88%',
      healthAdvice: data.health_advice || '',
      changeRate: data.change_rate || '+0% from 1hr ago',
      dataStatus: data.data_status || 'demo_preview',
      isDemoData: data.is_demo_data ?? true,
      pollutants: data.pollutants || MOCK_CURRENT_SUMMARY.pollutants,
      lastUpdated: data.last_updated,
    };
  } catch (err) {
    // Graceful offline fallback
    return {
      ...MOCK_CURRENT_SUMMARY,
      locationName: location,
      dataStatus: 'demo_preview',
    };
  }
}

/**
 * Fetches active monitoring stations with geo-coordinates and AQI metrics.
 */
export async function getMonitoringStations(): Promise<Station[]> {
  try {
    const res = await fetch(`${BASE_URL}/aqi/stations`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    const data: StationResponse = await res.json();
    return data.stations || MOCK_STATIONS;
  } catch (err) {
    return MOCK_STATIONS;
  }
}

/**
 * Fetches multi-horizon model predictions with explicit model metadata and disclaimer.
 */
export async function getForecast(
  location: string = 'Delhi NCR',
  horizon: number = 24,
  allowDemo: boolean = true
): Promise<ForecastResponse> {
  try {
    const url = `${BASE_URL}/aqi/forecast?location=${encodeURIComponent(
      location
    )}&horizon=${horizon}&allow_demo=${allowDemo}`;
    const res = await fetch(url, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    // Construct structured demo fallback response
    return {
      target_variable: 'pm25',
      target_unit: 'µg/m³',
      forecast_horizon_hours: horizon,
      generated_at: new Date().toISOString(),
      location_name: location,
      station_id: 'DL001_ANAND_VIHAR',
      data_status: 'demo_preview',
      is_demo_model: true,
      real_data_validated: false,
      model_version: 'baseline_random_forest.pkl',
      model_provenance: 'synthetic_fixture',
      model_mae: 7.943,
      model_rmse: 8.494,
      forecast_points: MOCK_FORECAST_24H.map((pt) => ({
        time: pt.time,
        predicted_pm25: pt.predictedAqi * 0.6,
        predicted_aqi: pt.predictedAqi,
        lower_bound_pm25: (pt.lowerBound ?? 100) * 0.6,
        upper_bound_pm25: (pt.upperBound ?? 250) * 0.6,
        category: pt.category,
      })),
      disclaimer:
        'DEMO PREVIEW: Fallback preview output. Model trained on synthetic test fixture; not validated against live CPCB data.',
    };
  }
}

/**
 * Converts backend forecast response points into chart-ready series.
 */
export function transformForecastToChartData(
  forecast: ForecastResponse
): ForecastDataPoint[] {
  if (!forecast.forecast_points || forecast.forecast_points.length === 0) {
    return MOCK_FORECAST_24H;
  }
  return forecast.forecast_points.map((pt) => ({
    time: pt.time,
    predictedAqi: pt.predicted_aqi,
    predictedPm25: pt.predicted_pm25,
    lowerBound: Math.round(pt.lower_bound_pm25 * 1.66), // Mapped lower bound for chart
    upperBound: Math.round(pt.upper_bound_pm25 * 1.66), // Mapped upper bound for chart
    category: pt.category,
  }));
}
