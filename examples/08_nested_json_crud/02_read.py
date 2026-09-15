"""02_read.py - Single Responsibility: READ & QUERY

Queries and retrieves nested company documents from disk database using dotted path notation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import Q, WTinyDB

DB_FILE = "nested_company_db.json"


def read_nested_company():
    """Query and read nested company documents from disk database."""
    print("=== Step 2: READ (Query by Dotted Path) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        if db.count() == 0:
            print("Database is empty. Please run 01_create.py first.")
            return

        # 1. Query by nested dotted path
        print("Querying path 'department.manager.contact.address.city' == 'San Francisco'...")
        results = db.find(Q("department.manager.contact.address.city").eq("San Francisco"))

        print(f"Found {len(results)} matching record(s):")
        for company in results:
            print(f"  - doc_id={company.doc_id} | Name: '{company.company_name}' | Manager: {company.department.manager.name}")


if __name__ == "__main__":
    read_nested_company()
