from pathlib import Path
import json

from models.cart_item import CartItem
from models.product import Product
from models.order import Order

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FILE_PATH = DATA_DIR / "products.json"
ORDERS_PATH = DATA_DIR / "orders.json"

class Storage:
    def load_products(self) -> list[Product]:
        if not FILE_PATH.exists():
            print("File not found!")
            return []
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("File is corrupted!")
                return []
        products = []
        for item in data:
            product = Product(
                id = item["id"],
                name = item["name"],
                cost = item["cost"],
                remains=item["remains"]
            )
            products.append(product)
        return products

    def save_products(self, products: list[Product]) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        products_data = []
        for product in products:
            product_dictionary = {
                "id": product.id,
                "name": product.name,
                "cost": product.cost,
                "remains": product.remains
            }
            products_data.append(product_dictionary)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(products_data, f, ensure_ascii=False, indent=4)

    def load_orders(self) -> list[Order]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not ORDERS_PATH.exists():
            with ORDERS_PATH.open("w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []
        try:
            with ORDERS_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []
        orders: list[Order] = []

        for order in data:
            items = []
            for item in order["items"]:
                product = Product(**item["product"])
                items.append(CartItem(product, item["qty"]))

            orders.append(
                Order(
                    order_id=order["order_id"],
                    items=items,
                    total_cost=order["total"],
                    created_at=order["created_at"]
                )
            )
        return orders

    def save_orders(self, order: Order) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if ORDERS_PATH.exists():
            try:
                with ORDERS_PATH.open("r", encoding="utf-8") as f:
                    orders = json.load(f)
            except json.JSONDecodeError:
                orders = []
        else:
            orders = []
        order_data = {
            "order_id": order.order_id,
            "total": order.total_cost,
            "created_at": order.created_at,
            "items": []
        }
        for cart_item in order.items:
            item_dict = {
                "product": {
                    "id": cart_item.product.id,
                    "name": cart_item.product.name,
                    "cost": cart_item.product.cost,
                    "remains": cart_item.product.remains
                },
                "qty": cart_item.qty
            }
            order_data["items"].append(item_dict)
        orders.append(order_data)
        with ORDERS_PATH.open("w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=4)