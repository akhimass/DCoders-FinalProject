from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import order_details as controller
from ..schemas import order_details as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Order Details'],
    prefix="/orderdetails"
)


@router.post("/", response_model=schema.OrderDetail, status_code=status.HTTP_201_CREATED)
def create(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.OrderDetail])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.OrderDetail)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.OrderDetail)
def update(item_id: int, request: schema.OrderDetailUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete(item_id: int, db: Session = Depends(get_db)):
    controller.delete(db=db, item_id=item_id)
    return {"message": f"Order detail with ID {item_id} deleted successfully."}

from fastapi import FastAPI

def load_routes(app: FastAPI):
    app.include_router(router)