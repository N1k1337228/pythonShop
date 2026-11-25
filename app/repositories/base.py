from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")

class BaseRepository(ABC, Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, obj_id: int) -> ModelType | None:
        return await self.db.get(self.model, obj_id)

    async def create(self, obj_in: dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, obj: ModelType) -> None:
        await self.db.delete(obj)
        await self.db.commit()