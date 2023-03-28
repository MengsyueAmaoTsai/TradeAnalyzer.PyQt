from typing import List

from PyQt6.QtSql import QSqlQuery

from ..entities import Order


class OrderRepository:
    INSERT_ORDERS_SQL: str = """
    INSERT INTO orders (datetime, symbol, type, action, quantity, price, strategy_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    DELETE_SQL: str = """
    DELETE FROM orders 
    WHERE
    strategy_id = :strategy_id
    """

    SELECT_BY_STRATEGY_ID_SQL: str = """
    SELECT * FROM orders WHERE strategy_id = :strategy_id
    """

    @classmethod
    def insert_batch(cls, orders: List[Order]) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.INSERT_ORDERS_SQL)

        query.addBindValue(
            [order.datetime.strftime("%Y-%m-%d %H:%M:%S") for order in orders]
        )
        query.addBindValue([order.symbol for order in orders])
        query.addBindValue([order.type.value for order in orders])
        query.addBindValue([order.action.value for order in orders])
        query.addBindValue([order.quantity for order in orders])
        query.addBindValue([order.price for order in orders])
        query.addBindValue([order.strategy_id for order in orders])
        success: bool = query.execBatch()

        if not success:
            print(query.lastError().text())
        return success

    @classmethod
    def delete_by_strategy_id(cls, strategy_id: str) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.DELETE_SQL)
        query.bindValue(":strategy_id", strategy_id)
        return query.exec()

    @classmethod
    def query_by_strategy_id(cls, strategy_id: str) -> List[Order]:
        orders: List[Order] = []

        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.SELECT_BY_STRATEGY_ID_SQL)
        query.bindValue(":strategy_id", strategy_id)
        query.exec()

        while query.next():
            orders.append(Order.from_query(query))
        return orders
