#!/usr/bin/env python3
"""
Test script to verify Telegram chat IDs are correct.
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

async def test_chat_ids():
    """Test if chat IDs are valid and accessible."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '').strip().replace('\n', '').replace('\r', '')
    chat_id_str = os.getenv('TELEGRAM_CHAT_ID', '')
    
    if not bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    if not chat_id_str:
        print("ERROR: TELEGRAM_CHAT_ID not found in environment variables")
        return
    
    print("="*60)
    print("TELEGRAM CHAT ID VERIFICATION")
    print("="*60)
    print(f"\nBot Token: {bot_token[:10]}...{bot_token[-5:]}")
    print(f"Chat IDs from env: {chat_id_str}")
    
    # Parse chat IDs
    chat_ids = [cid.strip().lstrip('=').strip() for cid in chat_id_str.split(',') if cid.strip()]
    print(f"\nParsed Chat IDs: {chat_ids}")
    
    bot = Bot(token=bot_token)
    
    # Get bot info
    try:
        bot_info = await bot.get_me()
        print(f"\nBot Username: @{bot_info.username}")
        print(f"Bot Name: {bot_info.first_name}")
    except Exception as e:
        print(f"\nERROR getting bot info: {e}")
        return
    
    # Test each chat ID
    print("\n" + "="*60)
    print("TESTING CHAT IDs")
    print("="*60)
    
    for chat_id_str in chat_ids:
        try:
            chat_id = int(chat_id_str)
            print(f"\nTesting Chat ID: {chat_id}")
            
            # Try to get chat info
            try:
                chat = await bot.get_chat(chat_id)
                print(f"  ✓ Chat found!")
                print(f"    Type: {chat.type}")
                if hasattr(chat, 'title'):
                    print(f"    Title: {chat.title}")
                if hasattr(chat, 'username'):
                    print(f"    Username: @{chat.username}" if chat.username else "    Username: (private)")
                
                # Try to send a test message
                try:
                    test_msg = f"Test message from bot @{bot_info.username}"
                    await bot.send_message(chat_id=chat_id, text=test_msg)
                    print(f"  ✓ Test message sent successfully!")
                except TelegramError as e:
                    print(f"  ✗ Cannot send message: {e}")
                    if "Not Found" in str(e):
                        print(f"    → Chat ID might be wrong, or bot doesn't have access")
                    elif "Forbidden" in str(e):
                        print(f"    → Bot doesn't have permission to send messages")
                    else:
                        print(f"    → Error: {e}")
                        
            except TelegramError as e:
                print(f"  ✗ Chat not found or inaccessible: {e}")
                if "Not Found" in str(e):
                    print(f"    → This chat ID doesn't exist or bot doesn't have access")
                    print(f"    → For personal chat: Make sure you sent /start to the bot")
                    print(f"    → For channel: Make sure bot is added as admin with 'Post Messages' permission")
                    
        except ValueError:
            print(f"\n✗ Invalid chat ID format: {chat_id_str}")
        except Exception as e:
            print(f"\n✗ Error testing chat ID {chat_id_str}: {e}")
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_chat_ids())

