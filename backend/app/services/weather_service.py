# app/services/weather_service.py
from typing import Dict, Optional, List
from app.ai.weather_processing import WeatherProcessor
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class WeatherService:
    """
    Service for weather data operations.
    """
    
    def __init__(self):
        self.processor = WeatherProcessor()
    
    def get_rainfall(self, district: str, season: Optional[str] = None) -> Dict:
        """Get rainfall data for a district"""
        try:
            return self.processor.get_rainfall(district, season)
        except Exception as e:
            logger.error(f"Error getting rainfall for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_temperature(self, district: str) -> Dict:
        """Get temperature data for a district"""
        try:
            return self.processor.get_temperature(district)
        except Exception as e:
            logger.error(f"Error getting temperature for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_weather_summary(self, district: str) -> Dict:
        """Get comprehensive weather summary"""
        try:
            return self.processor.get_weather_summary(district)
        except Exception as e:
            logger.error(f"Error getting weather summary for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_historical_weather(self, district: str, seasons: int = 3) -> List[Dict]:
        """Get historical weather data"""
        try:
            return self.processor.get_historical_weather(district, seasons)
        except Exception as e:
            logger.error(f"Error getting historical weather for {district}: {str(e)}")
            return []