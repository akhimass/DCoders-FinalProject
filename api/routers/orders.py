from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid

from ..dependencies.database import get_db

# Models
from ..models.orders import Order as DBOrder
from ..models.order_details import OrderDetail as DBOrderDetail
from ..models.sandwiches import Sandwich as DBSandwich
from ..models.ingredient import Ingredient as DBIngredient
from ..models.recipes import Recipe as DBRecipe
from ..models.promo_code import PromoCode as DBPromoCode

# Schemas
from ..schemas.orders import OrderCreate, Order
from ..schemas.order_details import OrderDetailCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


def _generate_tracking_number() -> str:
    return f"TRK-{uuid.uuid4().hex[:8].upper()}"


@router.post("/", response_model=Order)
def create(request: OrderCreate, db: Session = Depends(get_db)):
    """
    Create an order:
    - Validates sandwiches exist
    - Validates ingredient stock via recipes (Recipe.amount per sandwich)
    - Computes total price (uses Decimal), applies promo if present & not expired
    - Creates Order + OrderDetail, decrements ingredient stock
    """
    if not request.order_details or len(request.order_details) == 0:
        raise HTTPException(status_code=400, detail="Order must include at least one item in order_details.")

    # Compute total and validate inventory
    total_price_dec = Decimal("0.00")

    for detail in request.order_details:
        # Validate sandwich
        sandwich = db.query(DBSandwich).filter(DBSandwich.id == detail.sandwich_id).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail=f"Sandwich with ID {detail.sandwich_id} not found.")

        # Add to total with Decimal to avoid float/decimal mixing issues
        sandwich_price = Decimal(str(sandwich.price))
        total_price_dec += sandwich_price * Decimal(int(detail.quantity))

        # Validate inventory for this sandwich via its recipe
        recipe_rows = db.query(DBRecipe).filter(DBRecipe.sandwich_id == detail.sandwich_id).all()
        for recipe_item in recipe_rows:
            # amount = quantity of this ingredient per single sandwich
            required_qty = int(recipe_item.amount) * int(detail.quantity)
            ingredient = db.query(DBIngredient).filter(DBIngredient.id == recipe_item.ingredient_id).first()
            if not ingredient:
                raise HTTPException(status_code=404, detail=f"Ingredient {recipe_item.ingredient_id} not found.")
            if ingredient.quantity < required_qty:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Insufficient '{ingredient.name}' for sandwich {detail.sandwich_id}. "
                        f"Have {ingredient.quantity}, need {required_qty}."
                    ),
                )

    # Apply promo code if provided
    applied_promo: Optional[DBPromoCode] = None
    if request.promo_code:
        promo = db.query(DBPromoCode).filter(DBPromoCode.code == request.promo_code).first()
        if promo:
            # Treat as valid if not expired (or expires_at is in the future)
            if promo.expires_at and promo.expires_at < datetime.utcnow():
                # expired, ignore
                pass
            else:
                # apply discount
                discount = Decimal(str(promo.discount_percent or 0)) / Decimal("100")
                if discount > 0:
                    total_price_dec = (total_price_dec * (Decimal("1.00") - discount)).quantize(Decimal("0.01"))
                applied_promo = promo
        # If not found, silently ignore or raise — choose your policy. We'll ignore.

    # Create the order
    tracking = request.tracking_number or _generate_tracking_number()

    db_order = DBOrder(
        customer_name=request.customer_name,
        description=request.description,
        # order_date uses DB default if you don't set it; leaving it to DB is fine
        total_price=float(total_price_dec),  # store as float/DECIMAL in DB as defined
        tracking_number=tracking,
        order_type=request.order_type,
        payment_status=request.payment_status,
        promo_code=request.promo_code or None,
    )
    db.add(db_order)
    db.flush()  # get db_order.id

    # Create order details and decrement inventory
    for detail in request.order_details:
        db_detail = DBOrderDetail(
            order_id=db_order.id,
            sandwich_id=detail.sandwich_id,
            quantity=detail.quantity,
        )
        db.add(db_detail)

        # Decrement ingredients for this sandwich
        recipe_rows = db.query(DBRecipe).filter(DBRecipe.sandwich_id == detail.sandwich_id).all()
        for recipe_item in recipe_rows:
            required_qty = int(recipe_item.amount) * int(detail.quantity)
            ingredient = db.query(DBIngredient).filter(DBIngredient.id == recipe_item.ingredient_id).first()
            # Ingredient existence already validated above; just decrement now.
            ingredient.quantity = ingredient.quantity - required_qty

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[Order])
def list_orders(db: Session = Depends(get_db)):
    return db.query(DBOrder).order_by(DBOrder.id.desc()).all()


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def load_routes(app):
    app.include_router(router)