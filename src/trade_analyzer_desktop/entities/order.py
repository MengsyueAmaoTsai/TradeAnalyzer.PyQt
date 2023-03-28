from datetime import datetime as DateTime

from PyQt6.QtSql import QSqlQuery

from ..enums import OrderType, Action, OrderStatus


class Order:
    def __init__(
        self,
        datetime: DateTime,
        symbol: str,
        type: OrderType,
        action: Action,
        quantity: float,
        price: float,
        strategy_id: str = "",
    ) -> None:
        self.__datetime: DateTime = datetime
        self.__symbol: str = symbol
        self.__type: OrderType = type
        self.__action: Action = action
        self.__quantity: float = quantity
        self.__price: float = price
        self.__strategy_id: str = strategy_id
        self.__remaining_quantity: float = quantity
        self.__filled_quantity: float = 0
        self.__avg_filled_price: float = 0
        self.__status: OrderStatus = OrderStatus.Opening
        self.__is_day_trade: bool = False

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def datetime(self) -> DateTime:
        return self.__datetime

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def type(self) -> OrderType:
        return self.__type

    @property
    def action(self) -> Action:
        return self.__action

    @property
    def quantity(self) -> float:
        return self.__quantity

    @property
    def price(self) -> float:
        return self.__price

    @property
    def strategy_id(self) -> str:
        return self.__strategy_id

    @strategy_id.setter
    def strategy_id(self, strategy_id: str) -> None:
        self.__strategy_id = strategy_id

    @property
    def remaining_quantity(self) -> float:
        return self.__remaining_quantity

    @remaining_quantity.setter
    def remaining_quantity(self, remaining_quantity: float) -> None:
        self.__remaining_quantity = remaining_quantity

    @property
    def filled_quantity(self) -> float:
        return self.__filled_quantity

    @filled_quantity.setter
    def filled_quantity(self, filled_quantity: float) -> None:
        self.__filled_quantity = filled_quantity

    @property
    def avg_filled_price(self) -> float:
        return self.__avg_filled_price

    @avg_filled_price.setter
    def avg_filled_price(self, price: float) -> None:
        self.__avg_filled_price = price

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @status.setter
    def status(self, status: OrderStatus) -> None:
        self.__status = status

    @property
    def is_day_trade(self) -> bool:
        return self.__is_day_trade

    @is_day_trade.setter
    def is_day_trade(self, is_day_trade: bool) -> None:
        self.__is_day_trade = is_day_trade

    # -------------------------------------------------- Public Methods --------------------------------------------------
    @classmethod
    def from_query(cls, query: QSqlQuery) -> "Order":
        return cls(
            DateTime.strptime(query.value("datetime"), "%Y-%m-%d %H:%M:%S"),
            query.value("symbol"),
            OrderType(query.value("type")),
            Action(query.value("action")),
            query.value("quantity"),
            query.value("price"),
            query.value("strategy_id"),
        )
