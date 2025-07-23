from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.promotion import PromotionCreate, PromotionRead
from ..models.promotion import Promotion

router = APIRouter(prefix="/promotions", tags=["Promotions"])

@router.post("/", response_model=PromotionRead)
def create_promotion(promo: PromotionCreate, db: Session = Depends(get_db)):
    db_promo = Promotion(**promo.dict())
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return db_promo

@router.get("/{promo_id}", response_model=PromotionRead)
def read_promotion(promo_id: int, db: Session = Depends(get_db)):
    promo = db.query(Promotion).get(promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo