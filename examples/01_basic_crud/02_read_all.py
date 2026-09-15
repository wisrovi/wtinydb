"""02_read_all.py - Single Responsibility: READ ALL & READ BY ID

Reads all user records or fetches a specific user by doc_id or field from 'users_db.json'.
"""

try:
    from .dto import User
except ImportError:
    from dto import User
from wtinydb import WTinyDB

DB_FILE = "users_db.json"


def read_users():
    """Retrieve all users and fetch specific user by doc_id or field."""
    print("=== Step 2: READ ALL & READ BY ID ===")

    with WTinyDB(User, db_path=DB_FILE) as db:
        users = db.get_all()
        print(f"Total users found in '{DB_FILE}': {len(users)}")

        for user in users:
            print(f"  - Record ID {user.doc_id}: '{user.name}' ({user.email}), Age: {user.age}")

        # Fetch explicitly by doc_id=1
        user_1 = db.get(1)
        if user_1:
            print(f"\nRetrieved directly by doc_id=1: '{user_1.name}' ({user_1.email})")

        # Fetch by field key-value
        bob = db.get_by_field("email", "bob@example.com")
        if bob:
            print(f"Retrieved by email field 'bob@example.com': '{bob.name}' (doc_id={bob.doc_id})")


if __name__ == "__main__":
    read_users()
