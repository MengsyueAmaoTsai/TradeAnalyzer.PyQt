from typing import Optional, List, Union
from datetime import date as Date

from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHeaderView,
    QMenu,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QPoint, QDate, pyqtSignal
from PyQt6.QtGui import QAction

from ..entities import BacktestReport, Strategy
from ..repositories import BacktestReportRepository, OrderRepository, StrategyRepository
from .analysis_window import AnalysisWindow
from .analysis_setting_dialog import AnalysisSettingsDialog
from ..analysis import AnalysisResults, Analyzer, BenchmarkSymbol


class BacktestReportTable(QTableWidget):
    FIELDS: List[str] = ["Id", "Description", "Start Date", "End Date"]

    report_deleted: pyqtSignal = pyqtSignal()
    strategy_updated: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setColumnCount(len(self.FIELDS))
        self.setHorizontalHeaderLabels(self.FIELDS)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.customContextMenuRequested.connect(self.on_context_menu_requested)
        self.verticalHeader().setVisible(False)

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def current_backtest_report_id(self) -> str:
        return self.item(self.currentRow(), 0).text().strip()

    @property
    def selected_backtest_reports(self) -> List[BacktestReport]:
        backtest_reports: List[BacktestReport] = []

        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())
        for row in selected_rows:
            backtest_report_id: str = self.item(row, 0).text().strip()
            backtest_report: Union[
                BacktestReport, None
            ] = BacktestReportRepository.query_by_id(backtest_report_id)
            if backtest_report:
                backtest_reports.append(backtest_report)
        return backtest_reports

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_context_menu_requested(self, point: QPoint) -> None:
        if not self.selectedItems():
            return

        menu: QMenu = QMenu(self)
        as_default_action: QAction = menu.addAction("Set As Default")
        as_default_action.triggered.connect(self.on_as_default_action_clicked)

        delete_action: QAction = menu.addAction("Delete")
        delete_action.triggered.connect(self.on_delete_action_clicked)

        menu.addSeparator()
        analyze_action: QAction = menu.addAction("Analyze Backtest Report")
        analyze_action.triggered.connect(self.on_analyze_action_clicked)

        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())

        if len(selected_rows) > 1:
            as_default_action.setEnabled(False)
            delete_action.setEnabled(False)
            analyze_action.setText("Analyze Backtest Reports")
        menu.exec(self.mapToGlobal(point))

    def on_as_default_action_clicked(self, checked: bool) -> None:
        report: Union[BacktestReport, None] = BacktestReportRepository.query_by_id(
            self.current_backtest_report_id
        )
        assert report is not None

        strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
            report.strategy_id
        )
        assert strategy is not None
        strategy.default_report_id = report.id

        result: bool = StrategyRepository.update(strategy)

        if not result:
            QMessageBox.warning(
                self, "WARN", "Error on updating strategy default report."
            )
            return

        QMessageBox.information(self, "INFO", "Update success.")
        self.strategy_updated.emit()
        return

    def on_delete_action_clicked(self, checked: bool) -> None:
        report: Union[BacktestReport, None] = BacktestReportRepository.query_by_id(
            self.current_backtest_report_id
        )

        if not report:
            return

        report_deleted: bool = BacktestReportRepository.delete(report)

        if not report_deleted:
            QMessageBox.warning(self, "WARN", "Error on deleting backtest report.")
            return

        orders_deleted: bool = OrderRepository.delete_by_strategy_id(
            f"{report.strategy_id}:{report.id}"
        )
        if not orders_deleted:
            QMessageBox.warning(self, "WARN", "Error on deleting orders.")
            return

        QMessageBox.information(self, "INFO", "Backtest report deleted.")
        self.report_deleted.emit()
        return

    def on_analyze_action_clicked(self, checked: bool) -> None:
        strategies: List[Strategy] = []
        for report in self.selected_backtest_reports:
            strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
                report.strategy_id
            )
            assert strategy is not None
            strategy.default_report_id = report.id
            strategies.append(strategy)

        self.__setting_dialog: AnalysisSettingsDialog = AnalysisSettingsDialog()
        self.__setting_dialog.analysis_settings_confirmed.connect(
            self.on_analysis_setting_confirmed
        )
        self.__setting_dialog.starting_capital = max(
            strategy.starting_capital for strategy in strategies
        )
        self.__setting_dialog.start_date = max(
            report.start_date for report in self.selected_backtest_reports
        )
        self.__setting_dialog.end_date = min(
            report.end_date for report in self.selected_backtest_reports
        )
        self.__setting_dialog.exec()

    def on_analysis_setting_confirmed(
        self,
        starting_capital: float,
        start_date: Date,
        end_date: Date,
        benchmark_sybol: BenchmarkSymbol,
    ) -> None:
        results: AnalysisResults = Analyzer.analyze_reports(
            self.selected_backtest_reports,
            starting_capital,
            start_date,
            end_date,
            benchmark_sybol,
        )
        self.__analysis_window: AnalysisWindow = AnalysisWindow(results)
        self.__analysis_window.showMaximized()

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_backtest_reports(self, backtest_reports: List[BacktestReport]) -> None:
        self.clearContents()
        self.setRowCount(0)

        for report in backtest_reports:
            row: int = self.rowCount()
            self.setRowCount(row + 1)

            self.setItem(row, 0, QTableWidgetItem(report.id))
            self.setItem(row, 1, QTableWidgetItem(report.description))
            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    QDate(
                        report.start_date.year,
                        report.start_date.month,
                        report.start_date.day,
                    ).toString("yyyy-MM-dd")
                ),
            )
            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    QDate(
                        report.end_date.year, report.end_date.month, report.end_date.day
                    ).toString("yyyy-MM-dd")
                ),
            )

    # -------------------------------------------------- Private Methods --------------------------------------------------
