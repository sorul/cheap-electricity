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


@dataclass
class Price:
    hour: datetime
    value: float
    unit: str
    category: PriceCategory
