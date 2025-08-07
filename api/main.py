import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import model_loader
from .dependencies.config import conf

from .routers import (
    index as indexRoute,
    customer,
    menu_item,
    ingredient,
    review,
)

# Routers all Registered
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)
customer.load_routes(app)
menu_item.load_routes(app)
ingredient.load_routes(app)
review.load_routes(app)

from .routers.promo_code import load_routes as load_promo_code_routes
load_promo_code_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)