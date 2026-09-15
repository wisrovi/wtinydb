#!/usr/bin/env bash
set -e

echo "=== Running WTinyDB Code Coverage Analysis ==="
pytest --cov=wtinydb --cov-report=term-missing --cov-report=html:coverage_html tests/
echo "=== Coverage report generated in coverage_html/ index.html ==="
