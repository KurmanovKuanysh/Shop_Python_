from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.utils.utils import int_big, numeric_10_2

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    order_id: Mapped[int_big] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int_big] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[numeric_10_2] = mapped_column(nullable=False)

    #relationship
    orders = relationship("Order", back_populates="order_items")
    products = relationship("Product", back_populates="order_items")