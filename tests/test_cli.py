"""Unit tests for WTinyDB command-line interface (CLI)."""

import sys
from unittest.mock import patch
from pydantic import BaseModel
from wtinydb import WTinyDB
from wtinydb.cli.main import main


class Task(BaseModel):
    """Task model for CLI test."""

    title: str


def test_cli_inspect_and_count(tmp_path):
    """Validates CLI inspect and count subcommands on a temporary JSON database file."""
    db_file = str(tmp_path / "test_cli.json")
    db = WTinyDB(Task, db_path=db_file)
    db.insert(Task(title="Do homework"))
    db.insert(Task(title="Buy milk"))
    db.close()

    # Test CLI inspect command
    test_args = ["wtinydb", "inspect", db_file]
    with patch.object(sys, "argv", test_args):
        main()

    # Test CLI count command
    test_args_count = ["wtinydb", "count", db_file, "--table", "task"]
    with patch.object(sys, "argv", test_args_count):
        main()
