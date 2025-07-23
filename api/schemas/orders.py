from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    tracking_number: str
    status: str
    total_price: float
    customer_id: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    total_price: Optional[float] = None
    customer_id: Optional[int] = None

    class Config:
        orm_mode = True

class OrderRead(OrderBase):
    id: int
    order_date: datetime
    order_items: List[OrderItemRead] = []

    class Config:
        from_attributes = True