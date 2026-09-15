"""04_soft_delete_and_audit/example.py

Demonstrates AuditMixin timestamps and logical soft delete in WTinyDB.
"""

from pydantic import BaseModel
from wtinydb import AuditMixin, WTinyDB


class Article(AuditMixin, BaseModel):
    """Article model with full audit capabilities."""

    title: str
    body: str


def main():
    print("=== WTinyDB Soft Delete & Audit Mixin Example ===")

    db = WTinyDB(Article, in_memory=True)

    # 1. Insert article with auto creation timestamp
    art = db.insert(Article(title="WTinyDB Release", body="WTinyDB 0.1.0 is released!"))
    print(f"Created Article at UTC: {art.created_at}")

    # 2. Perform soft delete
    print("\nPerforming soft delete on doc_id=1...")
    db.delete(1, hard=False)

    # 3. Query active vs all documents
    active_articles = db.get_all(include_deleted=False)
    print(f"Active articles count: {len(active_articles)}")

    all_articles = db.get_all(include_deleted=True)
    print(f"All articles count (including deleted): {len(all_articles)}")
    print(f"Deleted flag: {all_articles[0].is_deleted}, Deleted at: {all_articles[0].deleted_at}")

    db.close()


if __name__ == "__main__":
    main()
