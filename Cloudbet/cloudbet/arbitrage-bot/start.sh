#!/bin/bash
set -e

echo "Starting Cloudbet Arbitrage Bot..."

# Create virtual environment if it doesn't exist
if [ ! -d "/opt/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv --copies /opt/venv
fi

# Activate virtual environment
source /opt/venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the application
echo "Starting application..."

# Determine which process to start based on PROCESS environment variable
if [ "$PROCESS_TYPE" = "web" ]; then
    echo "Starting web service..."
    python -m uvicorn asgi:app --host 0.0.0.0 --port ${PORT:-8000}
elif [ "$PROCESS_TYPE" = "worker" ]; then
    echo "Starting worker process..."
    python src/main.py
else
    # Default to web service if not specified
    echo "No process type specified, starting web service..."
    python -m uvicorn asgi:app --host 0.0.0.0 --port ${PORT:-8000}
fi
