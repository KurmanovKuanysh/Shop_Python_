from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Product, CartItem, Cart


class CartService:
    def __init__(self, session: Session):
        self.session = session

    def get_cart_by_customer_id(self, customer_id: int) -> Cart | None:
        return self.session.scalar(
            select(Cart)
            .where(Cart.customer_id == customer_id)
        )

    def create_cart(self, customer_id: int) -> Cart:
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

    def clear_cart(self, cart: Cart) -> None:
        try:
            self.session.delete(cart)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_cart_item(self, cart_item: CartItem) -> None:
        try:
            self.session.delete(cart_item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_cart(self, cart: Cart) -> None:
        self.session.delete(cart)
        self.session.commit()