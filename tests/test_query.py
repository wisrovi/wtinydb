"""Unit tests for QueryBuilder and Q helper functionality.

This file validates fluent query construction, comparison operators,
regex matching, nested dotted path querying, and list containment queries.
"""

from pydantic import BaseModel
from wtinydb import Q, QueryBuilder, WTinyDB


class Product(BaseModel):
    """Pydantic model representing a product in inventory."""

    title: str
    price: float
    category: str


class Geo(BaseModel):
    lat: float
    lon: float


class Address(BaseModel):
    city: str
    geo: Geo


class Organization(BaseModel):
    name: str
    address: Address


def test_query_builder_operators():
    """Validates equality, greater-than, and list comparison operators with QueryBuilder."""
    db = WTinyDB(Product, in_memory=True)

    db.insert(Product(title="Laptop", price=999.99, category="electronics"))
    db.insert(Product(title="Mouse", price=25.00, category="electronics"))
    db.insert(Product(title="Book", price=15.00, category="books"))

    books = db.find(Q("category").eq("category", "books"))
    assert len(books) == 1
    assert books[0].title == "Book"

    expensive = db.find(Q("price").gte("price", 100.00))
    assert len(expensive) == 1
    assert expensive[0].title == "Laptop"

    items = db.find(Q("category").in_list("category", ["electronics", "books"]))
    assert len(items) == 3

    db.close()


def test_query_regex_and_text_search():
    """Validates regex pattern matching and text search functionality."""
    db = WTinyDB(Product, in_memory=True)
    db.insert(Product(title="Wireless Keyboard", price=45.00, category="electronics"))
    db.insert(Product(title="Mechanical Keyboard", price=85.00, category="electronics"))

    keyboards = db.find(Q("title").search_text("title", "keyboard"))
    assert len(keyboards) == 2

    wireless = db.find(Q("title").matches("title", r"^Wireless"))
    assert len(wireless) == 1
    assert wireless[0].title == "Wireless Keyboard"

    db.close()


def test_nested_dotted_path_query():
    """Validates querying N-level nested JSON fields using dotted notation paths."""
    db = WTinyDB(Organization, in_memory=True)
    org = Organization(
        name="Acme",
        address=Address(city="Madrid", geo=Geo(lat=40.4168, lon=-3.7038)),
    )
    db.insert(org)

    # Query 3-level deep nested field
    found_city = db.find(Q("address.city").eq("address.city", "Madrid"))
    assert len(found_city) == 1
    assert found_city[0].name == "Acme"

    # Query 4-level deep nested numeric field
    found_geo = db.find(Q("address.geo.lat").gte("address.geo.lat", 40.0))
    assert len(found_geo) == 1

    db.close()
