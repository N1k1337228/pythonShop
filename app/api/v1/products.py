from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService(db).list()

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService(db).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).create(data)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return await service.update(product, data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await service.delete(product)