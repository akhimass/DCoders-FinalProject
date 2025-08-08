from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(300))

    total_price = Column(DECIMAL(10, 2), nullable=False)
    tracking_number = Column(String(100), unique=True)
    order_type = Column(String(50))  # e.g., 'takeout', 'delivery'
    payment_status = Column(String(50))  # e.g., 'paid', 'pending'
    promo_code = Column(String(100), nullable=True)  # ✅ Add this line
    created_at = Column(DateTime, default=datetime.utcnow)

    order_details = relationship("OrderDetail", back_populates="order")