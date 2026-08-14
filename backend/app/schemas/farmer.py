# app/schemas/farmer.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.farmer import GenderEnum, FarmerStatusEnum, VerificationLevelEnum


class FarmerBase(BaseModel):
    """Base farmer schema"""
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    middle_name: Optional[str] = Field(None, max_length=100, description="Middle name")
    
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number")
    alternative_phone: Optional[str] = Field(None, max_length=20, description="Alternative phone")
    
    national_id: str = Field(..., min_length=5, max_length=20, description="National ID")
    
    gender: Optional[GenderEnum] = Field(None, description="Gender")
    date_of_birth: Optional[datetime] = Field(None, description="Date of birth")
    village: str = Field(..., min_length=1, max_length=100, description="Village")
    district: str = Field(..., min_length=1, max_length=50, description="District")
    region: str = Field(..., min_length=1, max_length=50, description="Region")
    traditional_authority: Optional[str] = Field(None, max_length=100, description="Traditional Authority")
    
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    farm_area_hectares: Optional[float] = Field(None, ge=0, description="Farm area in hectares")
    
    class Config:
        from_attributes = True


class FarmerCreate(FarmerBase):
    """Schema for creating a new farmer"""
    pass


class FarmerUpdate(BaseModel):
    """Schema for updating a farmer"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    alternative_phone: Optional[str] = Field(None, max_length=20)
    
    national_id: Optional[str] = Field(None, min_length=5, max_length=20)
    
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[datetime] = None
    village: Optional[str] = Field(None, min_length=1, max_length=100)
    district: Optional[str] = Field(None, min_length=1, max_length=50)
    region: Optional[str] = Field(None, min_length=1, max_length=50)
    traditional_authority: Optional[str] = Field(None, max_length=100)
    
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    farm_area_hectares: Optional[float] = Field(None, ge=0)
    
    status: Optional[FarmerStatusEnum] = None
    is_verified: Optional[bool] = None
    credit_score: Optional[int] = Field(None, ge=0, le=1000)
    has_blockchain_identity: Optional[bool] = None
    
    # Verification fields
    is_gps_verified: Optional[bool] = None
    is_satellite_verified: Optional[bool] = None
    is_officer_verified: Optional[bool] = None
    is_community_verified: Optional[bool] = None
    has_historical_records: Optional[bool] = None
    officer_name: Optional[str] = None
    community_verifier: Optional[str] = None
    verification_notes: Optional[str] = None


class FarmerResponse(FarmerBase):
    """Schema for farmer response"""
    id: int
    status: FarmerStatusEnum
    is_verified: bool
    verification_date: Optional[datetime]
    credit_score: int
    has_blockchain_identity: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    
    # Verification fields
    verification_score: int
    verification_level: VerificationLevelEnum
    is_gps_verified: bool
    is_satellite_verified: bool
    is_officer_verified: bool
    is_community_verified: bool
    has_historical_records: bool
    gps_verified_at: Optional[datetime]
    satellite_verified_at: Optional[datetime]
    officer_verified_at: Optional[datetime]
    officer_name: Optional[str]
    community_verifier: Optional[str]
    community_verified_at: Optional[datetime]
    ai_consistency_pass: bool
    ai_flags: Optional[str]
    verification_notes: Optional[str]
    
    class Config:
        from_attributes = True


class FarmerListResponse(BaseModel):
    """Schema for list of farmers response"""
    farmers: List[FarmerResponse]
    total: int
    page: Optional[int] = 1
    limit: Optional[int] = 100