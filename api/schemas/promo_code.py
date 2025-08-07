from pydantic import BaseModel
from datetime import datetime

class PromoCodeBase(BaseModel):
    code: str
    discount_percent: float
    expires_at: datetime

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeOut(PromoCodeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True