from typing import Optional

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout

from ..analysis import AnalysisResults, StrategyPerformance


class StatisticsView(QWidget):

    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Widgets

        # Layout 
        layout: QGridLayout = QGridLayout(self)
        self.__total_net_profit_label: QLabel = QLabel()
        layout.addWidget(self.__total_net_profit_label)

        # Data
        self.__analysis_results: AnalysisResults = results
        
    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_data(self, performance: StrategyPerformance) -> None:
        total_net_profit: float = performance.trade_statistics.total_net_profit
        total_number_of_trades: int = performance.trade_statistics.total_number_of_trades
        number_of_winning_trades: int = performance.trade_statistics.number_of_winning_trades            
        number_of_lossing_trades: int = performance.trade_statistics.number_of_lossing_trades            
        
    # -------------------------------------------------- Private Methods --------------------------------------------------