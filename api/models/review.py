# models/review.py
# Review add
from sqlalchemy import Column, Integer, String, ForeignKey
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String(255))
    customer_id = Column(Integer, ForeignKey("customers.id"))