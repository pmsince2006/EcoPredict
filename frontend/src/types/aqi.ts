export type AQICategory =
  | 'Good'
  | 'Moderate'
  | 'Poor'
  | 'Very Poor'
  | 'Severe'
  | 'Hazardous';

export type DataStatus =
  | 'real_observation'
  | 'real_data_forecast'
  | 'demo_preview'
  | 'unavailable';

export interface PollutantValues {
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  co: number;
  o3: number;
}

export interface AQISummary {
  locationName: string;
  aqi: number;
  category: AQICategory;
  severityColor: string;
  primaryPollutant: string;
  primaryConcentration: string;
  twelveHourPrediction: number;
  twelveHourCategory: AQICategory;
  predictionConfidence: string;
  healthAdvice: string;
  changeRate: string;
  dataStatus?: DataStatus;
  isDemoData: boolean;
  pollutants: PollutantValues;
  lastUpdated?: string;
}

export interface Station {
  id: string;
  name: string;
  lat: number;
  lng: number;
  aqi: number;
  category: AQICategory;
  status: 'Active' | 'Alert' | 'Maintenance';
  mainPollutant: string;
}

export interface StationResponse {
  stations: Station[];
  data_status: DataStatus;
  is_demo_data: boolean;
  count: number;
}

export interface ForecastDataPoint {
  time: string;
  predictedAqi: number;
  predictedPm25?: number;
  lowerBound?: number;
  upperBound?: number;
  category: AQICategory;
}

export interface ForecastResponse {
  target_variable: string;
  target_unit: string;
  forecast_horizon_hours: number;
  generated_at: string;
  location_name: string;
  station_id?: string;
  data_status: DataStatus;
  is_demo_model: boolean;
  real_data_validated: boolean;
  model_version?: string;
  model_provenance?: string;
  model_mae?: number;
  model_rmse?: number;
  forecast_points: Array<{
    time: string;
    predicted_pm25: number;
    predicted_aqi: number;
    lower_bound_pm25: number;
    upper_bound_pm25: number;
    category: AQICategory;
  }>;
  disclaimer: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  checkpoint: string;
  data_status: DataStatus;
  model_loaded: boolean;
  model_provenance?: string;
  real_data_validated: boolean;
  environment: string;
}

export interface HistoricalDataPoint {
  time: string;
  aqi: number;
  pm25: number;
  pm10: number;
}

export interface PollutionSource {
  name: string;
  percentage: number;
  color: string;
}

export interface AnomalyAlert {
  id: string;
  title: string;
  description: string;
  severity: 'warning' | 'critical' | 'info';
  timestamp: string;
  location: string;
}
