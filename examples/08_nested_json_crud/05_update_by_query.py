"""05_update_by_query.py - Single Responsibility: UPDATE BY QUERY

Updates collection documents matching a query filter condition (WMongo style).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def update_by_query():
    """Update documents matching collection query filter."""
    print("=== Step 5: UPDATE BY QUERY (Collection Query Update) ===")

    with WTinyDB(db_path=DB_FILE) as db:
        print("Updating collection 'company' matching query {'company_name': 'TechCorp Global'}...")
        count = db.update(
            "company",
            {"company_name": "TechCorp Global"},
            {"company_name": "TechCorp Enterprise Global"},
        )
        print(f"Updated {count} document(s) matching query filter.")


if __name__ == "__main__":
    update_by_query()
