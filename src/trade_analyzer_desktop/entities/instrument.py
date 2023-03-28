from typing import Union

from PyQt6.QtSql import QSqlQuery

from .exchange import Exchange
from ..enums import InstrumentType


class Instrument:
    def __init__(
        self,
        symbol: str,
        description: str,
        exchange: str,
        type: InstrumentType,
        fee_pricing: float,
        point_value: float,
    ) -> None:
        self.__symbol: str = symbol
        self.__description: str = description

        ex: Union[Exchange, None] = Exchange.create(exchange, fee_pricing)
        assert ex is not None

        self.__exchange: Exchange = ex
        self.__type: InstrumentType = type
        self.__fee_pricing: float = fee_pricing
        self.__point_value: float = point_value

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def description(self) -> str:
        return self.__description

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def type(self) -> InstrumentType:
        return self.__type

    @property
    def fee_pricing(self) -> float:
        return self.__fee_pricing

    @property
    def point_value(self) -> float:
        return self.__point_value

    @classmethod
    def from_query(cls, query: QSqlQuery) -> "Instrument":
        return cls(
            query.value("symbol"),
            query.value("description"),
            query.value("exchange"),
            InstrumentType(query.value("type")),
            query.value("fee_pricing"),
            query.value("point_value"),
        )
