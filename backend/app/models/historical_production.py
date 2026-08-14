# app/models/historical_production.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class RecordSourceEnum(str, enum.Enum):
    MANUAL = "manual"              # Entered by officer
    SYSTEM = "system"              # Auto-recorded from harvest
    DISTRICT_AVERAGE = "district_average"  # Fallback
    SATELLITE = "satellite"        # Estimated from satellite


class EnterpriseTypeEnum(str, enum.Enum):
    CROP = "crop"
    LIVESTOCK = "livestock"


class HistoricalProduction(Base):
    __tablename__ = "historical_production"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    
    # Record details
    season = Column(String(20), nullable=False)  # e.g., "2024-2025"
    enterprise_type = Column(Enum(EnterpriseTypeEnum), nullable=False)
    crop_name = Column(String(50), nullable=True)
    livestock_type = Column(String(50), nullable=True)
    
    # Crop-specific
    area_hectares = Column(Float, nullable=True)
    bags_50kg = Column(Integer, nullable=True)  # Number of 50kg bags
    yield_tons = Column(Float, nullable=True)   # Calculated or entered
    
    # Livestock-specific
    animal_count = Column(Integer, nullable=True)
    milk_liters = Column(Float, nullable=True)   # For dairy
    eggs_count = Column(Integer, nullable=True)  # For poultry
    
    # Source
    source = Column(Enum(RecordSourceEnum), default=RecordSourceEnum.MANUAL)
    verified_by = Column(String(100), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="historical_records")
    
    def __repr__(self):
        return f"<HistoricalProduction {self.id}: Farmer {self.farmer_id} - {self.season}>"