#!/bin/bash
set -e

echo "Running Postgres producer job..."
docker compose up --no-deps --build postgres-producer

echo "Postgres producer finished (or exited if 'restart: no')."
