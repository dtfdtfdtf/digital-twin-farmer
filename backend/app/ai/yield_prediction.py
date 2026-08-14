# app/ai/yield_prediction.py
import numpy as np
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class YieldPredictor:
    """
    AI-powered yield prediction for Malawian farmers.
    Uses satellite data, weather data, and historical yields.
    """
    
    def __init__(self):
        # Base yields by crop (tons/hectare) for Malawi
        self.crop_base_yields = {
            "Maize": 3.5,
            "Soybean": 2.2,
            "Groundnuts": 1.8,
            "Tobacco": 2.0,
            "Rice": 3.0,
            "Cassava": 8.0,
            "Beans": 1.5,
            "Tomatoes": 15.0,
            "Dairy": 500,  # liters per cow per lactation
            "Goats": 120,   # kg meat per animal
            "Poultry": 2.0,  # kg per bird
        }
    
    def predict_yield(
        self,
        district: str,
        crop_type: str,
        area_hectares: float,
        ndvi: float,
        rainfall: float,
        temperature: float,
        previous_yields: Optional[List[float]] = None
    ) -> Dict:
        """
        Predict crop yield based on multiple factors.
        
        Args:
            district: District name
            crop_type: Type of crop (e.g., "Maize")
            area_hectares: Farm size in hectares
            ndvi: NDVI value (0.2-0.8)
            rainfall: Annual rainfall (mm)
            temperature: Average temperature (°C)
            previous_yields: List of historical yields
        
        Returns:
            Prediction results with confidence intervals
        """
        # Get base yield for crop
        base_yield = self.crop_base_yields.get(crop_type, 2.0)
        
        # Calculate environmental factors
        ndvi_factor = self._ndvi_factor(ndvi)
        rainfall_factor = self._rainfall_factor(rainfall, crop_type)
        temp_factor = self._temperature_factor(temperature, crop_type)
        
        # Historical trend factor
        trend_factor = self._trend_factor(previous_yields)
        
        # District adjustment
        district_factor = self._district_factor(district)
        
        # Calculate predicted yield
        predicted_yield = (
            base_yield *
            ndvi_factor *
            rainfall_factor *
            temp_factor *
            trend_factor *
            district_factor
        )
        
        # Add some randomness for realism
        variation = random.uniform(0.85, 1.15)
        predicted_yield *= variation
        
        # Ensure reasonable bounds
        predicted_yield = max(predicted_yield, base_yield * 0.3)
        predicted_yield = min(predicted_yield, base_yield * 2.0)
        
        # Calculate total production
        total_production = predicted_yield * area_hectares
        
        # Calculate confidence
        confidence = self._calculate_confidence(ndvi, rainfall, previous_yields)
        
        return {
            "district": district,
            "crop_type": crop_type,
            "area_hectares": area_hectares,
            "predicted_yield_per_hectare": round(predicted_yield, 2),
            "total_predicted_yield": round(total_production, 2),
            "unit": "tons" if crop_type not in ["Dairy"] else "liters",
            "confidence_score": round(confidence, 2),
            "confidence_level": self._confidence_level(confidence),
            "factors": {
                "ndvi_factor": round(ndvi_factor, 2),
                "rainfall_factor": round(rainfall_factor, 2),
                "temperature_factor": round(temp_factor, 2),
                "trend_factor": round(trend_factor, 2),
                "district_factor": round(district_factor, 2),
            },
            "recommendations": self._generate_recommendations(ndvi_factor, rainfall_factor, temp_factor),
        }
    
    def predict_yield_advanced(
        self,
        district: str,
        enterprise_data: Dict,
        weather_data: Dict,
        satellite_data: Dict
    ) -> Dict:
        """
        Advanced yield prediction using multiple data sources.
        """
        crop_type = enterprise_data.get("name", "Maize")
        area = enterprise_data.get("area_hectares", 1.0)
        
        ndvi = satellite_data.get("ndvi", 0.5)
        rainfall = weather_data.get("total_rainfall", 800)
        temperature = weather_data.get("average_temperature", 24)
        
        previous_yields = enterprise_data.get("previous_yields", [])
        
        return self.predict_yield(
            district=district,
            crop_type=crop_type,
            area_hectares=area,
            ndvi=ndvi,
            rainfall=rainfall,
            temperature=temperature,
            previous_yields=previous_yields
        )
    
    def _ndvi_factor(self, ndvi: float) -> float:
        """Calculate NDVI factor (0.5-1.2)"""
        if ndvi >= 0.6:
            return 1.2
        elif ndvi >= 0.5:
            return 1.0
        elif ndvi >= 0.4:
            return 0.8
        else:
            return 0.5
    
    def _rainfall_factor(self, rainfall: float, crop_type: str) -> float:
        """Calculate rainfall factor"""
        if crop_type in ["Rice", "Maize"]:
            optimal = 900
        elif crop_type in ["Tobacco", "Soybean"]:
            optimal = 800
        elif crop_type in ["Cassava", "Groundnuts"]:
            optimal = 700
        else:
            optimal = 800
        
        if rainfall >= optimal * 1.2:
            return 1.1
        elif rainfall >= optimal * 0.8:
            return 1.0
        elif rainfall >= optimal * 0.5:
            return 0.7
        else:
            return 0.4
    
    def _temperature_factor(self, temperature: float, crop_type: str) -> float:
        """Calculate temperature factor"""
        if crop_type in ["Maize", "Tobacco", "Soybean"]:
            optimal = 25
        elif crop_type in ["Cassava", "Groundnuts"]:
            optimal = 27
        elif crop_type == "Rice":
            optimal = 28
        else:
            optimal = 25
        
        diff = abs(temperature - optimal)
        
        if diff <= 2:
            return 1.0
        elif diff <= 5:
            return 0.9
        elif diff <= 8:
            return 0.7
        else:
            return 0.5
    
    def _trend_factor(self, previous_yields: Optional[List[float]]) -> float:
        """Calculate trend factor from historical yields"""
        if not previous_yields or len(previous_yields) < 2:
            return 1.0
        
        # Calculate trend
        try:
            x = np.array(range(len(previous_yields)))
            y = np.array(previous_yields)
            slope, _ = np.polyfit(x, y, 1)
            
            # Normalize slope
            avg_y = np.mean(previous_yields)
            if avg_y > 0:
                trend = 1 + (slope / avg_y)
            else:
                trend = 1.0
            
            # Clamp to reasonable range
            return max(0.8, min(1.2, trend))
        except:
            return 1.0
    
    def _district_factor(self, district: str) -> float:
        """District-specific adjustment factor"""
        factors = {
            "Lilongwe": 1.05,
            "Blantyre": 1.02,
            "Mzuzu": 0.98,
            "Zomba": 1.03,
            "Kasungu": 0.95,
            "Mzimba": 0.97,
            "Rumphi": 0.99,
            "Dedza": 1.00,
            "Salima": 0.92,
            "Mangochi": 0.93,
        }
        return factors.get(district, 1.0)
    
    def _calculate_confidence(self, ndvi: float, rainfall: float, previous_yields: Optional[List[float]]) -> float:
        """Calculate confidence score (0-1)"""
        confidence = 0.5
        
        # NDVI confidence
        if 0.3 <= ndvi <= 0.7:
            confidence += 0.15
        elif 0.2 <= ndvi <= 0.8:
            confidence += 0.08
        
        # Rainfall confidence
        if 600 <= rainfall <= 1000:
            confidence += 0.15
        elif 400 <= rainfall <= 1200:
            confidence += 0.08
        
        # Historical data confidence
        if previous_yields and len(previous_yields) >= 3:
            confidence += 0.20
        elif previous_yields and len(previous_yields) >= 1:
            confidence += 0.10
        
        return min(confidence, 1.0)
    
    def _confidence_level(self, confidence: float) -> str:
        """Classify confidence level"""
        if confidence >= 0.8:
            return "High"
        elif confidence >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _generate_recommendations(self, ndvi_factor: float, rainfall_factor: float, temp_factor: float) -> List[str]:
        """Generate recommendations based on factors"""
        recommendations = []
        
        if ndvi_factor < 0.8:
            recommendations.append("Consider improving soil health through composting or organic matter")
        
        if rainfall_factor < 0.7:
            recommendations.append("Consider drought-resistant crop varieties")
        
        if temp_factor < 0.7:
            recommendations.append("Adjust planting dates to avoid extreme temperatures")
        
        if not recommendations:
            recommendations.append("Current conditions are favorable for good yields")
        
        return recommendations