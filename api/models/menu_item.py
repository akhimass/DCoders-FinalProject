from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ingredients = Column(String)
    price = Column(Float, nullable=False)
    calories = Column(Float)
    category = Column(String)

    reviews = relationship("Review", back_populates="menu_item")
