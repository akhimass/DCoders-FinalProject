import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    customer,
    orders,
    menu_item,
    order_item,
    review,
    payment,
    promotion,
    ingredient
)
from .routers import order_details
from .models import model_loader
from .dependencies.config import conf
from .dependencies.database import Base, engine

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and create tables
model_loader.index()

# Register routers
app.include_router(customer.router)
app.include_router(orders.router)
app.include_router(menu_item.router)
app.include_router(order_item.router)
app.include_router(review.router)
app.include_router(payment.router)
app.include_router(promotion.router)
app.include_router(ingredient.router)
app.include_router(order_details.router)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)