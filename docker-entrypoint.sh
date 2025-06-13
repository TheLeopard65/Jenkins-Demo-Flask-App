#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=production

# Load environment variables from .env if present
if [ -f .env ]; then
    echo "[#] Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
fi

echo "[#] Running database migrations"
flask db init
flask db migrate -m "Initial Migration"
flask db upgrade

echo "[#] Starting Flask app"
exec flask run --host=0.0.0.0
