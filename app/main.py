from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import products, categories
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(title="Shop API - Lab 4", version="1.0.0", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")