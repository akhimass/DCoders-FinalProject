from sqlalchemy.orm import Session
from ..models.order_item import OrderItem
from schemas.order_item import OrderItemCreate, OrderItemUpdate


def create(db: Session, request: OrderItemCreate):
    new_item = OrderItem(**request.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def read_all(db: Session):
    return db.query(OrderItem).all()


def read_one(db: Session, item_id: int):
    return db.query(OrderItem).filter(OrderItem.id == item_id).first()


def update(db: Session, request: OrderItemUpdate, item_id: int):
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    for key, value in request.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete(db: Session, item_id: int):
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    db.delete(item)
    db.commit()
    return {'detail': 'Order item deleted'}