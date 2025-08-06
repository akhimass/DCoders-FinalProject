from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.promo_code import PromoCode
from ..schemas.promo_code import PromoCodeCreate, PromoCodeOut
from datetime import datetime
router = APIRouter(prefix="/promo_codes", tags=["Promo Codes"])

@router.post("/", response_model=PromoCodeOut)
def create_promo(promo: PromoCodeCreate, db: Session = Depends(get_db)):
    db_promo = db.query(PromoCode).filter(PromoCode.code == promo.code).first()
    if db_promo:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    new_promo = PromoCode(**promo.dict())
    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)
    return new_promo

@router.get("/{code}", response_model=PromoCodeOut)
def get_promo(code: str, db: Session = Depends(get_db)):
    promo = db.query(PromoCode).filter(PromoCode.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    if promo.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Promo code expired")
    return promo

@router.delete("/{code}")
def delete_promo(code: str, db: Session = Depends(get_db)):
    promo = db.query(PromoCode).filter(PromoCode.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    db.delete(promo)
    db.commit()
    return {"message": "Promo code deleted"}

def load_routes(app):
    app.include_router(router)