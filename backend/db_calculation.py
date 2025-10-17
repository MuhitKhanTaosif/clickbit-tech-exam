from sqlmodel import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

from ..models.sqlModels import (CartItem, RegionEnum)
from ..models.models import StockStatus
from .db import SessionDep

def calculate_cart_sub_amount(cart_id: int, session: SessionDep) -> Decimal:
    cart_items = session.exec(
        select(CartItem).where(CartItem.cart_id == cart_id).options(
            selectinload(CartItem.product_variant)
        )
    ).all()

    return sum(
        item.quantity * item.product_variant.price for item in cart_items
    )

def get_shipping_charge(region: RegionEnum) -> Decimal:
    return Decimal(100 if region == RegionEnum.DHAKA else 200)

LOW_STOCK_THRESHOLD = 5

def get_stock_status(quantity: int) -> StockStatus:
    """
    Determines the stock status based on the quantity.

    Args:
        quantity: The current stock quantity of the item.

    Returns:
        The appropriate StockStatus enum member.
    """
    if quantity <= 0:
        return StockStatus.OUT_OF_STOCK
    if quantity <= LOW_STOCK_THRESHOLD:
        return StockStatus.LOW_STOCK
    return StockStatus.IN_STOCK