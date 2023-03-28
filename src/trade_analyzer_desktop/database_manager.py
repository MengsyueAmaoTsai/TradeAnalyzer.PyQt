import os
from typing import Optional

from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class DatabaseManager:
    DATABASE_NAME: str = "dev.db"

    __sqlite: Optional[QSqlDatabase] = None

    CREATE_STRATEGIES_TABLE_SQL: str = """
    CREATE TABLE strategies (
        id VARCHAR(50) NOT NULL PRIMARY KEY,
        description TEXT,
        type VARCHAR(50),
        resolution VARCHAR(50),
        side VARCHAR(50),
        platform VARCHAR(50),
        starting_capital FLOAT,
        default_report_id VARCHAR(50)
    )
    """

    CREATE_BACKTEST_REPORTS_TABLE_SQL: str = """
    CREATE TABLE backtest_reports (
        id VARCHAR(50) NOT NULL,
        description TEXT,
        start_date VARCHAR(50),
        end_date VARCHAR(50),
        strategy_id VARCHAR(50), 
        FOREIGN KEY (strategy_id) REFERENCES strategies (id)
    )
    """

    CREATE_ORDERS_TABLE_SQL: str = """
    CREATE TABLE orders (
        datetime VARCHAR(50) NOT NULL,
        symbol VARCHAR(50) NOT NULL,
        type VARCHAR(50) NOT NULL,
        action VARCHAR(50) NOT NULL,
        quantity FLOAT NOT NULL,
        price FLOAT NOT NULL,
        strategy_id VARCHAR(50)
    )
    """

    CREATE_INSTRUMENTS_TABLE_SQL: str = """
    CREATE TABLE instruments (
        symbol VARCHAR(50) PRIMARY KEY,
        description VARCHAR(50),
        exchange VARCHAR(50),
        type VARCHAR(50),
        fee_pricing FLOAT,
        point_value FLOAT
    )
    """

    @classmethod
    def connect(cls) -> None:
        if cls.__sqlite:
            return

        cls.__sqlite = QSqlDatabase.addDatabase("QSQLITE")
        cls.__sqlite.setDatabaseName(cls.DATABASE_NAME)
        cls.__sqlite.open()
        print(f"Sqlite database is connected.")

    @classmethod
    def reset_database(cls) -> None:
        if os.path.exists(cls.DATABASE_NAME):
            os.remove(cls.DATABASE_NAME)

        connection: QSqlDatabase = QSqlDatabase.addDatabase("QSQLITE")
        connection.setDatabaseName(cls.DATABASE_NAME)
        connection.open()

        query: QSqlQuery = QSqlQuery()
        if query.exec(cls.CREATE_STRATEGIES_TABLE_SQL):
            print("Created table strategies.")

        if query.exec(cls.CREATE_BACKTEST_REPORTS_TABLE_SQL):
            print("Created table backtest_reports.")

        if query.exec(cls.CREATE_ORDERS_TABLE_SQL):
            print("Created table orders.")

        if query.exec(cls.CREATE_INSTRUMENTS_TABLE_SQL):
            print("Created table instruments.")
        connection.close()
        return
