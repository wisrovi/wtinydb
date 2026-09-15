"""Unit tests for WTinyDB synchronous operations.

This test file validates CRUD operations, soft-deletion handling,
batch inserts, document lookups, exceptions, and WMongo-compatible collection operations.
"""

from typing import Optional
from pydantic import BaseModel, Field
import pytest

from wtinydb import WTinyDB, DocumentNotFoundError, SoftDeleteMixin


class User(BaseModel):
    """Pydantic model representing a User document."""

    name: str = Field(description="User full name")
    email: str = Field(description="User email address")
    age: int = Field(default=18, description="User age")


class SoftUser(SoftDeleteMixin, BaseModel):
    """Pydantic model representing a User document with soft-delete capabilities."""

    name: str
    role: str = "member"


def test_insert_and_get():
    """Validates model insertion and retrieval by doc_id."""
    db = WTinyDB(User, in_memory=True)
    user_data = User(name="Alice", email="alice@example.com", age=30)
    inserted_user = db.insert(user_data)

    assert inserted_user.name == "Alice"
    assert inserted_user.email == "alice@example.com"
    assert getattr(inserted_user, "_doc_id") == 1

    retrieved_user = db.get(1)
    assert retrieved_user.name == "Alice"
    assert retrieved_user.age == 30
    db.close()


def test_wmongo_collection_crud():
    """Validates WMongo-compatible collection CRUD operations (insert, find, update, delete)."""
    db = WTinyDB(in_memory=True)

    # Collection insert
    doc_id = db.insert("customers", {"name": "John Doe", "status": "active"})
    assert doc_id == 1

    # Collection find
    found = db.find("customers", {"status": "active"})
    assert len(found) == 1
    assert found[0]["name"] == "John Doe"

    # Collection update
    updated_count = db.update("customers", {"name": "John Doe"}, {"status": "inactive"})
    assert updated_count == 1

    # Collection delete
    deleted_count = db.delete("customers", {"status": "inactive"})
    assert deleted_count == 1

    db.close()


def test_insert_many_and_get_all():
    """Validates batch insertion of multiple documents."""
    db = WTinyDB(User, in_memory=True)
    users = [
        User(name="Bob", email="bob@example.com", age=25),
        User(name="Charlie", email="charlie@example.com", age=35),
    ]
    inserted = db.insert_many(users)

    assert len(inserted) == 2
    assert db.count() == 2

    all_users = db.get_all()
    assert len(all_users) == 2
    assert all_users[0].name == "Bob"
    assert all_users[1].name == "Charlie"
    db.close()


def test_get_by_field():
    """Validates document lookup by specific field name and value."""
    db = WTinyDB(User, in_memory=True)
    db.insert(User(name="David", email="david@example.com", age=40))

    user = db.get_by_field("email", "david@example.com")
    assert user is not None
    assert user.name == "David"

    missing_user = db.get_by_field("email", "nonexistent@example.com")
    assert missing_user is None
    db.close()


def test_update_document():
    """Validates document modification using dictionary update data."""
    db = WTinyDB(User, in_memory=True)
    inserted = db.insert(User(name="Eve", email="eve@example.com", age=22))

    updated = db.update(1, {"age": 23})
    assert updated.age == 23

    retrieved = db.get(1)
    assert retrieved.age == 23
    db.close()


def test_soft_delete():
    """Validates soft-delete functionality using SoftDeleteMixin."""
    db = WTinyDB(SoftUser, in_memory=True)
    user = db.insert(SoftUser(name="Frank", role="admin"))

    db.delete(1, hard=False)

    with pytest.raises(DocumentNotFoundError):
        db.get(1)

    assert len(db.get_all(include_deleted=False)) == 0

    all_docs = db.get_all(include_deleted=True)
    assert len(all_docs) == 1
    assert all_docs[0].is_deleted is True
    db.close()


def test_document_not_found_exception():
    """Validates that accessing a non-existent document ID raises DocumentNotFoundError."""
    db = WTinyDB(User, in_memory=True)

    with pytest.raises(DocumentNotFoundError):
        db.get(999)

    db.close()
