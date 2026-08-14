# app/services/medf_service.py
from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.models.farmer import Farmer
from app.models.loan import Loan, LoanStatusEnum
from app.models.repayment import Repayment, RepaymentStatusEnum
from app.ai.yield_prediction import YieldPredictor
from app.ai.credit_scoring import CreditScorer
from app.services.farmer_service import FarmerService
from app.services.loan_service import LoanService
import logging

logger = logging.getLogger(__name__)


class MEDFService:
    """
    MEDF (Malawi Enterprise Development Fund) specific service.
    Handles loan assessment and recommendations for MEDF officers.
    """
    
    def __init__(self):
        self.yield_predictor = YieldPredictor()
        self.credit_scorer = CreditScorer()
    
    def assess_farmer_for_loan(
        self,
        db: Session,
        farmer_id: int,
        loan_amount: float
    ) -> Dict:
        """
        Comprehensive farmer assessment for MEDF loan decision.
        """
        # Get farmer with enterprises
        farmer_data = FarmerService.get_farmer_with_enterprises(db, farmer_id)
        if not farmer_data:
            return {"error": "Farmer not found"}
        
        farmer = farmer_data["farmer"]
        enterprises = farmer_data["enterprises"]
        
        # Get AI predictions
        predictions = []
        for enterprise in enterprises:
            # Simplified prediction
            pred = self.yield_predictor.predict_yield(
                district=farmer.district,
                crop_type=enterprise.name,
                area_hectares=enterprise.area_hectares or 1.0,
                ndvi=0.55,  # Placeholder
                rainfall=850,  # Placeholder
                temperature=24.5,  # Placeholder
                previous_yields=[]
            )
            predictions.append(pred)
        
        # Calculate credit score
        credit_result = self.credit_scorer.calculate_credit_score(
            farmer_data={
                "age": 35,  # Placeholder
                "district": farmer.district,
                "village": farmer.village,
                "farm_area_hectares": farmer.farm_area_hectares or 1.0,
                "enterprises": enterprises,
                "primary_enterprise": enterprises[0].name if enterprises else "Unknown",
                "has_blockchain_identity": farmer.has_blockchain_identity
            },
            yield_prediction=predictions[0] if predictions else {},
            repayment_history=[],
            loan_history=[]
        )
        
        # Assess loan risk
        loan_assessment = self.credit_scorer.assess_loan_risk(
            credit_score=credit_result["credit_score"],
            loan_amount=loan_amount,
            predicted_yield=predictions[0].get("predicted_yield_per_hectare", 2.0) if predictions else 2.0,
            farmer_data={"district": farmer.district}
        )
        
        return {
            "farmer": {
                "id": farmer.id,
                "name": farmer.full_name,
                "district": farmer.district,
                "village": farmer.village,
                "national_id": farmer.national_id
            },
            "enterprises": [
                {
                    "name": e.name,
                    "type": e.type.value,
                    "area_hectares": e.area_hectares,
                    "estimated_yield": e.estimated_yield
                }
                for e in enterprises
            ],
            "ai_predictions": predictions,
            "credit_score": credit_result,
            "loan_assessment": loan_assessment,
            "recommendation": {
                "decision": loan_assessment["decision"],
                "reason": loan_assessment["reason"],
                "recommended_amount": loan_assessment["recommended_amount"],
                "max_amount": loan_assessment["max_amount"]
            }
        }
    
    def process_loan_application(
        self,
        db: Session,
        farmer_id: int,
        loan_amount: float,
        loan_purpose: str,
        reviewed_by: str
    ) -> Dict:
        """
        Process a complete loan application workflow.
        """
        # 1. Assess farmer
        assessment = self.assess_farmer_for_loan(db, farmer_id, loan_amount)
        
        if "error" in assessment:
            return assessment
        
        # 2. Check if farmer is eligible
        if assessment["loan_assessment"]["decision"] == "REJECT":
            return {
                "status": "REJECTED",
                "farmer_id": farmer_id,
                "reason": assessment["loan_assessment"]["reason"],
                "assessment": assessment
            }
        
        # 3. Create loan application
        from app.schemas.loan import LoanCreate
        
        loan_data = LoanCreate(
            farmer_id=farmer_id,
            loan_type="INPUT_FINANCING",
            purpose=loan_purpose,
            amount_requested=loan_amount,
            amount_approved=min(loan_amount, assessment["loan_assessment"]["recommended_amount"]),
            term_months=6,
            grace_period_days=30,
            repayment_frequency="SEASONAL"
        )
        
        loan = LoanService.create_loan(db, loan_data)
        
        # 4. Get loan summary
        summary = LoanService.get_loan_summary(db, loan.id)
        
        return {
            "status": "PENDING_REVIEW",
            "farmer_id": farmer_id,
            "loan_id": loan.id,
            "assessment": assessment,
            "loan_summary": summary,
            "reviewed_by": reviewed_by,
            "next_steps": "MEDF officer review required"
        }
    
    def get_medf_dashboard(self, db: Session) -> Dict:
        """
        Get MEDF dashboard data.
        """
        farmer_stats = FarmerService.get_farmer_stats(db)
        loan_stats = LoanService.get_loan_stats(db)
        
        # Get pending loans
        pending_loans = LoanService.get_loans(
            db,
            status=LoanStatusEnum.PENDING
        )
        
        return {
            "farmer_stats": farmer_stats,
            "loan_stats": loan_stats,
            "pending_loans": pending_loans["loans"],
            "pending_count": pending_loans["total"],
            "timestamp": datetime.now().isoformat()
        }