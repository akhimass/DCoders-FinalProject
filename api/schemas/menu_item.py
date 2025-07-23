from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    ingredients: Optional[str]
    price: float
    calories: Optional[float]
    category: Optional[str]

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemRead(MenuItemBase):
    id: int

    class Config:
        orm_mode = True