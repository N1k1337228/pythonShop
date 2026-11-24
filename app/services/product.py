from datetime import datetime
from app.schemas.product import ProductCreate, ProductUpdate

class InMemoryProductService:
    def __init__(self) -> None:
        # Вместо базы данных используем словарь
        self._items: dict[int, dict] = {}
        self._next_id = 1

    def list(self) -> list[dict]:
        return list(self._items.values())

    def get(self, product_id: int) -> dict | None:
        return self._items.get(product_id)

    def create(self, data: ProductCreate) -> dict:
        product = {
            "id": self._next_id,
            "created_at": datetime.utcnow(),
            **data.model_dump(),
        }
        self._items[self._next_id] = product
        self._next_id += 1
        return product

    def update(self, product_id: int, data: ProductUpdate) -> dict | None:
        product = self._items.get(product_id)
        if product is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            product[key] = value
        return product

    def delete(self, product_id: int) -> bool:
        return self._items.pop(product_id, None) is not None