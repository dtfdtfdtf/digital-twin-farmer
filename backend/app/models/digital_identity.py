from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class DigitalIdentity(Base):
    __tablename__ = "digital_identities"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to farmer (one-to-one relationship)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), unique=True, nullable=False)
    
    # Blockchain identity
    wallet_address = Column(String(100), unique=True, nullable=False)
    token_id = Column(String(100), unique=True, nullable=False)
    blockchain = Column(String(20), default="celo")  # celo, ethereum, polygon, etc.
    
    # Biometric data (stored as hashes for security)
    fingerprint_hash = Column(String(255), nullable=True)
    facial_hash = Column(String(255), nullable=True)
    
    # Identity verification
    is_verified = Column(Boolean, default=False)
    verification_hash = Column(String(255), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    # Token metadata
    token_uri = Column(String(255), nullable=True)  # IPFS or metadata URL
    metadata_hash = Column(String(100), nullable=True)
    
    # Chain transaction details
    transaction_hash = Column(String(100), nullable=True)
    block_number = Column(Integer, nullable=True)
    
    # QR code data (for easy scanning)
    qr_code_data = Column(String(255), nullable=True)
    
    # Activity tracking
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="digital_identity")
    
    def __repr__(self):
        return f"<DigitalIdentity {self.id}: {self.token_id} - Farmer {self.farmer_id}>"
    
    @property
    def is_active(self):
        """Check if the digital identity is active and verified"""
        return self.is_verified and self.farmer.is_verified if self.farmer else False
    
    @property
    def short_address(self):
        """Return shortened wallet address for display"""
        if self.wallet_address and len(self.wallet_address) > 10:
            return f"{self.wallet_address[:6]}...{self.wallet_address[-4:]}"
        return self.wallet_address