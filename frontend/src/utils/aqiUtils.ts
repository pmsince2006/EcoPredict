import { AQICategory } from '../types/aqi';

export function getAqiCategory(aqi: number): AQICategory {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Moderate';
  if (aqi <= 200) return 'Poor';
  if (aqi <= 300) return 'Very Poor';
  if (aqi <= 400) return 'Severe';
  return 'Hazardous';
}

export function getAqiColor(category: AQICategory): string {
  switch (category) {
    case 'Good':
      return '#22c55e'; // emerald-500
    case 'Moderate':
      return '#eab308'; // yellow-500
    case 'Poor':
      return '#f97316'; // orange-500
    case 'Very Poor':
      return '#ef4444'; // red-500
    case 'Severe':
      return '#a855f7'; // purple-500
    case 'Hazardous':
      return '#991b1b'; // dark red
    default:
      return '#64748b'; // slate-500
  }
}

export function getAqiBadgeClasses(category: AQICategory): string {
  switch (category) {
    case 'Good':
      return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    case 'Moderate':
      return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
    case 'Poor':
      return 'bg-orange-500/10 text-orange-400 border-orange-500/30';
    case 'Very Poor':
      return 'bg-red-500/10 text-red-400 border-red-500/30';
    case 'Severe':
      return 'bg-purple-500/10 text-purple-400 border-purple-500/30';
    case 'Hazardous':
      return 'bg-rose-950/40 text-rose-300 border-rose-800/40';
    default:
      return 'bg-slate-800 text-slate-300 border-slate-700';
  }
}
