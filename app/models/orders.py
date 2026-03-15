from dataclasses import dataclass

from app.models.cart_items import CartItem


@dataclass
class Order:
    order_id: int
    items: list[CartItem]
    total_cost: float
    created_at: str