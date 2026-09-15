#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Building Docker test image for WTinyDB ==="
docker build -t wtinydb-tests -f "$SCRIPT_DIR/Dockerfile" "$REPO_DIR"

echo "=== Running WTinyDB Unit Tests inside Docker ==="
docker run --rm wtinydb-tests
