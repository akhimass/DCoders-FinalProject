from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    card_info: str
    status: str
    payment_type: str

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int

    class Config:
        orm_mode = True
