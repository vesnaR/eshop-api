
from decimal import Decimal

from app.db.database import SessionLocal
from app.db.models.category import Category
from app.db.models.product import Product


def seed_database():
    db = SessionLocal()

    try:
        categories_data = [
            {"name": "Phones", "description": "Smartphones and mobile phones"},
            {"name": "Laptops", "description": "Laptops for work and gaming"},
            {"name": "Accessories", "description": "Tech accessories"},
            {"name": "Monitors", "description": "Computer monitors"},
            {"name": "Audio", "description": "Headphones and speakers"},
        ]

        categories = {}

        for data in categories_data:
            category = (
                db.query(Category)
                .filter(Category.name == data["name"])
                .first()
            )

            if category is None:
                category = Category(**data)
                db.add(category)
                db.flush()

            categories[data["name"]] = category

        products_data = [
            {
                "name": "Samsung Galaxy",
                "description": "Android smartphone",
                "price": Decimal("699.99"),
                "stock": 10,
                "category": "Phones",
            },
            {
                "name": "iPhone 16",
                "description": "Apple smartphone",
                "price": Decimal("899.99"),
                "stock": 15,
                "category": "Phones",
            },
            {
                "name": "Budget Phone",
                "description": "Affordable smartphone",
                "price": Decimal("199.99"),
                "stock": 25,
                "category": "Phones",
            },
            {
                "name": "Gaming Laptop",
                "description": "Laptop for gaming",
                "price": Decimal("1499.99"),
                "stock": 5,
                "category": "Laptops",
            },
            {
                "name": "Office Laptop",
                "description": "Laptop for everyday work",
                "price": Decimal("749.99"),
                "stock": 8,
                "category": "Laptops",
            },
            {
                "name": "Wireless Mouse",
                "description": "Wireless computer mouse",
                "price": Decimal("29.99"),
                "stock": 40,
                "category": "Accessories",
            },
            {
                "name": "USB-C Hub",
                "description": "Multiport USB-C adapter",
                "price": Decimal("49.99"),
                "stock": 20,
                "category": "Accessories",
            },
            {
                "name": "4K Monitor",
                "description": "27-inch 4K monitor",
                "price": Decimal("399.99"),
                "stock": 7,
                "category": "Monitors",
            },
            {
                "name": "Gaming Headset",
                "description": "Headset with microphone",
                "price": Decimal("89.99"),
                "stock": 12,
                "category": "Audio",
            },
            {
                "name": "Bluetooth Speaker",
                "description": "Portable Bluetooth speaker",
                "price": Decimal("59.99"),
                "stock": 18,
                "category": "Audio",
            },
        ]

        added_products = 0

        for data in products_data:
            existing = (
                db.query(Product)
                .filter(Product.name == data["name"])
                .first()
            )

            if existing is not None:
                continue

            product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                stock=data["stock"],
                category_id=categories[data["category"]].id,
            )

            db.add(product)
            added_products += 1

        db.commit()

        print("Database seeding completed!")
        print(f"Categories available: {len(categories)}")
        print(f"New products added: {added_products}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
