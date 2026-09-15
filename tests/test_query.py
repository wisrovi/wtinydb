"""Unit tests for QueryBuilder and Q helper functionality.

This file validates fluent query construction, comparison operators,
regex matching, and list containment queries.
"""

from pydantic import BaseModel
from wtinydb import Q, QueryBuilder, WTinyDB


class Product(BaseModel):
    """Pydantic model representing a product in inventory."""

    title: str
    price: float
    category: str


def test_query_builder_operators():
    """Validates equality, greater-than, and list comparison operators with QueryBuilder."""
    db = WTinyDB(Product, in_memory=True)

    db.insert(Product(title="Laptop", price=999.99, category="electronics"))
    db.insert(Product(title="Mouse", price=25.00, category="electronics"))
    db.insert(Product(title="Book", price=15.00, category="books"))

    # Test equality
    books = db.find(Q("category").eq("category", "books"))
    assert len(books) == 1
    assert books[0].title == "Book"

    # Test greater than or equal
    expensive = db.find(Q("price").gte("price", 100.00))
    assert len(expensive) == 1
    assert expensive[0].title == "Laptop"

    # Test in_list operator
    items = db.find(Q("category").in_list("category", ["electronics", "books"]))
    assert len(items) == 3

    db.close()


def test_query_regex_and_text_search():
    """Validates regex pattern matching and text search functionality."""
    db = WTinyDB(Product, in_memory=True)
    db.insert(Product(title="Wireless Keyboard", price=45.00, category="electronics"))
    db.insert(Product(title="Mechanical Keyboard", price=85.00, category="electronics"))

    # Test text search
    keyboards = db.find(Q("title").search_text("title", "keyboard"))
    assert len(keyboards) == 2

    # Test regex match
    wireless = db.find(Q("title").matches("title", r"^Wireless"))
    assert len(wireless) == 1
    assert wireless[0].title == "Wireless Keyboard"

    db.close()
