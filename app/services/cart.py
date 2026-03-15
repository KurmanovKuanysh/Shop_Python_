from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Product, CartItem, Cart


class CartService:
    def __init__(self, session: Session):
        self.session = session

    def create_cart(self, customer_id: int) -> Cart:
        exist_cart = self.session.scalar(
            select(Cart)
            .where(Cart.customer_id == customer_id)
        )
        if exist_cart:
            raise ValueError("Cart already exists for this customer")
        cart = Cart(customer_id=customer_id)
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    def get_or_create_cart(self, customer_id: int) -> Cart:
        cart = self.session.scalar(
            select(Cart)
            .where(Cart.customer_id == customer_id)
        )
        if cart is None:
            cart = Cart(customer_id=customer_id)
            self.session.add(cart)
            self.session.commit()
            self.session.refresh(cart)

        return cart

    def get_cart_by_customer_id(self, customer_id: int) -> Cart | None:
        return self.session.scalar(
            select(Cart)
            .where(Cart.customer_id == customer_id)
        )

    def get_cart_by_id(self, cart_id: int) -> Cart | None:
        return self.session.scalar(
            select(Cart)
            .where(Cart.id == cart_id)
        )

    def clear_cart(self, cart: Cart) -> None:
        cart = self.get_cart_by_id(cart.id)
        if cart is None:
            raise ValueError("Cart not found")
        for item in cart.cart_items:
            self.session.delete(item)

        self.session.commit()

    def delete_cart(self, cart_id: int) -> None:
        cart = self.get_cart_by_id(cart_id)
        if cart is None:
            raise ValueError("Cart not found")
        self.session.delete(cart)
        self.session.commit()

    def get_cart_total(self, cart_id: int) -> float:
        cart = self.session.scalar(
            select(Cart)
            .where(Cart.id == cart_id)
        )
        if cart is None:
            return 0.0

        total = 0.0
        for item in cart.cart_items:
            if item.products:
                total += item.products.price * item.quantity

        return total

    def get_cart_item_count(self, cart_id: int) -> int:
        cart = self.get_cart_by_id(cart_id)
        if cart is None:
            return 0

        return sum(item.quantity for item in cart.cart_items)