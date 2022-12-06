
from datetime import datetime as DateTime

from ..enums import Action, OrderStatus
from ..entities import Order

class OrderFilledEvent:

    def __init__(self, order: Order) -> None:
        self.__order: Order = order
        self.__fee: float = 0

    @property
    def datetime(self) -> DateTime:
        return self.__order.datetime

    @property
    def symbol(self) -> str:
        return self.__order.symbol

    @property
    def action(self) -> Action:
        return self.__order.action

    @property
    def quantity(self) -> float:
        return self.__order.quantity

    @property
    def price(self) -> float:
        return self.__order.price

    @property
    def filled_quantity(self) -> float:
        return self.__order.filled_quantity

    @property
    def avg_filled_price(self) -> float:
        return self.__order.avg_filled_price
    
    @property
    def fee(self) -> float:
        return self.__fee
    
    @fee.setter
    def fee(self, fee: float) -> None:
        self.__fee = fee

    @property
    def status(self) -> OrderStatus:
        return self.__order.status

    @property
    def is_day_trade(self) -> bool:
        return self.__order.is_day_trade

    @is_day_trade.setter
    def is_day_trade(self, is_day_trade: bool) -> None:
        self.__is_day_trade = is_day_trade

    @property
    def strategy_id(self) -> str:
        return self.__order.strategy_id