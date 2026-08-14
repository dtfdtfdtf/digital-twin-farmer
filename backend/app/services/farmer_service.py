# app/services/farmer_service.py
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from app.models.farmer import Farmer, FarmerStatusEnum
from app.models.enterprise import Enterprise, EnterpriseTypeEnum
from app.models.digital_identity import DigitalIdentity
from app.schemas.farmer import FarmerCreate, FarmerUpdate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FarmerService:
    """Service for farmer-related business logic"""
    
    @staticmethod
    def create_farmer(db: Session, farmer_data: FarmerCreate) -> Farmer:
        """Create a new farmer with validation"""
        # Check if farmer already exists
        existing = db.query(Farmer).filter(
            (Farmer.national_id == farmer_data.national_id) |
            (Farmer.phone == farmer_data.phone)
        ).first()
        
        if existing:
            raise ValueError("Farmer with this National ID or Phone already exists")
        
        # Create farmer
        db_farmer = Farmer(**farmer_data.model_dump())
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        
        logger.info(f"Farmer created: {db_farmer.id} - {db_farmer.full_name}")
        return db_farmer
    
    @staticmethod
    def get_farmer(db: Session, farmer_id: int) -> Optional[Farmer]:
        """Get farmer by ID"""
        return db.query(Farmer).filter(Farmer.id == farmer_id).first()
    
    @staticmethod
    def get_farmer_by_national_id(db: Session, national_id: str) -> Optional[Farmer]:
        """Get farmer by National ID"""
        return db.query(Farmer).filter(Farmer.national_id == national_id).first()
    
    @staticmethod
    def get_farmers(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        district: Optional[str] = None,
        region: Optional[str] = None,
        status: Optional[FarmerStatusEnum] = None,
        search: Optional[str] = None
    ) -> Dict:
        """Get farmers with filters"""
        query = db.query(Farmer)
        
        if district:
            query = query.filter(Farmer.district == district)
        if region:
            query = query.filter(Farmer.region == region)
        if status:
            query = query.filter(Farmer.status == status)
        if search:
            query = query.filter(
                (Farmer.first_name.contains(search)) |
                (Farmer.last_name.contains(search)) |
                (Farmer.national_id.contains(search)) |
                (Farmer.phone.contains(search))
            )
        
        total = query.count()
        farmers = query.offset(skip).limit(limit).all()
        
        return {
            "farmers": farmers,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    @staticmethod
    def update_farmer(db: Session, farmer_id: int, farmer_data: FarmerUpdate) -> Optional[Farmer]:
        """Update farmer details"""
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            return None
        
        update_data = farmer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(farmer, field, value)
        
        farmer.updated_at = datetime.now()
        db.commit()
        db.refresh(farmer)
        
        logger.info(f"Farmer updated: {farmer.id} - {farmer.full_name}")
        return farmer
    
    @staticmethod
    def verify_farmer(db: Session, farmer_id: int) -> Optional[Farmer]:
        """Verify a farmer"""
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            return None
        
        farmer.is_verified = True
        farmer.status = FarmerStatusEnum.VERIFIED
        farmer.verification_date = datetime.now()
        farmer.updated_at = datetime.now()
        db.commit()
        db.refresh(farmer)
        
        logger.info(f"Farmer verified: {farmer.id} - {farmer.full_name}")
        return farmer
    
    @staticmethod
    def get_farmer_with_enterprises(db: Session, farmer_id: int) -> Optional[Dict]:
        """Get farmer with their enterprises"""
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            return None
        
        enterprises = db.query(Enterprise).filter(Enterprise.farmer_id == farmer_id).all()
        
        return {
            "farmer": farmer,
            "enterprises": enterprises,
            "enterprise_count": len(enterprises)
        }
    
    @staticmethod
    def get_farmer_digital_identity(db: Session, farmer_id: int) -> Optional[Dict]:
        """Get farmer with their digital identity"""
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            return None
        
        identity = db.query(DigitalIdentity).filter(DigitalIdentity.farmer_id == farmer_id).first()
        
        return {
            "farmer": farmer,
            "digital_identity": identity,
            "has_blockchain_identity": identity is not None
        }
    
    @staticmethod
    def get_districts(db: Session) -> List[str]:
        """Get all districts with farmers"""
        districts = db.query(Farmer.district).distinct().all()
        return [d[0] for d in districts if d[0]]
    
    @staticmethod
    def get_regions(db: Session) -> List[str]:
        """Get all regions with farmers"""
        regions = db.query(Farmer.region).distinct().all()
        return [r[0] for r in regions if r[0]]
    
    @staticmethod
    def get_farmer_stats(db: Session) -> Dict:
        """Get farmer statistics"""
        total = db.query(Farmer).count()
        verified = db.query(Farmer).filter(Farmer.is_verified == True).count()
        pending = db.query(Farmer).filter(Farmer.status == FarmerStatusEnum.PENDING).count()
        active = db.query(Farmer).filter(Farmer.status == FarmerStatusEnum.ACTIVE).count()
        
        return {
            "total": total,
            "verified": verified,
            "pending": pending,
            "active": active,
            "verification_rate": round((verified / total) * 100, 1) if total > 0 else 0
        }