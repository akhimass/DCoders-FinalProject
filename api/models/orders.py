from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))

    total_price = Column(DECIMAL(10, 2), nullable=False)
    tracking_number = Column(String(100), unique=True)
    order_type = Column(String(50))  # e.g., 'takeout', 'delivery'
    payment_status = Column(String(50))  # e.g., 'paid', 'pending'
    created_at = Column(DateTime, default=datetime.utcnow)

    order_details = relationship("OrderDetail", back_populates="order")
