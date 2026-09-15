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

    def _get_target_and_val(self, arg1: Any, arg2: Any = None) -> tuple[str, Any]:
        """Resolve target field name and comparison value."""
        if arg2 is None:
            if not self.field_name:
                raise ValueError("Target field name must be specified in Q('field') or method call.")
            return self.field_name, arg1
        return str(arg1), arg2

    def eq(self, arg1: Any, arg2: Any = None) -> Any:
        """Field equals value. Accepts `Q('field').eq(val)` or `Q().eq('field', val)`."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) == val

    def neq(self, arg1: Any, arg2: Any = None) -> Any:
        """Field does not equal value."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) != val

    def gt(self, arg1: Any, arg2: Any = None) -> Any:
        """Field greater than value."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) > val

    def gte(self, arg1: Any, arg2: Any = None) -> Any:
        """Field greater than or equal to value."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) >= val

    def lt(self, arg1: Any, arg2: Any = None) -> Any:
        """Field less than value."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) < val

    def lte(self, arg1: Any, arg2: Any = None) -> Any:
        """Field less than or equal to value."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field) <= val

    def in_list(self, arg1: Any, arg2: Any = None) -> Any:
        """Field value is in list of values."""
        field, val = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field).one_of(val)

    def matches(self, arg1: Any, arg2: Any = None, flags: int = 0) -> Any:
        """Field matches regular expression pattern."""
        field, pattern = self._get_target_and_val(arg1, arg2)
        return _resolve_query(field).matches(pattern, flags=flags)

    def exists(self, field: Optional[str] = None) -> Any:
        """Field exists in document."""
        target = field or self.field_name
        if not target:
            raise ValueError("Target field name must be specified.")
        return _resolve_query(target).exists()

    def search_text(self, arg1: Any, arg2: Any = None, case_sensitive: bool = False) -> Any:
        """Field contains text substring."""
        field, substring = self._get_target_and_val(arg1, arg2)
        if case_sensitive:
            return _resolve_query(field).search(re.escape(str(substring)))
        return _resolve_query(field).search(re.escape(str(substring)), flags=re.IGNORECASE)


def Q(field: str) -> QueryBuilder:
    """Factory helper for QueryBuilder."""
    return QueryBuilder(field)
