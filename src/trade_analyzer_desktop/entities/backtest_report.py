from datetime import date as Date, datetime as DateTime

from PyQt6.QtSql import QSqlQuery


class BacktestReport:
    def __init__(
        self,
        id: str,
        description: str,
        start_date: Date,
        end_date: Date,
        strategy_id: str,
    ) -> None:
        self.__id: str = id
        self.__description: str = description
        self.__start_date: Date = start_date
        self.__end_date: Date = end_date
        self.__strategy_id: str = strategy_id

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
    def start_date(self) -> Date:
        return self.__start_date

    @start_date.setter
    def start_date(self, date: Date) -> None:
        self.__start_date = date

    @property
    def end_date(self) -> Date:
        return self.__end_date

    @end_date.setter
    def end_date(self, date: Date) -> None:
        self.__end_date = date

    @property
    def strategy_id(self) -> str:
        return self.__strategy_id

    @strategy_id.setter
    def strategy_id(self, strategy_id: str) -> None:
        self.__strategy_id = strategy_id

    # -------------------------------------------------- Public Methods --------------------------------------------------
    @classmethod
    def from_query(cls, query: QSqlQuery) -> "BacktestReport":
        return cls(
            query.value("id"),
            query.value("description"),
            DateTime.strptime(query.value("start_date"), "%Y-%m-%d").date(),
            DateTime.strptime(query.value("end_date"), "%Y-%m-%d").date(),
            query.value("strategy_id"),
        )
