from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def paginate(
            self, page: int, size: int, category_id: int | None = None,
            status: str | None = None, search: str | None = None,
            sort_by: str = "created_at", order: str = "desc"
    ) -> tuple[list[Product], int]:

        stmt = select(Product).options(selectinload(Product.category))
        count_stmt = select(func.count(Product.id))

        conditions = []
        if category_id is not None:
            conditions.append(Product.category_id == category_id)
        if status is not None:
            conditions.append(Product.status == status)
        if search:
            conditions.append(Product.title.ilike(f"%{search}%"))

        for cond in conditions:
            stmt = stmt.where(cond)
            count_stmt = count_stmt.where(cond)

        sort_column = getattr(Product, sort_by, Product.created_at)
        stmt = stmt.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
        stmt = stmt.offset((page - 1) * size).limit(size)

        items = (await self.db.execute(stmt)).scalars().all()
        total = (await self.db.execute(count_stmt)).scalar_one()
        return list(items), total

    async def get(self, product_id: int) -> Product | None:
        stmt = select(Product).options(selectinload(Product.category)).where(Product.id == product_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()