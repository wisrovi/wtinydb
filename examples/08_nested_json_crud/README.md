# 08. N-Level Nested JSON CRUD (Single Responsibility Modular Architecture)

This example demonstrates how **WTinyDB** supports $N$-level nested JSON documents with clean single-responsibility scripts.

## Directory & File Structure

```text
examples/08_nested_json_crud/
├── dto/
│   ├── __init__.py
│   └── company.py        # Pydantic DTO models (GeoCoordinates -> Address -> ContactInfo -> Manager -> Department -> Company)
├── 01_create.py          # Single Responsibility: CREATE (Insert 5-level nested document)
├── 02_read.py            # Single Responsibility: READ & QUERY (Search by nested dotted path)
├── 03_update.py          # Single Responsibility: UPDATE (Modify nested fields)
├── 04_delete.py          # Single Responsibility: DELETE (Delete document from DB)
└── 05_drop_db.py         # Single Responsibility: DROP DATABASE (Remove physical JSON file)
```

## Running the Example Steps

Execute each CRUD step independently in sequence:

```bash
python examples/08_nested_json_crud/01_create.py
python examples/08_nested_json_crud/02_read.py
python examples/08_nested_json_crud/03_update.py
python examples/08_nested_json_crud/04_delete.py
python examples/08_nested_json_crud/05_drop_db.py
```
