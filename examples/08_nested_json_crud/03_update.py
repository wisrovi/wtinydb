"""03_update.py - Single Responsibility: UPDATE

Updates nested document fields on disk using model instance resolution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def update_nested_company():
    """Update nested manager title in disk database."""
    print("=== Step 3: UPDATE (Modify Nested Document Data) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        records = db.get_all()
        if not records:
            print("No records found to update. Please run 01_create.py first.")
            return

        company_to_update = records[0]
        print(f"Updating manager title for company doc_id={company_to_update.doc_id}...")

        # Update nested title passing company_to_update instance directly
        db.update(company_to_update, {
            "department": {
                "name": company_to_update.department.name,
                "budget": 5500000.00,
                "manager": {
                    "name": company_to_update.department.manager.name,
                    "title": "Chief AI Officer (CAIO)",
                    "contact": company_to_update.department.manager.contact.model_dump(),
                },
            }
        })

        updated = db.get(company_to_update)
        print(f"Successfully updated Manager Title to: '{updated.department.manager.title}'")


if __name__ == "__main__":
    update_nested_company()
