"""Fluent Query Builder for WTinyDB operations with N-level nested JSON support."""

import re
from typing import Any, Callable, Dict, List, Optional
from tinydb import Query, where


def _resolve_query(field: str) -> Query:
    """Resolve field path into a TinyDB Query object, supporting N-level nested dotted notation."""
    if "." not in field:
        return where(field)
    parts = field.split(".")
    q = Query()
    for part in parts:
        q = q[part]
    return q


class QueryBuilder:
    """Fluent Builder for constructing complex TinyDB query conditions with nested field support."""

    def __init__(self, field_name: Optional[str] = None):
        """Initialize QueryBuilder, optionally specifying target field."""
        self.field_name = field_name

    def eq(self, field: str, value: Any) -> Any:
        """Field equals value."""
        return _resolve_query(field) == value

    def neq(self, field: str, value: Any) -> Any:
        """Field does not equal value."""
        return _resolve_query(field) != value

    def gt(self, field: str, value: Any) -> Any:
        """Field greater than value."""
        return _resolve_query(field) > value

    def gte(self, field: str, value: Any) -> Any:
        """Field greater than or equal to value."""
        return _resolve_query(field) >= value

    def lt(self, field: str, value: Any) -> Any:
        """Field less than value."""
        return _resolve_query(field) < value

    def lte(self, field: str, value: Any) -> Any:
        """Field less than or equal to value."""
        return _resolve_query(field) <= value

    def in_list(self, field: str, values: List[Any]) -> Any:
        """Field value is in list of values."""
        return _resolve_query(field).one_of(values)

    def matches(self, field: str, regex_pattern: str, flags: int = 0) -> Any:
        """Field matches regular expression pattern."""
        return _resolve_query(field).matches(regex_pattern, flags=flags)

    def exists(self, field: str) -> Any:
        """Field exists in document."""
        return _resolve_query(field).exists()

    def search_text(self, field: str, substring: str, case_sensitive: bool = False) -> Any:
        """Field contains text substring."""
        if case_sensitive:
            return _resolve_query(field).search(re.escape(substring))
        return _resolve_query(field).search(re.escape(substring), flags=re.IGNORECASE)


def Q(field: str) -> QueryBuilder:
    """Factory helper for QueryBuilder."""
    return QueryBuilder(field)
