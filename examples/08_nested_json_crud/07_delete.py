"""07_delete.py - Single Responsibility: DELETE BY ID / MODEL INSTANCE

Deletes a record from the database by passing its model instance or ID.
WTinyDB internally resolves doc_id from the Pydantic instance.
"""

try:
    from .dto import Company
except ImportError:
    from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def delete_company():
    """Delete a company record directly by instance."""
    print("=== Step 7: DELETE BY MODEL INSTANCE ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        companies = db.get_all()
        if not companies:
            print("No records available to delete.")
            return

        target_company = companies[0]
        target_id = target_company.doc_id
        print(f"Targeting record ID {target_id} ('{target_company.company_name}') for deletion...")

        # Pass model instance directly to db.delete()
        success = db.delete(target_company)
        print(f"Delete operation returned: {success}")

        # Verify deletion
        remaining = db.get_all()
        print(f"Remaining records in '{DB_FILE}': {len(remaining)}")


if __name__ == "__main__":
    delete_company()
