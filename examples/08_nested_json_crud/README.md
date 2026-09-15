# 08. N-Level Nested JSON CRUD (Single Responsibility Modular Architecture)

This example demonstrates how **WTinyDB** supports $N$-level nested JSON documents with clean single-responsibility scripts and Pydantic DTO models.

## Key Technologies & Libraries

- **Python 3.10+**: Core programming language.
- **Pydantic v2**: Data validation and nested model serialization.
- **TinyDB**: Embedded document-oriented database engine.
- **WTinyDB**: Object-document wrapper providing WMongo-like API, query builder (`Q`), and $N$-level nested document path querying.

## Directory & File Structure

```text
examples/08_nested_json_crud/
├── dto/
│   ├── __init__.py
│   └── company.py                # Pydantic DTO models (GeoCoordinates -> Address -> ContactInfo -> Manager -> Department -> Company)
├── 01_create.py                  # Single Responsibility: CREATE (Insert 5-level nested document)
├── 02_read_all.py                # Single Responsibility: READ ALL & READ BY ID
├── 03_read_by_dict_query.py     # Single Responsibility: READ BY DICTIONARY QUERY (Without Q)
├── 04_read_by_q_query.py        # Single Responsibility: READ BY Q QUERY (N-level nested path with Q)
├── 05_update.py                  # Single Responsibility: UPDATE BY ID / MODEL INSTANCE
├── 06_update_by_query.py         # Single Responsibility: UPDATE BY QUERY
├── 07_delete.py                  # Single Responsibility: DELETE BY ID / MODEL INSTANCE
├── 08_delete_by_query.py         # Single Responsibility: DELETE BY QUERY
└── 09_drop_db.py                 # Single Responsibility: DROP DATABASE / CLEANUP
```

## Running the Example Steps

Execute each CRUD step independently in sequence:

```bash
python 01_create.py
python 02_read_all.py
python 03_read_by_dict_query.py
python 04_read_by_q_query.py
python 05_update.py
python 06_update_by_query.py
python 07_delete.py
python 08_delete_by_query.py
python 09_drop_db.py
```
