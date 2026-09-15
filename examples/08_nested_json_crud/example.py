"""08_nested_json_crud/example.py

Master runner executing all single-responsibility CRUD scripts for Example 08 in sequence:
- 01_create.py
- 02_read.py
- 03_update.py
- 04_delete.py
- 05_drop_db.py
"""

import sys
from pathlib import Path

# Add current example directory to sys.path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import importlib


def main():
    print("=== WTinyDB Example 08: Single-Responsibility Modular CRUD ===")

    # Run Step 1: Create
    create_module = importlib.import_module("01_create")
    create_module.create_nested_company()

    print("\n----------------------------------------\n")

    # Run Step 2: Read
    read_module = importlib.import_module("02_read")
    read_module.read_nested_company()

    print("\n----------------------------------------\n")

    # Run Step 3: Update
    update_module = importlib.import_module("03_update")
    update_module.update_nested_company()

    print("\n----------------------------------------\n")

    # Run Step 4: Delete
    delete_module = importlib.import_module("04_delete")
    delete_module.delete_nested_company()

    print("\n----------------------------------------\n")

    # Run Step 5: Drop DB
    drop_module = importlib.import_module("05_drop_db")
    drop_module.drop_database_file()


if __name__ == "__main__":
    main()
