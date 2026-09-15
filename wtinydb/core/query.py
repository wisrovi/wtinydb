"""Fluent Query Builder for WTinyDB operations."""

import re
from typing import Any, Callable, Dict, List, Optional
from tinydb import Query, where


class QueryBuilder:
    """Fluent Builder for constructing complex TinyDB query conditions."""

    def __init__(self, field_name: Optional[str] = None):
        """Initialize QueryBuilder, optionally specifying target field."""
        self.field_name = field_name
        self._query = Query()

    def eq(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field equals value."""
        return where(field) == value

    def neq(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field does not equal value."""
        return where(field) != value

    def gt(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field greater than value."""
        return where(field) > value

    def gte(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field greater than or equal to value."""
        return where(field) >= value

    def lt(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field less than value."""
        return where(field) < value

    def lte(self, field: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """Field less than or equal to value."""
        return where(field) <= value

    def in_list(self, field: str, values: List[Any]) -> Callable[[Dict[str, Any]], bool]:
        """Field value is in list of values."""
        return where(field).one_of(values)

    def matches(self, field: str, regex_pattern: str, flags: int = 0) -> Callable[[Dict[str, Any]], bool]:
        """Field matches regular expression pattern."""
        return where(field).matches(regex_pattern, flags=flags)

    def exists(self, field: str) -> Callable[[Dict[str, Any]], bool]:
        """Field exists in document."""
        return where(field).exists()

    def search_text(self, field: str, substring: str, case_sensitive: bool = False) -> Callable[[Dict[str, Any]], bool]:
        """Field contains text substring."""
        if case_sensitive:
            return where(field).search(re.escape(substring))
        return where(field).search(re.escape(substring), flags=re.IGNORECASE)


def Q(field: str) -> QueryBuilder:
    """Factory helper for QueryBuilder."""
    return QueryBuilder(field)
