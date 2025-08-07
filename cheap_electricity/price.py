from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ColorEnum(Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"


@dataclass(frozen=True)
class PriceCategory:
    color: ColorEnum
    emoji: str


# Predefined categories
PriceCategory.GREEN = PriceCategory(ColorEnum.GREEN, "\U0001F7E2")
PriceCategory.YELLOW = PriceCategory(ColorEnum.YELLOW, "\U0001F7E1")
PriceCategory.RED = PriceCategory(ColorEnum.RED, "\U0001F534")


@dataclass
class Price:
    hour: datetime
    value: float
    unit: str
    category: PriceCategory
