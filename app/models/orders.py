from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from app.utils.utils import int_big, numeric_10_2, str_30, date_

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    customer_id: Mapped[int_big] = mapped_column(ForeignKey("customer.id"), nullable=False)
    order_date: Mapped[date_] = mapped_column(nullable=False)
    total_price: Mapped[numeric_10_2] = mapped_column(nullable=False, default=0)
    status: Mapped[str_30] = mapped_column(nullable=False)

    #relationship
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders")
    payments = relationship("Payment", back_populates="orders")

    __table_args__ = (
        CheckConstraint("total_price >= 0", name="orders_total_price_check"),
    )