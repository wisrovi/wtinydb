"""04_delete.py - Single Responsibility: DELETE

Deletes a user record by passing model instance or ID.
"""

try:
    from .dto import User
except ImportError:
    from dto import User
from wtinydb import WTinyDB

DB_FILE = "users_db.json"


def delete_user():
    """Delete a user document from database."""
    print("=== Step 4: DELETE (Remove User Document) ===")

    with WTinyDB(User, db_path=DB_FILE) as db:
        user_1 = db.get(1)
        if not user_1:
            print("User with doc_id=1 not found.")
            return

        print(f"Deleting user doc_id={user_1.doc_id} ('{user_1.name}')...")
        success = db.delete(user_1, hard=True)
        print(f"Delete operation returned: {success}")

        remaining = db.get_all()
        print(f"Remaining users count in '{DB_FILE}': {len(remaining)}")


if __name__ == "__main__":
    delete_user()
