# app/routers/loans.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.loan import Loan, LoanStatusEnum
from app.models.farmer import Farmer
from app.schemas.loan import (
    LoanCreate,
    LoanUpdate,
    LoanResponse,
    LoanListResponse,
)
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """Create a new loan application"""
    # Check if farmer exists
    farmer = db.query(Farmer).filter(Farmer.id == loan.farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    # Check if farmer is eligible
    if not farmer.is_eligible_for_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farmer is not eligible for a loan at this time"
        )
    
    # Create loan
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


@router.get("/", response_model=LoanListResponse)
def get_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    farmer_id: Optional[int] = None,
    status: Optional[LoanStatusEnum] = None,
    db: Session = Depends(get_db)
):
    """Get all loans with optional filters"""
    query = db.query(Loan)
    
    if farmer_id:
        query = query.filter(Loan.farmer_id == farmer_id)
    if status:
        query = query.filter(Loan.status == status)
    
    total = query.count()
    loans = query.offset(skip).limit(limit).all()
    
    return LoanListResponse(
        loans=loans,
        total=total,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit
    )


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """Get a specific loan by ID"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    loan_update: LoanUpdate,
    db: Session = Depends(get_db)
):
    """Update a loan"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    update_data = loan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(loan, field, value)
    
    loan.updated_at = datetime.now()
    db.commit()
    db.refresh(loan)
    return loan


@router.post("/{loan_id}/approve", response_model=LoanResponse)
def approve_loan(
    loan_id: int,
    approved_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Approve a loan"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    if loan.status != LoanStatusEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Loan cannot be approved. Current status: {loan.status.value}"
        )
    
    loan.status = LoanStatusEnum.APPROVED
    loan.approval_date = datetime.now()
    loan.reviewed_at = datetime.now()
    if approved_amount:
        loan.amount_approved = approved_amount
    
    loan.updated_at = datetime.now()
    db.commit()
    db.refresh(loan)
    return loan


@router.post("/{loan_id}/disburse", response_model=LoanResponse)
def disburse_loan(loan_id: int, db: Session = Depends(get_db)):
    """Disburse approved loan"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    if loan.status != LoanStatusEnum.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Loan cannot be disbursed. Current status: {loan.status.value}"
        )
    
    loan.status = LoanStatusEnum.DISBURSED
    loan.disbursement_date = datetime.now()
    loan.amount_disbursed = loan.amount_approved or loan.amount_requested
    loan.updated_at = datetime.now()
    
    db.commit()
    db.refresh(loan)
    return loan


@router.post("/{loan_id}/reject", response_model=LoanResponse)
def reject_loan(
    loan_id: int,
    reason: str,
    db: Session = Depends(get_db)
):
    """Reject a loan application"""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    if loan.status not in [LoanStatusEnum.PENDING, LoanStatusEnum.UNDER_REVIEW]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Loan cannot be rejected. Current status: {loan.status.value}"
        )
    
    loan.status = LoanStatusEnum.REJECTED
    loan.rejection_reason = reason
    loan.reviewed_at = datetime.now()
    loan.updated_at = datetime.now()
    
    db.commit()
    db.refresh(loan)
    return loan