# routers/menu_item.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.menu_item import MenuItem
from ..schemas.menu_item import MenuItemCreate, MenuItem as MenuItemSchema

router = APIRouter(prefix="/menu_items", tags=["Menu Items"])

@router.post("/", response_model=MenuItemSchema)
def create_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    db_item = MenuItem(**menu_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[MenuItemSchema])
def get_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

@router.get("/{item_id}", response_model=MenuItemSchema)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=MenuItemSchema)
def update_menu_item(item_id: int, updated_item: MenuItemCreate, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for key, value in updated_item.dict().items():
        setattr(item, key, value)
    db.commit()
    return item

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Menu item deleted"}

def load_routes(app):
    app.include_router(router)