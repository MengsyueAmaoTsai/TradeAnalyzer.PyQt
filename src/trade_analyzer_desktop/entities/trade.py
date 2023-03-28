from datetime import datetime as DateTime, timedelta as TimeDelta
from typing import List

from ..enums import Side
from ..events import OrderFilledEvent


class Trade:
    def __init__(
        self,
        id: int,
        symbol: str,
        entry_time: DateTime,
        entry_price: float,
        side: Side,
        quantity: float,
        exit_time: DateTime,
        exit_price: float,
        gross_profit_loss: float,
        fee: float,
        strategy_id,
        fills: List[OrderFilledEvent],
    ) -> None:
        self.__id: int = id
        self.__symbol: str = symbol
        self.__entry_time: DateTime = entry_time
        self.__entry_price: float = entry_price
        self.__side: Side = side
        self.__trade_size: float = quantity
        self.__exit_time: DateTime = exit_time
        self.__exit_price: float = exit_price
        self.__gross_profit_loss: float = gross_profit_loss
        self.__fee: float = fee
        self.__mae: float = 0
        self.__mfe: float = 0
        self.__strategy_id: str = strategy_id
        self.__fills: List[OrderFilledEvent] = fills

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def entry_time(self) -> DateTime:
        return self.__entry_time

    @property
    def entry_price(self) -> float:
        return self.__entry_price

    @property
    def side(self) -> Side:
        return self.__side

    @property
    def trade_size(self) -> float:
        return self.__trade_size

    @property
    def exit_time(self) -> DateTime:
        return self.__exit_time

    @property
    def exit_price(self) -> float:
        return self.__exit_price

    @property
    def gross_profit_loss(self) -> float:
        return self.__gross_profit_loss

    @property
    def fee(self) -> float:
        return self.__fee

    @property
    def net_profit_loss(self) -> float:
        return self.__gross_profit_loss - self.__fee

    @property
    def mae(self) -> float:
        return self.__mae

    @property
    def mfe(self) -> float:
        return self.__mfe

    @property
    def duration(self) -> TimeDelta:
        return self.__exit_time - self.__entry_time

    @property
    def end_trade_drawdown(self) -> float:
        return self.net_profit_loss - self.__mfe

    @property
    def strategy_id(self) -> str:
        return self.__strategy_id

    @property
    def fills(self) -> List[OrderFilledEvent]:
        return self.__fills
