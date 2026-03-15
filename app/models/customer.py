from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.utils import int_big, str_50, str_100, str_255, date_

class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str_50] = mapped_column(nullable=False)
    email: Mapped[str_100] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_255] = mapped_column(nullable=False)
    registered_at: Mapped[date_] = mapped_column(nullable=False)
    city: Mapped[str_50] = mapped_column(nullable=False)

    #relationship
    cart = relationship("Cart", back_populates="customer")
    orders = relationship("Order", back_populates="customer")