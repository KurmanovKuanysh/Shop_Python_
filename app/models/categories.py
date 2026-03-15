from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.utils import int_big, str_50

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int_big] = mapped_column(primary_key=True)
    name: Mapped[str_50] = mapped_column(nullable=False, unique=True)

    #relationship
    products = relationship("Product", back_populates="categories")
