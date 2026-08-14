# app/services/loan_service.py
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from app.models.loan import Loan, LoanStatusEnum, LoanTypeEnum
from app.models.farmer import Farmer
from app.models.repayment import Repayment, RepaymentStatusEnum
from app.schemas.loan import LoanCreate, LoanUpdate
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class LoanService:
    """Service for loan-related business logic"""
    
    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
        """Create a new loan application"""
        # Check if farmer exists
        farmer = db.query(Farmer).filter(Farmer.id == loan_data.farmer_id).first()
        if not farmer:
            raise ValueError("Farmer not found")
        
        # Check if farmer is eligible
        if not farmer.is_eligible_for_loan:
            raise ValueError("Farmer is not eligible for a loan at this time")
        
        # Create loan
        db_loan = Loan(**loan_data.model_dump())
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        
        logger.info(f"Loan created: {db_loan.id} - Farmer {db_loan.farmer_id}")
        return db_loan
    
    @staticmethod
    def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
        """Get loan by ID"""
        return db.query(Loan).filter(Loan.id == loan_id).first()
    
    @staticmethod
    def get_loans(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        farmer_id: Optional[int] = None,
        status: Optional[LoanStatusEnum] = None,
        loan_type: Optional[LoanTypeEnum] = None
    ) -> Dict:
        """Get loans with filters"""
        query = db.query(Loan)
        
        if farmer_id:
            query = query.filter(Loan.farmer_id == farmer_id)
        if status:
            query = query.filter(Loan.status == status)
        if loan_type:
            query = query.filter(Loan.loan_type == loan_type)
        
        total = query.count()
        loans = query.offset(skip).limit(limit).all()
        
        return {
            "loans": loans,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    @staticmethod
    def update_loan(db: Session, loan_id: int, loan_data: LoanUpdate) -> Optional[Loan]:
        """Update loan details"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        update_data = loan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(loan, field, value)
        
        loan.updated_at = datetime.now()
        db.commit()
        db.refresh(loan)
        
        logger.info(f"Loan updated: {loan.id}")
        return loan
    
    @staticmethod
    def approve_loan(db: Session, loan_id: int, approved_amount: Optional[float] = None) -> Optional[Loan]:
        """Approve a loan"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        if loan.status != LoanStatusEnum.PENDING:
            raise ValueError(f"Loan cannot be approved. Current status: {loan.status.value}")
        
        loan.status = LoanStatusEnum.APPROVED
        loan.approval_date = datetime.now()
        loan.reviewed_at = datetime.now()
        if approved_amount:
            loan.amount_approved = approved_amount
        
        loan.updated_at = datetime.now()
        db.commit()
        db.refresh(loan)
        
        logger.info(f"Loan approved: {loan.id}")
        return loan
    
    @staticmethod
    def disburse_loan(db: Session, loan_id: int) -> Optional[Loan]:
        """Disburse an approved loan"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        if loan.status != LoanStatusEnum.APPROVED:
            raise ValueError(f"Loan cannot be disbursed. Current status: {loan.status.value}")
        
        loan.status = LoanStatusEnum.DISBURSED
        loan.disbursement_date = datetime.now()
        loan.amount_disbursed = loan.amount_approved or loan.amount_requested
        
        # Set due date based on loan term
        if loan.term_months:
            loan.due_date = datetime.now() + timedelta(days=loan.term_months * 30)
        
        loan.updated_at = datetime.now()
        db.commit()
        db.refresh(loan)
        
        logger.info(f"Loan disbursed: {loan.id}")
        return loan
    
    @staticmethod
    def reject_loan(db: Session, loan_id: int, reason: str) -> Optional[Loan]:
        """Reject a loan application"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        if loan.status not in [LoanStatusEnum.PENDING, LoanStatusEnum.UNDER_REVIEW]:
            raise ValueError(f"Loan cannot be rejected. Current status: {loan.status.value}")
        
        loan.status = LoanStatusEnum.REJECTED
        loan.rejection_reason = reason
        loan.reviewed_at = datetime.now()
        loan.updated_at = datetime.now()
        db.commit()
        db.refresh(loan)
        
        logger.info(f"Loan rejected: {loan.id}")
        return loan
    
    @staticmethod
    def complete_loan(db: Session, loan_id: int) -> Optional[Loan]:
        """Mark loan as completed"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        if loan.status not in [LoanStatusEnum.ACTIVE, LoanStatusEnum.DISBURSED]:
            raise ValueError(f"Loan cannot be completed. Current status: {loan.status.value}")
        
        loan.status = LoanStatusEnum.COMPLETED
        loan.completed_date = datetime.now()
        loan.updated_at = datetime.now()
        db.commit()
        db.refresh(loan)
        
        logger.info(f"Loan completed: {loan.id}")
        return loan
    
    @staticmethod
    def get_loan_repayments(db: Session, loan_id: int) -> List[Repayment]:
        """Get all repayments for a loan"""
        return db.query(Repayment).filter(Repayment.loan_id == loan_id).all()
    
    @staticmethod
    def get_loan_summary(db: Session, loan_id: int) -> Optional[Dict]:
        """Get comprehensive loan summary"""
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        
        repayments = db.query(Repayment).filter(Repayment.loan_id == loan_id).all()
        
        total_repayment = sum(r.amount for r in repayments if r.status == RepaymentStatusEnum.COMPLETED)
        total_pending = sum(r.amount for r in repayments if r.status == RepaymentStatusEnum.PENDING)
        
        return {
            "loan": loan,
            "repayments": repayments,
            "total_repayment": total_repayment,
            "total_pending": total_pending,
            "remaining_balance": (loan.amount_disbursed or 0) - total_repayment,
            "repayment_progress": loan.repayment_progress,
            "is_overdue": loan.is_overdue,
            "repayment_count": len(repayments)
        }
    
    @staticmethod
    def get_loan_stats(db: Session) -> Dict:
        """Get loan statistics"""
        total = db.query(Loan).count()
        pending = db.query(Loan).filter(Loan.status == LoanStatusEnum.PENDING).count()
        approved = db.query(Loan).filter(Loan.status == LoanStatusEnum.APPROVED).count()
        disbursed = db.query(Loan).filter(Loan.status == LoanStatusEnum.DISBURSED).count()
        completed = db.query(Loan).filter(Loan.status == LoanStatusEnum.COMPLETED).count()
        defaulted = db.query(Loan).filter(Loan.status == LoanStatusEnum.DEFAULTED).count()
        
        total_amount = db.query(Loan.amount_requested).all()
        total_requested = sum(a[0] for a in total_amount if a[0])
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "disbursed": disbursed,
            "completed": completed,
            "defaulted": defaulted,
            "total_requested": total_requested,
            "approval_rate": round((approved / (pending + approved)) * 100, 1) if (pending + approved) > 0 else 0
        }