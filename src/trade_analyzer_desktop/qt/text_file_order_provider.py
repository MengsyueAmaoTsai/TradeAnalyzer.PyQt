from typing import List
from datetime import datetime as DateTime

from ..entities import Order
from ..enums import OrderType, Action

class TextFileOrderProvider:
    
    FIELD_SEPARATOR: str = ','

    @classmethod
    def read(cls, path: str) -> List[Order]:
        if not path.endswith(".txt"):
            raise ValueError()

        orders: List[Order] = []
        with open(path, 'r') as file:
            lines: List[str] = file.readlines()

            for line in lines:
                if not line.isspace() and not line.__eq__(str()):
                    fields: List[str] = line.split(cls.FIELD_SEPARATOR)
                    orders.append(
                        Order(
                            DateTime.strptime(f"{fields[0]} {fields[1]}", "%Y-%m-%d %H:%M:%S"),
                            fields[2],
                            OrderType.Limit,
                            Action(fields[3]),
                            float(fields[4]),
                            float(fields[5])
                        )
                    )
        return sorted(orders, key = lambda order: order.datetime, reverse = False)