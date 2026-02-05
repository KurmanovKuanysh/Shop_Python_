from models.cart import Cart
from models.catalog import Catalog
from models.order import Order
from storage import Storage
from datetime import datetime

class OrderService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def order_id(self) -> int:
        orders = self.storage.load_orders()
        if not orders:
            return 1
        return max(order.order_id for order in orders) + 1

    def checkout(self, cart: Cart, catalog: Catalog) -> Order|None:
        if cart.is_empty():
            print("Cart is empty!")
            return None
        order_id = self.order_id()
        for item in cart.items:
            if item.qty > item.product.remains:
                print(f"Not enough quantity of product {item.product.name} in stock!")
                return None
        for item in cart.items:
            item.product.remains -= item.qty

        order = Order(
            order_id = order_id,
            items = list(cart.items),
            total_cost = cart.total(),
            created_at = datetime.now().isoformat(timespec="seconds")
        )
        cart.clear()
        return order