from enum import Enum

class OrderStatus(Enum):
    Rejected = "Rejected"
    Cancelled = "Cancelled"
    Opening = "Opening"
    PartiallyFilled = "PartiallyFilled"
    Filled = "Filled"