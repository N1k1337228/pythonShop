from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_with_category(self, product_id: int) -> Product | None:
        stmt = select(Product).options(selectinload(Product.category)).where(Product.id == product_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def paginate(self, page: int, size: int, **filters) -> tuple[list[Product], int]:
        stmt = select(Product).options(selectinload(Product.category))
        count_stmt = select(func.count(Product.id))

        # Применяем фильтры
        if "category_id" in filters and filters["category_id"] is not None:
            stmt = stmt.where(Product.category_id == filters["category_id"])
            count_stmt = count_stmt.where(Product.category_id == filters["category_id"])
        if "status" in filters and filters["status"] is not None:
            stmt = stmt.where(Product.status == filters["status"])
            count_stmt = count_stmt.where(Product.status == filters["status"])

        # Сортировка и пагинация
        sort_by = filters.get("sort_by", "created_at")
        order = filters.get("order", "desc")
        sort_column = getattr(Product, sort_by, Product.created_at)
        stmt = stmt.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
        stmt = stmt.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(stmt)).scalars().all()
        total = (await self.db.execute(count_stmt)).scalar_one()
        return list(items), total