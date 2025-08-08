from typing import Optional
from pydantic import BaseModel
from .ingredient import Ingredient
from .sandwiches import Sandwich


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    sandwich_id: int
    ingredient_id: int

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    ingredient_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    sandwich: Sandwich = None
    ingredient: Ingredient = None

    class ConfigDict:
        from_attributes = True