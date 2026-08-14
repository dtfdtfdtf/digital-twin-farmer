from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class FarmerStatusEnum(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    FLAGGED = "flagged"  # For AI inconsistency flags


class VerificationLevelEnum(str, enum.Enum):
    UNVERIFIED = "unverified"
    LIMITED = "limited"      # 50-69%
    PARTIAL = "partial"      # 70-89%
    FULL = "full"            # 90-100%


class Farmer(Base):
    __tablename__ = "farmers"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    
    # Contact information
    phone = Column(String(20), nullable=False)
    alternative_phone = Column(String(20), nullable=True)
    
    # Identification - National ID only (for scanning)
    national_id = Column(String(20), unique=True, nullable=False)
    
    # Demographics
    gender = Column(Enum(GenderEnum), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    village = Column(String(100), nullable=False)
    district = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    traditional_authority = Column(String(100), nullable=True)
    
    # Farm location (GPS)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    farm_area_hectares = Column(Float, nullable=True)
    
    # Status
    status = Column(Enum(FarmerStatusEnum), default=FarmerStatusEnum.PENDING)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    
    # Financial
    credit_score = Column(Integer, default=0)  # 0-1000 scale
    has_blockchain_identity = Column(Boolean, default=False)
    
    # === VERIFICATION FIELDS ===
    
    # Verification Score (0-100%)
    verification_score = Column(Integer, default=0)
    verification_level = Column(Enum(VerificationLevelEnum), default=VerificationLevelEnum.UNVERIFIED)
    
    # Layer-specific verification flags
    is_gps_verified = Column(Boolean, default=False)
    is_satellite_verified = Column(Boolean, default=False)
    is_officer_verified = Column(Boolean, default=False)
    is_community_verified = Column(Boolean, default=False)
    has_historical_records = Column(Boolean, default=False)
    
    # Verification details
    gps_verified_at = Column(DateTime, nullable=True)
    satellite_verified_at = Column(DateTime, nullable=True)
    officer_verified_at = Column(DateTime, nullable=True)
    officer_name = Column(String(100), nullable=True)
    community_verifier = Column(String(100), nullable=True)
    community_verified_at = Column(DateTime, nullable=True)
    
    # AI flags
    ai_consistency_pass = Column(Boolean, default=True)
    ai_flags = Column(Text, nullable=True)  # JSON string of flags
    
    # Verification notes
    verification_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    digital_identity = relationship("DigitalIdentity", back_populates="farmer", uselist=False)
    loans = relationship("Loan", back_populates="farmer")
    repayments = relationship("Repayment", back_populates="farmer")
    enterprises = relationship("Enterprise", back_populates="farmer")
    historical_records = relationship("HistoricalProduction", back_populates="farmer")
    
    def __repr__(self):
        return f"<Farmer {self.id}: {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_eligible_for_loan(self):
        """Check if farmer meets minimum requirements for a loan"""
        return (
            self.is_verified and
            self.status == FarmerStatusEnum.ACTIVE and
            self.has_blockchain_identity and
            self.credit_score >= 300 and
            self.verification_score >= 70  # Must be at least 70% verified
        )
    
    @property
    def verification_status_text(self):
        """Get human-readable verification status"""
        if self.verification_score >= 90:
            return "Fully Verified ✅"
        elif self.verification_score >= 70:
            return "Partially Verified"
        elif self.verification_score >= 50:
            return "Limited Verification"
        else:
            return "Unverified"