"""08_delete_by_query.py - Single Responsibility: DELETE BY QUERY

Deletes records matching query criteria.
"""

try:
    from .dto import Address, Company, ContactInfo, Department, GeoCoordinates, Manager
except ImportError:
    from dto import Address, Company, ContactInfo, Department, GeoCoordinates, Manager
from wtinydb import Q, WTinyDB

DB_FILE = "nested_company_db.json"


def delete_by_query():
    """Delete records matching a query filter."""
    print("=== Step 8: DELETE BY QUERY ===")

    with WTinyDB(Company, db_path=DB_FILE) as db:
        # First ensure a test document exists to delete via query
        test_company = Company(
            company_name="Temporary Startup",
            department=Department(
                name="Research",
                budget=100000.0,
                manager=Manager(
                    name="John Doe",
                    title="Lead Researcher",
                    contact=ContactInfo(
                        email="john@startup.io",
                        phone="+1-555-0100",
                        address=Address(
                            street="1 First St",
                            city="Seattle",
                            country="USA",
                            geo=GeoCoordinates(lat=47.6062, lon=-122.3321),
                        ),
                    ),
                ),
            ),
        )
        db.insert(test_company)
        print("Inserted temporary document 'Temporary Startup'.")

        # Delete by Q query matching company_name
        query = Q("company_name").eq("Temporary Startup")
        removed_ids = db.delete(query)
        print(f"Deleted {len(removed_ids)} document(s) matching query. Deleted doc IDs: {removed_ids}")


if __name__ == "__main__":
    delete_by_query()
