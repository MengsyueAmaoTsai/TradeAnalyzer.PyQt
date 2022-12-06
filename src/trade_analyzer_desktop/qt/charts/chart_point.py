from typing import Union, overload
from datetime import datetime as DateTime, date as Date


class ChartPoint():
    """
    Represents a data point on chart.
    """

    @overload
    def __init__(self, x: int, y: float) -> None: ...

    @overload
    def __init__(self, x: DateTime, y: float) -> None: ...

    @overload
    def __init__(self, x: Date, y: float) -> None: ...

    def __init__(self, x: Union[int, DateTime, Date], y: float) -> None:
        self.x: int = 0
        
        if isinstance(x, DateTime):
            self.x = int(x.timestamp())

        elif isinstance(x, Date):
            self.x = int(DateTime(x.year, x.month, x.day, 0, 0, 0).timestamp())
        
        else:
            self.x = x

        self.y: float = y