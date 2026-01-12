"""
Telegram notification system for arbitrage alerts.

Uses python-telegram-bot 20.x with async/await.
Handles retries, errors gracefully, and never blocks the main event loop.
"""
import asyncio
from typing import Dict, Optional, Union, List
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError, RetryAfter, TimedOut, NetworkError
from telegram.request import HTTPXRequest

from .logger import setup_logger


class TelegramNotifier:
    """
    Sends arbitrage alerts via Telegram.
    
    Features:
    - Async/await (non-blocking)
    - Automatic retries (up to 3 attempts)
    - Graceful error handling
    - Formatted alert messages
    - Multiple chat ID support (send to multiple recipients)
    """
    
    def __init__(self, bot_token: str, chat_id: Union[int, str, List[int]]):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID(s) - can be:
                - Single integer: one chat ID
                - Comma-separated string: "123,456,789"
                - List of integers: [123, 456, 789]
        """
        # Clean bot token - remove any newlines or invalid characters
        self.bot_token = bot_token.strip().replace('\n', '').replace('\r', '').strip() if isinstance(bot_token, str) else bot_token
        
        # Handle multiple chat IDs
        if isinstance(chat_id, str):
            # Comma-separated string
            # Strip = signs (Railway sometimes includes them)
            cleaned_ids = [cid.strip().lstrip('=').strip() for cid in chat_id.split(',') if cid.strip()]
            self.chat_ids = [int(cid) for cid in cleaned_ids if cid]
        elif isinstance(chat_id, list):
            # List of chat IDs
            self.chat_ids = [int(cid) for cid in chat_id]
        else:
            # Single integer
            self.chat_ids = [int(chat_id)]
        
        if not self.chat_ids:
            raise ValueError("At least one chat_id must be provided")
        
        self.logger = setup_logger("telegram_notifier")
        # Initialize Bot with proper timeout settings
        request = HTTPXRequest(
            connect_timeout=10.0,
            read_timeout=10.0,
            write_timeout=10.0
        )
        self.bot = Bot(token=bot_token, request=request)
        self.max_retries = 3
    
    def _format_alert_message(self, opportunity: Dict) -> str:
        """
        Format arbitrage opportunity as Telegram message.
        
        Format matches the required specification:
        - 🚨 Arbitrage Found header with profit %
        - Market name
        - Platform A bet (odds + amount + link)
        - Platform B bet (odds + amount + link)
        - Total investment
        - Guaranteed profit
        
        Args:
            opportunity: Arbitrage opportunity dictionary
        
        Returns:
            Formatted message string with Markdown formatting
        """
        market_name = opportunity.get('market_name', 'Unknown Market')
        profit_pct = opportunity.get('profit_percentage', 0)
        
        platform_a = opportunity.get('platform_a', 'Platform A')
        platform_b = opportunity.get('platform_b', 'Platform B')
        
        # Get outcome names for display
        outcome_a = opportunity.get('outcome_a', {}).get('name', 'YES')
        outcome_b = opportunity.get('outcome_b', {}).get('name', 'NO')
        
        odds_a = opportunity.get('odds_a', 0)
        odds_b = opportunity.get('odds_b', 0)
        
        bet_amount_a = opportunity.get('bet_amount_a', 0)
        bet_amount_b = opportunity.get('bet_amount_b', 0)
        total_capital = opportunity.get('total_capital', 0)
        guaranteed_profit = opportunity.get('guaranteed_profit', 0)
        
        url_a = opportunity.get('market_a', {}).get('url', 'N/A')
        url_b = opportunity.get('market_b', {}).get('url', 'N/A')
        
        # Clean URLs - remove newlines and other invalid characters
        if isinstance(url_a, str):
            url_a = url_a.strip().replace('\n', '').replace('\r', '')
        if isinstance(url_b, str):
            url_b = url_b.strip().replace('\n', '').replace('\r', '')
        
        # Format platform names for display
        platform_a_display = platform_a.capitalize()
        platform_b_display = platform_b.capitalize()
        
        # Remove Unicode emojis for Windows compatibility
        message = f"""*ARBITRAGE FOUND ({profit_pct:.2f}%)*

*Market:* {market_name}

*{platform_a_display}:*
{outcome_a} @ {odds_a:.2f} - ${bet_amount_a:.2f}
{url_a}

*{platform_b_display}:*
{outcome_b} @ {odds_b:.2f} - ${bet_amount_b:.2f}
{url_b}

