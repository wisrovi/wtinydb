"""02_read_all.py - Single Responsibility: STANDARD READ

Retrieves all company documents from disk database using standard `get_all()` and `get(doc_id)`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def read_all_companies():
    """Retrieve all companies using standard get_all() method."""
    print("=== Step 2: READ ALL (Standard Document Retrieval) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        if db.count() == 0:
            print("Database is empty. Please run 01_create.py first.")
            return

        all_companies = db.get_all()
        print(f"Retrieved {len(all_companies)} company document(s) from '{DB_FILE}':")
        for company in all_companies:
            print(f"  - doc_id={company.doc_id} | Company: '{company.company_name}' | Dept: {company.department.name}")


if __name__ == "__main__":
    read_all_companies()
