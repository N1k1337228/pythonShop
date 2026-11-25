from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import products, categories, auth, users, attachments
from app.db.session import engine
from app.core.logging import setup_logging
from app.core.exceptions import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(title="Shop API - Lab 8", version="1.0.0", lifespan=lifespan)

# Подключаем глобальные обработчики ошибок
app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(attachments.router, prefix="/api/v1")