"""01_create.py - Single Responsibility: CREATE

Inserts a 5-level nested Pydantic Company document into disk database 'nested_company_db.json'.
"""

import sys
from pathlib import Path

# Add example directory to sys.path to allow dto import when executed directly
sys.path.insert(0, str(Path(__file__).parent))

from dto import Address, Company, ContactInfo, Department, GeoCoordinates, Manager
from wtinydb import WTinyDB

DB_FILE = "nested_company_db.json"


def create_nested_company():
    """Create and insert a 5-level nested company document into disk database."""
    print("=== Step 1: CREATE (Insert 5-Level Nested Company) ===")

    # Construct nested Pydantic DTO
    nested_company = Company(
        company_name="TechCorp Global",
        department=Department(
            name="Artificial Intelligence",
            budget=5000000.00,
            manager=Manager(
                name="Dr. Sarah Connor",
                title="VP of AI Systems",
                contact=ContactInfo(
                    email="sarah.connor@techcorp.com",
                    phone="+1-555-0199",
                    address=Address(
                        street="100 Innovation Way",
                        city="San Francisco",
                        country="USA",
                        geo=GeoCoordinates(lat=37.7749, lon=-122.4194),
                    ),
                ),
            ),
        ),
    )

    with WTinyDB(Company, db_path=DB_FILE) as db:
        inserted = db.insert(nested_company)
        print(f"Successfully inserted record into '{DB_FILE}':")
        print(f"  - Assigned doc_id (direct property) : {inserted.doc_id}")
        print(f"  - Company Name                       : '{inserted.company_name}'")
        print(f"  - Dept (Level 2)                     : {inserted.department.name}")
        print(f"  - Manager (Level 3)                  : {inserted.department.manager.name}")
        print(f"  - City (Level 4)                     : {inserted.department.manager.contact.address.city}")
        print(f"  - Geo Lat (Level 5)                  : {inserted.department.manager.contact.address.geo.lat}")


if __name__ == "__main__":
    create_nested_company()
