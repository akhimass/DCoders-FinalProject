# routers/review.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import review as models
from ..schemas import review as schemas

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=list[schemas.Review])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(models.Review).all()

def load_routes(app):
    app.include_router(router)