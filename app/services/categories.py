from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Category

class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    def add_category(self, name: str):
        if self.get_category_by_name(name):
            raise ValueError("Category already exists!")
        category = Category(
            name=name.strip().capitalize()
        )
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return category

    def get_category_by_name(self, name: str) -> Category | None:
        return self.session.scalar(
            select(Category).where(Category.name == name)
        )

    def get_category_by_id(self, category_id: int) -> Category | None:
        return self.session.scalar(
            select(Category).where(Category.id == category_id)
        )

    def get_all_categories(self):
        return self.session.scalars(
            select(Category)
        ).all()