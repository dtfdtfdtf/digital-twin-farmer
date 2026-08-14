from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class EnterpriseTypeEnum(str, enum.Enum):
    CROP = "crop"
    LIVESTOCK = "livestock"


class EnterpriseStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PLANNED = "planned"
    COMPLETED = "completed"


class Enterprise(Base):
    __tablename__ = "enterprises"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to farmer
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    
    # Enterprise details
    name = Column(String(100), nullable=False)
    type = Column(Enum(EnterpriseTypeEnum), nullable=False)
    description = Column(Text, nullable=True)
    
    # Crop-specific fields
    crop_variety = Column(String(100), nullable=True)
    planting_date = Column(DateTime, nullable=True)
    expected_harvest_date = Column(DateTime, nullable=True)
    seed_source = Column(String(200), nullable=True)
    
    # Livestock-specific fields
    animal_breed = Column(String(100), nullable=True)
    animal_count = Column(Integer, nullable=True)
    animal_age_months = Column(Integer, nullable=True)
    
    # Common fields
    area_hectares = Column(Float, nullable=True)
    estimated_yield = Column(Float, nullable=True)
    yield_unit = Column(String(20), default="tons")
    
    # Status
    status = Column(Enum(EnterpriseStatusEnum), default=EnterpriseStatusEnum.ACTIVE)
    is_primary = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="enterprises")
    # No loans relationship - we'll handle loans separately
    
    def __repr__(self):
        return f"<Enterprise {self.id}: {self.name} ({self.type.value}) - Farmer {self.farmer_id}>"