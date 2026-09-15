"""Asynchronous WTinyDB wrapper matching WMongoAsync interface."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from tinydb import Query

from wtinydb.core.database import WTinyDB

T = TypeVar("T", bound=BaseModel)


class AsyncWTinyDB(Generic[T]):
    """Asynchronous wrapper for WTinyDB operations using asyncio thread executor."""

    QUEUE_NAME = "wtinydb:notifications:changes"

    def __init__(
        self,
        sync_db: Optional[WTinyDB[T]] = None,
        executor: Optional[ThreadPoolExecutor] = None,
        **kwargs: Any,
    ):
        """Initialize AsyncWTinyDB wrapping a synchronous WTinyDB instance.

        If sync_db is not provided, passes kwargs to construct a default WTinyDB instance.
        """
        if sync_db is None:
            sync_db = WTinyDB(**kwargs)
        self.sync_db = sync_db
        self._executor = executor

    async def _run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Run synchronous function in thread executor."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, lambda: func(*args, **kwargs))

    async def insert(
        self,
        collection_or_instance: Union[str, T],
        document: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Async insert single model instance or collection document."""
        return await self._run(self.sync_db.insert, collection_or_instance, document)

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
        self,
        collection_or_cond: Union[str, Query, Callable[[Dict[str, Any]], bool]],
        query: Optional[Dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> List[Any]:
        """Async find documents matching condition or collection query."""
        return await self._run(self.sync_db.find, collection_or_cond, query=query, include_deleted=include_deleted)

    async def update(
        self,
        collection_or_id: Union[str, int],
        query_or_data: Union[Dict[str, Any], T],
        update_values: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Async update document by doc_id or collection query."""
        return await self._run(self.sync_db.update, collection_or_id, query_or_data, update_values=update_values)

    async def delete(
        self,
        collection_or_id: Union[str, int],
        query: Optional[Dict[str, Any]] = None,
        hard: bool = False,
    ) -> Any:
        """Async delete document by doc_id or collection query."""
        return await self._run(self.sync_db.delete, collection_or_id, query=query, hard=hard)

    async def count(self, include_deleted: bool = False) -> int:
        """Async count total documents."""
        return await self._run(self.sync_db.count, include_deleted=include_deleted)

    async def clear(self) -> None:
        """Async purge table documents."""
        await self._run(self.sync_db.clear)

    async def close(self) -> None:
        """Async close database storage."""
        await self._run(self.sync_db.close)

    async def __aenter__(self) -> "AsyncWTinyDB":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()
