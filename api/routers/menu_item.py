# routers/menu_item.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import menu_item as models
from ..schemas import menu_item as schemas

router = APIRouter(prefix="/menu_items", tags=["Menu Items"])

@router.post("/", response_model=schemas.MenuItem)
def create_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[schemas.MenuItem])
def read_items(db: Session = Depends(get_db)):
    return db.query(models.MenuItem).all()

def load_routes(app):
    app.include_router(router)