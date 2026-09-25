# Enterprise Forensic Automation & Ghost Table Audit Trail (`wtinydb`)

This example demonstrates the **Enterprise Forensic Automation** feature introduced in `wtinydb` v1.1.0.

## Overview

When forensic mode is enabled (`forensic=True` or via `ForensicModel`), `wtinydb` automatically provisions a ghost audit log table named `_forensic_audit_log` per document database schema.

### Key Features
- **Zero Configuration**: Single `_forensic_audit_log` table captures mutation trails for all application entities.
- **Backward Compatibility**: Forensic mode is disabled by default (`forensic=False`).
- **Complete Lineage**: Captures `data_before` and `data_after` JSON payloads for `INSERT`, `UPDATE`, and `DELETE` actions.
- **Multi-Table Registry**: Seamless access using dictionary indexing `db[User]` or dynamic attributes `db.user`.

## Key Technologies & Libraries Used

- **Python 3.9+** - Modern type annotations and async support.
- **Pydantic v2** - Data validation and JSON serialization (`model_dump()`).
- **TinyDB** - Lightweight document database engine.
- **WTinyDB Engine** - Automated schema management and multi-table collection dispatcher.

## Running the Example

```bash
python examples/18_ghost_table_audit/example.py
```
