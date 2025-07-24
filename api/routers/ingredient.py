# routers/ingredient.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import ingredient as models
from ..schemas import ingredient as schemas

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.get("/", response_model=list[schemas.Ingredient])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()

def load_routes(app):
    app.include_router(router)