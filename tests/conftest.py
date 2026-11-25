import asyncio
from collections.abc import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.db.base import Base
from app.core.security import create_access_token, hash_password
from app.models.user import User

# Создаем тестовый движок SQLite в памяти
engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    # Создаем таблицы перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаляем после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db() -> AsyncGenerator:
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db) -> AsyncGenerator:
    # Подменяем зависимость get_db на тестовую
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def admin_token(db) -> str:
    # Создаем администратора для тестов
    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("password123"),
        role="admin"
    )
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return create_access_token(admin.id)