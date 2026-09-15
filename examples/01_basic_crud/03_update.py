"""03_update.py - Single Responsibility: UPDATE

Updates fields of a user record by passing model instance or ID.
"""

try:
    from .dto import User
except ImportError:
    from dto import User
from wtinydb import WTinyDB

DB_FILE = "users_db.json"


def update_user():
    """Update fields of a user document."""
    print("=== Step 3: UPDATE (Update User Fields) ===")

    with WTinyDB(User, db_path=DB_FILE) as db:
        user_1 = db.get(1)
        if not user_1:
            print("User with doc_id=1 not found.")
            return

        print(f"Original doc_id=1: Name='{user_1.name}', Age={user_1.age}")

        # Update age using target model instance directly
        updated = db.update(user_1, {"age": 31})
        print(f"Updated doc_id={updated.doc_id} successfully: Name='{updated.name}', New Age={updated.age}")


if __name__ == "__main__":
    update_user()
