"""06_delete.py - Single Responsibility: STANDARD DELETE

Deletes a document from the database by passing the model instance directly to `db.delete()`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def delete_company():
    """Delete company document by passing model instance."""
    print("=== Step 6: DELETE (Delete Document by Model Instance) ===")

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
    delete_company()
