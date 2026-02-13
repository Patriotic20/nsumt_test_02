#!/bin/bash
set -e

# Navigate to the directory where alembic.ini is located
cd /face/app

echo "Running migrations..."
# Use 'uv run' to execute alembic within the virtual environment
uv run alembic upgrade head

echo "Migrations completed. Starting application..."

# Execute the CMD (also using uv run to ensure the app sees the packages)
exec uv run "$@"