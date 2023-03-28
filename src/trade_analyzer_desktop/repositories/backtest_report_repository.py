from typing import List, Union

from PyQt6.QtSql import QSqlQuery

from ..entities import BacktestReport


class BacktestReportRepository:
    SELECT_BY_STRATEGY_ID_SQL: str = """
    SELECT * FROM backtest_reports WHERE strategy_id = :strategy_id
    """

    SELECT_BY_ID_SQL: str = """
    SELECT * FROM backtest_reports WHERE id = :report_id
    """
    INSERT_BACKTEST_REPORT_SQL: str = """
    INSERT INTO backtest_reports (id, description, start_date, end_date, strategy_id) VALUES (
        ?, ?, ?, ?, ?
    )
    """

    UPDATE_BACKTEST_REPORT_SQL: str = """
    UPDATE backtest_reports SET 
        description = :description,
        start_date = :start_date,
        end_date = :end_date,
        strategy_id = :strategy_id
    WHERE 
    id = :backtest_report_id 
    AND 
    strategy_id = :strategy_id
    """

    DELETE_SQL: str = """
    DELETE FROM backtest_reports 
    WHERE 
    id = :backtest_report_id 
    AND 
    strategy_id = :strategy_id
    """

    @classmethod
    def insert(cls, backtest_report: BacktestReport) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.INSERT_BACKTEST_REPORT_SQL)

        query.addBindValue(backtest_report.id)
        query.addBindValue(backtest_report.description)
        query.addBindValue(backtest_report.start_date.strftime("%Y-%m-%d"))
        query.addBindValue(backtest_report.end_date.strftime("%Y-%m-%d"))
        query.addBindValue(backtest_report.strategy_id)
        return query.exec()

    @classmethod
    def update(cls, backtest_report: BacktestReport) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.UPDATE_BACKTEST_REPORT_SQL)
        query.bindValue(":description", backtest_report.description)
        query.bindValue(":start_date", backtest_report.start_date.strftime("%Y-%m-%d"))
        query.bindValue(":end_date", backtest_report.end_date.strftime("%Y-%m-%d"))
        query.bindValue(":strategy_id", backtest_report.strategy_id)
        query.bindValue(":backtest_report_id", backtest_report.id)
        return query.exec()

    @classmethod
    def query_by_id(cls, id: str) -> Union[BacktestReport, None]:
        report: Union[BacktestReport, None] = None

        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.SELECT_BY_ID_SQL)
        query.bindValue(":report_id", id)
        query.exec()

        if query.next():
            report = BacktestReport.from_query(query)
        return report

    @classmethod
    def query_by_strategy_id(cls, strategy_id: str) -> List[BacktestReport]:
        reports: List[BacktestReport] = []

        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.SELECT_BY_STRATEGY_ID_SQL)
        query.bindValue(":strategy_id", strategy_id)
        query.exec()

        while query.next():
            reports.append(BacktestReport.from_query(query))
        return reports

    @classmethod
    def delete(cls, backtest_report: BacktestReport) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.DELETE_SQL)
        query.bindValue(":backtest_report_id", backtest_report.id)
        query.bindValue(":strategy_id", backtest_report.strategy_id)
        return query.exec()
