from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.order_item import OrderItemCreate, OrderItemRead
from ..models.order_item import OrderItem

router = APIRouter(prefix="/order_items", tags=["Order Items"])

@router.post("/", response_model=OrderItemRead)
def create_order_item(item: OrderItemCreate, db: Session = Depends(get_db)):
    db_item = OrderItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=OrderItemRead)
def read_order_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(OrderItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item