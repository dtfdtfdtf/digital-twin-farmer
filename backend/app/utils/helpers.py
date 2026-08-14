# app/utils/helpers.py
import random
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import re


class Helpers:
    """General helper functions"""
    
    @staticmethod
    def generate_random_id(prefix: str = "", length: int = 8) -> str:
        """Generate a random ID with optional prefix"""
        chars = string.ascii_uppercase + string.digits
        random_id = ''.join(random.choices(chars, k=length))
        return f"{prefix}{random_id}" if prefix else random_id
    
    @staticmethod
    def generate_reference_number(prefix: str = "DTF", length: int = 10) -> str:
        """Generate a reference number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_part = ''.join(random.choices(string.digits, k=length))
        return f"{prefix}-{timestamp}-{random_part}"
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a one-time password"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def hash_string(text: str) -> str:
        """Hash a string using SHA256"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to a maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_currency(amount: float, currency: str = "MWK") -> str:
        """Format currency with proper separators"""
        if currency == "MWK":
            return f"MWK {amount:,.2f}"
        return f"{currency} {amount:,.2f}"
    
    @staticmethod
    def format_date(date: datetime, format: str = "%Y-%m-%d %H:%M") -> str:
        """Format a datetime object"""
        if not date:
            return ""
        return date.strftime(format)
    
    @staticmethod
    def parse_date(date_string: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
        """Parse a date string to datetime object"""
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            return None
    
    @staticmethod
    def calculate_age(birth_date: datetime) -> int:
        """Calculate age from birth date"""
        if not birth_date:
            return 0
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    @staticmethod
    def calculate_days_between(start: datetime, end: Optional[datetime] = None) -> int:
        """Calculate days between two dates"""
        if not end:
            end = datetime.now()
        if not start:
            return 0
        return (end - start).days
    
    @staticmethod
    def safe_json_loads(json_string: str) -> Optional[Dict]:
        """Safely parse JSON string"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def safe_json_dumps(data: Any, indent: int = 2) -> str:
        """Safely convert to JSON string"""
        try:
            return json.dumps(data, indent=indent, default=str)
        except TypeError:
            return str(data)
    
    @staticmethod
    def clean_phone_number(phone: str) -> str:
        """Clean and format phone number"""
        # Remove non-numeric characters
        cleaned = re.sub(r'[^0-9]', '', phone)
        # Ensure it starts with 0 or 265
        if not cleaned.startswith('265') and not cleaned.startswith('0'):
            cleaned = '0' + cleaned
        return cleaned
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_national_id(national_id: str) -> bool:
        """Validate Malawian National ID format"""
        # Simple validation: alphanumeric, 5-20 characters
        return bool(re.match(r'^[A-Z0-9]{5,20}$', national_id.upper()))
    
    @staticmethod
    def snake_to_title(text: str) -> str:
        """Convert snake_case to Title Case"""
        return ' '.join(word.capitalize() for word in text.split('_'))
    
    @staticmethod
    def title_to_snake(text: str) -> str:
        """Convert Title Case to snake_case"""
        return '_'.join(word.lower() for word in text.split())
    
    @staticmethod
    def chunk_list(lst: List, chunk_size: int) -> List[List]:
        """Split a list into chunks"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def get_status_label(status: str) -> str:
        """Get human-readable status label"""
        status_map = {
            "pending": "Pending",
            "approved": "Approved",
            "rejected": "Rejected",
            "active": "Active",
            "inactive": "Inactive",
            "completed": "Completed",
            "failed": "Failed",
            "verified": "Verified",
            "pending_review": "Pending Review",
            "under_review": "Under Review",
            "disbursed": "Disbursed",
            "defaulted": "Defaulted",
            "cancelled": "Cancelled",
        }
        return status_map.get(status.lower(), status.title())