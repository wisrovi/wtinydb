"""08_nested_json_crud/example.py

Demonstrates N-level nested JSON object storage, retrieval, and dotted field querying in WTinyDB.
WTinyDB handles document IDs internally (accessible directly via `inserted_company.doc_id` or passing model instances directly).
"""

import json
import os
from typing import Dict, Optional
from pydantic import BaseModel, Field
from wtinydb import Q, WTinyDB

# Global configuration flags
DB_FILE = "nested_company_db.json"
CLEANUP_DB_ON_EXIT = False


# Level 4 Model: GeoLocation & Address
class GeoCoordinates(BaseModel):
    lat: float
    lon: float


class Address(BaseModel):
    street: str
    city: str
    country: str
    geo: GeoCoordinates


# Level 3 Model: Contact & Manager
class ContactInfo(BaseModel):
    email: str
    phone: str
    address: Address


class Manager(BaseModel):
    name: str
    title: str
    contact: ContactInfo


# Level 2 Model: Department
class Department(BaseModel):
    name: str
    budget: float
    manager: Manager


# Level 1 Model: Company (Root Document)
class Company(BaseModel):
    company_name: str
    department: Department


def run_nested_json_example():
    print("=== WTinyDB N-Level Nested JSON CRUD Example ===")

    # Initialize WTinyDB with disk persistence
    with WTinyDB(Company, db_path=DB_FILE) as db:
        db.clear()

        # Construct a 5-level nested document
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

        # 1. CREATE: Insert model instance. WTinyDB automatically populates .doc_id and .id
        inserted_company = db.insert(nested_company)
        
        print(f"1. CREATE -> Inserted Company into disk DB:")
        print(f"   - Assigned doc_id (direct property) : {inserted_company.doc_id}")
        print(f"   - Company Name                       : '{inserted_company.company_name}'")
        print(f"   - Dept (Level 2)                     : {inserted_company.department.name}")
        print(f"   - Manager (Level 3)                  : {inserted_company.department.manager.name}")
        print(f"   - City (Level 4)                     : {inserted_company.department.manager.contact.address.city}")
        print(f"   - Geo Lat (Level 5)                  : {inserted_company.department.manager.contact.address.geo.lat}")

        # 2. READ / QUERY: Search by nested dotted field path
        print(f"\n2. READ -> Querying nested path 'department.manager.contact.address.city' == 'San Francisco'...")
        results = db.find(Q("department.manager.contact.address.city").eq("department.manager.contact.address.city", "San Francisco"))
        
        found_company = results[0]
        print(f"   - Found record with doc_id={found_company.doc_id}: '{found_company.company_name}'")

        # 3. UPDATE: Pass the inserted_company instance directly to db.update()! WTinyDB resolves ID internally.
        print(f"\n3. UPDATE -> Modifying nested manager title using inserted_company instance directly...")
        db.update(inserted_company, {
            "department": {
                "name": "Artificial Intelligence",
                "budget": 5500000.00,
                "manager": {
                    "name": "Dr. Sarah Connor",
                    "title": "Chief AI Officer (CAIO)",
                    "contact": inserted_company.department.manager.contact.model_dump(),
                },
            }
        })

        # Re-fetch document using inserted_company instance directly
        updated_company = db.get(inserted_company)
        print(f"   - Updated Manager Title: '{updated_company.department.manager.title}'")


def inspect_disk_file_json():
    """Inspect raw JSON on disk to verify true nested hierarchy storage."""
    print("\n--- Direct Disk JSON File Inspection ---")
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Raw contents of physical file '{DB_FILE}':")
        print(json.dumps(data, indent=2))


def main():
    run_nested_json_example()
    inspect_disk_file_json()

    if CLEANUP_DB_ON_EXIT and os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"\nCleaned up temp file '{DB_FILE}'")
    else:
        print(f"\nDatabase persisted on disk at: '{os.path.abspath(DB_FILE)}'")


if __name__ == "__main__":
    main()
