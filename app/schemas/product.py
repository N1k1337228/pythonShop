from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.category import CategoryRead

class ProductBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    stock: int = Field(ge=0, default=0)
    status: str = "active"
    category_id: int | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    status: str | None = None
    category_id: int | None = None

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    category: CategoryRead | None = None

    model_config = ConfigDict(from_attributes=True)