"""05_fastapi_integration/example.py

Demonstrates integrating AsyncWTinyDB into a FastAPI REST service.
"""

from pydantic import BaseModel, Field
from wtinydb import AsyncWTinyDB, AuditMixin, WTinyDB


class Customer(AuditMixin, BaseModel):
    """Customer model for FastAPI endpoint payload."""

    name: str = Field(description="Customer full name")
    email: str = Field(description="Customer email address")


# Initialize Repository
sync_db = WTinyDB(Customer, in_memory=True)
db = AsyncWTinyDB(sync_db)


def demonstrate_fastapi_flow():
    """Simulate REST API request handler flow."""
    import asyncio

    async def run_handler():
        print("=== WTinyDB FastAPI Integration Simulation ===")

        # POST /customers endpoint simulation
        print("1. Handling POST /customers...")
        new_customer = Customer(name="David Miller", email="david@company.com")
        saved = await db.insert(new_customer)
        print(f"   Created customer: {saved.name} (email: {saved.email})")

        # GET /customers endpoint simulation
        print("2. Handling GET /customers...")
        customers = await db.get_all()
        print(f"   Total customers in DB: {len(customers)}")

        await db.close()

    asyncio.run(run_handler())


if __name__ == "__main__":
    demonstrate_fastapi_flow()
