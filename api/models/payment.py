from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    card_info = Column(String)
    status = Column(String, nullable=False)
    payment_type = Column(String, nullable=False)

    order = relationship("Order", back_populates="payment")
