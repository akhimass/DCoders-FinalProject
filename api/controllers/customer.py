# controllers/customer.py
from sqlalchemy.orm import Session
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerUpdate


def create(db: Session, request: CustomerCreate):
    new_customer = Customer(**request.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def read_all(db: Session):
    return db.query(Customer).all()


def read_one(db: Session, item_id: int):
    return db.query(Customer).filter(Customer.id == item_id).first()


def update(db: Session, request: CustomerUpdate, item_id: int):
    customer = db.query(Customer).filter(Customer.id == item_id).first()
    for key, value in request.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete(db: Session, item_id: int):
    customer = db.query(Customer).filter(Customer.id == item_id).first()
    db.delete(customer)
    db.commit()
    return {'detail': 'Customer deleted'}