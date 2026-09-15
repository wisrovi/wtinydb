"""02_query_builder/example.py

Demonstrates fluent QueryBuilder (Q) usage for complex document filtering.
"""

from pydantic import BaseModel
from wtinydb import Q, WTinyDB


class Product(BaseModel):
    """Product document model."""

    name: str
    category: str
    price: float
    tags: list[str] = []


def main():
    print("=== WTinyDB Query Builder Example ===")

    db = WTinyDB(Product, in_memory=True)

    db.insert(Product(name="Gaming Laptop", category="electronics", price=1299.99, tags=["gaming", "pc"]))
    db.insert(Product(name="Wireless Mouse", category="electronics", price=29.99, tags=["accessories", "pc"]))
    db.insert(Product(name="Coffee Mug", category="kitchen", price=12.50, tags=["home"]))
    db.insert(Product(name="Mechanical Keyboard", category="electronics", price=89.99, tags=["gaming", "pc"]))

    # Query 1: Filter by category equality
    kitchen_items = db.find(Q("category").eq("category", "kitchen"))
    print(f"Kitchen items: {[p.name for p in kitchen_items]}")

    # Query 2: Filter by price comparison (price >= 50.00)
    expensive_items = db.find(Q("price").gte("price", 50.00))
    print(f"Items price >= $50: {[p.name for p in expensive_items]}")

    # Query 3: Text search in name field
    keyboards = db.find(Q("name").search_text("name", "keyboard"))
    print(f"Keyboards found: {[p.name for p in keyboards]}")

    # Query 4: Regex matching pattern (names starting with 'Wireless')
    wireless = db.find(Q("name").matches("name", r"^Wireless"))
    print(f"Wireless items: {[p.name for p in wireless]}")

    db.close()


if __name__ == "__main__":
    main()
