from fastapi import FastAPI

from app.db import Base, engine_primary, engine_replica
from app.models import Product
from app.routes import health, products, admin

app = FastAPI()

Base.metadata.create_all(bind=engine_primary)
Base.metadata.create_all(bind=engine_replica)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(admin.router)
