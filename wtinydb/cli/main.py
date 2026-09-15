"""WTinyDB Command Line Interface (CLI)."""

import argparse
import json
import sys
from tinydb import TinyDB


def main():
    """Main CLI entrypoint for WTinyDB commands."""
    parser = argparse.ArgumentParser(description="WTinyDB CLI Manager")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    # Command: inspect
    inspect_parser = subparsers.add_parser("inspect", help="Inspect tables in a TinyDB JSON database file")
    inspect_parser.add_argument("db_path", help="Path to TinyDB JSON file")

    # Command: count
    count_parser = subparsers.add_parser("count", help="Count documents in a table")
    count_parser.add_argument("db_path", help="Path to TinyDB JSON file")
    count_parser.add_argument("--table", default="_default", help="Table name (default: _default)")

    # Command: export
    export_parser = subparsers.add_parser("export", help="Export table content as formatted JSON")
    export_parser.add_argument("db_path", help="Path to TinyDB JSON file")
    export_parser.add_argument("--table", default="_default", help="Table name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        db = TinyDB(args.db_path)
        if args.command == "inspect":
            tables = list(db.tables())
            print(f"Database: {args.db_path}")
            print(f"Tables found: {len(tables)}")
            for t in tables:
                table_obj = db.table(t)
                print(f"  - Table '{t}': {len(table_obj)} document(s)")

        elif args.command == "count":
            table_obj = db.table(args.table)
            print(f"Table '{args.table}' contains {len(table_obj)} document(s).")

        elif args.command == "export":
            table_obj = db.table(args.table)
            docs = table_obj.all()
            print(json.dumps(docs, indent=2))

        db.close()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
