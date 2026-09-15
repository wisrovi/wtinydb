"""Asynchronous WTinyDB wrapper for non-blocking database operations."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from tinydb import Query

from wtinydb.core.database import WTinyDB

T = TypeVar("T", bound=BaseModel)


class AsyncWTinyDB(Generic[T]):
    """Asynchronous wrapper for WTinyDB operations using asyncio thread executor."""

    def __init__(self, sync_db: WTinyDB[T], executor: Optional[ThreadPoolExecutor] = None):
        """Initialize AsyncWTinyDB wrapping a synchronous WTinyDB instance.

        :param sync_db: Target synchronous WTinyDB instance.
        :param executor: Optional ThreadPoolExecutor for background execution.
        """
        self.sync_db = sync_db
        self._executor = executor

    async def _run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Run synchronous function in thread executor."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, lambda: func(*args, **kwargs))

    async def insert(self, instance: T) -> T:
        """Async insert single model instance."""
        return await self._run(self.sync_db.insert, instance)

    async def insert_many(self, instances: List[T]) -> List[T]:
        """Async insert multiple model instances."""
        return await self._run(self.sync_db.insert_many, instances)

    async def get(self, doc_id: int) -> T:
        """Async get model instance by doc_id."""
        return await self._run(self.sync_db.get, doc_id)

    async def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """Async get document by field value."""
        return await self._run(self.sync_db.get_by_field, field_name, value)

    async def get_all(self, include_deleted: bool = False) -> List[T]:
        """Async get all documents."""
        return await self._run(self.sync_db.get_all, include_deleted=include_deleted)

    async def find(
        self, cond: Union[Query, Callable[[Dict[str, Any]], bool]], include_deleted: bool = False
    ) -> List[T]:
        """Async find documents matching condition."""
        return await self._run(self.sync_db.find, cond, include_deleted=include_deleted)

    async def update(self, doc_id: int, data: Union[Dict[str, Any], T]) -> T:
        """Async update document by doc_id."""
        return await self._run(self.sync_db.update, doc_id, data)

    async def delete(self, doc_id: int, hard: bool = False) -> bool:
        """Async delete document by doc_id."""
        return await self._run(self.sync_db.delete, doc_id, hard=hard)

    async def count(self, include_deleted: bool = False) -> int:
        """Async count total documents."""
        return await self._run(self.sync_db.count, include_deleted=include_deleted)

    async def clear(self) -> None:
        """Async purge table documents."""
        await self._run(self.sync_db.clear)

    async def close(self) -> None:
        """Async close database storage."""
        await self._run(self.sync_db.close)
