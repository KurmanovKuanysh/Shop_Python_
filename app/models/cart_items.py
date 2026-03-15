from dataclasses import dataclass

from app.models.products import Product


@dataclass
class CartItem:
    product: Product
    qty: int