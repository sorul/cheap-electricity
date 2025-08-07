import asyncio
import datetime
from unittest.mock import AsyncMock, patch

from tests.mock_data import MOCK_PRICES_DATA
from cheap_electricity.main import main


class FixedDateTime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 1, 0, 0)


def test_main_triggers_notification(monkeypatch):
    monkeypatch.setattr("cheap_electricity.main.get_prices_for_today", lambda: MOCK_PRICES_DATA)
    async_mock = AsyncMock()
    monkeypatch.setattr("cheap_electricity.main.send_telegram_notification", async_mock)

    with patch("cheap_electricity.main.datetime.datetime", FixedDateTime):
        asyncio.run(main())

    async_mock.assert_awaited_once_with(90.0)
