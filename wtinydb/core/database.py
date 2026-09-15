"""Synchronous WTinyDB Database implementation with Pydantic integration."""

import os
import threading
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError as PydanticValidationError
from tinydb import Query, TinyDB, where
from tinydb.storages import JSONStorage, MemoryStorage

from wtinydb.exceptions import DocumentNotFoundError, StorageError, ValidationError
from wtinydb.models import SoftDeleteMixin

T = TypeVar("T", bound=BaseModel)


class WTinyDB(Generic[T]):
    """Main synchronous database wrapper linking TinyDB and Pydantic models."""

    def __init__(
        self,
        model_class: Type[T],
        db_path: Optional[str] = None,
        table_name: Optional[str] = None,
        storage: Type = JSONStorage,
        in_memory: bool = False,
        **storage_kwargs: Any,
    ):
        """Initialize WTinyDB instance for a given Pydantic model.

        :param model_class: The Pydantic BaseModel class for schema validation and mapping.
        :param db_path: Path to JSON database file. Defaults to memory if in_memory is True.
        :param table_name: Table name inside TinyDB. Defaults to model_class.__name__.lower().
        :param storage: TinyDB storage engine class (JSONStorage, MemoryStorage, etc.).
        :param in_memory: If True, uses MemoryStorage ignoring db_path.
        """
        self.model_class = model_class
        self.table_name = table_name or model_class.__name__.lower()
        self._lock = threading.RLock()

        if in_memory:
            self.db = TinyDB(storage=MemoryStorage)
        else:
            if not db_path:
                db_path = f"{self.table_name}.json"
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.db = TinyDB(db_path, storage=storage, **storage_kwargs)

        self.table = self.db.table(self.table_name)
        self.is_soft_delete_model = issubclass(model_class, SoftDeleteMixin)

    def _to_doc(self, instance: T) -> Dict[str, Any]:
        """Serialize Pydantic model instance to dict with json-safe types."""
        return instance.model_dump(mode="json")

    def _to_model(self, doc: Dict[str, Any], doc_id: int) -> T:
        """Deserialize TinyDB doc dict into Pydantic model instance with doc_id injected."""
        try:
            doc_copy = dict(doc)
            if "doc_id" not in doc_copy and "id" not in doc_copy:
                doc_copy["doc_id"] = doc_id
            model = self.model_class.model_validate(doc_copy)
            # Attach internal doc_id attribute dynamically if not part of model schema
            setattr(model, "_doc_id", doc_id)
            return model
        except PydanticValidationError as e:
            raise ValidationError(f"Failed to validate document doc_id={doc_id}: {e}") from e

    def insert(self, instance: T) -> T:
        """Insert a single Pydantic model document into the database."""
        with self._lock:
            doc_data = self._to_doc(instance)
            doc_id = self.table.insert(doc_data)
            return self._to_model(doc_data, doc_id)

    def insert_many(self, instances: List[T]) -> List[T]:
        """Insert multiple Pydantic model documents in a single operation."""
        with self._lock:
            docs = [self._to_doc(inst) for inst in instances]
            doc_ids = self.table.insert_multiple(docs)
            return [self._to_model(doc, doc_id) for doc, doc_id in zip(docs, doc_ids)]

    def get(self, doc_id: int) -> T:
        """Retrieve a single document by its TinyDB doc_id."""
        with self._lock:
            doc = self.table.get(doc_id=doc_id)
            if doc is None:
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)
            model = self._to_model(doc, doc_id)
            if self.is_soft_delete_model and getattr(model, "is_deleted", False):
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)
            return model

    def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """Retrieve the first document matching field_name == value."""
        with self._lock:
            results = self.find(where(field_name) == value)
            return results[0] if results else None

    def get_all(self, include_deleted: bool = False) -> List[T]:
        """Retrieve all documents in the table."""
        with self._lock:
            models = []
            for doc in self.table.all():
                model = self._to_model(doc, doc.doc_id)
                if not include_deleted and self.is_soft_delete_model and getattr(model, "is_deleted", False):
                    continue
                models.append(model)
            return models

    def find(self, cond: Union[Query, Callable[[Dict[str, Any]], bool]], include_deleted: bool = False) -> List[T]:
        """Search documents matching TinyDB Query condition or custom filter callable."""
        with self._lock:
            results = self.table.search(cond)
            models = []
            for doc in results:
                model = self._to_model(doc, doc.doc_id)
                if not include_deleted and self.is_soft_delete_model and getattr(model, "is_deleted", False):
                    continue
                models.append(model)
            return models

    def update(self, doc_id: int, data: Union[Dict[str, Any], T]) -> T:
        """Update an existing document by doc_id with dictionary or new model instance."""
        with self._lock:
            if not self.table.contains(doc_id=doc_id):
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)

            update_dict = self._to_doc(data) if isinstance(data, BaseModel) else data
            self.table.update(update_dict, doc_ids=[doc_id])
            return self.get(doc_id)

    def delete(self, doc_id: int, hard: bool = False) -> bool:
        """Delete a document by doc_id. Performs soft delete if model supports it and hard is False."""
        with self._lock:
            if not self.table.contains(doc_id=doc_id):
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)

            if self.is_soft_delete_model and not hard:
                from datetime import datetime, timezone

                self.table.update({"is_deleted": True, "deleted_at": datetime.now(timezone.utc).isoformat()}, doc_ids=[doc_id])
                return True
            else:
                self.table.remove(doc_ids=[doc_id])
                return True

    def count(self, include_deleted: bool = False) -> int:
        """Return total document count in table."""
        with self._lock:
            if not self.is_soft_delete_model or include_deleted:
                return len(self.table)
            return len(self.get_all(include_deleted=False))

    def clear(self) -> None:
        """Purge all documents from the table."""
        with self._lock:
            self.table.truncate()

    def close(self) -> None:
        """Close TinyDB instance and liberate storage resources."""
        with self._lock:
            self.db.close()
