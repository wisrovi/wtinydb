"""Synchronous WTinyDB client matching WMongo interface with Pydantic support, caching, and notifications."""

import json
import os
import threading
import time
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union
from cryptography.fernet import Fernet
from pydantic import BaseModel, ValidationError as PydanticValidationError
from tinydb import Query, TinyDB, where
from tinydb.storages import JSONStorage, MemoryStorage

from wtinydb.exceptions import DocumentNotFoundError, StorageError, ValidationError
from wtinydb.models import SoftDeleteMixin

try:
    import redis
except ImportError:
    redis = None

try:
    from wredis.queue import RedisQueueManager
except ImportError:
    RedisQueueManager = None

T = TypeVar("T", bound=BaseModel)

# 🔐 Encryption Key
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)


def _extract_id(target: Any) -> int:
    """Extract integer document ID from integer or Pydantic model instance."""
    if isinstance(target, int):
        return target
    if isinstance(target, BaseModel):
        for attr in ("doc_id", "id", "_doc_id", "_id"):
            val = getattr(target, attr, None)
            if isinstance(val, int):
                return val
    try:
        return int(target)
    except (ValueError, TypeError):
        raise ValueError(f"Could not extract document ID from target: {target}")


from wtinydb.models import ForensicModel, SoftDeleteMixin


