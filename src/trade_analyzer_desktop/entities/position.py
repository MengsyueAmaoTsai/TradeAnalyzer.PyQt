from typing import List

from ..enums import Side, Action, PositionStatus
from ..events import OrderFilledEvent


class Position:
    def __init__(self, id: int, symbol: str, side: Side, strategy_id: str) -> None:
        self.__id: int = id
        self.__symbol: str = symbol
        self.__side: Side = side
        self.__strategy_id: str = strategy_id
        self.__status: PositionStatus = PositionStatus.Opened
        self.__fills: List[OrderFilledEvent] = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def side(self) -> Side:
        return self.__side

    @property
    def stauts(self) -> PositionStatus:
        return self.__status

    @stauts.setter
    def status(self, status: PositionStatus) -> None:
        self.__status = status

    @property
    def strategy_id(self) -> str:
        return self.__strategy_id

    @property
    def fills(self) -> List[OrderFilledEvent]:
        return self.__fills

    @property
    def total_entry_size(self) -> float:
        if self.side == Side.Long:
            return self.total_buy_size
        else:
            return self.total_sell_size

    @property
    def total_exit_size(self) -> float:
        if self.side == Side.Long:
            return self.total_sell_size
        else:
            return self.total_buy_size

    @property
    def total_buy_size(self) -> float:
        return sum(fill.filled_quantity for fill in self.buy_fills)

    @property
    def total_sell_size(self) -> float:
        return sum(fill.filled_quantity for fill in self.sell_fills)

    @property
    def buy_fills(self) -> List[OrderFilledEvent]:
        return list(filter(lambda fill: fill.action == Action.Buy, self.__fills))

    @property
    def sell_fills(self) -> List[OrderFilledEvent]:
        return list(filter(lambda fill: fill.action == Action.Sell, self.__fills))

    #
    def add_fill(self, e: OrderFilledEvent) -> None:
        self.__fills.append(e)
