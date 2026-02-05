from dataclasses import dataclass

from models.cart_item import CartItem


@dataclass
class Order:
    order_id: int
    items: list[CartItem]
    total_cost: float
    created_at: str