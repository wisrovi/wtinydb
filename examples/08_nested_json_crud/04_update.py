"""04_update.py - Single Responsibility: STANDARD UPDATE

Updates nested document fields by passing the model instance directly to `db.update()`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def update_company():
    """Update nested manager title by model instance."""
    print("=== Step 4: UPDATE (Standard Document Update by Model Instance) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        records = db.get_all()
        if not records:
            print("No records found to update. Please run 01_create.py first.")
            return

        target_company = records[0]
        print(f"Updating manager title for company doc_id={target_company.doc_id}...")

        # Update nested title passing target_company instance directly
        db.update(target_company, {
            "department": {
                "name": target_company.department.name,
                "budget": 5500000.00,
                "manager": {
                    "name": target_company.department.manager.name,
                    "title": "Chief AI Officer (CAIO)",
                    "contact": target_company.department.manager.contact.model_dump(),
                },
            }
        })

        updated = db.get(target_company)
        print(f"Successfully updated Manager Title to: '{updated.department.manager.title}'")


if __name__ == "__main__":
    update_company()
