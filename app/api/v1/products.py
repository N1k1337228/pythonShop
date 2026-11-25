from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.api.deps import get_db, require_role
from app.schemas.common import Page
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=Page[ProductRead])
async def list_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: int | None = None,
    status: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: AsyncSession = Depends(get_db),
):
    items, total = await ProductService(db).paginate(page, size, category_id, status, search, sort_by, order)
    return Page.create(items=items, total=total, page=page, size=size)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService(db).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin", "manager")) # ЗАЩИТА
):
    return await ProductService(db).create(data)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin", "manager")) # ЗАЩИТА
):
    service = ProductService(db)
    product = await service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return await service.update(product, data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin", "manager")) # ЗАЩИТА
):
    service = ProductService(db)
    product = await service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await service.delete(product)