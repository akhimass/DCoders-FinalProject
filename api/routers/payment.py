from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.payment import PaymentCreate, PaymentRead
from ..models.payment import Payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentRead)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/{payment_id}", response_model=PaymentRead)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment