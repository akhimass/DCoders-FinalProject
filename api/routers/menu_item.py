from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.menu_item import MenuItemCreate, MenuItemRead
from ..models.menu_item import MenuItem

router = APIRouter(prefix="/menu_items", tags=["Menu Items"])

@router.post("/", response_model=MenuItemRead)
def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=MenuItemRead)
def read_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


