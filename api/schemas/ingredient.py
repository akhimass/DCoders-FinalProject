from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    amount: float
    unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int

    class Config:
        orm_mode = True
