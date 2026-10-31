export type AQICategory =
  | 'Good'
  | 'Moderate'
  | 'Poor'
  | 'Very Poor'
  | 'Severe'
  | 'Hazardous';

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
  isDemoData: boolean;
  pollutants: PollutantValues;
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

export interface ForecastDataPoint {
  time: string;
  predictedAqi: number;
  lowerBound: number;
  upperBound: number;
  category: AQICategory;
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
