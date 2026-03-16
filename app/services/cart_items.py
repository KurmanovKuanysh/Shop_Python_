from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Product, CartItem, Cart

class CartItemsService:
    def __init__(self, session: Session):
        self.session = session

    def add_to_cart(self, cart_id: int, product_id: int, quantity: int):
        cart = self.session.scalar(
            select(Cart)
            .where(Cart.id == cart_id)
        )

        if cart is None:
            raise ValueError("Cart not found")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        product = self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )
        if product is None:
            raise ValueError("Product not found")

        cart_item = self.session.scalar(
            select(CartItem)
            .where(CartItem.cart_id == cart_id,
                   CartItem.product_id == product_id)
        )
        if cart_item:
            if cart_item.quantity + quantity > product.remains:
                raise ValueError("Not enough products in stock")
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
            )
            self.session.add(cart_item)

        self.session.commit()
        self.session.refresh(cart_item)
        return cart_item

    def remove_from_cart(self, cart_id: int, product_id: int, quantity: int | None = None) -> CartItem | None:
        cart_item = self.session.scalar(
            select(CartItem)
            .where(CartItem.cart_id == cart_id,
                   CartItem.product_id == product_id)
        )

        if cart_item is None:
            raise ValueError("Cart item not found")

        if quantity is not None and quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if quantity is None:
            self.session.delete(cart_item)
            self.session.commit()
            return None

        if cart_item.quantity < quantity:
            raise ValueError("Quantity exceeds available quantity")

        cart_item.quantity -= quantity

        if cart_item.quantity == 0:
            self.session.delete(cart_item)
            self.session.commit()
            return None

        self.session.commit()
        self.session.refresh(cart_item)
        return cart_item

    def update_quantity(self, cart_id: int, product_id: int, quantity: int) -> CartItem | None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        cart_item = self.session.scalar(
            select(CartItem)
            .where(CartItem.cart_id == cart_id,
                   CartItem.product_id == product_id)
        )

        if cart_item is None:
            raise ValueError("Cart item not found")

        product = self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )

        if product is None:
            raise ValueError("Product not found")

        if quantity > product.remains:
            raise ValueError("Not enough products in stock")

        cart_item.quantity = quantity

        self.session.commit()
        self.session.refresh(cart_item)
        return cart_item

    def get_cart_item(self, product_id: int, cart_id: int) -> CartItem | None:
        cart_item = self.session.scalar(
            select(CartItem)
            .where(CartItem.cart_id == cart_id,
                CartItem.product_id == product_id)
        )
        return cart_item

    def get_cart_items(self, cart_id: int) -> list[CartItem]:
        cart = self.session.scalar(
            select(Cart)
            .where(Cart.id == cart_id)
        )
        if cart is None:
            raise ValueError("Cart not found")
        cart_items = self.session.scalars(
            select(CartItem)
            .where(CartItem.cart_id == cart_id)
        ).all()
        return list(cart_items)

    def is_product_in_cart(self, product_id: int, cart_id: int) -> bool:
        return self.session.scalar(
            select(CartItem)
            .where(CartItem.product_id == product_id,
                   CartItem.cart_id == cart_id)
        ) is not None
