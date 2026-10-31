"""Service layer for fetching air quality summaries, CPCB AQI calculation, and managing mock/scaffold data."""

from typing import Dict, Any, List
from datetime import datetime, timezone


class AQIService:
    """Provides AQI calculations, retrieval, and demo scaffolding."""

    @staticmethod
    def get_severity_category(aqi: int) -> Dict[str, str]:
        """Maps numeric AQI to standard health severity category and color code."""
        if aqi <= 50:
            return {"category": "Good", "color": "#22c55e", "severity": "low"}
        elif aqi <= 100:
            return {"category": "Moderate", "color": "#eab308", "severity": "moderate"}
        elif aqi <= 200:
            return {"category": "Poor", "color": "#f97316", "severity": "high"}
        elif aqi <= 300:
            return {"category": "Very Poor", "color": "#ef4444", "severity": "severe"}
        elif aqi <= 400:
            return {"category": "Severe", "color": "#a855f7", "severity": "hazardous"}
        else:
            return {"category": "Hazardous", "color": "#881337", "severity": "emergency"}

    @staticmethod
    def calculate_aqi_from_pm25(pm25_conc: float) -> int:
        """Calculates CPCB National Air Quality Index (NAQI) sub-index for PM2.5.

        Formula:
            I = I_low + ((I_high - I_low) / (B_high - B_low)) * (C - B_low)

        Breakpoints (µg/m³):
            0 - 30   -> AQI 0 - 50
            31 - 60  -> AQI 51 - 100
            61 - 90  -> AQI 101 - 200
            91 - 120 -> AQI 201 - 300
            121 - 250 -> AQI 301 - 400
            250+     -> AQI 401 - 500
        """
        c = max(0.0, float(pm25_conc))
        if c <= 30.0:
            aqi = (50.0 / 30.0) * c
        elif c <= 60.0:
            aqi = 50.0 + ((100.0 - 50.0) / (60.0 - 30.0)) * (c - 30.0)
        elif c <= 90.0:
            aqi = 100.0 + ((200.0 - 100.0) / (90.0 - 60.0)) * (c - 60.0)
        elif c <= 120.0:
            aqi = 200.0 + ((300.0 - 200.0) / (120.0 - 90.0)) * (c - 90.0)
        elif c <= 250.0:
            aqi = 300.0 + ((400.0 - 300.0) / (250.0 - 120.0)) * (c - 120.0)
        else:
            aqi = 400.0 + ((500.0 - 400.0) / (380.0 - 250.0)) * min(c - 250.0, 130.0)
        return int(round(min(500.0, aqi)))

    @staticmethod
    def get_demo_summary(location: str = "Delhi NCR") -> Dict[str, Any]:
        """Returns representative demonstration data for Checkpoint 3 preview."""
        return {
            "location_name": location,
            "aqi": 234,
            "category": "Poor",
            "severity_color": "#f97316",
            "primary_pollutant": "PM 2.5",
            "primary_concentration": "92 µg/m³",
            "twelve_hour_prediction": 164,
            "twelve_hour_category": "Poor",
            "prediction_confidence": "88%",
            "health_advice": "Wear N95 mask outdoors today. Sensitive groups should avoid prolonged exertion.",
            "change_rate": "+5% from 1hr ago",
            "data_status": "demo_preview",
            "is_demo_data": True,
            "pollutants": {
                "pm25": 92.4,
                "pm10": 168.0,
                "no2": 44.2,
                "so2": 18.1,
                "co": 1.4,
                "o3": 32.5,
            },
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def get_demo_stations() -> List[Dict[str, Any]]:
        """Returns representative monitoring station locations for map visualization."""
        return [
            {
                "id": "st-1",
                "name": "Connaught Place",
                "lat": 28.6315,
                "lng": 77.2167,
                "aqi": 210,
                "category": "Poor",
                "status": "Active",
                "main_pollutant": "PM 2.5 (88 µg/m³)",
            },
            {
                "id": "st-2",
                "name": "Okhla Industrial Area",
                "lat": 28.5355,
                "lng": 77.2732,
                "aqi": 312,
                "category": "Severe",
                "status": "Alert",
                "main_pollutant": "PM 2.5 (182 µg/m³)",
            },
            {
                "id": "st-3",
                "name": "Anand Vihar",
                "lat": 28.6508,
                "lng": 77.3153,
                "aqi": 285,
                "category": "Very Poor",
                "status": "Active",
                "main_pollutant": "PM 10 (240 µg/m³)",
            },
            {
                "id": "st-4",
                "name": "Punjabi Bagh",
                "lat": 28.6679,
                "lng": 77.1265,
                "aqi": 195,
                "category": "Poor",
                "status": "Active",
                "main_pollutant": "PM 2.5 (78 µg/m³)",
            },
            {
                "id": "st-5",
                "name": "South Delhi / Saket",
                "lat": 28.5244,
                "lng": 77.2066,
                "aqi": 158,
                "category": "Poor",
                "status": "Active",
                "main_pollutant": "PM 2.5 (62 µg/m³)",
            },
            {
                "id": "st-6",
                "name": "Rohini Sector 16",
                "lat": 28.7325,
                "lng": 77.1197,
                "aqi": 245,
                "category": "Poor",
                "status": "Active",
                "main_pollutant": "PM 10 (195 µg/m³)",
            },
            {
                "id": "st-7",
                "name": "Noida Sector 62",
                "lat": 28.6280,
                "lng": 77.3649,
                "aqi": 268,
                "category": "Very Poor",
                "status": "Active",
                "main_pollutant": "PM 2.5 (115 µg/m³)",
            },
        ]
