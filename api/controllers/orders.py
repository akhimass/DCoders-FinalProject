from datetime import datetime
from ..models.order_details import OrderDetail
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request, total_price: float):
    from ..models.sandwiches import Sandwich
    total_price = 0.0
    try:
        # Placeholder for new_item, will set after details are processed
        # We'll collect order_details to add after order is created
        order_details_to_add = []
        for detail in request.order_details:
            sandwich = db.query(Sandwich).filter(Sandwich.id == detail.sandwich_id).first()
            if not sandwich:
                raise HTTPException(status_code=404, detail=f"Sandwich with ID {detail.sandwich_id} not found.")
            total_price += float(sandwich.price) * detail.quantity
            order_details_to_add.append(detail)

        new_item = model.Order(
            customer_name=request.customer_name,
            description=request.description,
            total_price=total_price,
            tracking_number=request.tracking_number,
            order_type=request.order_type,
            payment_status=request.payment_status,
            promo_code=request.promo_code,
            created_at=datetime.utcnow()
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        for detail in order_details_to_add:
            new_detail = OrderDetail(
                order_id=new_item.id,
                sandwich_id=detail.sandwich_id,
                quantity=detail.quantity
            )
            db.add(new_detail)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
