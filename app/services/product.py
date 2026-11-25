import logging
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get(self, product_id: int) -> Product:
        product = await self.repo.get_with_category(product_id)
        if not product:
            raise ValueError("Product not found")
        return product

    async def list(self, page: int, size: int, **filters) -> tuple[list[Product], int]:
        return await self.repo.paginate(page, size, **filters)

    async def create(self, data: ProductCreate, user_role: str) -> Product:
        if user_role not in ("admin", "manager"):
            raise PermissionError("Not enough permissions")
        product = await self.repo.create(data.model_dump())
        logger.info(f"Создан новый товар: {product.title}")
        return product

    async def update(self, product_id: int, data: ProductUpdate, user_role: str) -> Product:
        if user_role not in ("admin", "manager"):
            raise PermissionError("Not enough permissions")

        product = await self.repo.get(product_id)
        if not product:
            raise ValueError("Product not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        await self.repo.db.commit()
        await self.repo.db.refresh(product)
        return product

    async def delete(self, product_id: int, user_role: str) -> None:
        if user_role not in ("admin", "manager"):
            raise PermissionError("Not enough permissions")

        product = await self.repo.get(product_id)
        if not product:
            raise ValueError("Product not found")
        await self.repo.delete(product)