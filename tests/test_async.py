"""Unit tests for AsyncWTinyDB async database wrapper.

Validates non-blocking async CRUD operations.
"""

from pydantic import BaseModel
import pytest

from wtinydb import AsyncWTinyDB, WTinyDB


class Item(BaseModel):
    """Pydantic model for async testing."""

    name: str
    quantity: int


@pytest.mark.asyncio
async def test_async_crud_operations():
    """Validates asynchronous insert, get, update, count, and delete operations."""
    sync_db = WTinyDB(Item, in_memory=True)
    async_db = AsyncWTinyDB(sync_db)

    # Async insert
    inserted = await async_db.insert(Item(name="Widget", quantity=10))
    assert inserted.name == "Widget"

    # Async count
    cnt = await async_db.count()
    assert cnt == 1

    # Async get
    retrieved = await async_db.get(1)
    assert retrieved.quantity == 10

    # Async update
    updated = await async_db.update(1, {"quantity": 15})
    assert updated.quantity == 15

    # Async get_all
    all_items = await async_db.get_all()
    assert len(all_items) == 1

    # Async delete
    deleted = await async_db.delete(1)
    assert deleted is True
    assert await async_db.count() == 0

    await async_db.close()
