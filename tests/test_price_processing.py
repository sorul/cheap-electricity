import datetime
from unittest.mock import patch

from tests.mock_data import MOCK_PRICES_DATA
from cheap_electricity.main import process_and_categorize_prices


class FixedDateTimeGreen(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 1, 0, 0)


class FixedDateTimeYellow(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 0, 0, 0)


class FixedDateTimeRed(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2025, 8, 7, 19, 0, 0)


def test_process_and_categorize_prices_green():
    with patch("cheap_electricity.main.datetime.datetime", FixedDateTimeGreen):
        price, category = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert price == 90.0
    assert category == "Green"


def test_process_and_categorize_prices_yellow():
    with patch("cheap_electricity.main.datetime.datetime", FixedDateTimeYellow):
        price, category = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert price == 100.0
    assert category == "Yellow"


def test_process_and_categorize_prices_red():
    with patch("cheap_electricity.main.datetime.datetime", FixedDateTimeRed):
        price, category = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert price == 230.0
    assert category == "Red"
