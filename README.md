# WTinyDB: Lightweight Pydantic Document Database Engine

`wtinydb` is a high-level, document-oriented NoSQL database abstraction built on top of **TinyDB** and **Pydantic**. It provides schema-validated CRUD operations, fluent query builders, async support, audit mixins, and command-line management for embedded Python applications.

## Key Technologies & Libraries

- **[TinyDB](https://tinydb.readthedocs.io/)**: Pure Python document-oriented database storing records as JSON.
- **[Pydantic v2](https://docs.pydantic.dev/)**: Data validation, settings management, and JSON-schema document serialization.
- **[Pytest](https://docs.pytest.org/)**: Modern Python testing framework.
- **[Pytest-Cov](https://pytest-cov.readthedocs.io/)**: Code coverage measurement for pytest.
- **[Docker](https://www.docker.com/)**: Containerization for reproducible testing environments.

---

## Features

- **Pydantic Model Mapping**: Automatic serialization, deserialization, and schema validation.
- **Fluent Query Builder (`Q`)**: Intuitive query building with comparison operators, regex matching, and text search.
- **Async Support (`AsyncWTinyDB`)**: Non-blocking thread-pool execution for FastAPI and Starlette apps.
- **Soft Delete & Audit Mixins**: Built-in support for `created_at`, `updated_at`, `is_deleted`, and `deleted_at`.
- **Thread Safety**: Integrated reentrant locks for safe multi-threaded access.
- **CLI Utility**: Command-line tool `wtinydb` to inspect, count, and export JSON tables.

---

## Quickstart Example

```python
from pydantic import BaseModel, Field
from wtinydb import WTinyDB, Q, SoftDeleteMixin

# Define document schema
class User(SoftDeleteMixin, BaseModel):
    name: str
    email: str = Field(description="User email")
    age: int = 18

# Initialize WTinyDB repository (in-memory or file-backed)
db = WTinyDB(User, in_memory=True)

# 1. Insert
user = db.insert(User(name="Alice", email="alice@example.com", age=30))

# 2. Query
results = db.find(Q("age").gte("age", 25))

# 3. Soft Delete & Restore
db.delete(1, hard=False)
```

---

## Running Unit Tests & Coverage

### Local Pytest Execution

```bash
# Run pytest test suite
pytest tests/

# Calculate code coverage
./scripts/run_coverage.sh
```

### Docker Containerized Test Execution

All unit tests can be executed inside an isolated Docker container:

```bash
./scripts/run_tests_docker.sh
```

---

*Part of the wisrovi SUITE ecosystem.*