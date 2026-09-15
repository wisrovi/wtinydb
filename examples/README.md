# WTinyDB Examples Catalog

This directory contains executable code examples demonstrating key features and patterns of **WTinyDB**.

## Available Examples

1. **`01_basic_crud/`**: Basic Pydantic document schema definition, model insertion, retrieval by ID/field, document updating, and deletion.
2. **`02_query_builder/`**: Fluent NoSQL queries using `Q` helper with numeric comparisons, list containment, regex matching, and text search.
3. **`03_async_usage/`**: Non-blocking asynchronous document operations using `AsyncWTinyDB`.
4. **`04_soft_delete_and_audit/`**: Document lifecycle management using `SoftDeleteMixin`, `TimestampMixin`, and `AuditMixin`.
5. **`05_fastapi_integration/`**: Integrating WTinyDB repository pattern into a FastAPI REST API endpoint handler.
6. **`06_wmongo_style_collections/`**: WMongo-compatible collection CRUD interface, encryption/decryption, and permissions.
7. **`07_disk_persistence_crud/`**: Explicit disk persistence, physical JSON database file inspection, and data survival across application restarts.
8. **`08_nested_json_crud/`**: Single-responsibility modular CRUD for N-level nested JSON objects (`01_create.py`, `02_read.py`, `03_update.py`, `04_delete.py`, `05_drop_db.py`).

## Running Examples

Execute example scripts directly with Python:

```bash
python examples/01_basic_crud/example.py
python examples/02_query_builder/example.py
python examples/03_async_usage/example.py
python examples/04_soft_delete_and_audit/example.py
python examples/05_fastapi_integration/example.py
python examples/06_wmongo_style_collections/example.py
python examples/07_disk_persistence_crud/example.py
python examples/08_nested_json_crud/01_create.py
```
