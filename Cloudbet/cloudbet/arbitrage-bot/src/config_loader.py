"""
Configuration loader with environment variable support.
"""
import os
from pathlib import Path
from typing import Any, Dict, Union
import yaml
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class BankrollConfig(BaseModel):
    """Bankroll configuration."""
    amount: float = Field(gt=0, description="Total capital in USD")
    kelly_fraction: float = Field(ge=0, le=1, description="Kelly multiplier (0-1)")


class ArbitrageConfig(BaseModel):
    """Arbitrage detection configuration."""
    min_profit_threshold: float = Field(gt=0, description="Minimum profit percentage")
    polling_interval: int = Field(gt=0, description="Polling interval in seconds")
    similarity_threshold: float = Field(ge=0, le=100, description="Market matching similarity threshold")


class TelegramConfig(BaseModel):
    """Telegram notification configuration."""
    bot_token: str = Field(default="", description="Telegram bot token")
    chat_id: Union[int, str] = Field(default=0, description="Telegram chat ID (integer or comma-separated string for multiple)")


class CloudbetAPIConfig(BaseModel):
    """Cloudbet API configuration."""
    api_key: str = Field(default="", description="Cloudbet API key")
    base_url: str = "https://sports-api.cloudbet.com/pub"
    timeout: int = 10
    retry_attempts: int = 3
    retry_delay: int = 2


class PolymarketAPIConfig(BaseModel):
    """Polymarket API configuration."""
    base_url: str = "https://clob.polymarket.com"
    timeout: int = 10
    retry_attempts: int = 3
    retry_delay: int = 2


class QuietHoursConfig(BaseModel):
    """Quiet hours configuration."""
    enabled: bool = False
    start_hour: int = Field(ge=0, le=23)
    end_hour: int = Field(ge=0, le=23)


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    file: str = "logs/arbitrage_bot.log"
    max_bytes: int = 10485760
    backup_count: int = 5


class DatabaseConfig(BaseModel):
    """Database configuration."""
    path: str = "data/arbitrage_events.db"


class APIConfig(BaseModel):
    """API configuration container."""
    cloudbet: CloudbetAPIConfig
    polymarket: PolymarketAPIConfig


class Config(BaseModel):
    """Main configuration model."""
    bankroll: BankrollConfig
    arbitrage: ArbitrageConfig
    telegram: TelegramConfig
    apis: APIConfig
    quiet_hours: QuietHoursConfig
    logging: LoggingConfig
    database: DatabaseConfig
    debug_api: bool = False
    use_mock_data: bool = False


def load_config(config_path: str = "config/config.yaml") -> Config:
    """
    Load configuration from YAML file with environment variable overrides.
    
    Args:
        config_path: Path to configuration YAML file
    
    Returns:
        Validated Config object
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If configuration is invalid
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Load environment variables for empty strings (override config with env vars)
    if 'telegram' in config_dict:
        # Always prefer environment variables if they exist
        env_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        env_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if env_bot_token:
            # Clean bot token - remove newlines, carriage returns, and whitespace
            config_dict['telegram']['bot_token'] = env_bot_token.strip().replace('\n', '').replace('\r', '').strip()
        if env_chat_id:
            # Support multiple chat IDs (comma-separated)
            # If comma-separated, keep as string (TelegramNotifier will handle it)
            # If single value, convert to int for backward compatibility
            chat_ids = [cid.strip() for cid in env_chat_id.split(',') if cid.strip()]
            if len(chat_ids) == 1:
                try:
                    config_dict['telegram']['chat_id'] = int(chat_ids[0])
                except (ValueError, TypeError):
                    config_dict['telegram']['chat_id'] = env_chat_id  # Keep as string if invalid
            else:
                # Multiple chat IDs - keep as comma-separated string
                config_dict['telegram']['chat_id'] = env_chat_id
        
        # Ensure chat_id is handled correctly (int for single, string for multiple)
        current_chat_id = config_dict['telegram'].get('chat_id')
        if isinstance(current_chat_id, str) and ',' in current_chat_id:
            # Multiple chat IDs - keep as string
            pass
        elif isinstance(current_chat_id, str):
            # Single chat ID as string - try to convert to int
            try:
                config_dict['telegram']['chat_id'] = int(current_chat_id)
            except (ValueError, TypeError):
                config_dict['telegram']['chat_id'] = 0
    
    if 'apis' in config_dict and 'cloudbet' in config_dict['apis']:
        env_api_key = os.getenv('CLOUDBET_API_KEY')
        if env_api_key:
            config_dict['apis']['cloudbet']['api_key'] = env_api_key
    
    # Handle nested API config
    if 'apis' in config_dict:
        if 'cloudbet' in config_dict['apis']:
            config_dict['apis']['cloudbet'] = CloudbetAPIConfig(**config_dict['apis']['cloudbet'])
        if 'polymarket' in config_dict['apis']:
            config_dict['apis']['polymarket'] = PolymarketAPIConfig(**config_dict['apis']['polymarket'])
        config_dict['apis'] = APIConfig(**config_dict['apis'])
    
    # Convert all nested dicts to models
    config_dict['bankroll'] = BankrollConfig(**config_dict['bankroll'])
    config_dict['arbitrage'] = ArbitrageConfig(**config_dict['arbitrage'])
    config_dict['telegram'] = TelegramConfig(**config_dict['telegram'])
    config_dict['quiet_hours'] = QuietHoursConfig(**config_dict['quiet_hours'])
    config_dict['logging'] = LoggingConfig(**config_dict['logging'])
    config_dict['database'] = DatabaseConfig(**config_dict['database'])
    
    return Config(**config_dict)

