from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from app.utils.utils import int_big, str_50, numeric_10_2

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str_50] = mapped_column(nullable=False)
    price: Mapped[numeric_10_2] = mapped_column(nullable=False)
    remains: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int_big] = mapped_column(ForeignKey("categories.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    description: Mapped[str_50] = mapped_column(nullable=True)

    #relationship
    categories = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="products")
    cart_items = relationship("CartItem", back_populates="products")

    __table_args__ = (
        CheckConstraint("price >= 0", name="products_price_check"),
        CheckConstraint("remains >= 0", name="products_remains_check"),
    )