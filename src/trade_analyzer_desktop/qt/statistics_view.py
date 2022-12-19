from typing import Optional

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout

from ..analysis import AnalysisResults, StrategyPerformance


class StatisticsView(QWidget):

    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Widgets
        self.__total_net_profit: QLabel = QLabel("Total Net Profit:")
        self.__total_number_of_trades: QLabel = QLabel("# of Trades:")

        self.__average_winning_trade_duration: QLabel = QLabel("Average Winning Trade Duration:")
        self.__average_lossing_trade_duration: QLabel = QLabel("Average Lossing Trade Duration:")
        self.__max_drawdown: QLabel = QLabel("Max Drawdown:")
        self.__max_drawdown_percent: QLabel = QLabel("Max Drawdown%:")
        self.__annual_return: QLabel = QLabel("Annual Return%:")
        self.__sharpe_ratio: QLabel = QLabel("Sharpe Ratio:")
        self.__sortino_ratio: QLabel = QLabel("Sortino Ratio:")


        # Layout 
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(self.__total_net_profit)
        layout.addWidget(self.__average_winning_trade_duration)
        layout.addWidget(self.__average_lossing_trade_duration)
        layout.addWidget(self.__max_drawdown)
        layout.addWidget(self.__max_drawdown_percent)
        layout.addWidget(self.__annual_return)
        layout.addWidget(self.__sharpe_ratio)
        layout.addWidget(self.__sortino_ratio)

        # Data
        
    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_performance(self, performance: StrategyPerformance) -> None:
        self.__total_net_profit.setText(f"Total Net Profit: {round(performance.trade_statistics.total_net_profit, 2)}")
        self.__total_number_of_trades.setText(f"# of Trades: {round(performance.trade_statistics.total_number_of_trades, 2)}")
        self.__average_winning_trade_duration.setText(f"Average Winning Trade Duration: {performance.trade_statistics.average_winning_trade_duration}")
        self.__average_lossing_trade_duration.setText(f"Average Lossing Trade Duration: {performance.trade_statistics.average_lossing_trade_duration}")
        self.__max_drawdown.setText(f"Max Drawdown: {round(performance.trade_statistics.max_closed_trade_drawdown)}")
        self.__max_drawdown_percent.setText(f"Max Drawdown%: {round(max(performance.trade_statistics.drawdown_percent.values()))}")
        print("set performance")       
        
    # -------------------------------------------------- Private Methods --------------------------------------------------