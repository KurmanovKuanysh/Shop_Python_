from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.utils.utils import int_big, date_, str_10

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    order_id: Mapped[int_big] = mapped_column(ForeignKey("orders.id"), nullable=False)
    paid_at: Mapped[date_] = mapped_column(nullable=False)
    amount: Mapped[int_big] = mapped_column(nullable=False)
    method: Mapped[str_10] = mapped_column(nullable=False)

    #relationship
    orders = relationship("Order", back_populates="payments")
