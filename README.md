<p align="center">
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

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

- **Enterprise Forensic Automation**: Ghost table (`_forensic_audit_log`) audit trail for all document mutations (`INSERT`, `UPDATE`, `DELETE`).
- **Multi-Table Manager & Registry**: Multi-model registration with dictionary indexing `app[User]` and dynamic attribute dispatch `app.user`.
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

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)
