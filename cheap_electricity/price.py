from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PriceCategory(Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"


@dataclass
class Price:
    hour: datetime
    value: float
    unit: str
    category: PriceCategory
