# 08. N-Level Nested JSON CRUD (Single Responsibility Modular Architecture)

This example demonstrates how **WTinyDB** supports $N$-level nested JSON documents with clean single-responsibility scripts and DTO models.

## Directory & File Structure

```text
examples/08_nested_json_crud/
├── dto/
│   ├── __init__.py
│   └── company.py           # Pydantic DTO models (GeoCoordinates -> Address -> ContactInfo -> Manager -> Department -> Company)
├── 01_create.py             # Single Responsibility: CREATE (Insert 5-level nested document)
├── 02_read_all.py           # Single Responsibility: READ ALL (Standard get_all retrieval)
├── 03_read_by_query.py      # Single Responsibility: READ BY QUERY (Search by nested dotted path with Q)
├── 04_update.py             # Single Responsibility: STANDARD UPDATE (Update document by model instance)
├── 05_update_by_query.py    # Single Responsibility: UPDATE BY QUERY (Update collection documents by query filter)
├── 06_delete.py             # Single Responsibility: STANDARD DELETE (Delete document by model instance)
├── 07_delete_by_query.py    # Single Responsibility: DELETE BY QUERY (Delete collection documents by query filter)
└── 08_drop_db.py            # Single Responsibility: DROP DATABASE (Remove physical JSON file from disk)
```

## Running the Example Steps

Execute each CRUD step independently in sequence:

```bash
python examples/08_nested_json_crud/01_create.py
python examples/08_nested_json_crud/02_read_all.py
python examples/08_nested_json_crud/03_read_by_query.py
python examples/08_nested_json_crud/04_update.py
python examples/08_nested_json_crud/05_update_by_query.py
python examples/08_nested_json_crud/06_delete.py
python examples/08_nested_json_crud/07_delete_by_query.py
python examples/08_nested_json_crud/08_drop_db.py
```
