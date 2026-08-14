# app/schemas/enterprise.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.enterprise import EnterpriseTypeEnum, EnterpriseStatusEnum


class EnterpriseBase(BaseModel):
    """Base enterprise schema"""
    farmer_id: int = Field(..., description="Farmer ID")
    
    name: str = Field(..., min_length=1, max_length=100, description="Enterprise name (e.g., Maize, Dairy)")
    type: EnterpriseTypeEnum = Field(..., description="CROP or LIVESTOCK")
    description: Optional[str] = Field(None, description="Description")
    
    # Crop fields
    crop_variety: Optional[str] = Field(None, max_length=100)
    planting_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    seed_source: Optional[str] = Field(None, max_length=200)
    
    # Livestock fields
    animal_breed: Optional[str] = Field(None, max_length=100)
    animal_count: Optional[int] = Field(None, ge=0)
    animal_age_months: Optional[int] = Field(None, ge=0)
    
    # Common fields
    area_hectares: Optional[float] = Field(None, ge=0)
    estimated_yield: Optional[float] = Field(None, ge=0)
    yield_unit: Optional[str] = Field("tons", max_length=20)
    
    is_primary: bool = Field(False, description="Is this the primary enterprise")
    
    class Config:
        from_attributes = True


class EnterpriseCreate(EnterpriseBase):
    """Schema for creating a new enterprise"""
    pass


class EnterpriseUpdate(BaseModel):
    """Schema for updating an enterprise"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[EnterpriseTypeEnum] = None
    description: Optional[str] = None
    
    crop_variety: Optional[str] = Field(None, max_length=100)
    planting_date: Optional[datetime] = None
    expected_harvest_date: Optional[datetime] = None
    seed_source: Optional[str] = Field(None, max_length=200)
    
    animal_breed: Optional[str] = Field(None, max_length=100)
    animal_count: Optional[int] = Field(None, ge=0)
    animal_age_months: Optional[int] = Field(None, ge=0)
    
    area_hectares: Optional[float] = Field(None, ge=0)
    estimated_yield: Optional[float] = Field(None, ge=0)
    yield_unit: Optional[str] = Field(None, max_length=20)
    
    status: Optional[EnterpriseStatusEnum] = None
    is_primary: Optional[bool] = None


class EnterpriseResponse(EnterpriseBase):
    """Schema for enterprise response"""
    id: int
    status: EnterpriseStatusEnum
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class EnterpriseListResponse(BaseModel):
    """Schema for list of enterprises response"""
    enterprises: List[EnterpriseResponse]
    total: int
    farmer_id: Optional[int] = None