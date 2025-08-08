"""
Telegram alerting utilities.

This module provides a simple function to send notifications via Telegram
using the bot token and chat ID specified in the configuration. It uses
the `python-telegram-bot` library.

Usage:

    from alerts import send_alert
    send_alert("New trade executed!")

Ensure that `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are correctly set
in ``config.py`` before calling ``send_alert``.
"""

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

try:
    import telegram  # type: ignore
except ImportError:
    telegram = None


def send_alert(message: str) -> None:
    """Send a text message via Telegram.

    Parameters
    ----------
    message : str
        The message to send.

    Notes
    -----
    If the python-telegram-bot package is not installed, the function
    gracefully does nothing.
    """
    if telegram is None:
        print(f"[Telegram disabled] {message}")
        return
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")