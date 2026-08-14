# app/ai/satellite_analysis.py
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class SatelliteAnalyzer:
    """
    Satellite data analysis for Malawi.
    Uses simulated data (will integrate Sentinel-2 API later).
    """
    
    # Malawi districts with approximate coordinates
    DISTRICTS = {
        "Lilongwe": {"lat": -13.9833, "lng": 33.7833},
        "Blantyre": {"lat": -15.7861, "lng": 35.0058},
        "Mzuzu": {"lat": -11.4656, "lng": 34.2107},
        "Zomba": {"lat": -15.3867, "lng": 35.3283},
        "Kasungu": {"lat": -13.0333, "lng": 33.4833},
        "Mzimba": {"lat": -11.9000, "lng": 33.6000},
        "Rumphi": {"lat": -11.0200, "lng": 33.8600},
        "Dedza": {"lat": -14.3333, "lng": 34.3333},
        "Salima": {"lat": -13.7833, "lng": 34.4333},
        "Mangochi": {"lat": -14.4667, "lng": 35.2667},
    }
    
    def __init__(self):
        self.ndvi_data = {}
        
    def get_ndvi(self, district: str, season: Optional[str] = None) -> Dict:
        """
        Get NDVI (Normalized Difference Vegetation Index) for a district.
        Returns simulated NDVI values between 0.2 and 0.8.
        """
        if district not in self.DISTRICTS:
            raise ValueError(f"District '{district}' not found. Available: {list(self.DISTRICTS.keys())}")
        
        # Seed random based on district for consistent results
        seed = hash(district) % 100
        random.seed(seed)
        
        # Generate NDVI values for a growing season (Oct-Mar)
        months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        
        # Base NDVI varies by district (different soil/vegetation)
        base_ndvi = {
            "Lilongwe": 0.55,
            "Blantyre": 0.60,
            "Mzuzu": 0.50,
            "Zomba": 0.58,
            "Kasungu": 0.45,
            "Mzimba": 0.48,
            "Rumphi": 0.52,
            "Dedza": 0.50,
            "Salima": 0.42,
            "Mangochi": 0.44,
        }
        
        base = base_ndvi.get(district, 0.50)
        
        # Simulate seasonal variation
        seasonal_ndvi = []
        for i, month in enumerate(months):
            # Peak in Jan/Feb (mid-season)
            peak_factor = 1.0 - 0.3 * abs((i - 2.5) / 2.5)
            variation = random.uniform(-0.05, 0.05)
            value = min(max(base * peak_factor + variation, 0.2), 0.8)
            seasonal_ndvi.append(round(value, 3))
        
        return {
            "district": district,
            "season": season or "2025-2026",
            "months": months,
            "ndvi_values": seasonal_ndvi,
            "average_ndvi": round(sum(seasonal_ndvi) / len(seasonal_ndvi), 3),
            "max_ndvi": round(max(seasonal_ndvi), 3),
            "min_ndvi": round(min(seasonal_ndvi), 3),
            "vegetation_health": self._get_vegetation_health(sum(seasonal_ndvi) / len(seasonal_ndvi)),
            "coordinates": self.DISTRICTS[district],
        }
    
    def get_land_suitability(self, district: str) -> Dict:
        """
        Get land suitability for agriculture in a district.
        Returns soil type, drainage, and suitability score.
        """
        suitability_scores = {
            "Lilongwe": {"soil_type": "Clay Loam", "drainage": "Good", "score": 0.85},
            "Blantyre": {"soil_type": "Sandy Loam", "drainage": "Moderate", "score": 0.78},
            "Mzuzu": {"soil_type": "Loam", "drainage": "Good", "score": 0.82},
            "Zomba": {"soil_type": "Clay", "drainage": "Moderate", "score": 0.75},
            "Kasungu": {"soil_type": "Sandy", "drainage": "Poor", "score": 0.55},
            "Mzimba": {"soil_type": "Loam", "drainage": "Good", "score": 0.80},
            "Rumphi": {"soil_type": "Clay Loam", "drainage": "Good", "score": 0.83},
            "Dedza": {"soil_type": "Loam", "drainage": "Moderate", "score": 0.72},
            "Salima": {"soil_type": "Sandy", "drainage": "Poor", "score": 0.45},
            "Mangochi": {"soil_type": "Sandy", "drainage": "Poor", "score": 0.50},
        }
        
        data = suitability_scores.get(district, {"soil_type": "Unknown", "drainage": "Unknown", "score": 0.50})
        return {
            "district": district,
            "soil_type": data["soil_type"],
            "drainage": data["drainage"],
            "suitability_score": data["score"],
            "suitability_level": self._get_suitability_level(data["score"]),
        }
    
    def get_vegetation_indices(self, district: str) -> Dict:
        """Get various vegetation indices"""
        ndvi_data = self.get_ndvi(district)
        
        return {
            "district": district,
            "ndvi": ndvi_data["average_ndvi"],
            "ndre": round(ndvi_data["average_ndvi"] * 0.85, 3),  # Simulated NDRE
            "evi": round(ndvi_data["average_ndvi"] * 1.1, 3),     # Simulated EVI
            "vegetation_health": ndvi_data["vegetation_health"],
        }
    
    def _get_vegetation_health(self, ndvi: float) -> str:
        """Classify vegetation health based on NDVI"""
        if ndvi >= 0.6:
            return "Excellent"
        elif ndvi >= 0.5:
            return "Good"
        elif ndvi >= 0.4:
            return "Moderate"
        else:
            return "Poor"
    
    def _get_suitability_level(self, score: float) -> str:
        """Classify land suitability"""
        if score >= 0.8:
            return "Highly Suitable"
        elif score >= 0.6:
            return "Moderately Suitable"
        elif score >= 0.4:
            return "Marginally Suitable"
        else:
            return "Not Suitable"