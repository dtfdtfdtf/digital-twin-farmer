# app/services/satellite_service.py
from typing import Dict, Optional
from app.ai.satellite_analysis import SatelliteAnalyzer
import logging

logger = logging.getLogger(__name__)


class SatelliteService:
    """
    Service for satellite data operations.
    """
    
    def __init__(self):
        self.analyzer = SatelliteAnalyzer()
    
    def get_district_ndvi(self, district: str, season: Optional[str] = None) -> Dict:
        """Get NDVI data for a district"""
        try:
            return self.analyzer.get_ndvi(district, season)
        except Exception as e:
            logger.error(f"Error getting NDVI for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_land_suitability(self, district: str) -> Dict:
        """Get land suitability data"""
        try:
            return self.analyzer.get_land_suitability(district)
        except Exception as e:
            logger.error(f"Error getting land suitability for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_vegetation_indices(self, district: str) -> Dict:
        """Get vegetation indices"""
        try:
            return self.analyzer.get_vegetation_indices(district)
        except Exception as e:
            logger.error(f"Error getting vegetation indices for {district}: {str(e)}")
            return {"error": str(e)}
    
    def get_comprehensive_analysis(self, district: str) -> Dict:
        """Get comprehensive satellite analysis"""
        ndvi = self.get_district_ndvi(district)
        suitability = self.get_land_suitability(district)
        indices = self.get_vegetation_indices(district)
        
        return {
            "district": district,
            "ndvi": ndvi,
            "land_suitability": suitability,
            "vegetation_indices": indices,
            "timestamp": datetime.now().isoformat()
        }