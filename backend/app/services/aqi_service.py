"""Service layer for fetching air quality summaries and managing mock/scaffold data."""

from typing import Dict, Any, List


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
    def get_demo_summary(location: str = "Delhi NCR") -> Dict[str, Any]:
        """Returns representative demonstration data for Checkpoint 1."""
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
            "is_demo_data": True,
            "pollutants": {
                "pm25": 92.4,
                "pm10": 168.0,
                "no2": 44.2,
                "so2": 18.1,
                "co": 1.4,
                "o3": 32.5,
            },
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
            },
            {
                "id": "st-2",
                "name": "Okhla Industrial Area",
                "lat": 28.5355,
                "lng": 77.2732,
                "aqi": 312,
                "category": "Severe",
                "status": "Alert",
            },
            {
                "id": "st-3",
                "name": "Anand Vihar",
                "lat": 28.6508,
                "lng": 77.3153,
                "aqi": 285,
                "category": "Very Poor",
                "status": "Active",
            },
            {
                "id": "st-4",
                "name": "Punjabi Bagh",
                "lat": 28.6679,
                "lng": 77.1265,
                "aqi": 195,
                "category": "Poor",
                "status": "Active",
            },
            {
                "id": "st-5",
                "name": "South Delhi / Saket",
                "lat": 28.5244,
                "lng": 77.2066,
                "aqi": 158,
                "category": "Poor",
                "status": "Active",
            },
        ]
