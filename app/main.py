from fastapi import FastAPI
from app.api.v1 import products

app = FastAPI(title="Shop API - Lab 1", version="1.0.0")

# Подключаем наши маршруты к приложению
app.include_router(products.router, prefix="/api/v1")