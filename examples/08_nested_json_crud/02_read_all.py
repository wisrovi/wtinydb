"""02_read_all.py - Single Responsibility: READ ALL / READ BY ID

Reads all records or fetches a specific record by ID from 'nested_company_db.json'.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def read_all_companies():
    """Retrieve all nested companies and fetch by ID."""
    print("=== Step 2: READ ALL & READ BY ID ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        companies = db.get_all()
        print(f"Total companies found in '{DB_FILE}': {len(companies)}")

        for comp in companies:
            print(f"\n[Record ID {comp.doc_id}]")
            print(f"  - Company Name : '{comp.company_name}'")
            print(f"  - Department   : {comp.department.name}")
            print(f"  - Manager      : {comp.department.manager.name}")

            # Fetch explicitly by ID
            by_id = db.get(comp.doc_id)
            if by_id:
                print(f"  -> Verified fetch by ID {comp.doc_id}: Found '{by_id.company_name}'")


if __name__ == "__main__":
    read_all_companies()
