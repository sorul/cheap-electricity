import asyncio
import datetime
from unittest.mock import AsyncMock, patch

from tests.mock_data import MOCK_PRICES_DATA
from cheap_electricity.main import main
from cheap_electricity.price import PriceCategory


class FixedDateTime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 1, 0, 0)


class FixedDateTimeExit(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 2, 0, 0)


def test_main_triggers_notification(monkeypatch):
    monkeypatch.setattr("cheap_electricity.main.get_prices_for_today", lambda: MOCK_PRICES_DATA)
    async_mock = AsyncMock()
    monkeypatch.setattr("cheap_electricity.main.send_telegram_notification", async_mock)

    with patch("cheap_electricity.price_processing.datetime.datetime", FixedDateTime):
        asyncio.run(main())

    async_mock.assert_awaited_once()
    current, previous = async_mock.call_args[0]
    assert current.value == 90.0
    assert current.category is PriceCategory.GREEN
    assert previous.value == 100.0
    assert previous.category is PriceCategory.YELLOW


def test_main_triggers_notification_on_exit(monkeypatch):
    monkeypatch.setattr("cheap_electricity.main.get_prices_for_today", lambda: MOCK_PRICES_DATA)
    async_mock = AsyncMock()
    monkeypatch.setattr("cheap_electricity.main.send_telegram_notification", async_mock)

    with patch("cheap_electricity.price_processing.datetime.datetime", FixedDateTimeExit):
        asyncio.run(main())

    async_mock.assert_awaited_once()
    current, previous = async_mock.call_args[0]
    assert current.value == 150.0
    assert current.category is PriceCategory.YELLOW
    assert previous.value == 90.0
    assert previous.category is PriceCategory.GREEN
