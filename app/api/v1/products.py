from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Literal

from app.api.deps import get_product_service, get_current_user
from app.schemas.common import Page
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=Page[ProductRead])
async def list_products(
    page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),
    category_id: int | None = None, status: str | None = None,
    sort_by: str = "created_at", order: Literal["asc", "desc"] = "desc",
    service: ProductService = Depends(get_product_service),
):
    items, total = await service.list(page, size, category_id=category_id, status=status, sort_by=sort_by, order=order)
    return Page.create(items=items, total=total, page=page, size=size)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    try:
        return await service.get(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.create(data, current_user.role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))