import asyncio
import types
import datetime
from unittest.mock import AsyncMock

from cheap_electricity.notifications import send_telegram_notification
from cheap_electricity.price import Price, PriceCategory, ColorEnum


def build_bot(async_mock):
  bot = types.SimpleNamespace()
  bot.send_message = async_mock
  return bot


def test_send_telegram_notification_green(monkeypatch):
  async_mock = AsyncMock()
  monkeypatch.setattr("cheap_electricity.notifications.Bot",
                      lambda token: build_bot(async_mock))
  monkeypatch.setattr("cheap_electricity.config.TELEGRAM_BOT_TOKEN", "TOKEN")
  monkeypatch.setattr("cheap_electricity.config.TELEGRAM_CHAT_ID", "CHAT")

  current = Price(
      hour=datetime.datetime.now(),
      value=90.0,
      unit="€/MWh",
      category=PriceCategory(ColorEnum.GREEN, '🟢'),
  )
  previous = Price(
      hour=datetime.datetime.now(),
      value=100.0,
      unit="€/MWh",
      category=PriceCategory(ColorEnum.YELLOW, '🟡'),
  )
  asyncio.run(send_telegram_notification(current, previous))

  async_mock.assert_awaited_once_with(
      chat_id="CHAT",
      text=("Time for cheap power! 🟢\n"
            "Price changed from 100.0 €/MWh (Yellow) to 90.0 €/MWh (Green)."),
  )


def test_send_telegram_notification_non_green(monkeypatch):
  async_mock = AsyncMock()
  monkeypatch.setattr("cheap_electricity.notifications.Bot",
                      lambda token: build_bot(async_mock))
  monkeypatch.setattr("cheap_electricity.config.TELEGRAM_BOT_TOKEN", "TOKEN")
  monkeypatch.setattr("cheap_electricity.config.TELEGRAM_CHAT_ID", "CHAT")

  current = Price(
      hour=datetime.datetime.now(),
      value=50.0,
      unit="€/MWh",
      category=PriceCategory(ColorEnum.RED, '🔴'),
  )
  previous = Price(
      hour=datetime.datetime.now(),
      value=123.45,
      unit="€/MWh",
      category=PriceCategory(ColorEnum.GREEN, '🟢'),
  )
  asyncio.run(send_telegram_notification(current, previous))

  async_mock.assert_awaited_once_with(
      chat_id="CHAT",
      text=("Cheap power period ended.\n"
            "Price changed from 123.45 €/MWh (Green) to 50.0 €/MWh (Red)."),
  )
