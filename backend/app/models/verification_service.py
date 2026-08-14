# app/services/verification_service.py
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
from app.models.farmer import Farmer, VerificationLevelEnum, FarmerStatusEnum
from app.models.historical_production import HistoricalProduction
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class VerificationService:
    """Service for farmer verification"""
    
    @staticmethod
    def calculate_verification_score(farmer: Farmer, db: Session) -> int:
        """
        Calculate verification score based on all verification layers.
        
        Returns: Score 0-100
        """
        score = 0
        
        # Layer 1: National ID (already registered) - 15%
        if farmer.national_id:
            score += 15
        
        # Layer 2: GPS Verification - 15%
        if farmer.is_gps_verified and farmer.latitude and farmer.longitude:
            score += 15
        
        # Layer 3: Satellite Verification - 20%
        if farmer.is_satellite_verified:
            score += 20
        
        # Layer 4: Officer Verification - 20%
        if farmer.is_officer_verified:
            score += 20
        
        # Layer 5: Community Verification - 15%
        if farmer.is_community_verified:
            score += 15
        
        # Layer 6: Historical Records - 15%
        if farmer.has_historical_records:
            # Check if there are actual records
            records = db.query(HistoricalProduction).filter(
                HistoricalProduction.farmer_id == farmer.id
            ).count()
            if records > 0:
                score += 15
            elif farmer.has_historical_records:
                score += 10  # Partial credit if marked but no records yet
        
        # AI Consistency Check - Bonus or Penalty
        if farmer.ai_consistency_pass is False:
            score = max(0, score - 20)  # Penalty for inconsistency
        
        # Ensure score is within 0-100
        return min(max(score, 0), 100)
    
    @staticmethod
    def get_verification_level(score: int) -> VerificationLevelEnum:
        """Get verification level based on score"""
        if score >= 90:
            return VerificationLevelEnum.FULL
        elif score >= 70:
            return VerificationLevelEnum.PARTIAL
        elif score >= 50:
            return VerificationLevelEnum.LIMITED
        else:
            return VerificationLevelEnum.UNVERIFIED
    
    @staticmethod
    def update_verification_status(farmer: Farmer, db: Session) -> Dict:
        """
        Update farmer's verification status and score.
        Returns: Updated verification data
        """
        score = VerificationService.calculate_verification_score(farmer, db)
        level = VerificationService.get_verification_level(score)
        
        farmer.verification_score = score
        farmer.verification_level = level
        
        # Auto-update status based on verification
        if score >= 70 and farmer.status == FarmerStatusEnum.PENDING:
            farmer.status = FarmerStatusEnum.VERIFIED
            farmer.is_verified = True
            farmer.verification_date = datetime.now()
        
        db.commit()
        db.refresh(farmer)
        
        return {
            "verification_score": score,
            "verification_level": level.value,
            "status": farmer.status.value,
            "is_verified": farmer.is_verified
        }
    
    @staticmethod
    def verify_layer(
        farmer: Farmer,
        layer: str,
        db: Session,
        officer_name: Optional[str] = None,
        community_verifier: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Verify a specific layer for a farmer.
        
        Layers: 'gps', 'satellite', 'officer', 'community', 'historical'
        """
        now = datetime.now()
        
        if layer == 'gps':
            farmer.is_gps_verified = True
            farmer.gps_verified_at = now
            farmer.verification_notes = notes or "GPS location verified"
            
        elif layer == 'satellite':
            farmer.is_satellite_verified = True
            farmer.satellite_verified_at = now
            farmer.verification_notes = notes or "Satellite vegetation detected"
            
        elif layer == 'officer':
            farmer.is_officer_verified = True
            farmer.officer_verified_at = now
            farmer.officer_name = officer_name or "Unknown Officer"
            farmer.verification_notes = notes or "Verified by extension officer"
            
        elif layer == 'community':
            farmer.is_community_verified = True
            farmer.community_verified_at = now
            farmer.community_verifier = community_verifier or "Village Head"
            farmer.verification_notes = notes or "Confirmed by village leadership"
            
        elif layer == 'historical':
            farmer.has_historical_records = True
            
        else:
            raise ValueError(f"Unknown verification layer: {layer}")
        
        db.commit()
        db.refresh(farmer)
        
        # Recalculate verification score
        result = VerificationService.update_verification_status(farmer, db)
        result["layer_verified"] = layer
        result["verified_at"] = now.isoformat()
        
        return result
    
    @staticmethod
    def run_ai_consistency_check(farmer: Farmer, db: Session) -> Dict:
        """
        Run AI consistency checks on farmer data.
        Returns: {pass: bool, flags: list}
        """
        flags = []
        passed = True
        
        # Check 1: Farm size vs claimed yield
        area = farmer.farm_area_hectares or 0
        if area > 0:
            # Check historical records for unrealistic yields
            records = db.query(HistoricalProduction).filter(
                HistoricalProduction.farmer_id == farmer.id
            ).all()
            
            for record in records:
                # Maize yield should be roughly 2-8 tons/ha
                if record.crop_name and record.crop_name.lower() == "maize":
                    if record.yield_tons and record.area_hectares and record.area_hectares > 0:
                        yield_per_ha = record.yield_tons / record.area_hectares
                        if yield_per_ha > 10:
                            flags.append(f"Unrealistic maize yield: {yield_per_ha:.1f} tons/ha")
                            passed = False
                        elif yield_per_ha < 0.5:
                            flags.append(f"Very low maize yield: {yield_per_ha:.1f} tons/ha")
        
        # Check 2: Check if GPS coordinates are within Malawi bounds
        if farmer.latitude and farmer.longitude:
            if not (-17.5 <= farmer.latitude <= -9.0) or not (32.5 <= farmer.longitude <= 36.0):
                flags.append(f"GPS coordinates outside Malawi: ({farmer.latitude}, {farmer.longitude})")
                passed = False
        
        # Check 3: District consistency
        if farmer.district and farmer.region:
            valid_regions = {
                "Southern": ["Balaka", "Blantyre", "Chikwawa", "Chiradzulu", "Machinga", 
                           "Mangochi", "Mulanje", "Mwanza", "Neno", "Nsanje", "Phalombe", 
                           "Thyolo", "Zomba"],
                "Central": ["Dedza", "Dowa", "Kasungu", "Lilongwe", "Mchinji", 
                          "Nkhotakota", "Ntcheu", "Ntchisi", "Salima"],
                "Northern": ["Chitipa", "Karonga", "Likoma", "Mzimba", "Nkhata Bay", "Rumphi"]
            }
            
            if farmer.district in valid_regions.get(farmer.region, []):
                pass  # Valid
            else:
                flags.append(f"District '{farmer.district}' not in region '{farmer.region}'")
                passed = False
        
        # Save AI flags
        farmer.ai_consistency_pass = passed
        farmer.ai_flags = json.dumps(flags) if flags else None
        
        db.commit()
        db.refresh(farmer)
        
        return {
            "passed": passed,
            "flags": flags,
            "flag_count": len(flags)
        }
    
    @staticmethod
    def get_verification_summary(farmer: Farmer, db: Session) -> Dict:
        """
        Get a detailed verification summary for display.
        """
        score = VerificationService.calculate_verification_score(farmer, db)
        level = VerificationService.get_verification_level(score)
        
        # Count historical records
        record_count = db.query(HistoricalProduction).filter(
            HistoricalProduction.farmer_id == farmer.id
        ).count()
        
        return {
            "farmer_id": farmer.id,
            "farmer_name": farmer.full_name,
            "verification_score": score,
            "verification_level": level.value,
            "verification_status_text": farmer.verification_status_text,
            "layers": {
                "national_id": {
                    "verified": bool(farmer.national_id),
                    "weight": 15,
                    "status": "✅ Verified" if farmer.national_id else "❌ Missing"
                },
                "gps": {
                    "verified": farmer.is_gps_verified,
                    "weight": 15,
                    "verified_at": farmer.gps_verified_at,
                    "status": "✅ Verified" if farmer.is_gps_verified else "⏳ Pending"
                },
                "satellite": {
                    "verified": farmer.is_satellite_verified,
                    "weight": 20,
                    "verified_at": farmer.satellite_verified_at,
                    "status": "✅ Verified" if farmer.is_satellite_verified else "⏳ Pending"
                },
                "officer": {
                    "verified": farmer.is_officer_verified,
                    "weight": 20,
                    "verified_at": farmer.officer_verified_at,
                    "officer_name": farmer.officer_name,
                    "status": "✅ Verified" if farmer.is_officer_verified else "⏳ Pending"
                },
                "community": {
                    "verified": farmer.is_community_verified,
                    "weight": 15,
                    "verified_at": farmer.community_verified_at,
                    "verifier": farmer.community_verifier,
                    "status": "✅ Verified" if farmer.is_community_verified else "⏳ Pending"
                },
                "historical_records": {
                    "verified": farmer.has_historical_records,
                    "weight": 15,
                    "record_count": record_count,
                    "status": "✅ Verified" if farmer.has_historical_records else "⏳ Pending"
                }
            },
            "ai_consistency": {
                "passed": farmer.ai_consistency_pass,
                "flags": json.loads(farmer.ai_flags) if farmer.ai_flags else []
            },
            "loan_eligibility": {
                "eligible": farmer.is_eligible_for_loan,
                "requirements": {
                    "is_verified": farmer.is_verified,
                    "status_active": farmer.status == FarmerStatusEnum.ACTIVE,
                    "has_blockchain": farmer.has_blockchain_identity,
                    "credit_score_min_300": farmer.credit_score >= 300,
                    "verification_score_min_70": score >= 70
                }
            }
        }