"""03_async_usage/example.py

Demonstrates AsyncWTinyDB asynchronous document operations.
"""

import asyncio
from pydantic import BaseModel
from wtinydb import AsyncWTinyDB, WTinyDB


class LogEntry(BaseModel):
    """Log Entry document model."""

    level: str
    message: str


async def main():
    print("=== WTinyDB Async Operations Example ===")

    sync_db = WTinyDB(LogEntry, in_memory=True)
    async_db = AsyncWTinyDB(sync_db)

    # 1. Async insert
    await async_db.insert(LogEntry(level="INFO", message="System started"))
    await async_db.insert(LogEntry(level="WARNING", message="High memory usage"))
    await async_db.insert(LogEntry(level="ERROR", message="Connection failed"))

    # 2. Async count
    total_logs = await async_db.count()
    print(f"Total log entries created async: {total_logs}")

    # 3. Async get all
    all_logs = await async_db.get_all()
    for log in all_logs:
        print(f"  [{log.level}] {log.message}")

    await async_db.close()


if __name__ == "__main__":
    asyncio.run(main())
