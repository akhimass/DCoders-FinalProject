from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.review import ReviewCreate, ReviewRead
from ..models.review import Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{review_id}", response_model=ReviewRead)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

