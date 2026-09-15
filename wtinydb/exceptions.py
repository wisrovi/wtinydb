"""WTinyDB custom exception definitions."""


class WTinyDBError(Exception):
    """Base exception class for all WTinyDB errors."""

    pass


class DocumentNotFoundError(WTinyDBError):
    """Raised when a requested document is not found in the database collection."""

    def __init__(self, doc_id: str or int, table_name: str = "default"):
        """Initialize DocumentNotFoundError with doc_id and table_name."""
        super().__init__(f"Document with ID '{doc_id}' not found in table '{table_name}'.")
        self.doc_id = doc_id
        self.table_name = table_name


class ValidationError(WTinyDBError):
    """Raised when document data fails Pydantic schema validation."""

    pass


class StorageError(WTinyDBError):
    """Raised when a underlying storage or IO error occurs."""

    pass
