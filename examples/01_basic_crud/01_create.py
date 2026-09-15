"""01_create.py - Single Responsibility: CREATE

Creates and inserts single and multiple User records into disk database 'users_db.json'.
"""

try:
    from .dto import User
except ImportError:
    from dto import User
from wtinydb import WTinyDB

DB_FILE = "users_db.json"


def create_users():
    """Create and insert user documents into disk database."""
    print("=== Step 1: CREATE (Insert User Documents) ===")

    with WTinyDB(User, db_path=DB_FILE) as db:
        db.clear()

        # Insert single user instance
        alice = User(name="Alice Smith", email="alice@example.com", age=30)
        inserted_alice = db.insert(alice)
        print(f"Successfully inserted single user:")
        print(f"  - doc_id : {inserted_alice.doc_id}")
        print(f"  - Name   : '{inserted_alice.name}'")
        print(f"  - Email  : '{inserted_alice.email}'")

        # Insert multiple user instances
        batch_users = [
            User(name="Bob Jones", email="bob@example.com", age=25),
            User(name="Charlie Brown", email="charlie@example.com", age=40),
        ]
        inserted_batch = db.insert_many(batch_users)
        print(f"\nBatch inserted {len(inserted_batch)} users:")
        for user in inserted_batch:
            print(f"  - doc_id : {user.doc_id} | Name: '{user.name}' ({user.email})")


if __name__ == "__main__":
    create_users()
