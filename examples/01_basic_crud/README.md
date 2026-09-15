# 01. Basic CRUD (Single Responsibility Modular Architecture)

This example demonstrates how **WTinyDB** supports standard CRUD operations with single-responsibility scripts and Pydantic DTO models.

## Key Technologies & Libraries

- **Python 3.10+**: Core programming language.
- **Pydantic v2**: Data validation and model schemas.
- **TinyDB**: Embedded NoSQL document store.
- **WTinyDB**: High-level wrapper with direct `.doc_id` / `.id` resolution and context manager support.

## Directory & File Structure

```text
examples/01_basic_crud/
├── dto/
│   ├── __init__.py
│   └── user.py                 # Pydantic DTO model for User
├── 01_create.py                # Single Responsibility: CREATE (Single & Batch Insert)
├── 02_read_all.py              # Single Responsibility: READ ALL & READ BY ID/FIELD
├── 03_update.py                # Single Responsibility: UPDATE (Update fields via instance)
├── 04_delete.py                # Single Responsibility: DELETE (Remove document via instance)
└── 05_drop_db.py               # Single Responsibility: DROP DATABASE / CLEANUP
```

## Running the Example Steps

Execute each CRUD step independently in sequence:

```bash
python 01_create.py
python 02_read_all.py
python 03_update.py
python 04_delete.py
python 05_drop_db.py
```
