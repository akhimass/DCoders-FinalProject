from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail
from pydantic import BaseModel
from typing import Optional, List

class OrderDetailCreate(BaseModel):
    sandwich_id: int
    quantity: int

class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    total_price: float
    tracking_number: str
    order_type: str
    payment_status: str
    promo_code: Optional[str] = None
    order_details: Optional[List[OrderDetailCreate]] = []


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    total_price: float
    tracking_number: str
    order_type: str
    payment_status: str
    promo_code: Optional[str] = None
    order_details: Optional[List[OrderDetailCreate]] = []

    class Config:
        orm_mode = True
