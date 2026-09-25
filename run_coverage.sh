#!/usr/bin/env bash
set -e

echo "=== Calculating Code Coverage for WTinyDB ==="
PYTHONPATH=. pytest --cov=wtinydb --cov-report=term-missing --cov-report=html tests/
echo "=== Coverage Report Generated in htmlcov/index.html ==="
