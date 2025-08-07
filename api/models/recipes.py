from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))  # ✅ Needed for depletion check
    amount = Column(Integer, index=True, nullable=False, server_default='0')
    quantity_needed = Column(Integer, nullable=False, default=1)  # ✅ Optional: How much is needed per sandwich

    sandwich = relationship("Sandwich", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")
    ingredient = relationship("Ingredient", back_populates="recipes")