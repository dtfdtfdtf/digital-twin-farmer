from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime  # ← ADDED AT TOP


class RepaymentMethodEnum(str, enum.Enum):
    MOBILE_MONEY = "mobile_money"       # TNM Mpamba, Airtel Money
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    HARVEST_DEDUCTION = "harvest_deduction"  # Automatic deduction at harvest
    SMART_CONTRACT = "smart_contract"        # Blockchain automatic settlement


class RepaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


class RepaymentSourceEnum(str, enum.Enum):
    MANUAL = "manual"                # Farmer or officer entered manually
    HARVEST_SETTLEMENT = "harvest_settlement"  # Automatic from harvest
    SMART_CONTRACT = "smart_contract"          # Blockchain triggered
    MOBILE_MONEY_WEBHOOK = "mobile_money_webhook"  # API callback from mobile money


class Repayment(Base):
    __tablename__ = "repayments"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    
    # Repayment details
    amount = Column(Float, nullable=False)
    amount_principal = Column(Float, nullable=True)  # Portion going to principal
    amount_interest = Column(Float, nullable=True)   # Portion going to interest
    amount_fees = Column(Float, nullable=True)       # Portion going to fees
    
    # Method and source
    method = Column(Enum(RepaymentMethodEnum), nullable=False)
    source = Column(Enum(RepaymentSourceEnum), default=RepaymentSourceEnum.MANUAL)
    reference_number = Column(String(100), nullable=True)  # Mobile money reference, bank ref, etc.
    
    # Status
    status = Column(Enum(RepaymentStatusEnum), default=RepaymentStatusEnum.PENDING)
    failure_reason = Column(Text, nullable=True)
    
    # Dates
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Blockchain
    transaction_hash = Column(String(100), nullable=True)
    block_verified = Column(Boolean, default=False)
    block_verified_at = Column(DateTime, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    recorded_by = Column(String(100), nullable=True)  # Officer who recorded this
    
    # Relationships
    loan = relationship("Loan", back_populates="repayments")
    farmer = relationship("Farmer", back_populates="repayments")
    
    def __repr__(self):
        return f"<Repayment {self.id}: Loan {self.loan_id} - {self.amount} ({self.status.value})>"
    
    @property
    def is_late(self):
        """Check if repayment is late"""
        if self.due_date and self.status not in [RepaymentStatusEnum.COMPLETED, RepaymentStatusEnum.REVERSED]:
            return datetime.now() > self.due_date  # ← REMOVED import
        return False
    
    @property
    def days_late(self):
        """Calculate number of days late"""
        if self.is_late and self.due_date:
            return (datetime.now() - self.due_date).days  # ← REMOVED import
        return 0
    
    @property
    def is_successful(self):
        """Check if repayment was successful"""
        return self.status == RepaymentStatusEnum.COMPLETED
    
    @property
    def is_blockchain_verified(self):
        """Check if repayment is verified on blockchain"""
        return self.block_verified and self.transaction_hash is not None
    
    @property
    def repayment_type(self):
        """Determine if this is principal, interest, or full payment"""
        if self.amount_principal and self.amount_interest and self.amount_fees:
            if self.amount_principal == self.amount and self.amount_interest == 0:
                return "principal_only"
            elif self.amount_interest > 0 and self.amount_principal == 0:
                return "interest_only"
            else:
                return "full_payment"
        return "unknown"