"""03_read_by_query.py - Single Responsibility: READ BY QUERY (Q Helper)

Queries nested documents using dotted path notation with `Q("path").eq(val)`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import Q, WTinyDB

DB_FILE = "nested_company_db.json"


def read_by_query():
    """Query nested documents by dotted field path."""
    print("=== Step 3: READ BY QUERY (Nested Path Matching with Q) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        if db.count() == 0:
            print("Database is empty. Please run 01_create.py first.")
            return

        print("Querying path 'department.manager.contact.address.city' == 'San Francisco'...")
        results = db.find(Q("department.manager.contact.address.city").eq("San Francisco"))

        print(f"Found {len(results)} matching record(s):")
        for company in results:
            print(f"  - doc_id={company.doc_id} | Name: '{company.company_name}' | Manager: {company.department.manager.name}")


if __name__ == "__main__":
    read_by_query()
