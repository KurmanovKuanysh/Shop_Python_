from models.cart_item import CartItem
from typing import List

from models.product import Product


class Cart:
    def __init__(self):
        self.items: List[CartItem] = []
    def add(self, product: Product, qty: int) -> bool:
        if qty <= 0:
            return False
        for item in self.items:
            if item.product.id == product.id:
                item.qty += qty
                return True
        self.items.append(CartItem(product, qty))
        return True
    def remove(self, product_id: int, qty: int) -> None:
        for item in self.items:
            if item.product.id == product_id:
                item.qty -= qty
                if item.qty <= 0:
                    self.items.remove(item)
                return
    def total(self) -> float:
        total = 0.0
        for item in self.items:
            total += item.product.cost * item.qty
        return total

    def is_empty(self) -> bool:
        if len(self.items) == 0:
            return True
        return False

    def clear(self) -> None:
        self.items = []
