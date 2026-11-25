from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import products, categories, auth, users, attachments
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(title="Shop API - Lab 6", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(attachments.router, prefix="/api/v1")