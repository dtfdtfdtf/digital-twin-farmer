# app/schemas/loan.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.loan import (
    LoanStatusEnum,
    LoanPurposeEnum,
    LoanTypeEnum,
    RepaymentFrequencyEnum,
)


class LoanBase(BaseModel):
    """Base loan schema"""
    farmer_id: int = Field(..., description="Farmer ID")
    enterprise_id: Optional[int] = Field(None, description="Enterprise ID")
    
    loan_type: LoanTypeEnum
    purpose: LoanPurposeEnum
    purpose_description: Optional[str] = None
    
    amount_requested: float = Field(..., ge=0, description="Amount requested")
    amount_approved: Optional[float] = Field(None, ge=0)
    amount_disbursed: Optional[float] = Field(None, ge=0)
    interest_rate: float = Field(0.0, ge=0)
    service_fee: float = Field(0.0, ge=0)
    
    term_months: int = Field(..., ge=1, description="Loan term in months")
    grace_period_days: int = Field(30, ge=0)
    repayment_frequency: RepaymentFrequencyEnum = RepaymentFrequencyEnum.SEASONAL
    
    class Config:
        from_attributes = True


class LoanCreate(LoanBase):
    """Schema for creating a new loan"""
    pass


class LoanUpdate(BaseModel):
    """Schema for updating a loan"""
    enterprise_id: Optional[int] = None
    
    loan_type: Optional[LoanTypeEnum] = None
    purpose: Optional[LoanPurposeEnum] = None
    purpose_description: Optional[str] = None
    
    amount_requested: Optional[float] = Field(None, ge=0)
    amount_approved: Optional[float] = Field(None, ge=0)
    amount_disbursed: Optional[float] = Field(None, ge=0)
    interest_rate: Optional[float] = Field(None, ge=0)
    service_fee: Optional[float] = Field(None, ge=0)
    
    term_months: Optional[int] = Field(None, ge=1)
    grace_period_days: Optional[int] = Field(None, ge=0)
    repayment_frequency: Optional[RepaymentFrequencyEnum] = None
    
    predicted_yield: Optional[float] = Field(None, ge=0)
    actual_yield: Optional[float] = Field(None, ge=0)
    predicted_repayment: Optional[float] = Field(None, ge=0)
    actual_repayment: Optional[float] = Field(None, ge=0)
    
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    risk_level: Optional[str] = Field(None, max_length=20)
    repayment_probability: Optional[float] = Field(None, ge=0, le=1)
    
    status: Optional[LoanStatusEnum] = None
    rejection_reason: Optional[str] = None
    
    reviewed_by: Optional[str] = Field(None, max_length=100)
    reviewed_at: Optional[datetime] = None
    
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    
    smart_contract_address: Optional[str] = Field(None, max_length=100)
    blockchain_transaction_hash: Optional[str] = Field(None, max_length=100)
    is_blockchain_verified: Optional[bool] = None
    
    harvest_date: Optional[datetime] = None
    harvest_amount: Optional[float] = Field(None, ge=0)
    harvest_quality: Optional[str] = Field(None, max_length=20)


class LoanResponse(LoanBase):
    """Schema for loan response"""
    id: int
    predicted_yield: Optional[float]
    actual_yield: Optional[float]
    predicted_repayment: Optional[float]
    actual_repayment: Optional[float]
    risk_score: Optional[int]
    risk_level: Optional[str]
    repayment_probability: Optional[float]
    status: LoanStatusEnum
    rejection_reason: Optional[str]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    application_date: datetime
    approval_date: Optional[datetime]
    disbursement_date: Optional[datetime]
    due_date: Optional[datetime]
    completed_date: Optional[datetime]
    smart_contract_address: Optional[str]
    blockchain_transaction_hash: Optional[str]
    is_blockchain_verified: bool
    smart_contract_deployed_at: Optional[datetime]
    harvest_date: Optional[datetime]
    harvest_amount: Optional[float]
    harvest_quality: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class LoanListResponse(BaseModel):
    """Schema for list of loans response"""
    loans: List[LoanResponse]
    total: int
    page: Optional[int] = 1
    limit: Optional[int] = 100