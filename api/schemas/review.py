# schemas/review.py
from pydantic import BaseModel

class ReviewBase(BaseModel):
    rating: int
    comment: str
    customer_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True