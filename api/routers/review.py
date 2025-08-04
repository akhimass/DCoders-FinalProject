# routers/review.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.review import Review
from ..schemas.review import ReviewCreate, Review as ReviewSchema

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=list[ReviewSchema])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, updated_review: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in updated_review.dict().items():
        setattr(review, key, value)
    db.commit()
    return review

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted"}

def load_routes(app):
    app.include_router(router)