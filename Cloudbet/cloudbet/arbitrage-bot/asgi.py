"""
Entry point for Railway deployment - creates FastAPI app instance for Uvicorn.
"""
import os
from src.dashboard.app import DashboardApp

# Create the dashboard app instance
dashboard = DashboardApp(db_path="data/arbitrage_events.db")

# Get the FastAPI app
app = dashboard.get_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
