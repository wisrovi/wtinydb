"""07_delete_by_query.py - Single Responsibility: DELETE BY QUERY

Deletes collection documents matching a query filter condition (WMongo style).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def delete_by_query():
    """Delete documents matching collection query filter."""
    print("=== Step 7: DELETE BY QUERY (Collection Query Delete) ===")

    with WTinyDB(db_path=DB_FILE) as db:
        print("Deleting collection 'company' records matching query {'company_name': 'TechCorp Enterprise Global'}...")
        count = db.delete("company", {"company_name": "TechCorp Enterprise Global"})
        print(f"Deleted {count} document(s) matching query filter.")


if __name__ == "__main__":
    delete_by_query()
