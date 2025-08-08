from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.sandwiches import SandwichCreate, Sandwich
from ..models.sandwiches import Sandwich as DBSandwich
from ..dependencies.database import get_db

router = APIRouter(prefix="/sandwiches", tags=["Sandwiches"])

@router.post("/", response_model=Sandwich)
def create_sandwich(sandwich: SandwichCreate, database: Session = Depends(get_db)):
    db_sandwich = DBSandwich(**sandwich.dict())
    database.add(db_sandwich)
    database.commit()
    database.refresh(db_sandwich)
    return db_sandwich

@router.get("/", response_model=list[Sandwich])
def get_sandwiches(database: Session = Depends(get_db)):
    return database.query(DBSandwich).all()

@router.get("/{sandwich_id}", response_model=Sandwich)
def get_sandwich(sandwich_id: int, database: Session = Depends(get_db)):
    sandwich = database.query(DBSandwich).filter(DBSandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich