# models/orders.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import datetime

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    tracking_number = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")
    promotion = relationship("Promotion", back_populates="orders")
