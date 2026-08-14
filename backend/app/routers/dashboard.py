# app/routers/dashboard.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.farmer import Farmer
from app.models.loan import Loan, LoanStatusEnum
from app.models.repayment import Repayment, RepaymentStatusEnum

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    district: Optional[str] = None,
    region: Optional[str] = None,
):
    """Get dashboard statistics"""
    
    # Base queries with filters
    farmer_query = db.query(Farmer)
    loan_query = db.query(Loan)
    
    if district:
        farmer_query = farmer_query.filter(Farmer.district == district)
        loan_query = loan_query.join(Loan.farmer).filter(Farmer.district == district)
    if region:
        farmer_query = farmer_query.filter(Farmer.region == region)
        loan_query = loan_query.join(Loan.farmer).filter(Farmer.region == region)
    
    # Farmer statistics
    total_farmers = farmer_query.count()
    verified_farmers = farmer_query.filter(Farmer.is_verified == True).count()
    pending_farmers = farmer_query.filter(Farmer.status == "pending").count()
    active_farmers = farmer_query.filter(Farmer.status == "active").count()
    
    # Loan statistics
    total_loans = loan_query.count()
    pending_loans = loan_query.filter(Loan.status == LoanStatusEnum.PENDING).count()
    approved_loans = loan_query.filter(Loan.status == LoanStatusEnum.APPROVED).count()
    disbursed_loans = loan_query.filter(Loan.status == LoanStatusEnum.DISBURSED).count()
    completed_loans = loan_query.filter(Loan.status == LoanStatusEnum.COMPLETED).count()
    defaulted_loans = loan_query.filter(Loan.status == LoanStatusEnum.DEFAULTED).count()
    
    # Total amount statistics
    total_amount_requested = loan_query.with_entities(func.sum(Loan.amount_requested)).scalar() or 0
    total_amount_disbursed = loan_query.with_entities(func.sum(Loan.amount_disbursed)).scalar() or 0
    total_amount_repaid = db.query(func.sum(Repayment.amount)).join(Loan).filter(
        Repayment.status == RepaymentStatusEnum.COMPLETED
    ).scalar() or 0
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    new_farmers_week = db.query(Farmer).filter(Farmer.created_at >= week_ago).count()
    new_loans_week = db.query(Loan).filter(Loan.created_at >= week_ago).count()
    
    return {
        "farmers": {
            "total": total_farmers,
            "verified": verified_farmers,
            "pending": pending_farmers,
            "active": active_farmers,
            "new_this_week": new_farmers_week,
        },
        "loans": {
            "total": total_loans,
            "pending": pending_loans,
            "approved": approved_loans,
            "disbursed": disbursed_loans,
            "completed": completed_loans,
            "defaulted": defaulted_loans,
            "new_this_week": new_loans_week,
        },
        "financial": {
            "total_requested": total_amount_requested,
            "total_disbursed": total_amount_disbursed,
            "total_repaid": total_amount_repaid,
            "outstanding": total_amount_disbursed - total_amount_repaid,
        },
        "filters_applied": {
            "district": district,
            "region": region,
        }
    }


@router.get("/farmers-by-district")
def get_farmers_by_district(
    db: Session = Depends(get_db),
    region: Optional[str] = None,
):
    """Get farmer distribution by district"""
    query = db.query(Farmer.district, func.count(Farmer.id)).group_by(Farmer.district)
    if region:
        query = query.filter(Farmer.region == region)
    
    results = query.all()
    return [{"district": r[0], "count": r[1]} for r in results]


@router.get("/loans-by-status")
def get_loans_by_status(
    db: Session = Depends(get_db),
    district: Optional[str] = None,
):
    """Get loan distribution by status"""
    query = db.query(Loan.status, func.count(Loan.id))
    if district:
        query = query.join(Loan.farmer).filter(Farmer.district == district)
    query = query.group_by(Loan.status)
    
    results = query.all()
    return [{"status": r[0].value if r[0] else "unknown", "count": r[1]} for r in results]


@router.get("/recent-activity")
def get_recent_activity(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
):
    """Get recent activity (farmers and loans)"""
    
    # Recent farmers
    recent_farmers = db.query(Farmer).order_by(Farmer.created_at.desc()).limit(limit).all()
    
    # Recent loans
    recent_loans = db.query(Loan).order_by(Loan.created_at.desc()).limit(limit).all()
    
    return {
        "recent_farmers": [
            {
                "id": f.id,
                "name": f.full_name,
                "district": f.district,
                "created_at": f.created_at
            }
            for f in recent_farmers
        ],
        "recent_loans": [
            {
                "id": l.id,
                "farmer_id": l.farmer_id,
                "amount": l.amount_requested,
                "status": l.status.value,
                "created_at": l.created_at
            }
            for l in recent_loans
        ]
    }