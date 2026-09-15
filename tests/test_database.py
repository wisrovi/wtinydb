"""Unit tests for WTinyDB synchronous operations.

This test file validates CRUD operations, soft-deletion handling,
batch inserts, document lookups, exceptions, and memory storage functionality.
"""

from typing import Optional
from pydantic import BaseModel, Field
import pytest

from wtinydb import WTinyDB, DocumentNotFoundError, SoftDeleteMixin


# Sample Pydantic model for unit testing
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
    """Validates that a Pydantic model document can be inserted into WTinyDB

    and retrieved using its assigned document ID, asserting schema preservation.
    """
    # Initialize in-memory database instance for testing
    db = WTinyDB(User, in_memory=True)

    # Instantiate user model and insert into database
    user_data = User(name="Alice", email="alice@example.com", age=30)
    inserted_user = db.insert(user_data)

    # Validate returned user model attributes
    assert inserted_user.name == "Alice"
    assert inserted_user.email == "alice@example.com"
    assert getattr(inserted_user, "_doc_id") == 1

    # Retrieve inserted user by document ID
    retrieved_user = db.get(1)
    assert retrieved_user.name == "Alice"
    assert retrieved_user.age == 30

    db.close()


def test_insert_many_and_get_all():
    """Validates batch insertion of multiple documents in a single transaction

    and verifies retrieve all documents functionality.
    """
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

    # Update age field
    updated = db.update(1, {"age": 23})
    assert updated.age == 23

    # Re-retrieve to verify persistence
    retrieved = db.get(1)
    assert retrieved.age == 23

    db.close()


def test_soft_delete():
    """Validates soft-delete functionality using SoftDeleteMixin.

    Asserts that soft-deleted items are omitted from get_all() unless explicitly requested.
    """
    db = WTinyDB(SoftUser, in_memory=True)
    user = db.insert(SoftUser(name="Frank", role="admin"))

    # Assert soft delete sets flag
    db.delete(1, hard=False)

    # Getting soft-deleted item directly should raise DocumentNotFoundError
    with pytest.raises(DocumentNotFoundError):
        db.get(1)

    # get_all() should exclude soft deleted documents by default
    assert len(db.get_all(include_deleted=False)) == 0

    # get_all(include_deleted=True) should return the document
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
