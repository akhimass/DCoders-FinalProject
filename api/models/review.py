from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    score = Column(Integer, nullable=False)
    text = Column(String)

    menu_item = relationship("MenuItem", back_populates="reviews")
