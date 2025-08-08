from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))  # ✅ Needed for depletion check
    amount = Column(Integer, nullable=False, default=0, index=True)

    sandwich = relationship("Sandwich", back_populates="recipes")
    ingredient = relationship("Ingredient", back_populates="recipes")