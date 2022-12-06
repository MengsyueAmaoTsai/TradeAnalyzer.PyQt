from typing import Optional

from PyQt6.QtWidgets import QWidget, QTabWidget, QGridLayout

from .overview_window import OverviewWindow
from .equity_chart_window import EquityChartWindow
from .trade_analysis_window import TradeAnalysisWindow
from .list_of_trades_window import ListOfTradesWindow
from .correlation_analysis_window import CorrelationAnalysisWindow
from ..analysis import AnalysisResults

class AnalysisWindow(QWidget):

    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Analysis Results")

        # Widgets
        self.__overview_window: OverviewWindow = OverviewWindow(results)
        self.__equity_chart_window: EquityChartWindow = EquityChartWindow(results)
        self.__trade_analysis_window: TradeAnalysisWindow = TradeAnalysisWindow(results)
        self.__list_of_trades_window: ListOfTradesWindow = ListOfTradesWindow(results)
        self.__correlation_analysis_window: CorrelationAnalysisWindow = CorrelationAnalysisWindow(results)

        self.__tab: QTabWidget = QTabWidget(self)
        self.__tab.addTab(self.__overview_window, self.__overview_window.windowTitle())
        self.__tab.addTab(self.__equity_chart_window, self.__equity_chart_window.windowTitle())
        self.__tab.addTab(self.__trade_analysis_window, self.__trade_analysis_window.windowTitle())
        self.__tab.addTab(self.__list_of_trades_window, self.__list_of_trades_window.windowTitle())
        self.__tab.addTab(self.__correlation_analysis_window, self.__correlation_analysis_window.windowTitle())

        # Layout
        layout: QGridLayout = QGridLayout(self)

        layout.addWidget(self.__tab)

        # Data
        self.__analysis_results: AnalysisResults = results

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def analysis_results(self) -> AnalysisResults:
        return self.__analysis_results

    @analysis_results.setter
    def analysis_results(self, results: AnalysisResults) -> None:
        self.__analysis_results = results     

    # -------------------------------------------------- Event Handlers --------------------------------------------------        
    
    # -------------------------------------------------- Public Methods --------------------------------------------------        
    
    # -------------------------------------------------- Private Methods --------------------------------------------------        
