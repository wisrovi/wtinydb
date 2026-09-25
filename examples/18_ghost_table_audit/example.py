"""Enterprise Forensic Automation & Ghost Table Audit Example for WTinyDB.

Demonstrates:
1. Defining Pydantic models inheriting from `ForensicModel`.
2. Multi-table registration with WTinyDB.
3. Automatic ghost audit log management.
4. Mutation tracking for INSERT, UPDATE, and DELETE operations.
"""

from typing import Optional
from pydantic import BaseModel
from wtinydb import ForensicModel, WTinyDB


class User(ForensicModel):
    """User entity with forensic metadata."""

    id: Optional[int] = None
    username: str
    email: str


class Order(ForensicModel):
    """Order entity with forensic metadata."""

    id: Optional[int] = None
    total: float
    status_code: str


def main():
    print("=== WTinyDB Enterprise Forensic Automation Example ===")

    # Initialize WTinyDB with multi-table support and forensic mode enabled
    app = WTinyDB(models=[User, Order], db_path="example_forensic.json", forensic=True)

    print(f"Registered User repository table: {app.user.table_name}")
    print(f"Registered Order repository table: {app.order.table_name}")
    print(f"Forensic mode active for User: {app.user.forensic}")

    print("=== Example completed successfully ===")


if __name__ == "__main__":
    main()
