from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import Product

class ProductsService:
    def __init__(self, session: Session):
        self.session = session

    def add_product(
            self,
            name: str,
            price: float,
            remains: int,
            category_id: int,
            is_active: bool,
            description: str
    ):
        if price <= 0:
            raise ValueError("Price must be greater than 0")

        if remains < 0:
            raise ValueError("Remains must be positive")

        exist_product = self.session.scalar(
            select(Product)
            .where(func.lower(Product.name) == name.strip().lower())
        )

        if exist_product:
            raise ValueError("Product already exists")

        product = Product(
            name=name.strip().capitalize(),
            price=price,
            remains=remains,
            category_id=category_id,
            is_active=is_active,
            description=description
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def get_product_by_id(self, product_id: int):
        return self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )

    def get_product_by_price_range(self, min_price: float, max_price: float) -> list[Product] | []:
        if min_price > max_price:
            min_price, max_price = max_price, min_price

        if min_price <= 0 or max_price <= 0:
            return []

        return list(self.session.scalars(
            select(Product)
            .where(Product.price >= min_price, Product.price <= max_price)
        ).all())

    def get_product_by_name(self, name: str):
        return self.session.scalar(
            select(Product)
            .where(Product.name.ilike(f"%{name.strip()}%"))
        )

    def get_products_by_category_id(self, category_id: int) -> list[Product] | []:
        return list(self.session.scalars(
            select(Product)
            .where(Product.category_id == category_id)
        ).all())

    def get_all_products(self) -> list[Product] | []:
        return list(self.session.scalars(
            select(Product)
        ).all())

    def edit_product_by_id(self, product_id: int, edit: dict) -> Product | None:
        product = self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )
        if product is None:
            raise ValueError("Product not found")

        allowed = {
            "name",
            "price",
            "remains",
            "category_id",
            "is_active",
            "description"
        }
        for key in edit:
            if key not in allowed:
                raise ValueError(f"Invalid field: {key}")
            if key == "price" and edit["price"] <= 0:
                raise ValueError("Price must be greater than 0")
            if key == "remains" and edit["remains"] < 0:
                raise ValueError("Remains must be positive")
            if key == "category_id" and edit["category_id"] <= 0:
                category = self.session.scalar(
                    select(Product.category_id)
                    .where(Product.id == product_id)
                )
                if not category:
                    raise ValueError("Category not found")
            if key == "is_active" and not isinstance(edit["is_active"], bool):
                raise ValueError("is_active must be a boolean")
        for key, value in edit.items():
            setattr(product, key, value)

        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product_by_id(self, product_id: int) -> None:
        product = self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )
        if product is None:
            raise ValueError("Product not found")
        self.session.delete(product)
        self.session.commit()
