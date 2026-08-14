# app/utils/validators.py
import re
from typing import Optional, Tuple, List
from datetime import datetime


class Validators:
    """Validation helper functions for Malawian data"""
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate Malawian phone number.
        Returns: (is_valid, formatted_number_or_error)
        """
        # Remove whitespace and special characters
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it matches Malawi format
        # 0888xxxxxx or 0999xxxxxx or +265888xxxxxx
        pattern = r'^(?:\+?265|0)(88|99|98|97)\d{7}$'
        
        if re.match(pattern, cleaned):
            # Format nicely
            if cleaned.startswith('0'):
                formatted = cleaned[:4] + ' ' + cleaned[4:7] + ' ' + cleaned[7:]
            else:
                formatted = '+' + cleaned[:3] + ' ' + cleaned[3:6] + ' ' + cleaned[6:9] + ' ' + cleaned[9:]
            return True, formatted
        return False, "Invalid phone number format"
    
    @staticmethod
    def validate_national_id(national_id: str) -> bool:
        """Validate Malawi National ID format"""
        # Malawi National ID: alphanumeric, 5-20 characters
        pattern = r'^[A-Z0-9]{5,20}$'
        return bool(re.match(pattern, national_id.upper()))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, List[str]]:
        """
        Validate password strength.
        Returns: (is_valid, list_of_issues)
        """
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            issues.append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            issues.append("Password must contain at least one lowercase letter")
        if not re.search(r'\d', password):
            issues.append("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Password must contain at least one special character")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, Optional[datetime]]:
        """Validate date format and return datetime object"""
        try:
            parsed = datetime.strptime(date_str, format)
            return True, parsed
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_gps(latitude: float, longitude: float) -> bool:
        """Validate GPS coordinates"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
    
    @staticmethod
    def validate_amount(amount: float, min_amount: float = 0) -> bool:
        """Validate amount is positive"""
        return isinstance(amount, (int, float)) and amount >= min_amount
    
    @staticmethod
    def validate_enum_value(value: str, valid_values: List[str]) -> bool:
        """Validate value is in enum list"""
        return value in valid_values
    
    @staticmethod
    def validate_length(text: str, min_length: int = 1, max_length: int = 255) -> bool:
        """Validate text length"""
        return min_length <= len(text) <= max_length
    
    @staticmethod
    def validate_village_name(village: str) -> bool:
        """Validate village name for Malawi"""
        # Village names: letters, spaces, hyphens, apostrophes
        pattern = r'^[A-Za-z\s\-\'\.]+$'
        return bool(re.match(pattern, village))
    
    @staticmethod
    def validate_district(district: str, valid_districts: List[str]) -> bool:
        """Validate district name"""
        return district in valid_districts
    
    @staticmethod
    def validate_crop_name(crop: str) -> bool:
        """Validate crop name"""
        # Crop names: letters, spaces, hyphens
        pattern = r'^[A-Za-z\s\-]+$'
        return bool(re.match(pattern, crop))
    
    @staticmethod
    def validate_phone_network(phone: str) -> str:
        """
        Identify mobile network for Malawi.
        Returns: "TNM", "Airtel", "Unknown"
        """
        cleaned = re.sub(r'[^0-9]', '', phone)
        if cleaned.startswith('088') or cleaned.startswith('288') or cleaned.startswith('98'):
            return "TNM"
        elif cleaned.startswith('099') or cleaned.startswith('999') or cleaned.startswith('97'):
            return "Airtel"
        else:
            return "Unknown"
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate person name"""
        # Names: letters, spaces, hyphens, apostrophes
        pattern = r'^[A-Za-z\s\-\'\.]+$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def validate_positive_number(value: float) -> bool:
        """Validate positive number"""
        return isinstance(value, (int, float)) and value > 0
    
    @staticmethod
    def validate_range(value: float, min_val: float, max_val: float) -> bool:
        """Validate value is within range"""
        return min_val <= value <= max_val