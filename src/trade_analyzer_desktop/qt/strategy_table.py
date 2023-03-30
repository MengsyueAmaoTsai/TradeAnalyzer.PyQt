from typing import Optional, List, Union
from datetime import date as Date

from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHeaderView,
    QMenu,
    QMessageBox,
    QFileDialog,
    QTableWidgetSelectionRange,
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

from .analysis_setting_dialog import AnalysisSettingsDialog
from .edit_strategy_dialog import EditStrategyDialog
from .upload_backtest_report_dialog import UploadBacktestReportDialog
from ..entities import BacktestReport, Strategy
from ..analysis import Analyzer, BenchmarkSymbol, AnalysisResults
from .analysis_window import AnalysisWindow
from ..repositories import StrategyRepository, BacktestReportRepository, OrderRepository


class StrategyTable(QTableWidget):
    FIELDS: List[str] = [
        "ID",
        "Description",
        "Type",
        "Resolution",
        "Side",
        "Trading Platform",
        "Starting Capital",
        "Default Backtest Report",
    ]

    strategy_deleted: pyqtSignal = pyqtSignal()
    backtest_report_uploaded: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.strategy_deleted.connect(self.on_strategy_deleted)
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
    def current_strategy_id(self) -> str:
        return self.item(self.currentRow(), 0).text().strip()

    @property
    def selected_strategies(self) -> List[Strategy]:
        strategies: List[Strategy] = []
        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())
        for row in selected_rows:
            strategy_id: str = self.item(row, 0).text().strip()
            strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
                strategy_id
            )
            if strategy:
                strategies.append(strategy)
        return strategies

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_context_menu_requested(self, point: QPoint) -> None:
        if not self.selectedItems():
            return

        menu: QMenu = QMenu(self)

        edit_action: QAction = menu.addAction("Edit")
        edit_action.triggered.connect(self.on_edit_action_clicked)

        delete_action: QAction = menu.addAction("Delete")
        delete_action.triggered.connect(self.on_delete_action_clicked)

        menu.addSeparator()

        upload_report_action: QAction = menu.addAction("Upload Backtest Report")
        upload_report_action.triggered.connect(self.on_upload_report_action_clicked)

        create_portfolio_action: QAction = menu.addAction("Create Portfolio")
        create_portfolio_action.triggered.connect(
            self.on_create_portfolio_action_clicked
        )

        analyze_action: QAction = menu.addAction("Analyze Strategy")
        analyze_action.triggered.connect(self.on_analyze_action_clicked)

        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())

        if len(selected_rows) > 1:
            edit_action.setEnabled(False)
            delete_action.setEnabled(False)
            upload_report_action.setEnabled(False)
            analyze_action.setText("Analyze Strategies")
        else:
            create_portfolio_action.setEnabled(False)

        menu.exec(self.mapToGlobal(point))

    def on_edit_action_clicked(self, checked: bool) -> None:
        strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
            self.current_strategy_id
        )

        if not strategy:
            return
        self.__strategy_form: EditStrategyDialog = EditStrategyDialog(self)
        self.__strategy_form.strategy_updated.connect(self.on_strategy_updated)
        self.__strategy_form.id = strategy.id
        self.__strategy_form.description = strategy.description
        self.__strategy_form.type = strategy.type
        self.__strategy_form.resolution = strategy.resolution
        self.__strategy_form.side = strategy.side
        self.__strategy_form.platform = strategy.platform
        self.__strategy_form.starting_capital = strategy.starting_capital
        self.__strategy_form.exec()

    def on_delete_action_clicked(self, checked: bool) -> None:
        strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
            self.current_strategy_id
        )

        if not strategy:
            return

        backtest_reports: List[
            BacktestReport
        ] = BacktestReportRepository.query_by_strategy_id(strategy.id)

        reply: QMessageBox.StandardButton = QMessageBox.StandardButton.Yes

        if len(backtest_reports) != 0:
            reply = QMessageBox.question(
                self,
                "QUESTION",
                f"There are still {len(backtest_reports)} reports in this strategy. Make sure to delete?",
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.No,
            )

        if reply == QMessageBox.StandardButton.No:
            return

        strategy_deleted: bool = StrategyRepository.delete(strategy)

        if not strategy_deleted:
            QMessageBox.warning(self, "WARN", "Error")
            return

        for report in backtest_reports:
            BacktestReportRepository.delete(report)
            OrderRepository.delete_by_strategy_id(f"{report.strategy_id}:{report.id}")

        QMessageBox.information(self, "INFO", "Strategy deleted.")
        self.strategy_deleted.emit()
        return

    def on_upload_report_action_clicked(self, checked: bool) -> None:
        path: str = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "C:/RichillCapital/Output/Bots/Executions/History",
            "Text File(*.txt)",
        )[0]

        if path.isspace() or path.__eq__(str()):
            return
        backtest_report_id: str = path.split("/")[-1].split(".")[0]

        self.__upload_backtest_report_dialog: UploadBacktestReportDialog = (
            UploadBacktestReportDialog(path)
        )
        self.__upload_backtest_report_dialog.backtest_report_uploaded.connect(
            self.on_backtest_report_uploaded
        )
        self.__upload_backtest_report_dialog.strategy_id = self.current_strategy_id
        self.__upload_backtest_report_dialog.backtest_report_id = backtest_report_id
        self.__upload_backtest_report_dialog.exec()

    def on_create_portfolio_action_clicked(self, checked: bool) -> None:
        strategies: List[Strategy] = []
        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())

        for row in selected_rows:
            strategy_id: str = self.item(row, 0).text().strip()
            strategy: Union[Strategy, None] = StrategyRepository.query_by_id(
                strategy_id
            )
            if strategy:
                strategies.append(strategy)

        # TODO: Create a portfolio.

    def on_analyze_action_clicked(self, checked: bool) -> None:
        reports: List[BacktestReport] = []
        for strategy in self.selected_strategies:
            if not strategy.default_report_id:
                QMessageBox.warning(
                    self,
                    "WARN",
                    f"Default report must be set before analyzing the strategy. {strategy.id}",
                )
                return
            report: Union[BacktestReport, None] = BacktestReportRepository.query_by_id(
                strategy.default_report_id
            )
            assert report is not None
            reports.append(report)

        self.__setting_dialog: AnalysisSettingsDialog = AnalysisSettingsDialog()
        self.__setting_dialog.analysis_settings_confirmed.connect(
            self.on_analysis_setting_confirmed
        )
        self.__setting_dialog.starting_capital = max(
            strategy.starting_capital for strategy in self.selected_strategies
        )
        self.__setting_dialog.start_date = max(report.start_date for report in reports)
        self.__setting_dialog.end_date = min(report.end_date for report in reports)
        self.__setting_dialog.exec()

    def on_analysis_setting_confirmed(
        self,
        starting_capital: float,
        start_date: Date,
        end_date: Date,
        benchmark_sybol: BenchmarkSymbol,
    ) -> None:
        results: AnalysisResults = Analyzer.analyze_strategies(
            self.selected_strategies,
            starting_capital,
            start_date,
            end_date,
            benchmark_sybol,
        )
        self.__analysis_window: AnalysisWindow = AnalysisWindow(results)
        self.__analysis_window.showMaximized()

    def on_strategy_updated(self) -> None:
        strategies: List[Strategy] = StrategyRepository.query_all()
        self.set_strategies(strategies)

    def on_strategy_deleted(self) -> None:
        strategies: List[Strategy] = StrategyRepository.query_all()
        self.set_strategies(strategies)

    def on_backtest_report_uploaded(self) -> None:
        self.backtest_report_uploaded.emit()

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_strategies(self, strategies: List[Strategy]) -> None:
        self.clearContents()
        self.setRowCount(0)

        for strategy in strategies:
            row: int = self.rowCount()
            self.setRowCount(row + 1)

            self.setItem(row, 0, QTableWidgetItem(strategy.id))
            self.setItem(row, 1, QTableWidgetItem(strategy.description))
            self.setItem(row, 2, QTableWidgetItem(strategy.type.value))
            self.setItem(row, 3, QTableWidgetItem(strategy.resolution.value))
            self.setItem(row, 4, QTableWidgetItem(strategy.side.value))
            self.setItem(row, 5, QTableWidgetItem(strategy.platform.value))
            self.setItem(row, 6, QTableWidgetItem(str(strategy.starting_capital)))
            self.setItem(row, 7, QTableWidgetItem(strategy.default_report_id))

        if self.rowCount() != 0:
            self.selectRow(0)

    # -------------------------------------------------- Private Methods --------------------------------------------------
