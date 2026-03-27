from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: str

    model_config = ConfigDict(from_attributes=True)

