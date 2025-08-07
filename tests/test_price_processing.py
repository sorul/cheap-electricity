import datetime
from unittest.mock import patch

from tests.mock_data import MOCK_PRICES_DATA
from cheap_electricity.price_processing import process_and_categorize_prices
from cheap_electricity.price import ColorEnum


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
    with patch("cheap_electricity.price_processing.datetime.datetime", FixedDateTimeGreen):
        current, previous = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert current.value == 90.0
    assert current.category.color is ColorEnum.GREEN
    assert previous.value == 100.0
    assert previous.category.color is ColorEnum.YELLOW


def test_process_and_categorize_prices_yellow():
    with patch("cheap_electricity.price_processing.datetime.datetime", FixedDateTimeYellow):
        current, previous = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert current.value == 100.0
    assert current.category.color is ColorEnum.YELLOW
    assert previous.value == 250.0
    assert previous.category.color is ColorEnum.RED


def test_process_and_categorize_prices_red():
    with patch("cheap_electricity.price_processing.datetime.datetime", FixedDateTimeRed):
        current, previous = process_and_categorize_prices(MOCK_PRICES_DATA)
    assert current.value == 230.0
    assert current.category.color is ColorEnum.RED
    assert previous.value == 75.0
    assert previous.category.color is ColorEnum.GREEN
