# app/routers/ai.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.farmer import Farmer
from app.models.loan import Loan

router = APIRouter()


@router.get("/predict-yield/{farmer_id}")
def predict_yield(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    """Predict crop yield for a farmer"""
    # Placeholder - will be implemented in Phase 5
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return {
        "farmer_id": farmer_id,
        "predicted_yield": 4.5,  # Placeholder
        "confidence_score": 0.85,
        "season": "2026",
        "message": "AI prediction module coming soon!"
    }


@router.get("/credit-score/{farmer_id}")
def get_credit_score(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    """Get credit score for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return {
        "farmer_id": farmer_id,
        "credit_score": farmer.credit_score or 0,
        "risk_level": "LOW" if farmer.credit_score >= 700 else "MEDIUM" if farmer.credit_score >= 400 else "HIGH",
        "message": "AI credit scoring coming soon!"
    }


@router.get("/loan-recommendation/{farmer_id}")
def get_loan_recommendation(
    farmer_id: int,
    db: Session = Depends(get_db)
):
    """Get loan recommendation for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return {
        "farmer_id": farmer_id,
        "recommended_loan_amount": 1500000,
        "repayment_probability": 0.92,
        "risk_score": 15,
        "message": "AI loan recommendation coming soon!"
    }