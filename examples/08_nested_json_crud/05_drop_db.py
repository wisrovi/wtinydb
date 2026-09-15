"""05_drop_db.py - Single Responsibility: DROP DATABASE FILE

Deletes the physical JSON database file from disk.
"""

import os

DB_FILE = "nested_company_db.json"


def drop_database_file():
    """Delete physical JSON database file from disk."""
    print("=== Step 5: DROP DATABASE (Clean Up Disk File) ===")

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Successfully deleted physical database file: '{DB_FILE}'")
    else:
        print(f"File '{DB_FILE}' does not exist on disk.")


if __name__ == "__main__":
    drop_database_file()
