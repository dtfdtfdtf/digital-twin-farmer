# app/ai/credit_scoring.py
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CreditScorer:
    """
    AI-powered credit scoring for Malawian farmers.
    Based on historical data, predictions, and farmer characteristics.
    """
    
    def __init__(self):
        # Credit score ranges
        self.SCORE_RANGES = {
            "Excellent": (800, 1000),
            "Good": (700, 799),
            "Fair": (600, 699),
            "Poor": (500, 599),
            "Very Poor": (0, 499),
        }
    
    def calculate_credit_score(
        self,
        farmer_data: Dict,
        yield_prediction: Dict,
        repayment_history: Optional[List[Dict]] = None,
        loan_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Calculate comprehensive credit score for a farmer.
        
        Args:
            farmer_data: Farmer profile data
            yield_prediction: Yield prediction results
            repayment_history: List of past repayments
            loan_history: List of past loans
        
        Returns:
            Credit score with breakdown and risk assessment
        """
        score = 500  # Base score (0-1000)
        
        # 1. Demographic factors (max 100 points)
        demographic_score = self._demographic_score(farmer_data)
        score += demographic_score
        
        # 2. Farm/Enterprise factors (max 150 points)
        enterprise_score = self._enterprise_score(farmer_data, yield_prediction)
        score += enterprise_score
        
        # 3. Yield prediction factors (max 150 points)
        prediction_score = self._prediction_score(yield_prediction)
        score += prediction_score
        
        # 4. Repayment history (max 200 points)
        repayment_score = self._repayment_history_score(repayment_history)
        score += repayment_score
        
        # 5. Loan history (max 100 points)
        loan_history_score = self._loan_history_score(loan_history)
        score += loan_history_score
        
        # 6. Blockchain identity (bonus 50 points)
        if farmer_data.get("has_blockchain_identity", False):
            score += 50
        
        # Ensure score is within 0-1000
        score = max(0, min(1000, int(score)))
        
        # Calculate risk level
        risk_level = self._risk_level(score)
        
        # Calculate repayment probability
        repayment_probability = self._repayment_probability(score, yield_prediction)
        
        return {
            "credit_score": score,
            "risk_level": risk_level,
            "repayment_probability": round(repayment_probability, 2),
            "score_breakdown": {
                "demographic": demographic_score,
                "enterprise": enterprise_score,
                "prediction": prediction_score,
                "repayment_history": repayment_score,
                "loan_history": loan_history_score,
                "blockchain_bonus": 50 if farmer_data.get("has_blockchain_identity", False) else 0,
            },
            "rating": self._get_rating(score),
            "recommendations": self._get_recommendations(score, risk_level),
            "timestamp": datetime.now().isoformat(),
        }
    
    def assess_loan_risk(
        self,
        credit_score: int,
        loan_amount: float,
        predicted_yield: float,
        farmer_data: Dict
    ) -> Dict:
        """
        Assess risk for a specific loan application.
        """
        # Risk assessment factors
        score_factor = credit_score / 1000  # 0-1
        
        # Loan amount relative to predicted yield value
        yield_value = predicted_yield * 200000  # MWK per ton (simplified)
        loan_ratio = loan_amount / yield_value if yield_value > 0 else 1.0
        
        if loan_ratio <= 0.5:
            loan_factor = 1.0
        elif loan_ratio <= 0.8:
            loan_factor = 0.8
        else:
            loan_factor = 0.5
        
        # Combined risk score (0-100)
        risk_score = (1 - score_factor * loan_factor) * 100
        
        # Determine decision
        if risk_score <= 20:
            decision = "APPROVE"
            reason = "Low risk, strong credit profile"
        elif risk_score <= 40:
            decision = "APPROVE"
            reason = "Moderate risk, acceptable profile"
        elif risk_score <= 60:
            decision = "REVIEW"
            reason = "Requires additional documentation or collateral"
        else:
            decision = "REJECT"
            reason = "High risk, insufficient credit profile"
        
        return {
            "risk_score": round(risk_score, 1),
            "risk_level": self._risk_level_from_score(risk_score),
            "decision": decision,
            "reason": reason,
            "recommended_amount": int(predicted_yield * 200000 * 0.7),  # 70% of expected value
            "max_amount": int(predicted_yield * 200000 * 0.9),  # 90% of expected value
        }
    
    def _demographic_score(self, farmer_data: Dict) -> int:
        """Score based on farmer demographics"""
        score = 0
        
        # Age factor (30-50 is optimal)
        age = farmer_data.get("age", 35)
        if 30 <= age <= 50:
            score += 30
        elif 20 <= age <= 60:
            score += 20
        else:
            score += 10
        
        # Gender (both equal)
        score += 20
        
        # Village (established villages = more stability)
        village = farmer_data.get("village", "")
        if village:
            score += 10
        
        # District (some have better infrastructure)
        high_priority_districts = ["Lilongwe", "Blantyre", "Mzuzu"]
        if farmer_data.get("district") in high_priority_districts:
            score += 20
        
        # Education (if available)
        education = farmer_data.get("education_level", "")
        if education:
            score += 20
        
        return min(score, 100)
    
    def _enterprise_score(self, farmer_data: Dict, yield_prediction: Dict) -> int:
        """Score based on farm enterprises"""
        score = 0
        
        # Multiple enterprises = diversification
        enterprises = farmer_data.get("enterprises", [])
        if len(enterprises) >= 3:
            score += 50
        elif len(enterprises) >= 2:
            score += 30
        else:
            score += 15
        
        # Farm area
        area = farmer_data.get("farm_area_hectares", 0)
        if area >= 3:
            score += 40
        elif area >= 1.5:
            score += 25
        else:
            score += 10
        
        # Primary enterprise type
        primary = farmer_data.get("primary_enterprise", "")
        if primary in ["Maize", "Rice", "Tobacco"]:
            score += 30
        else:
            score += 15
        
        # Predicted yield (from AI)
        predicted = yield_prediction.get("predicted_yield_per_hectare", 0)
        if predicted >= 4:
            score += 30
        elif predicted >= 2.5:
            score += 20
        else:
            score += 10
        
        return min(score, 150)
    
    def _prediction_score(self, yield_prediction: Dict) -> int:
        """Score based on yield predictions"""
        score = 0
        
        confidence = yield_prediction.get("confidence_score", 0.5)
        predicted_yield = yield_prediction.get("predicted_yield_per_hectare", 0)
        
        # Confidence
        if confidence >= 0.8:
            score += 60
        elif confidence >= 0.6:
            score += 40
        else:
            score += 20
        
        # Yield potential
        if predicted_yield >= 4:
            score += 50
        elif predicted_yield >= 2.5:
            score += 35
        elif predicted_yield >= 1.5:
            score += 20
        else:
            score += 10
        
        # Environmental factors (if available)
        factors = yield_prediction.get("factors", {})
        if factors:
            ndvi_factor = factors.get("ndvi_factor", 0.5)
            rainfall_factor = factors.get("rainfall_factor", 0.5)
            score += int((ndvi_factor + rainfall_factor) * 20)
        
        return min(score, 150)
    
    def _repayment_history_score(self, repayment_history: Optional[List[Dict]]) -> int:
        """Score based on repayment history"""
        if not repayment_history:
            return 0
        
        total_repayments = len(repayment_history)
        on_time = sum(1 for r in repayment_history if r.get("on_time", False))
        
        if total_repayments == 0:
            return 0
        
        on_time_ratio = on_time / total_repayments
        
        if on_time_ratio >= 0.9:
            return 180
        elif on_time_ratio >= 0.7:
            return 140
        elif on_time_ratio >= 0.5:
            return 100
        else:
            return 40
    
    def _loan_history_score(self, loan_history: Optional[List[Dict]]) -> int:
        """Score based on loan history"""
        if not loan_history:
            return 0
        
        total_loans = len(loan_history)
        successful_loans = sum(1 for l in loan_history if l.get("completed", False))
        
        if total_loans == 0:
            return 0
        
        success_rate = successful_loans / total_loans
        
        if success_rate >= 0.9:
            return 90
        elif success_rate >= 0.7:
            return 70
        elif success_rate >= 0.5:
            return 50
        else:
            return 20
    
    def _risk_level(self, score: int) -> str:
        """Determine risk level from credit score"""
        if score >= 700:
            return "LOW"
        elif score >= 500:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _risk_level_from_score(self, score: float) -> str:
        """Determine risk level from risk score (0-100)"""
        if score <= 30:
            return "LOW"
        elif score <= 60:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _repayment_probability(self, score: int, yield_prediction: Dict) -> float:
        """Calculate repayment probability"""
        base_probability = score / 1000  # 0-1
        
        # Adjust based on yield prediction
        confidence = yield_prediction.get("confidence_score", 0.5)
        predicted_yield = yield_prediction.get("predicted_yield_per_hectare", 2.0)
        
        # Higher yield = higher probability
        yield_factor = min(predicted_yield / 3.5, 1.0)
        
        probability = base_probability * (0.7 + 0.3 * confidence) * (0.8 + 0.2 * yield_factor)
        
        return min(probability, 0.98)  # Cap at 98%
    
   