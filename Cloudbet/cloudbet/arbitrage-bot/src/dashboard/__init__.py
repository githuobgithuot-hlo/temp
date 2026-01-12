"""
Dashboard module - exports FastAPI app for uvicorn.
"""
import os
from pathlib import Path

# Get database path from environment or use default
db_path = os.getenv("DATABASE_PATH", "data/arbitrage_events.db")

# Ensure data directory exists
Path(db_path).parent.mkdir(parents=True, exist_ok=True)

# Import and create dashboard app
from .app import DashboardApp

# Create dashboard app instance
dashboard_app = DashboardApp(db_path=db_path)

# Export FastAPI app for uvicorn
app = dashboard_app.get_app()

