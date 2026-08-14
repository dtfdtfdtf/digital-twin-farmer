# app/utils/geo.py
import math
from typing import Tuple, Dict, Optional, List


class GeoUtils:
    """Geospatial helper functions for Malawi"""
    
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
        "Nkhotakota": {"lat": -12.9273, "lng": 34.2961},
        "Ntcheu": {"lat": -14.8200, "lng": 34.6360},
        "Chiradzulu": {"lat": -15.7000, "lng": 35.1833},
        "Mulanje": {"lat": -16.0333, "lng": 35.5000},
        "Thyolo": {"lat": -16.0667, "lng": 35.1333},
        "Chikwawa": {"lat": -16.0333, "lng": 34.8000},
        "Nsanje": {"lat": -16.9167, "lng": 35.2667},
        "Balaka": {"lat": -14.9833, "lng": 34.9500},
        "Machinga": {"lat": -15.1833, "lng": 35.3000},
        "Phalombe": {"lat": -15.8000, "lng": 35.6500},
        "Karonga": {"lat": -9.9333, "lng": 33.9333},
        "Nkhata Bay": {"lat": -11.6000, "lng": 34.3000},
        "Chitipa": {"lat": -9.7000, "lng": 33.2667},
    }
    
    # Malawi regions with districts
    REGIONS = {
        "Central": ["Lilongwe", "Kasungu", "Dedza", "Nkhotakota", "Ntcheu", "Salima"],
        "Southern": ["Blantyre", "Zomba", "Mangochi", "Chiradzulu", "Mulanje", "Thyolo", "Chikwawa", "Nsanje", "Balaka", "Machinga", "Phalombe"],
        "Northern": ["Mzuzu", "Mzimba", "Rumphi", "Karonga", "Nkhata Bay", "Chitipa"],
    }
    
    @staticmethod
    def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two GPS coordinates in kilometers.
        Using Haversine formula.
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (
            math.sin(delta_lat / 2) ** 2 +
            math.cos(lat1_rad) * math.cos(lat2_rad) *
            math.sin(delta_lng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return round(R * c, 2)
    
    @staticmethod
    def get_district_coordinates(district: str) -> Optional[Dict]:
        """Get GPS coordinates for a district"""
        return GeoUtils.DISTRICTS.get(district)
    
    @staticmethod
    def get_district_by_coordinates(lat: float, lng: float) -> Optional[str]:
        """Find the nearest district to given coordinates"""
        min_distance = float('inf')
        nearest_district = None
        
        for district, coords in GeoUtils.DISTRICTS.items():
            distance = GeoUtils.calculate_distance(
                lat, lng, coords["lat"], coords["lng"]
            )
            if distance < min_distance:
                min_distance = distance
                nearest_district = district
        
        return nearest_district
    
    @staticmethod
    def get_region(district: str) -> Optional[str]:
        """Get region for a district"""
        for region, districts in GeoUtils.REGIONS.items():
            if district in districts:
                return region
        return None
    
    @staticmethod
    def get_districts_by_region(region: str) -> List[str]:
        """Get all districts in a region"""
        return GeoUtils.REGIONS.get(region, [])
    
    @staticmethod
    def get_all_districts() -> List[str]:
        """Get list of all districts"""
        return list(GeoUtils.DISTRICTS.keys())
    
    @staticmethod
    def get_all_regions() -> List[str]:
        """Get list of all regions"""
        return list(GeoUtils.REGIONS.keys())
    
    @staticmethod
    def is_within_radius(
        lat1: float,
        lng1: float,
        lat2: float,
        lng2: float,
        radius_km: float
    ) -> bool:
        """Check if two points are within a radius"""
        distance = GeoUtils.calculate_distance(lat1, lng1, lat2, lng2)
        return distance <= radius_km
    
    @staticmethod
    def get_district_boundary(district: str) -> Optional[Dict]:
        """
        Get approximate boundary for a district (simplified).
        Returns a bounding box.
        """
        coords = GeoUtils.DISTRICTS.get(district)
        if not coords:
            return None
        
        # Approximate bounding box (0.5 degrees ~ 55km)
        return {
            "center": coords,
            "min_lat": coords["lat"] - 0.3,
            "max_lat": coords["lat"] + 0.3,
            "min_lng": coords["lng"] - 0.3,
            "max_lng": coords["lng"] + 0.3,
        }
    
    @staticmethod
    def format_coordinates(lat: float, lng: float, format: str = "dms") -> str:
        """
        Format coordinates in different formats.
        format: "dms" (degrees, minutes, seconds) or "decimal"
        """
        if format == "decimal":
            return f"{lat:.6f}, {lng:.6f}"
        
        # DMS format
        lat_d = int(abs(lat))
        lat_m = int((abs(lat) - lat_d) * 60)
        lat_s = ((abs(lat) - lat_d - lat_m/60) * 3600)
        lat_dir = "N" if lat >= 0 else "S"
        
        lng_d = int(abs(lng))
        lng_m = int((abs(lng) - lng_d) * 60)
        lng_s = ((abs(lng) - lng_d - lng_m/60) * 3600)
        lng_dir = "E" if lng >= 0 else "W"
        
        return f"{lat_d}°{lat_m:02d}'{lat_s:.1f}\" {lat_dir}, {lng_d}°{lng_m:02d}'{lng_s:.1f}\" {lng_dir}"