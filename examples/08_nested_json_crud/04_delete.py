"""04_delete.py - Single Responsibility: DELETE

Deletes a company document record from the disk database.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def delete_nested_company():
    """Delete company document from disk database."""
    print("=== Step 4: DELETE (Delete Record from Disk) ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        records = db.get_all()
        if not records:
            print("No records found to delete.")
            return

        target_company = records[0]
        print(f"Deleting company record doc_id={target_company.doc_id} ('{target_company.company_name}')...")

        # Pass target_company instance directly to delete()
        db.delete(target_company, hard=True)
        print(f"Record deleted. Remaining count in DB: {db.count()}")


if __name__ == "__main__":
    delete_nested_company()
