"""07_disk_persistence_crud/example.py

Demonstrates disk persistence with 'with' context manager.
Controlled via global CLEANUP_DB_ON_EXIT flag.
"""

import json
import os
from pydantic import BaseModel, Field
from wtinydb import WTinyDB

# Global configuration flags
DB_FILE = "my_disk_database.json"
CLEANUP_DB_ON_EXIT = False  # Set to True if temporary file cleanup is desired


class Product(BaseModel):
    """Product model for disk persistence example."""

    name: str = Field(description="Product name")
    sku: str = Field(description="Stock keeping unit")
    price: float = Field(description="Price in USD")


def session_one_write():
    """First session: Create database file on disk and insert products using 'with' block."""
    print("--- Session 1: Writing data to disk with context manager ---")

    with WTinyDB(Product, db_path=DB_FILE) as db:
        if db.count() == 0:
            p1 = db.insert(Product(name="Laptop Pro 16", sku="LAP-16", price=1999.99))
            p2 = db.insert(Product(name="Ergonomic Mouse", sku="MOU-01", price=49.99))
            print(f"Inserted initial products into physical file: '{DB_FILE}'")
        else:
            print(f"File '{DB_FILE}' already contains {db.count()} document(s). Skipping initial insert.")


def session_two_read_and_modify():
    """Second session: Re-open physical file from disk using 'with' block."""
    print("\n--- Session 2: Re-opening database file from disk ---")

    with WTinyDB(Product, db_path=DB_FILE) as db:
        existing_products = db.get_all()
        print(f"Loaded {len(existing_products)} products from disk:")
        for prod in existing_products:
            print(f"  - SKU: {prod.sku} | Name: {prod.name} | Price: ${prod.price}")

        if len(existing_products) > 0:
            print("\nUpdating price of product doc_id=1 on disk...")
            db.update(1, {"price": 1849.99})


def inspect_disk_file_directly():
    """Third step: Directly inspect physical JSON file contents on disk."""
    print("\n--- Direct Disk File Inspection ---")
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            raw_json = json.load(f)
        print(f"Raw contents of physical file '{DB_FILE}':")
        print(json.dumps(raw_json, indent=2))


def main():
    print("=== WTinyDB Disk Persistence (Context Manager 'with') Example ===")
    session_one_write()
    session_two_read_and_modify()
    inspect_disk_file_directly()

    if CLEANUP_DB_ON_EXIT and os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"\nCleaned up temp file '{DB_FILE}'")
    else:
        print(f"\nDatabase persisted on disk at: '{os.path.abspath(DB_FILE)}'")


if __name__ == "__main__":
    main()
