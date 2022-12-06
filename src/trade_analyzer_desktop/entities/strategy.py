
from PyQt6.QtSql import QSqlQuery

from ..enums import Side, StrategyType, TradingPlatform

class Strategy:

    def __init__(self, 
        id: str, description: str, type: StrategyType, side: Side, platform: TradingPlatform, starting_capital: float, default_report_id: str = ""
    ) -> None:
        self.__id: str = id
        self.__description: str = description
        self.__type: StrategyType = type
        self.__side: Side = side  
        self.__platform: TradingPlatform = platform
        self.__starting_capital: float = starting_capital
        self.__default_report_id: str = default_report_id


    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, id: str) -> None:
        self.__id = id

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description

    @property
    def type(self) -> StrategyType:
        return self.__type

    @type.setter
    def type(self, type: StrategyType) -> None:
        self.__type = type

    @property
    def side(self) -> Side:
        return self.__side

    @side.setter
    def side(self, side: Side) -> None:
        self.__side = side 
        
    @property
    def platform(self) -> TradingPlatform:
        return self.__platform

    @platform.setter
    def platform(self, platform: TradingPlatform) -> None:
        self.__platform = platform

    @property
    def starting_capital(self) -> float:
        return self.__starting_capital

    @starting_capital.setter
    def starting_capital(self, starting_capital: float) -> None:
        self.__starting_capital = starting_capital

    @property
    def default_report_id(self) -> str:
        return self.__default_report_id

    @default_report_id.setter
    def default_report_id(self, report_id: str) -> None:
        self.__default_report_id = report_id

    # -------------------------------------------------- Public Methods --------------------------------------------------
    @classmethod
    def from_query(cls, query: QSqlQuery) -> "Strategy":
        """
        Create instance from SQL query.
        """
        return cls(
            query.value("id"),
            query.value("description"),
            StrategyType(query.value("type")),
            Side(query.value("side")),
            TradingPlatform(query.value("platform")),
            query.value("starting_capital"),
            query.value("default_report_id")
        )
    
    # -------------------------------------------------- Properties --------------------------------------------------
    