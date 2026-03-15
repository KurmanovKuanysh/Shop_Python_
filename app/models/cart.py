from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.utils.utils import int_big


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    customer_id: Mapped[int_big] = mapped_column(ForeignKey("customer.id"), nullable=False)

    #relationship
    customer = relationship("Customer", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart")
