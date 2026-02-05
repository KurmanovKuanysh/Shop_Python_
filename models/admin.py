from models.product import Product
from storage import Storage
from models.catalog import Catalog

class Admin():
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_product_adm(self, catalog: Catalog, pid:int, name: str, cost: float, remains: int) -> tuple[bool, str]:
        if catalog.get_by_id(pid):
            return False, "Product already exists!"
        if cost <= 0:
            return False, "Invalid cost!"
        if remains < 0:
            return False, "Unacceptable quantity@"
        product = Product(
            id=pid,
            name=name,
            cost=cost,
            remains=remains
        )
        catalog.add_product(product)
        self.storage.save_products(catalog.all())
        return True, "Product added successfully!"

    def edit_price_adm(self, catalog: Catalog, pid: int, new_price: float) -> tuple[bool, str]:
        if not catalog.get_by_id(pid):
            return False, "Product not found!"
        if new_price <= 0:
            return False, "Invalid price!"
        catalog.get_by_id(pid).cost = new_price
        self.storage.save_products(catalog.all())
        return True, "Price updated successfully!"

    def edit_remains_adm(self, catalog: Catalog, pid: int, new_remains: int) -> tuple[bool, str]:
        if not catalog.get_by_id(pid):
            return False, "Product not found!"
        if new_remains <= 0:
            return False, "Unacceptable quantity!"
        catalog.get_by_id(pid).remains = new_remains
        self.storage.save_products(catalog.all())
        return True, "Quantity updated successfully!"

    def delete_product_adm(self, catalog: Catalog, pid: int) -> tuple[bool, str]:
        if not catalog.get_by_id(pid):
            return False, "Product not found!"
        catalog.remove_product(pid)
        self.storage.save_products(catalog.all())
        return True, "Product deleted successfully!"