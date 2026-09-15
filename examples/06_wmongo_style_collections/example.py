"""06_wmongo_style_collections/example.py

Demonstrates WMongo-compatible collection CRUD with 'with' context manager.
"""

from wtinydb import WTinyDB


def main():
    print("=== WTinyDB (WMongo Compatible Interface with 'with') Example ===")

    # Initialize WTinyDB using 'with' block (automatically closed at exit)
    with WTinyDB(db_path="my_wtinydb.json", verbose=True) as db:
        # 1. Collection-based Insert (WMongo style)
        doc_id = db.insert("users", {"user_id": "u123", "name": "Alice", "role": "admin"})
        print(f"Inserted document into 'users' collection with doc_id: {doc_id}")

        # 2. Collection-based Find
        results = db.find("users", {"role": "admin"})
        print(f"Found admin users: {results}")

        # 3. Encryption / Decryption helper
        secret = "SuperSecretPassword123!"
        encrypted = db.encrypt(secret)
        decrypted = db.decrypt(encrypted)
        print(f"Encrypted secret: {encrypted[:20]}...")
        print(f"Decrypted secret matches original: {decrypted == secret}")

        # 4. Collection-based Update & Delete
        updated_cnt = db.update("users", {"user_id": "u123"}, {"role": "superadmin"})
        print(f"Updated {updated_cnt} document(s)")

        deleted_cnt = db.delete("users", {"user_id": "u123"})
        print(f"Deleted {deleted_cnt} document(s)")


if __name__ == "__main__":
    main()
