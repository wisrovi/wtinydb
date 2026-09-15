"""03_read_by_dict_query.py - Single Responsibility: READ BY DICTIONARY QUERY

Queries nested records using standard dictionary mapping WITHOUT using Q.
Demonstrates collection-style query matching (similar to WMongo).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def read_by_dict_query():
    """Query documents using dictionary key-value matching without Q."""
    print("=== Step 3: READ BY DICTIONARY QUERY (Without Q) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        # Match company_name at top level
        results = db.find({"company_name": "TechCorp Global"})
        print(f"Query matching {{'company_name': 'TechCorp Global'}}: Found {len(results)} record(s)")

        for comp in results:
            print(f"  - Record ID : {comp.doc_id}")
            print(f"  - Company   : '{comp.company_name}'")
            print(f"  - Manager   : {comp.department.manager.name}")


if __name__ == "__main__":
    read_by_dict_query()
