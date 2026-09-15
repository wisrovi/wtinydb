"""05_drop_db.py - Single Responsibility: DROP DATABASE / CLEANUP

Cleans up database file and clears tables associated with 'users_db.json'.
"""

import os

try:
    from .dto import User
except ImportError:
    from dto import User
from wtinydb import WTinyDB

DB_FILE = "users_db.json"


def drop_database():
    """Clear tables and remove database file from disk."""
    print("=== Step 5: DROP DATABASE (Cleanup) ===")

    with WTinyDB(User, db_path=DB_FILE) as db:
        db.clear()
        print(f"Cleared all records in WTinyDB instance for '{DB_FILE}'.")

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed disk database file '{DB_FILE}'. Clean state restored.")
    else:
        print(f"Database file '{DB_FILE}' already removed.")


if __name__ == "__main__":
    drop_database()
