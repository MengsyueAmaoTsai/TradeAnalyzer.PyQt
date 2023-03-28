from typing import Optional, List

from PyQt6.QtWidgets import QWidget, QGridLayout

from .strategy_table import StrategyTable
from .backtest_report_table import BacktestReportTable
from ..repositories import StrategyRepository, BacktestReportRepository
from ..entities import Strategy, BacktestReport


class StrategyWindow(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Strategies")

        # Widgets
        self.__strategy_table: StrategyTable = StrategyTable()
        self.__strategy_table.itemSelectionChanged.connect(
            self.on_strategy_table_item_section_changed
        )
        self.__strategy_table.backtest_report_uploaded.connect(
            self.on_backtest_report_uploaded
        )

        self.__backtest_report_table: BacktestReportTable = BacktestReportTable()
        self.__backtest_report_table.report_deleted.connect(self.on_report_deleted)
        self.__backtest_report_table.strategy_updated.connect(self.on_strategy_updated)

        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(self.__strategy_table)
        layout.addWidget(self.__backtest_report_table)

        # Default data
        strategies: List[Strategy] = StrategyRepository.query_all()
        self.__strategy_table.set_strategies(strategies)

    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_strategy_table_item_section_changed(self) -> None:
        backtest_reports: List[
            BacktestReport
        ] = BacktestReportRepository.query_by_strategy_id(
            self.__strategy_table.current_strategy_id
        )
        self.__backtest_report_table.set_backtest_reports(backtest_reports)

    def on_strategy_created(self) -> None:
        strategies: List[Strategy] = StrategyRepository.query_all()
        self.__strategy_table.set_strategies(strategies)

    def on_backtest_report_uploaded(self) -> None:
        backtest_reports: List[
            BacktestReport
        ] = BacktestReportRepository.query_by_strategy_id(
            self.__strategy_table.current_strategy_id
        )
        self.__backtest_report_table.set_backtest_reports(backtest_reports)

    def on_report_deleted(self) -> None:
        # TODO: If deleted report id is any strategy using it. Set strategy default report to null.
        backtest_reports: List[
            BacktestReport
        ] = BacktestReportRepository.query_by_strategy_id(
            self.__strategy_table.current_strategy_id
        )
        self.__backtest_report_table.set_backtest_reports(backtest_reports)

    def on_strategy_updated(self) -> None:
        strategies: List[Strategy] = StrategyRepository.query_all()
        self.__strategy_table.set_strategies(strategies)

    # -------------------------------------------------- Public Methods --------------------------------------------------

    # -------------------------------------------------- Private Methods --------------------------------------------------
