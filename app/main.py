from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import products
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()  # Корректно закрываем соединения при выключении

app = FastAPI(title="Shop API - Lab 3", version="1.0.0", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1")