class WTinyDB(Generic[T]):
    """Synchronous WTinyDB client providing WMongo-compatible collection CRUD, Redis cache, notifications, and Pydantic models."""

    QUEUE_NAME = "wtinydb:notifications:changes"

    def __init__(
        self,
        target: Optional[Union[Type[BaseModel], List[Type[BaseModel]], Tuple[Type[BaseModel], ...], str, dict]] = None,
        model_class: Optional[Type[T]] = None,
        db_path: str = "wtinydb.json",
        table_name: Optional[str] = None,
        verbose: bool = False,
        read_only: bool = False,
        enable_notifications: bool = False,
        enable_notification_receiver: bool = False,
        notification_callback: Optional[Callable[[str], None]] = None,
        redis_host: Optional[str] = None,
        redis_port: Optional[int] = None,
        redis_db: Optional[int] = None,
        in_memory: bool = False,
        storage: Type = JSONStorage,
        forensic: Optional[bool] = None,
        models: Optional[Union[List[Type[BaseModel]], Tuple[Type[BaseModel], ...]]] = None,
        db: Optional[TinyDB] = None,
        **storage_kwargs: Any,
    ):
        """Initialize WTinyDB instance with disk persistence by default."""
        resolved_db_path = db_path
        resolved_models: Optional[list[type[BaseModel]]] = list(models) if models is not None else None
        resolved_model: Optional[type[BaseModel]] = model_class

        if isinstance(target, str):
            resolved_db_path = target
        elif isinstance(target, dict):
            resolved_db_path = target.get("db_path") or target.get("database") or db_path
        elif isinstance(target, (list, tuple)):
            resolved_models = list(target)
        elif isinstance(target, type) and issubclass(target, BaseModel):
            resolved_model = target

        self.model_class = resolved_model
        self.db_path = resolved_db_path
        self.table_name = table_name or (resolved_model.__name__.lower() if resolved_model else "default")
        self.verbose = verbose
        self.read_only = read_only
        self.enable_notifications = enable_notifications
        self.enable_notification_receiver = enable_notification_receiver
        self.notification_callback = notification_callback
        self.forensic_setting = forensic
        self._lock = threading.RLock()

        self._repositories: dict[Union[type[BaseModel], str], "WTinyDB"] = {}
        self._repositories_by_name: dict[str, "WTinyDB"] = {}

        if db is not None:
            self.db = db
        elif in_memory:
            self.db = TinyDB(storage=MemoryStorage)
        else:
            db_dir = os.path.dirname(resolved_db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.db = TinyDB(resolved_db_path, storage=storage, **storage_kwargs)

        if resolved_models is not None:
            self.is_multi_table = True
            self.table = None
            self.forensic = False
            for m in resolved_models:
                self.register_model(m)
        elif resolved_model is not None:
            self.is_multi_table = False
            self.table = self.db.table(self.table_name)
            if forensic is None:
                self.forensic = (
                    issubclass(resolved_model, ForensicModel)
                    if isinstance(resolved_model, type) and issubclass(resolved_model, BaseModel)
                    else False
                )
            else:
                self.forensic = forensic
            self._register_repository_references(resolved_model, self)
        else:
            self.is_multi_table = True
            self.table = self.db.table(self.table_name)
            self.forensic = bool(forensic)

        self.is_soft_delete_model = issubclass(resolved_model, SoftDeleteMixin) if resolved_model else False

        # Configure Redis Cache
        self.use_cache = False
        self.redis_client = None
        if redis and redis_host and redis_port is not None and redis_db is not None:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host, port=redis_port, db=redis_db, decode_responses=True
                )
                self.redis_client.ping()
                self.use_cache = True
            except Exception:
                self.use_cache = False

        # Configure Redis Queue Manager
        self.redis_queue_manager = None
        if (self.enable_notifications or self.enable_notification_receiver) and RedisQueueManager and redis_host:
            try:
                self.redis_queue_manager = RedisQueueManager(
                    host=redis_host, port=redis_port, db=redis_db, verbose=self.verbose
                )
            except Exception:
                self.redis_queue_manager = None

    def register_model(
        self, model: type[BaseModel], forensic: Optional[bool] = None
    ) -> "WTinyDB":
        use_forensic = forensic if forensic is not None else self.forensic_setting
        repo = WTinyDB(
            model_class=model,
            db_path=self.db_path,
            db=self.db,
            forensic=use_forensic,
        )
        self._register_repository_references(model, repo)
        return repo

    def _register_repository_references(
        self, model: type[BaseModel], repo: "WTinyDB"
    ) -> None:
        table_name = getattr(model, "__tablename__", model.__name__.lower())
        model_name = model.__name__.lower()

        self._repositories[model] = repo
        self._repositories[model_name] = repo
        self._repositories[table_name] = repo
        self._repositories_by_name[model_name] = repo
        self._repositories_by_name[table_name] = repo

    def __getitem__(self, item: Union[type[BaseModel], str]) -> "WTinyDB":
        if isinstance(item, type) and issubclass(item, BaseModel):
            if item in self._repositories:
                return self._repositories[item]
        elif isinstance(item, str):
            item_lower = item.lower()
            if item_lower in self._repositories:
                return self._repositories[item_lower]

        if not self.is_multi_table and self.model_class:
            if item == self.model_class or (
                isinstance(item, str)
                and item.lower() in (self.table_name, self.model_class.__name__.lower())
            ):
                return self

        raise KeyError(f"Model or table '{item}' is not registered in WTinyDB registry.")

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        repositories = getattr(self, "_repositories_by_name", {})
        name_lower = name.lower()
        if name_lower in repositories:
            return repositories[name_lower]

        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def _to_doc(self, instance: T) -> Dict[str, Any]:
        """Serialize Pydantic model instance to dict."""
        return instance.model_dump(mode="json")

    def _to_model(self, doc: Dict[str, Any], doc_id: int) -> T:
        """Deserialize TinyDB doc dict into Pydantic model instance with doc_id and id attributes."""
        if not self.model_class:
            return doc
        try:
            doc_copy = dict(doc)
            if "doc_id" not in doc_copy:
                doc_copy["doc_id"] = doc_id
            if "id" not in doc_copy:
                doc_copy["id"] = doc_id

            model = self.model_class.model_validate(doc_copy)

            # Ensure doc_id, id, and _doc_id are accessible directly on model instance
            object.__setattr__(model, "doc_id", doc_id)
            object.__setattr__(model, "id", doc_id)
            object.__setattr__(model, "_doc_id", doc_id)
            return model
        except PydanticValidationError as e:
            raise ValidationError(f"Failed to validate document doc_id={doc_id}: {e}") from e

    def insert(
        self,
        collection_or_instance: Union[str, T],
        document: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Insert document or Pydantic model. Accepts WMongo style `insert('users', doc)` or `insert(model_instance)`."""
        if self.read_only:
            raise PermissionError("Database is in read-only mode!")

        with self._lock:
            if isinstance(collection_or_instance, str):
                collection_name = collection_or_instance
                doc_data = document or {}
                tbl = self.db.table(collection_name)
                doc_id = tbl.insert(doc_data)

                if self.use_cache and self.redis_client:
                    doc_data["_id"] = str(doc_id)
                    self.redis_client.set(f"cache:{collection_name}:{doc_id}", json.dumps(doc_data), ex=300)

                if self.enable_notifications:
                    self._send_notification({
                        "database": self.table_name,
                        "collection": collection_name,
                        "action": "insert",
                        "document": doc_data,
                        "timestamp": time.time(),
                        "id": str(doc_id),
                    })
                return doc_id
            else:
                instance = collection_or_instance
                doc_data = self._to_doc(instance)
                doc_id = self.table.insert(doc_data)
                return self._to_model(doc_data, doc_id)

    def find(
        self,
        collection_or_cond: Union[str, Query, Callable[[Dict[str, Any]], bool]],
        query: Optional[Dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> List[Any]:
        """Find documents. Accepts WMongo style `find('users', {'name': 'Alice'})` or Query objects."""
        with self._lock:
            if isinstance(collection_or_cond, dict):
                query_dict = collection_or_cond
                results = self.table.search(
                    lambda doc: all(doc.get(k) == v for k, v in query_dict.items())
                )
                models = []
                for doc in results:
                    model = self._to_model(doc, doc.doc_id)
                    if not include_deleted and self.is_soft_delete_model and getattr(model, "is_deleted", False):
                        continue
                    models.append(model)
                return models
            elif isinstance(collection_or_cond, str):
                collection_name = collection_or_cond
                query_dict = query or {}
                tbl = self.db.table(collection_name)

                if not query_dict:
                    results = tbl.all()
                else:
                    results = tbl.search(
                        lambda doc: all(doc.get(k) == v for k, v in query_dict.items())
                    )

                for doc in results:
                    if "_id" not in doc and hasattr(doc, "doc_id"):
                        doc["_id"] = str(doc.doc_id)
                return results
            else:
                cond = collection_or_cond
                results = self.table.search(cond)
                models = []
                for doc in results:
                    model = self._to_model(doc, doc.doc_id)
                    if not include_deleted and self.is_soft_delete_model and getattr(model, "is_deleted", False):
                        continue
                    models.append(model)
                return models

    def update(
        self,
        collection_or_id_or_model: Union[str, int, T],
        query_or_data: Union[Dict[str, Any], T],
        update_values: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Update documents. Accepts WMongo style `update('users', query, update_values)` or `update(model_instance_or_id, data)`."""
        if self.read_only:
            raise PermissionError("Database is in read-only mode!")

        with self._lock:
            if isinstance(collection_or_id_or_model, (Query, Callable)):
                cond = collection_or_id_or_model
                update_dict = query_or_data if isinstance(query_or_data, dict) else self._to_doc(query_or_data)
                return self.table.update(update_dict, cond)
            elif isinstance(collection_or_id_or_model, str):
                collection_name = collection_or_id_or_model
                query_dict = query_or_data if isinstance(query_or_data, dict) else {}
                vals = update_values or {}
                tbl = self.db.table(collection_name)

                updated_ids = tbl.update(
                    vals,
                    cond=lambda doc: all(doc.get(k) == v for k, v in query_dict.items()) if query_dict else True,
                )
                updated_count = len(updated_ids)

                if self.enable_notifications and updated_count > 0:
                    self._send_notification({
                        "database": self.table_name,
                        "collection": collection_name,
                        "action": "update",
                        "query": query_dict,
                        "update_values": vals,
                        "timestamp": time.time(),
                        "modified_count": updated_count,
                    })
                return updated_count
            else:
                doc_id = _extract_id(collection_or_id_or_model)
                if not self.table.contains(doc_id=doc_id):
                    raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)
                update_dict = self._to_doc(query_or_data) if isinstance(query_or_data, BaseModel) else query_or_data
                self.table.update(update_dict, doc_ids=[doc_id])
                return self.get(doc_id)

    def delete(
        self,
        collection_or_id_or_model: Union[str, int, Query, T],
        query: Optional[Dict[str, Any]] = None,
        hard: bool = False,
    ) -> Any:
        """Delete documents. Accepts WMongo style `delete('users', query)` or `delete(model_instance_or_id)` or `delete(Query)`."""
        if self.read_only:
            raise PermissionError("Database is in read-only mode!")

        with self._lock:
            if isinstance(collection_or_id_or_model, (Query, Callable)):
                cond = collection_or_id_or_model
                return self.table.remove(cond)
            elif isinstance(collection_or_id_or_model, str):
                collection_name = collection_or_id_or_model
                query_dict = query or {}
                tbl = self.db.table(collection_name)

                deleted_ids = tbl.remove(
                    cond=lambda doc: all(doc.get(k) == v for k, v in query_dict.items()) if query_dict else True
                )
                deleted_count = len(deleted_ids)

                if self.enable_notifications and deleted_count > 0:
                    self._send_notification({
                        "database": self.table_name,
                        "collection": collection_name,
                        "action": "delete",
                        "query": query_dict,
                        "timestamp": time.time(),
                        "deleted_count": deleted_count,
                    })
                return deleted_count
            else:
                doc_id = _extract_id(collection_or_id_or_model)
                if not self.table.contains(doc_id=doc_id):
                    raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)

                if self.is_soft_delete_model and not hard:
                    from datetime import datetime, timezone
                    self.table.update({"is_deleted": True, "deleted_at": datetime.now(timezone.utc).isoformat()}, doc_ids=[doc_id])
                    return True
                else:
                    self.table.remove(doc_ids=[doc_id])
                    return True

    def insert_many(self, instances: List[T]) -> List[T]:
        """Insert multiple Pydantic model instances."""
        if self.read_only:
            raise PermissionError("Database is in read-only mode!")
        with self._lock:
            docs = [self._to_doc(inst) for inst in instances]
            doc_ids = self.table.insert_multiple(docs)
            return [self._to_model(doc, doc_id) for doc, doc_id in zip(docs, doc_ids)]

    def get(self, target: Union[int, T]) -> T:
        """Retrieve a document by TinyDB doc_id or Pydantic model instance."""
        doc_id = _extract_id(target)
        with self._lock:
            doc = self.table.get(doc_id=doc_id)
            if doc is None:
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)
            model = self._to_model(doc, doc_id)
            if self.is_soft_delete_model and getattr(model, "is_deleted", False):
                raise DocumentNotFoundError(doc_id=doc_id, table_name=self.table_name)
            return model

    def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """Retrieve first document matching field_name == value."""
        with self._lock:
            results = self.find(where(field_name) == value)
            return results[0] if results else None

    def get_all(self, include_deleted: bool = False) -> List[T]:
        """Retrieve all documents in the primary table."""
        with self._lock:
            models = []
            for doc in self.table.all():
                model = self._to_model(doc, doc.doc_id)
                if not include_deleted and self.is_soft_delete_model and getattr(model, "is_deleted", False):
                    continue
                models.append(model)
            return models

    def count(self, include_deleted: bool = False) -> int:
        """Return total document count."""
        with self._lock:
            if not self.is_soft_delete_model or include_deleted:
                return len(self.table)
            return len(self.get_all(include_deleted=False))

    def clear(self) -> None:
        """Purge all documents from primary table."""
        if self.read_only:
            raise PermissionError("Database is in read-only mode!")
        with self._lock:
            self.table.truncate()

    def _send_notification(self, message: Dict[str, Any]) -> None:
        """Send notification via Redis Queue Manager."""
        if self.redis_queue_manager:
            try:
                self.redis_queue_manager.publish(self.QUEUE_NAME, message)
            except Exception:
                pass

    def listen_notifications(self) -> None:
        """Start listening for change notifications using Redis Queue Manager."""
        if self.redis_queue_manager and self.notification_callback:
            @self.redis_queue_manager.on_message(self.QUEUE_NAME)
            def handle_message(record: str) -> None:
                self.notification_callback(record)

            self.redis_queue_manager.start()
            self.redis_queue_manager.wait()

    def has_permission(self, user_id: str, collection: str) -> bool:
        """Check user permission for target collection."""
        roles_tbl = self.db.table("roles")
        roles = roles_tbl.search(where("user_id") == user_id)
        if not roles:
            return False
        return collection in roles[0].get("collections", [])

    def encrypt(self, data: str) -> str:
        """Encrypt sensitive string data."""
        return cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        """Decrypt encrypted string data."""
        return cipher_suite.decrypt(data.encode()).decode()

    def close(self) -> None:
        """Close TinyDB instance and liberate resources."""
        with self._lock:
            self.db.close()

    def __enter__(self) -> "WTinyDB":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
