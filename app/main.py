from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import products
from app.db.base import Base
from app.db.session import engine
from app.models.product import Product

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Shop API - Lab 2", version="1.0.0", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1")