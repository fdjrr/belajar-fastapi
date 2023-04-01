from typing import List

from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
  name: str = Field(...)
  description: str = Field(...)
  price: float = Field(...)


class Product(ProductSchema):
  id: int


class Products(BaseModel):
  limit: int = Field(default=10)
  offset: int = Field(default=0)
  products: List[Product] = []
