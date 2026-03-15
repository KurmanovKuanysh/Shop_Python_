from datetime import timedelta, datetime
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from argon2 import PasswordHasher

from app.models.cart import Cart
from app.models.cart_items import CartItem
from app.models.categories import Category
from app.models.customer import Customer
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.payments import Payment
from app.models.products import Product

from app.core.config import DB_URL



ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def seed_categories(session: Session) -> list[Category]:
    categories_data = [
        "Electronics",
        "Books",
        "Clothes",
        "Home",
        "Sports",
    ]

    categories = [Category(name=name) for name in categories_data]
    session.add_all(categories)
    session.flush()
    return categories


def seed_products(session: Session, categories: list[Category]) -> list[Product]:
    products_data = [
        ("iPhone 15", 999.99, 15, "Electronics", True, "Apple smartphone"),
        ("Samsung TV", 799.50, 8, "Electronics", True, "Smart television"),
        ("Python Book", 39.99, 40, "Books", True, "Programming book"),
        ("SQL Guide", 29.99, 25, "Books", True, "Database basics"),
        ("T-Shirt", 19.99, 100, "Clothes", True, "Cotton t-shirt"),
        ("Jeans", 49.99, 60, "Clothes", True, "Blue jeans"),
        ("Chair", 89.99, 20, "Home", True, "Wooden chair"),
        ("Desk Lamp", 24.99, 35, "Home", True, "LED lamp"),
        ("Football", 22.50, 50, "Sports", True, "Standard football"),
        ("Dumbbells", 59.90, 18, "Sports", True, "Fitness dumbbells"),
    ]

    category_map = {c.name: c for c in categories}
    products = []

    for name, price, remains, category_name, is_active, description in products_data:
        products.append(
            Product(
                name=name,
                price=price,
                remains=remains,
                category_id=category_map[category_name].id,
                is_active=is_active,
                description=description,
            )
        )

    session.add_all(products)
    session.flush()
    return products


def seed_customers(session: Session) -> list[Customer]:
    customers_data = [
        ("Alice", "alice@example.com", "Password123!", datetime(2025, 1, 10), "Almaty"),
        ("Bob", "bob@example.com", "Password123!", datetime(2025, 2, 5), "Astana"),
        ("Charlie", "charlie@example.com", "Password123!", datetime(2025, 3, 12), "Shymkent"),
        ("Diana", "diana@example.com", "Password123!", datetime(2025, 4, 20), "Karaganda"),
        ("Evan", "evan@example.com", "Password123!", datetime(2025, 5, 8), "Aktobe"),
    ]

    customers = []
    for name, email, raw_password, registered_at, city in customers_data:
        customers.append(
            Customer(
                name=name,
                email=email,
                password_hash=hash_password(raw_password),
                registered_at=registered_at,
                city=city,
            )
        )

    session.add_all(customers)
    session.flush()
    return customers


def seed_carts(session: Session, customers: list[Customer]) -> list[Cart]:
    carts = [Cart(customer_id=customer.id) for customer in customers]
    session.add_all(carts)
    session.flush()
    return carts


def seed_cart_items(session: Session, carts: list[Cart], products: list[Product]) -> list[CartItem]:
    cart_items = []

    for cart in carts:
        chosen_products = random.sample(products, k=2)
        for product in chosen_products:
            cart_items.append(
                CartItem(
                    cart_id=cart.id,
                    product_id=product.id,
                    quantity=random.randint(1, 3),
                )
            )

    session.add_all(cart_items)
    session.flush()
    return cart_items


def seed_orders(session: Session, customers: list[Customer], products: list[Product]) -> list[Order]:
    statuses = ["PENDING", "PAID", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
    orders = []

    for i, customer in enumerate(customers, start=1):
        order = Order(
            customer_id=customer.id,
            order_date=datetime.today() - timedelta(days=i * 3),
            total_price=0,
            status=random.choice(statuses),
        )
        session.add(order)
        session.flush()

        chosen_products = random.sample(products, k=2)
        total = 0.00

        for product in chosen_products:
            quantity = random.randint(1, 3)
            line_price = product.price * quantity
            total += line_price

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price,
            )
            session.add(order_item)

        order.total_price = total
        orders.append(order)

    session.flush()
    return orders


def seed_payments(session: Session, orders: list[Order]) -> list[Payment]:
    methods = ["CARD", "CASH", "PAYPAL"]
    payments = []

    for order in orders:
        if order.status in {"PAID", "PROCESSING", "SHIPPED", "DELIVERED"}:
            payments.append(
                Payment(
                    order_id=order.id,
                    paid_at=order.order_date,
                    amount=order.total_price,
                    method=random.choice(methods),
                )
            )

    session.add_all(payments)
    session.flush()
    return payments


def clear_tables(session: Session) -> None:
    session.query(Payment).delete()
    session.query(OrderItem).delete()
    session.query(CartItem).delete()
    session.query(Order).delete()
    session.query(Cart).delete()
    session.query(Product).delete()
    session.query(Category).delete()
    session.query(Customer).delete()
    session.commit()


def seed_db(session: Session) -> None:
    categories = seed_categories(session)
    products = seed_products(session, categories)
    customers = seed_customers(session)
    carts = seed_carts(session, customers)
    seed_cart_items(session, carts, products)
    orders = seed_orders(session, customers, products)
    seed_payments(session, orders)
    session.commit()


def main() -> None:
    engine = create_engine(DB_URL, echo=False)

    with Session(engine) as session:
        clear_tables(session)
        seed_db(session)

    print("Seeding completed successfully.")


if __name__ == "__main__":
    main()