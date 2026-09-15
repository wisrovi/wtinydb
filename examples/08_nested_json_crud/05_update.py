"""05_update.py - Single Responsibility: UPDATE BY ID / MODEL INSTANCE

Updates specific nested fields of a record by passing the model instance directly.
WTinyDB internally resolves doc_id from the Pydantic instance.
"""

try:
    from .dto import Company
except ImportError:
    from dto import Company
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def update_company():
    """Update a nested company record directly by instance."""
    print("=== Step 5: UPDATE BY MODEL INSTANCE ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        companies = db.get_all()
        if not companies:
            print("No records found to update.")
            return

        target_company = companies[0]
        print(f"Original record ID {target_company.doc_id}:")
        print(f"  - Dept Budget : ${target_company.department.budget:,.2f}")
        print(f"  - City        : {target_company.department.manager.contact.address.city}")

        # Update deep nested fields (Level 2 budget, Level 4 city)
        update_data = {
            "department.budget": 7500000.00,
            "department.manager.contact.address.city": "Austin",
            "department.manager.contact.address.geo.lat": 30.2672,
            "department.manager.contact.address.geo.lon": -97.7431,
        }

        # Pass target_company instance directly; WTinyDB extracts target_company.doc_id
        db.update(target_company, update_data)
        print("\nUpdated fields successfully!")

        # Verify update
        updated_comp = db.get(target_company.doc_id)
        if updated_comp:
            print(f"Verified Record ID {updated_comp.doc_id}:")
            print(f"  - New Dept Budget : ${updated_comp.department.budget:,.2f}")
            print(f"  - New City        : {updated_comp.department.manager.contact.address.city}")
            print(f"  - New Lat/Lon     : {updated_comp.department.manager.contact.address.geo.lat}, {updated_comp.department.manager.contact.address.geo.lon}")


if __name__ == "__main__":
    update_company()
