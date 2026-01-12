"""
FastAPI dashboard for monitoring arbitrage bot.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import json

from ..database import ArbitrageDatabase
from ..logger import setup_logger


class DashboardApp:
    """FastAPI application for arbitrage bot dashboard."""
    
    def __init__(self, db_path: str, port: int = 8000):
        self.app = FastAPI(title="Arbitrage Bot Dashboard")
        self.db = ArbitrageDatabase(db_path)
        self.port = port
        self.logger = setup_logger("dashboard")
        
        # Setup templates
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        self.templates = Jinja2Templates(directory=str(template_dir))
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint for Railway health checks."""
            return {"status": "ok", "service": "dashboard"}
        
        @self.app.get("/health")
        async def health():
            """Health check endpoint for Railway."""
            try:
                # Try to access database to ensure it's working
                self.db.get_statistics()
                return {"status": "ok", "service": "dashboard", "database": "connected"}
            except Exception as e:
                # Even if DB fails, return ok so Railway doesn't restart
                self.logger.warning(f"Health check DB error: {e}")
                return {"status": "ok", "service": "dashboard", "database": "warning"}
        
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page."""
            try:
                stats = self.db.get_statistics()
            except Exception as e:
                self.logger.error(f"Error getting statistics: {e}")
                stats = {
                    'total_opportunities': 0,
                    'alerted_opportunities': 0,
                    'total_profit': 0.0,
                    'average_profit_percentage': 0.0,
                    'recent_opportunities_24h': 0
                }
            
            try:
                recent = self.db.get_recent_opportunities(limit=5)
            except Exception as e:
                self.logger.error(f"Error getting recent opportunities: {e}")
                recent = []
            
            return self.templates.TemplateResponse(
                "dashboard.html",
                {
                    "request": request,
                    "stats": stats,
                    "recent_opportunities": recent,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        @self.app.get("/opportunities", response_class=HTMLResponse)
        async def opportunities(request: Request, limit: int = 100):
            """List all arbitrage opportunities."""
            opps = self.db.get_all_opportunities(limit=limit)
            
            return self.templates.TemplateResponse(
                "opportunities.html",
                {
                    "request": request,
                    "opportunities": opps,
                    "limit": limit,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        @self.app.get("/logs", response_class=HTMLResponse)
        async def logs(request: Request):
            """View recent logs and errors."""
            # Read recent log entries (last 100 lines)
            # Use absolute path relative to bot root
            bot_root = Path(__file__).parent.parent.parent.parent
            log_file = bot_root / "logs" / "arbitrage_bot.log"
            log_entries = []
            
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        # Get last 100 lines
                        log_entries = lines[-100:]
                except Exception as e:
                    self.logger.error(f"Error reading log file: {e}")
            
            return self.templates.TemplateResponse(
                "logs.html",
                {
                    "request": request,
                    "log_entries": log_entries,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        @self.app.get("/api/stats")
        async def api_stats():
            """API endpoint for statistics (JSON)."""
            try:
                return self.db.get_statistics()
            except Exception as e:
                self.logger.error(f"Error getting statistics: {e}")
                return {
                    'total_opportunities': 0,
                    'alerted_opportunities': 0,
                    'total_profit': 0.0,
                    'average_profit_percentage': 0.0,
                    'recent_opportunities_24h': 0,
                    'error': str(e)
                }
        
        @self.app.get("/api/opportunities")
        async def api_opportunities(limit: int = 100):
            """API endpoint for opportunities (JSON)."""
            try:
                return self.db.get_all_opportunities(limit=limit)
            except Exception as e:
                self.logger.error(f"Error getting opportunities: {e}")
                return {"error": str(e), "opportunities": []}
    
    def get_app(self):
        """Get FastAPI app instance."""
        return self.app

