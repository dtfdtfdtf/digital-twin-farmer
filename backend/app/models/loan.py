from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime


class LoanStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    ACTIVE = "active"
    DEFAULTED = "defaulted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LoanPurposeEnum(str, enum.Enum):
    SEEDS = "seeds"
    FERTILIZER = "fertilizer"
    PESTICIDES = "pesticides"
    IRRIGATION = "irrigation"
    EQUIPMENT = "equipment"
    LABOR = "labor"
    TRANSPORT = "transport"
    LIVESTOCK_FEED = "livestock_feed"
    ANIMAL_HEALTH = "animal_health"
    OTHER = "other"


class LoanTypeEnum(str, enum.Enum):
    INPUT_FINANCING = "input_financing"
    HARVEST_FINANCING = "harvest_financing"
    EQUIPMENT_FINANCING = "equipment_financing"
    LIVESTOCK_FINANCING = "livestock_financing"
    EMERGENCY = "emergency"


class RepaymentFrequencyEnum(str, enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEASONAL = "seasonal"
    HARVEST = "harvest"


class Loan(Base):
    __tablename__ = "loans"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    # enterprise_id removed - we'll use farmer to track enterprises
    
    # Loan details
    loan_type = Column(Enum(LoanTypeEnum), nullable=False)
    purpose = Column(Enum(LoanPurposeEnum), nullable=False)
    purpose_description = Column(Text, nullable=True)
    
    # Amounts
    amount_requested = Column(Float, nullable=False)
    amount_approved = Column(Float, nullable=True)
    amount_disbursed = Column(Float, nullable=True)
    interest_rate = Column(Float, default=0.0)
    service_fee = Column(Float, default=0.0)
    
    # Loan terms
    term_months = Column(Integer, nullable=False)
    grace_period_days = Column(Integer, default=30)
    repayment_frequency = Column(Enum(RepaymentFrequencyEnum), default=RepaymentFrequencyEnum.SEASONAL)
    
    # AI predictions
    predicted_yield = Column(Float, nullable=True)
    actual_yield = Column(Float, nullable=True)
    predicted_repayment = Column(Float, nullable=True)
    actual_repayment = Column(Float, nullable=True)
    
    # Risk assessment
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String(20), nullable=True)
    repayment_probability = Column(Float, nullable=True)
    
    # Status
    status = Column(Enum(LoanStatusEnum), default=LoanStatusEnum.DRAFT)
    rejection_reason = Column(Text, nullable=True)
    
    # Officer/Reviewer
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Dates
    application_date = Column(DateTime(timezone=True), server_default=func.now())
    approval_date = Column(DateTime, nullable=True)
    disbursement_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    
    # Blockchain
    smart_contract_address = Column(String(100), nullable=True)
    blockchain_transaction_hash = Column(String(100), nullable=True)
    is_blockchain_verified = Column(Boolean, default=False)
    smart_contract_deployed_at = Column(DateTime, nullable=True)
    
    # Harvest tracking
    harvest_date = Column(DateTime, nullable=True)
    harvest_amount = Column(Float, nullable=True)
    harvest_quality = Column(String(20), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="loans")
    repayments = relationship("Repayment", back_populates="loan")
    # enterprise relationship removed
    
    def __repr__(self):
        return f"<Loan {self.id}: Farmer {self.farmer_id} - {self.status.value}>"
    
    @property
    def is_overdue(self):
        if self.due_date and self.status not in [LoanStatusEnum.COMPLETED, LoanStatusEnum.DEFAULTED, LoanStatusEnum.CANCELLED]:
            return datetime.now() > self.due_date
        return False
    
    @property
    def repayment_progress(self):
        if self.amount_disbursed and self.actual_repayment:
            return min((self.actual_repayment / self.amount_disbursed) * 100, 100)
        return 0.0
    
    @property
    def remaining_balance(self):
        if self.amount_disbursed and self.actual_repayment:
            return max(self.amount_disbursed - self.actual_repayment, 0)
        return self.amount_disbursed or 0
    
    @property
    def is_ready_for_harvest_settlement(self):
        return (
            self.status == LoanStatusEnum.ACTIVE and
            self.harvest_date is None and
            self.due_date and
            datetime.now() >= self.due_date
        )