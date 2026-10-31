import { AQISummary, Station, ForecastDataPoint, HistoricalDataPoint, PollutionSource, AnomalyAlert } from '../types/aqi';

export const LOCATIONS = [
  'Delhi NCR',
  'Mumbai Metropolitan',
  'Bengaluru Urban',
  'Kolkata Central',
  'Hyderabad Tech Zone',
  'Chennai Coastal',
];

export const MOCK_CURRENT_SUMMARY: AQISummary = {
  locationName: 'Delhi NCR',
  aqi: 234,
  category: 'Poor',
  severityColor: '#f97316',
  primaryPollutant: 'PM 2.5',
  primaryConcentration: '92 µg/m³ concentration',
  twelveHourPrediction: 164,
  twelveHourCategory: 'Poor',
  predictionConfidence: '88%',
  healthAdvice: 'Wear N95 mask outdoors today. Sensitive groups should avoid prolonged outdoor exertion.',
  changeRate: '+5% from 1hr ago',
  isDemoData: true,
  pollutants: {
    pm25: 92.4,
    pm10: 168.0,
    no2: 44.2,
    so2: 18.1,
    co: 1.4,
    o3: 32.5,
  },
};

export const MOCK_STATIONS: Station[] = [
  {
    id: 'st-okhla',
    name: 'Okhla Industrial Estate',
    lat: 28.5355,
    lng: 77.2732,
    aqi: 312,
    category: 'Severe',
    status: 'Alert',
    mainPollutant: 'PM 2.5 (182 µg/m³)',
  },
  {
    id: 'st-cp',
    name: 'Connaught Place',
    lat: 28.6315,
    lng: 77.2167,
    aqi: 210,
    category: 'Poor',
    status: 'Active',
    mainPollutant: 'PM 2.5 (88 µg/m³)',
  },
  {
    id: 'st-anand-vihar',
    name: 'Anand Vihar ISBT',
    lat: 28.6508,
    lng: 77.3153,
    aqi: 285,
    category: 'Very Poor',
    status: 'Active',
    mainPollutant: 'PM 10 (240 µg/m³)',
  },
  {
    id: 'st-punjabi-bagh',
    name: 'Punjabi Bagh',
    lat: 28.6679,
    lng: 77.1265,
    aqi: 195,
    category: 'Poor',
    status: 'Active',
    mainPollutant: 'PM 2.5 (78 µg/m³)',
  },
  {
    id: 'st-saket',
    name: 'Saket / South Delhi',
    lat: 28.5244,
    lng: 77.2066,
    aqi: 158,
    category: 'Poor',
    status: 'Active',
    mainPollutant: 'PM 2.5 (62 µg/m³)',
  },
  {
    id: 'st-rohini',
    name: 'Rohini Sector 16',
    lat: 28.7325,
    lng: 77.1197,
    aqi: 245,
    category: 'Poor',
    status: 'Active',
    mainPollutant: 'PM 10 (195 µg/m³)',
  },
  {
    id: 'st-noida',
    name: 'Noida Sector 62',
    lat: 28.6280,
    lng: 77.3649,
    aqi: 268,
    category: 'Very Poor',
    status: 'Active',
    mainPollutant: 'PM 2.5 (115 µg/m³)',
  },
];

export const MOCK_ANOMALY_ALERT: AnomalyAlert = {
  id: 'alert-okhla-1',
  title: 'Anomaly Detected: Sudden AQI spike detected near Okhla',
  description: 'Localized PM2.5 spike +34% within 30 min. Heavy industrial & freight corridor congestion identified.',
  severity: 'critical',
  timestamp: 'Just now',
  location: 'Okhla Industrial Area',
};

export const MOCK_FORECAST_24H: ForecastDataPoint[] = [
  { time: '00:00', predictedAqi: 230, lowerBound: 215, upperBound: 245, category: 'Poor' },
  { time: '02:00', predictedAqi: 245, lowerBound: 228, upperBound: 262, category: 'Poor' },
  { time: '04:00', predictedAqi: 260, lowerBound: 240, upperBound: 280, category: 'Very Poor' },
  { time: '06:00', predictedAqi: 275, lowerBound: 252, upperBound: 298, category: 'Very Poor' },
  { time: '08:00', predictedAqi: 290, lowerBound: 265, upperBound: 315, category: 'Very Poor' },
  { time: '10:00', predictedAqi: 240, lowerBound: 220, upperBound: 260, category: 'Poor' },
  { time: '12:00', predictedAqi: 195, lowerBound: 175, upperBound: 215, category: 'Poor' },
  { time: '14:00', predictedAqi: 164, lowerBound: 145, upperBound: 183, category: 'Poor' },
  { time: '16:00', predictedAqi: 175, lowerBound: 155, upperBound: 195, category: 'Poor' },
  { time: '18:00', predictedAqi: 210, lowerBound: 190, upperBound: 230, category: 'Poor' },
  { time: '20:00', predictedAqi: 250, lowerBound: 225, upperBound: 275, category: 'Very Poor' },
  { time: '22:00', predictedAqi: 265, lowerBound: 240, upperBound: 290, category: 'Very Poor' },
];

export const MOCK_HISTORICAL_24H: HistoricalDataPoint[] = [
  { time: 'Yesterday 12:00', aqi: 180, pm25: 72, pm10: 140 },
  { time: '15:00', aqi: 192, pm25: 78, pm10: 152 },
  { time: '18:00', aqi: 215, pm25: 86, pm10: 168 },
  { time: '21:00', aqi: 240, pm25: 98, pm10: 182 },
  { time: '00:00', aqi: 255, pm25: 104, pm10: 190 },
  { time: '03:00', aqi: 268, pm25: 110, pm10: 198 },
  { time: '06:00', aqi: 280, pm25: 115, pm10: 205 },
  { time: '09:00', aqi: 248, pm25: 99, pm10: 178 },
  { time: 'Current 12:00', aqi: 234, pm25: 92, pm10: 168 },
];

export const MOCK_POLLUTION_SOURCES: PollutionSource[] = [
  { name: 'Traffic Congestion', percentage: 52, color: '#ef4444' },
  { name: 'Stubble / Biomass Burning', percentage: 31, color: '#10b981' },
  { name: 'Industrial Emissions & Dust', percentage: 17, color: '#f59e0b' },
];