*Total Invested:* ${total_capital:.2f}
*Guaranteed Profit:* ${guaranteed_profit:.2f}"""
        
        return message
    
    async def send_message(self, text: str, timeout: int = 5, chat_id: Optional[int] = None) -> bool:
        """
        Send a text message via Telegram with retry logic.
        
        Args:
            text: Message text to send
            timeout: Maximum time to wait for send (seconds)
            chat_id: Specific chat ID to send to (if None, sends to all chat IDs)
        
        Returns:
            True if sent successfully to at least one recipient, False otherwise
        """
        # Clean message text - remove any problematic characters that might cause URL parsing issues
        # Split by lines, strip each line, and rejoin with newlines (removes trailing/leading whitespace from URLs)
        if isinstance(text, str):
            lines = text.split('\n')
            cleaned_lines = [line.rstrip('\r') for line in lines]  # Remove \r but keep \n for formatting
            text = '\n'.join(cleaned_lines)
        
        target_chat_ids = [chat_id] if chat_id is not None else self.chat_ids
        success_count = 0
        
        for target_chat_id in target_chat_ids:
            for attempt in range(1, self.max_retries + 1):
                try:
                    self.logger.info(f"Telegram send attempt {attempt}/{self.max_retries} to chat {target_chat_id}...")
                    # Use asyncio.wait_for with timeout
                    result = await asyncio.wait_for(
                        self.bot.send_message(
                            chat_id=target_chat_id,
                            text=text,
                            parse_mode='Markdown',
                            disable_web_page_preview=False
                        ),
                        timeout=timeout
                    )
                    self.logger.info(f"Telegram message sent successfully to chat {target_chat_id} (attempt {attempt})")
                    success_count += 1
                    break  # Success for this chat_id, move to next
                
                except RetryAfter as e:
                    # Rate limited - wait for the specified time
                    wait_time = e.retry_after
                    self.logger.warning(f"Rate limited for chat {target_chat_id}. Waiting {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    continue
                    
                except (TimedOut, NetworkError) as e:
                    # Network error - retry with exponential backoff
                    if attempt < self.max_retries:
                        wait_time = attempt * 0.5  # 0.5s, 1s, 1.5s
                        self.logger.warning(
                            f"Network error on attempt {attempt}/{self.max_retries} for chat {target_chat_id}: {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        self.logger.error(f"Failed to send Telegram message to chat {target_chat_id} after {self.max_retries} attempts: {e}")
                        break  # Move to next chat_id
                        
                except TelegramError as e:
                    # Other Telegram errors - don't retry, move to next chat_id
                    self.logger.error(f"Telegram error for chat {target_chat_id}: {e}")
                    break  # Move to next chat_id
                    
                except asyncio.TimeoutError as e:
                    if attempt < self.max_retries:
                        self.logger.warning(f"Timeout on attempt {attempt}/{self.max_retries} for chat {target_chat_id}. Retrying...")
                        await asyncio.sleep(0.5)
                        continue
                    else:
                        self.logger.error(f"Telegram send timeout for chat {target_chat_id} after {self.max_retries} attempts: {e}")
                        break  # Move to next chat_id
                        
                except Exception as e:
                    # Unexpected errors - log and move to next chat_id
                    self.logger.error(f"Unexpected error sending Telegram message to chat {target_chat_id}: {e}")
                    break  # Move to next chat_id
        
        # Return True if at least one message was sent successfully
        return success_count > 0
    
    async def send_alert(self, opportunity: Dict, timeout: int = 5) -> bool:
        """
        Send arbitrage alert via Telegram to all configured chat IDs.
        
        This is a convenience method that formats the opportunity and calls send_message().
        Sends to all chat IDs configured in the notifier.
        
        Args:
            opportunity: Arbitrage opportunity dictionary
            timeout: Maximum time to wait for send (seconds)
        
        Returns:
            True if sent successfully to at least one recipient, False otherwise
        """
        try:
            message = self._format_alert_message(opportunity)
            success = await self.send_message(message, timeout)
            
            if success:
                self.logger.info(f"Telegram alert sent for: {opportunity.get('market_name')} (to {len(self.chat_ids)} recipient(s))")
            else:
                self.logger.warning(f"Failed to send Telegram alert for: {opportunity.get('market_name')} (to all {len(self.chat_ids)} recipient(s))")
            
            return success
            
        except Exception as e:
            # Never crash the main app
            self.logger.error(f"Error formatting/sending alert: {e}")
            return False
    
    async def send_test_message(self) -> bool:
        """
        Send a test message to verify Telegram configuration.
        Sends to all configured chat IDs.
        
        Returns:
            True if sent successfully to at least one recipient, False otherwise
        """
        test_text = f"Telegram bot integration test - Bot is working! Sending to {len(self.chat_ids)} recipient(s)."
        return await self.send_message(test_text)


# Test function for standalone testing
async def test_telegram(bot_token: str, chat_id: int):
    """
    Test function to verify Telegram integration.
    
    Usage:
        import asyncio
        from telegram_notifier import test_telegram
        
        asyncio.run(test_telegram("your_token", 123456789))
    
    Args:
        bot_token: Telegram bot token
        chat_id: Telegram chat ID (integer)
    """
    notifier = TelegramNotifier(bot_token, chat_id)
    success = await notifier.send_test_message()
    
    if success:
        print("SUCCESS: Telegram test message sent successfully!")
    else:
        print("FAILED: Failed to send Telegram test message. Check logs for details.")
    
    return success

