"""09_drop_db.py - Single Responsibility: DROP DATABASE / CLEANUP

Cleans up database file and cache associated with the nested company database.
"""

import os

try:
    from .dto import Company
except ImportError:
    from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def drop_database():
    """Drop the database tables/files completely."""
    print("=== Step 9: DROP DATABASE (Cleanup) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        db.clear()
        print(f"Cleared all records in WTinyDB instance for '{DB_FILE}'.")

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed disk database file '{DB_FILE}'. Clean state restored.")
    else:
        print(f"Database file '{DB_FILE}' already removed.")


if __name__ == "__main__":
    drop_database()
