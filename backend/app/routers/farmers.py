# app/routers/farmers.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from app.database import get_db
from app.models.farmer import Farmer, FarmerStatusEnum
from app.models.historical_production import HistoricalProduction, RecordSourceEnum, EnterpriseTypeEnum as HistoricalEnterpriseTypeEnum
from app.schemas.farmer import (
    FarmerCreate,
    FarmerUpdate,
    FarmerResponse,
    FarmerListResponse,
)
from app.services.verification_service import VerificationService
from datetime import datetime
import json

# Create router FIRST
router = APIRouter()


@router.post("/", response_model=FarmerResponse, status_code=status.HTTP_201_CREATED)
def create_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    """Register a new farmer"""
    # Check if farmer already exists
    existing_farmer = db.query(Farmer).filter(
        (Farmer.national_id == farmer.national_id) | (Farmer.phone == farmer.phone)
    ).first()
    
    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farmer with this National ID or Phone already exists"
        )
    
    # Create new farmer
    db_farmer = Farmer(**farmer.model_dump())
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    
    # Initialize verification status
    VerificationService.update_verification_status(db_farmer, db)
    db.refresh(db_farmer)
    
    return db_farmer


@router.get("/", response_model=FarmerListResponse)
def get_farmers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    district: Optional[str] = None,
    region: Optional[str] = None,
    status: Optional[FarmerStatusEnum] = None,
    search: Optional[str] = None,
    include_inactive: bool = Query(False, description="Include inactive farmers"),
    db: Session = Depends(get_db)
):
    """Get all farmers with optional filters"""
    query = db.query(Farmer)
    
    # Exclude inactive by default
    if not include_inactive:
        query = query.filter(Farmer.status != FarmerStatusEnum.INACTIVE)
    
    # Apply filters
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
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    farmers = query.offset(skip).limit(limit).all()
    
    return FarmerListResponse(
        farmers=farmers,
        total=total,
        page=(skip // limit) + 1 if limit > 0 else 1,
        limit=limit
    )


@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Get a specific farmer by ID"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    return farmer


@router.get("/search/by-national-id/{national_id}", response_model=FarmerResponse)
def get_farmer_by_national_id(national_id: str, db: Session = Depends(get_db)):
    """Get a farmer by National ID"""
    farmer = db.query(Farmer).filter(Farmer.national_id == national_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    return farmer


@router.put("/{farmer_id}", response_model=FarmerResponse)
def update_farmer(
    farmer_id: int,
    farmer_update: FarmerUpdate,
    db: Session = Depends(get_db)
):
    """Update a farmer's details"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    # Update only fields that are provided
    update_data = farmer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(farmer, field, value)
    
    farmer.updated_at = datetime.now()
    db.commit()
    db.refresh(farmer)
    
    # Recalculate verification status if verification fields changed
    VerificationService.update_verification_status(farmer, db)
    db.refresh(farmer)
    
    return farmer


@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """Delete a farmer (soft delete - set status to INACTIVE)"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found"
        )
    
    farmer.status = FarmerStatusEnum.INACTIVE
    farmer.updated_at = datetime.now()
    db.commit()
    return None


@router.get("/districts/", response_model=List[str])
def get_districts(db: Session = Depends(get_db)):
    """Get list of all districts with farmers"""
    districts = db.query(Farmer.district).distinct().all()
    return [d[0] for d in districts if d[0]]


@router.get("/regions/", response_model=List[str])
def get_regions(db: Session = Depends(get_db)):
    """Get list of all regions with farmers"""
    regions = db.query(Farmer.region).distinct().all()
    return [r[0] for r in regions if r[0]]


# ==================== VERIFICATION ENDPOINTS ====================

@router.post("/{farmer_id}/verify/gps", response_model=FarmerResponse)
def verify_gps(farmer_id: int, db: Session = Depends(get_db)):
    """Verify GPS location for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    VerificationService.verify_layer(farmer, 'gps', db, notes="GPS location verified")
    db.refresh(farmer)
    return farmer


@router.post("/{farmer_id}/verify/satellite", response_model=FarmerResponse)
def verify_satellite(farmer_id: int, db: Session = Depends(get_db)):
    """Verify satellite imagery for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    VerificationService.verify_layer(farmer, 'satellite', db, notes="Satellite vegetation detected")
    db.refresh(farmer)
    return farmer


@router.post("/{farmer_id}/verify/officer", response_model=FarmerResponse)
def verify_officer(
    farmer_id: int,
    officer_name: str,
    db: Session = Depends(get_db)
):
    """Verify by extension officer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    VerificationService.verify_layer(farmer, 'officer', db, officer_name=officer_name)
    db.refresh(farmer)
    return farmer


@router.post("/{farmer_id}/verify/community", response_model=FarmerResponse)
def verify_community(
    farmer_id: int,
    verifier: str,
    db: Session = Depends(get_db)
):
    """Verify by community (Village Head, cooperative)"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    VerificationService.verify_layer(farmer, 'community', db, community_verifier=verifier)
    db.refresh(farmer)
    return farmer


@router.post("/{farmer_id}/verify/historical", response_model=FarmerResponse)
def verify_historical(farmer_id: int, db: Session = Depends(get_db)):
    """Mark that farmer has historical records"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    VerificationService.verify_layer(farmer, 'historical', db)
    db.refresh(farmer)
    return farmer


@router.post("/{farmer_id}/ai-check", response_model=Dict)
def run_ai_consistency_check(farmer_id: int, db: Session = Depends(get_db)):
    """Run AI consistency check on farmer data"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    result = VerificationService.run_ai_consistency_check(farmer, db)
    return result


@router.get("/{farmer_id}/verification-status", response_model=Dict)
def get_verification_status(farmer_id: int, db: Session = Depends(get_db)):
    """Get detailed verification status for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    result = VerificationService.get_verification_summary(farmer, db)
    return result


# ==================== HISTORICAL RECORDS ENDPOINTS ====================

@router.post("/{farmer_id}/historical-record", response_model=Dict)
def add_historical_record(
    farmer_id: int,
    season: str,
    enterprise_type: HistoricalEnterpriseTypeEnum,
    crop_name: Optional[str] = None,
    livestock_type: Optional[str] = None,
    area_hectares: Optional[float] = None,
    bags_50kg: Optional[int] = None,
    yield_tons: Optional[float] = None,
    animal_count: Optional[int] = None,
    milk_liters: Optional[float] = None,
    eggs_count: Optional[int] = None,
    verified_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Add a historical production record for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    # Auto-calculate yield if bags provided
    if bags_50kg and area_hectares and bags_50kg > 0 and area_hectares > 0:
        # 1 bag = 50kg, convert to tons
        yield_tons = (bags_50kg * 50 * area_hectares) / 1000
    
    record = HistoricalProduction(
        farmer_id=farmer_id,
        season=season,
        enterprise_type=enterprise_type,
        crop_name=crop_name,
        livestock_type=livestock_type,
        area_hectares=area_hectares,
        bags_50kg=bags_50kg,
        yield_tons=yield_tons,
        animal_count=animal_count,
        milk_liters=milk_liters,
        eggs_count=eggs_count,
        source=RecordSourceEnum.MANUAL,
        verified_by=verified_by or "Officer"
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    # Update historical records flag
    farmer.has_historical_records = True
    db.commit()
    
    # Recalculate verification score
    VerificationService.update_verification_status(farmer, db)
    db.refresh(farmer)
    
    return {
        "message": "Historical record added successfully",
        "record_id": record.id,
        "yield_tons": yield_tons,
        "farmer_verification_score": farmer.verification_score
    }


@router.get("/{farmer_id}/historical-records", response_model=List[Dict])
def get_historical_records(farmer_id: int, db: Session = Depends(get_db)):
    """Get all historical records for a farmer"""
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    records = db.query(HistoricalProduction).filter(
        HistoricalProduction.farmer_id == farmer_id
    ).order_by(HistoricalProduction.season.desc()).all()
    
    return [
        {
            "id": r.id,
            "season": r.season,
            "enterprise_type": r.enterprise_type.value,
            "crop_name": r.crop_name,
            "livestock_type": r.livestock_type,
            "area_hectares": r.area_hectares,
            "bags_50kg": r.bags_50kg,
            "yield_tons": r.yield_tons,
            "animal_count": r.animal_count,
            "milk_liters": r.milk_liters,
            "eggs_count": r.eggs_count,
            "source": r.source.value,
            "verified_by": r.verified_by,
            "created_at": r.created_at
        }
        for r in records
    ]


@router.delete("/historical-record/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_historical_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a historical record"""
    record = db.query(HistoricalProduction).filter(HistoricalProduction.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    farmer_id = record.farmer_id
    db.delete(record)
    db.commit()
    
    # Check if farmer still has any records
    remaining = db.query(HistoricalProduction).filter(
        HistoricalProduction.farmer_id == farmer_id
    ).count()
    
    if remaining == 0:
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if farmer:
            farmer.has_historical_records = False
            db.commit()
            VerificationService.update_verification_status(farmer, db)
    
    return None