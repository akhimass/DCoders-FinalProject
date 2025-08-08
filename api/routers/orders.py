from fastapi import APIRouter, Depends, Query, FastAPI, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db
from datetime import datetime
from sqlalchemy import func
from ..models.orders import Order
from ..models.ingredient import Ingredient
from ..models.recipes import Recipe
from ..models.menu_item import MenuItem
from ..models.promo_code import PromoCode

# Orders update!
router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    # Check ingredient availability and deduct quantities
    if request.order_details:
        for order_detail in request.order_details:
            recipe_items = db.query(Recipe).filter(Recipe.sandwich_id == order_detail.sandwich_id).all()
            for recipe_item in recipe_items:
                ingredient = db.query(Ingredient).filter(Ingredient.id == recipe_item.ingredient_id).first()
                if not ingredient or ingredient.quantity < recipe_item.quantity_needed:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough {ingredient.name} in stock."
                    )
                ingredient.quantity -= recipe_item.quantity_needed
                db.add(ingredient)

    # Calculate total price
    total_price = 0
    if request.order_details:
        for order_detail in request.order_details:
            menu_item = db.query(MenuItem).filter(MenuItem.id == order_detail.sandwich_id).first()
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item with ID {order_detail.sandwich_id} not found.")
            total_price += menu_item.price * order_detail.quantity

    # Apply promo code if valid
    if request.promo_code:
        promo = db.query(PromoCode).filter(PromoCode.code == request.promo_code).first()
        if promo is not None:
            if promo.expires_at >= datetime.utcnow():
                discount = total_price * (promo.discount_percent / 100)
                total_price -= discount
            else:
                raise HTTPException(status_code=400, detail="Invalid or expired promo code.")
        else:
            raise HTTPException(status_code=400, detail="Invalid or expired promo code.")

    # Forward updated request and price to controller
    return controller.create(db=db, request=request, total_price=total_price)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/filter")
def get_orders_by_date_range(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.created_at.between(start_date, end_date)).all()
    return orders

@router.get("/revenue")
def get_total_revenue(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)
):
    revenue = db.query(func.sum(Order.total_price)).filter(Order.created_at.between(start_date, end_date)).scalar()
    return {"total_revenue": revenue or 0.0}


def load_routes(app):
    app.include_router(router)