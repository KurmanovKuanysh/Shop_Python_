from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from app.utils.utils import int_big

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    cart_id: Mapped[int_big] = mapped_column(ForeignKey("cart.id"), nullable=False)
    product_id: Mapped[int_big] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    #relationship
    cart = relationship("Cart", back_populates="cart_items")
    products = relationship("Product", back_populates="cart_items")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="cart_items_quantity_check"),
    )