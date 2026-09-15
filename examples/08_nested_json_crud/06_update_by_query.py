"""06_update_by_query.py - Single Responsibility: UPDATE BY QUERY

Updates records matching query criteria.
"""

try:
    from .dto import Company
except ImportError:
    from dto import Company
from wtinydb import Q, WTinyDB

DB_FILE = "nested_company_db.json"


def update_by_query():
    """Update nested company documents matching a query."""
    print("=== Step 6: UPDATE BY QUERY ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        # Match company where city is San Francisco
        query = Q("department.manager.contact.address.city").eq("San Francisco")

        update_payload = {
            "department.name": "AI & Advanced Robotics",
            "department.manager.title": "Chief AI Officer",
        }

        updated_ids = db.update(query, update_payload)
        print(f"Updated {len(updated_ids)} document(s) matching query. Updated doc IDs: {updated_ids}")

        for doc_id in updated_ids:
            comp = db.get(doc_id)
            if comp:
                print(f"  - Record ID {comp.doc_id} New Dept Name : '{comp.department.name}'")
                print(f"  - Record ID {comp.doc_id} New Title     : '{comp.department.manager.title}'")


if __name__ == "__main__":
    update_by_query()
