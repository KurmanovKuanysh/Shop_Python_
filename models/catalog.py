from typing import List, Dict
from models.product import Product

class Catalog:
    def __init__(self):
        self.products: Dict[int, Product] = {}

    def add_product(self, product: Product) -> None:
        self.products[product.id] = product

    def remove_product(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        else:
            return False
    def find_by_name(self, name: str) -> list[Product]:
        if not name:
            return []
        product_found = []
        for product in self.products.values():
            if name.lower() in product.name.lower():
                product_found.append(product)
        return product_found

    def get_by_id(self, product_id: int) -> Product | None:
        return self.products.get(product_id)

    def filter_by_price(self, min_price: float, max_price: float) -> List[Product]:
        filtered = []
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        for product in self.products.values():
            if min_price <= product.cost <= max_price:
                filtered.append(product)
        return filtered

    def show_catalog(self) -> list[Product]:
        return self.all()
    def all(self) -> list[Product]:
        return list(self.products.values())

    def sort_catalog_price_ascending(self):
        return sorted(self.products.values(), key=lambda x: x.cost)

    def sort_catalog_price_descending(self):
        return sorted(self.products.values(), key=lambda x: x.cost, reverse=True)

    def sort_catalog_name_ascending(self):
        return sorted(self.products.values(), key=lambda x: x.name)

    def sort_catalog_name_descending(self):
        return sorted(self.products.values(), key=lambda x: x.name, reverse=True)