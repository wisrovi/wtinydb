"""WTinyDB package initialization."""

from wtinydb.core.async_db import AsyncWTinyDB
from wtinydb.core.database import WTinyDB
from wtinydb.core.query import Q, QueryBuilder
from wtinydb.exceptions import DocumentNotFoundError, StorageError, ValidationError, WTinyDBError
from wtinydb.models import AuditMixin, ForensicModel, SoftDeleteMixin, TimestampMixin

__version__ = "1.1.0"

__all__ = [
    "WTinyDB",
    "AsyncWTinyDB",
    "ForensicModel",
    "QueryBuilder",
    "Q",
    "TimestampMixin",
    "SoftDeleteMixin",
    "AuditMixin",
    "WTinyDBError",
    "DocumentNotFoundError",
    "ValidationError",
    "StorageError",
]
