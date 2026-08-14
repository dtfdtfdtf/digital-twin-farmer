# app/ai/weather_processing.py
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class WeatherProcessor:
    """
    Weather data processing for Malawi.
    Uses simulated data (will integrate CHIRPS/API later).
    """
    
    # Seasonal patterns for Malawi (Oct-Mar growing season)
    SEASONS = {
        "2022-2023": {"rainfall": 950, "temp": 24.5},
        "2023-2024": {"rainfall": 1020, "temp": 24.0},
        "2024-2025": {"rainfall": 890, "temp": 25.0},
        "2025-2026": {"rainfall": 980, "temp": 24.2},
    }
    
    def __init__(self):
        self.rainfall_data = {}
        
    def get_rainfall(self, district: str, season: Optional[str] = None) -> Dict:
        """Get rainfall data for a district"""
        if not season:
            season = "2025-2026"
        
        # Base rainfall varies by district
        base_rainfall = {
            "Lilongwe": 850,
            "Blantyre": 900,
            "Mzuzu": 1100,
            "Zomba": 950,
            "Kasungu": 750,
            "Mzimba": 900,
            "Rumphi": 1000,
            "Dedza": 850,
            "Salima": 700,
            "Mangochi": 720,
        }
        
        base = base_rainfall.get(district, 850)
        
        # Seasonal variation
        seasonal_factor = 0.85 + random.uniform(0, 0.3)
        total_rainfall = base * seasonal_factor
        
        # Monthly distribution
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        monthly_rainfall = []
        
        for i in range(6):
            # Peak in Jan-Feb
            peak_factor = 0.5 + 0.5 * (1 - abs((i - 2.5) / 3))
            monthly = (total_rainfall / 6) * peak_factor * random.uniform(0.8, 1.2)
            monthly_rainfall.append(round(monthly, 1))
        
        return {
            "district": district,
            "season": season,
            "total_rainfall": round(total_rainfall, 1),
            "months": months,
            "monthly_rainfall": monthly_rainfall,
            "rainfall_category": self._get_rainfall_category(total_rainfall),
            "is_drought_risk": total_rainfall < 700,
        }
    
    def get_temperature(self, district: str) -> Dict:
        """Get temperature data for a district"""
        base_temp = {
            "Lilongwe": 24.5,
            "Blantyre": 26.0,
            "Mzuzu": 22.5,
            "Zomba": 25.0,
            "Kasungu": 24.0,
            "Mzimba": 23.5,
            "Rumphi": 23.0,
            "Dedza": 24.0,
            "Salima": 27.0,
            "Mangochi": 27.5,
        }
        
        temp = base_temp.get(district, 24.5)
        
        # Monthly temperatures (higher in Oct-Nov, lower in Jun-Jul)
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        monthly_temps = []
        
        for i in range(6):
            variation = random.uniform(-1.0, 1.0)
            monthly = temp + variation
            monthly_temps.append(round(monthly, 1))
        
        return {
            "district": district,
            "average_temperature": temp,
            "months": months,
            "monthly_temperatures": monthly_temps,
            "min_temperature": round(min(monthly_temps), 1),
            "max_temperature": round(max(monthly_temps), 1),
        }
    
    def get_weather_summary(self, district: str) -> Dict:
        """Get comprehensive weather summary"""
        rainfall = self.get_rainfall(district)
        temperature = self.get_temperature(district)
        
        return {
            "district": district,
            "rainfall": rainfall,
            "temperature": temperature,
            "growing_conditions": self._get_growing_conditions(rainfall, temperature),
        }
    
    def get_historical_weather(self, district: str, seasons: int = 3) -> List[Dict]:
        """Get historical weather data for past seasons"""
        historical = []
        
        for i, (season, data) in enumerate(list(self.SEASONS.items())[-seasons:]):
            rainfall = data["rainfall"] * random.uniform(0.9, 1.1)
            temp = data["temp"] + random.uniform(-0.5, 0.5)
            historical.append({
                "season": season,
                "rainfall": round(rainfall, 1),
                "temperature": round(temp, 1),
                "condition": "Good" if rainfall > 800 else "Fair" if rainfall > 600 else "Poor",
            })
        
        return historical
    
    def _get_rainfall_category(self, rainfall: float) -> str:
        """Classify rainfall amounts"""
        if rainfall >= 1000:
            return "Above Normal"
        elif rainfall >= 800:
            return "Normal"
        elif rainfall >= 600:
            return "Below Normal"
        else:
            return "Drought"
    
    def _get_growing_conditions(self, rainfall: Dict, temperature: Dict) -> str:
        """Evaluate growing conditions"""
        rain_category = rainfall["rainfall_category"]
        avg_temp = temperature["average_temperature"]
        
        if rain_category in ["Above Normal", "Normal"] and 20 <= avg_temp <= 28:
            return "Excellent"
        elif rain_category == "Normal" and 18 <= avg_temp <= 30:
            return "Good"
        elif rain_category == "Below Normal" or avg_temp > 30:
            return "Fair"
        else:
            return "Poor"