import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_product_unauthorized(client: AsyncClient):
    # Без токена
    response = await client.post("/api/v1/products", json={
        "title": "Test Product",
        "price": 100.0
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_product_forbidden(client: AsyncClient):
    # Регистрируем обычного юзера и логинимся
    await client.post("/api/v1/auth/register", json={
        "email": "user@example.com", "password": "password123"
    })
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "user@example.com", "password": "password123"
    })
    token = login_resp.json()["access_token"]

    response = await client.post(
        "/api/v1/products",
        json={"title": "Test Product", "price": 100.0},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Обычный юзер не может создавать

@pytest.mark.asyncio
async def test_create_product_as_admin(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/products",
        json={"title": "Admin Product", "price": 500.0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Admin Product"