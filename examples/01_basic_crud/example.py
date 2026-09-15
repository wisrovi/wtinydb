"""01_basic_crud/example.py

Demonstrates basic CRUD operations with WTinyDB and Pydantic models.
"""

from pydantic import BaseModel, Field
from wtinydb import WTinyDB


class User(BaseModel):
    """User document model."""

    name: str = Field(description="Full user name")
    email: str = Field(description="Email address")
    age: int = Field(default=18, description="Age in years")


def main():
    print("=== WTinyDB Basic CRUD Example ===")

    # Initialize in-memory database
    db = WTinyDB(User, in_memory=True)

    # 1. CREATE (Insert single and batch)
    user1 = db.insert(User(name="Alice Smith", email="alice@example.com", age=30))
    print(f"Inserted User: {user1.name} with doc_id={getattr(user1, '_doc_id', 1)}")

    users = [
        User(name="Bob Jones", email="bob@example.com", age=25),
        User(name="Charlie Brown", email="charlie@example.com", age=40),
    ]
    db.insert_many(users)
    print(f"Total users in DB: {db.count()}")

    # 2. READ (Get by ID, field, get_all)
    first_user = db.get(1)
    print(f"Retrieved doc_id=1: {first_user.name} ({first_user.email})")

    bob = db.get_by_field("email", "bob@example.com")
    print(f"Retrieved by email: {bob.name} (age {bob.age})")

    # 3. UPDATE
    updated_user = db.update(1, {"age": 31})
    print(f"Updated doc_id=1 age: {updated_user.age}")

    # 4. DELETE
    db.delete(1, hard=True)
    print(f"After deletion count: {db.count()}")

    db.close()


if __name__ == "__main__":
    main()
