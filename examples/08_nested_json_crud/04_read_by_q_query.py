"""04_read_by_q_query.py - Single Responsibility: READ BY Q QUERY

Queries deeply nested records using Q expression (dotted notation).
Demonstrates querying at N-level depth (e.g. level 4: city).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import Q, WTinyDB

DB_FILE = "nested_company_db.json"


def read_by_q_query():
    """Query documents using Q builder with dotted nested field notation."""
    print("=== Step 4: READ BY Q QUERY (N-Level Nested Dotted Path) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        # Query level 4 nested field: department.manager.contact.address.city
        query = Q("department.manager.contact.address.city").eq("San Francisco")
        results = db.find(query)

        print(f"Query Q('department.manager.contact.address.city').eq('San Francisco'): Found {len(results)} record(s)")

        for comp in results:
            print(f"  - Record ID : {comp.doc_id}")
            print(f"  - Company   : '{comp.company_name}'")
            print(f"  - City      : {comp.department.manager.contact.address.city}")
            print(f"  - Geo Lat   : {comp.department.manager.contact.address.geo.lat}")


if __name__ == "__main__":
    read_by_q_query()
