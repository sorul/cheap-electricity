import asyncio
import types
from unittest.mock import AsyncMock

from cheap_electricity.notifications import send_telegram_notification


def build_bot(async_mock):
    bot = types.SimpleNamespace()
    bot.send_message = async_mock
    return bot


def test_send_telegram_notification(monkeypatch):
    async_mock = AsyncMock()
    monkeypatch.setattr("cheap_electricity.notifications.Bot", lambda token: build_bot(async_mock))
    monkeypatch.setattr("cheap_electricity.config.TELEGRAM_BOT_TOKEN", "TOKEN")
    monkeypatch.setattr("cheap_electricity.config.TELEGRAM_CHAT_ID", "CHAT")

    asyncio.run(send_telegram_notification(123.45))

    async_mock.assert_awaited_once_with(chat_id="CHAT", text="Time for cheap power! 🟢\nThe current price is 123.45 €/MWh.")
