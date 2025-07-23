from pydantic import BaseModel
from datetime import date

class PromotionBase(BaseModel):
    code: str
    expiration_date: date

class PromotionCreate(PromotionBase):
    pass

class PromotionRead(PromotionBase):
    id: int

    class Config:
        orm_mode = True
