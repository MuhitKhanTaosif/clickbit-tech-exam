from pydantic import BaseModel
from enum import Enum


class CategoryBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    model_config = {"extra":"forbid"}


class CategoryPublic(CategoryBase):
    id: int
    img_url: str

class StockStatus(str, Enum):
    IN_STOCK = "In Stock"          # Item is available for sale
    LOW_STOCK = "Low Stock"        # Item quantity below reorder threshold
    OUT_OF_STOCK = "Out of Stock"  # Item not currently available