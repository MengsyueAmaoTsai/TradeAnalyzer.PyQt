from typing import List, Union

from PyQt6.QtSql import QSqlQuery

from ..entities import Strategy


class StrategyRepository:
    QUERY_ALL_STRATEGIES_SQL: str = """
    SELECT * FROM strategies
    """

    INSERT_STRATEGY_SQL: str = """
    INSERT INTO strategies (id, description, type, resolution, side, platform, starting_capital, default_report_id) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?
    )
    """

    SELECT_BY_ID_SQL: str = """
    SELECT * FROM strategies WHERE id = :strategy_id
    """

    UPDATE_STRATEGY_SQL: str = """
    UPDATE strategies SET 
        description = :description,
        type = :type,
        resolution = :resolution,
        side = :side,
        platform = :platform,
        starting_capital = :starting_capital,
        default_report_id = :default_report_id
    WHERE 
        id = :strategy_id
    """

    DELETE_BY_ID_SQL: str = """
    DELETE FROM strategies WHERE id = :strategy_id
    """

    @classmethod
    def insert(cls, strategy: Strategy) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.INSERT_STRATEGY_SQL)

        query.addBindValue(strategy.id)
        query.addBindValue(strategy.description)
        query.addBindValue(strategy.type.value)
        query.addBindValue(strategy.resolution.value)
        query.addBindValue(strategy.side.value)
        query.addBindValue(strategy.platform.value)
        query.addBindValue(strategy.starting_capital)
        query.addBindValue(strategy.default_report_id)
        return query.exec()

    @classmethod
    def query_all(cls) -> List[Strategy]:
        strategies: List[Strategy] = []
        query: QSqlQuery = QSqlQuery()
        query.exec(cls.QUERY_ALL_STRATEGIES_SQL)

        while query.next():
            strategies.append(Strategy.from_query(query))
        return strategies

    @classmethod
    def query_by_id(cls, id: str) -> Union[Strategy, None]:
        strategy: Union[Strategy, None] = None

        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.SELECT_BY_ID_SQL)
        query.bindValue(":strategy_id", id)
        query.exec()

        if query.next():
            strategy = Strategy.from_query(query)
        return strategy

    @classmethod
    def update(cls, strategy: Strategy) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.UPDATE_STRATEGY_SQL)
        query.bindValue(":description", strategy.description)
        query.bindValue(":type", strategy.type.value)
        query.bindValue(":side", strategy.side.value)
        query.bindValue(":resolution", strategy.resolution.value)
        query.bindValue(":platform", strategy.platform.value)
        query.bindValue(":starting_capital", strategy.starting_capital)
        query.bindValue(":default_report_id", strategy.default_report_id)
        query.bindValue(":strategy_id", strategy.id)
        return query.exec()

    @classmethod
    def delete_by_id(cls, id: str) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.DELETE_BY_ID_SQL)
        query.bindValue(":strategy_id", id)
        return query.exec()

    @classmethod
    def delete(cls, strategy: Strategy) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.DELETE_BY_ID_SQL)
        query.bindValue(":strategy_id", strategy.id)
        return query.exec()
