from fastapi import APIRouter, HTTPException, status
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import InMemoryProductService

router = APIRouter(prefix="/products", tags=["products"])
# Создаем экземпляр сервиса
service = InMemoryProductService()

@router.get("", response_model=list[ProductRead])
def list_products():
    return service.list()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int):
    product = service.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate):
    return service.create(data)

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate):
    product = service.update(product_id, data)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if not service.delete(product_id):
        raise HTTPException(status_code=404, detail="Product not found")