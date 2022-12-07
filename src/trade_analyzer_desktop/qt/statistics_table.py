from typing import Optional, List, Union

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from PyQt6.QtCore import Qt

from ..analysis import StatisticsResults, TradeStatistics, StrategyDailyStatistics, DailyStatistics

class StatisticsTable(QTableWidget):

    FIELDS: List[str] = [
        "Strategy", 
        "# of Trades", 
        "Net Profit", 
        "MDD", 
        "Win%", 
        "Profit Factor", 
        "Profit/Loss Ratio", 
        "Ret/DD Ratio", 
        "Annual Returns%",
        "ALPHA", 
        "BETA", 
        "Sharpe Ratio", 
        "Sortino Ratio", 
        "Information Ratio", 
        "Tracking Error", 
        "Treynor Ratio"
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.verticalHeader().setVisible(False)        
        self.setColumnCount(len(self.FIELDS))
        self.setHorizontalHeaderLabels(self.FIELDS)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.on_context_menu_requested)

    
    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------

    def add_statistics_results(self, key: str, statistics_results: StatisticsResults) -> None:
        trade_statistics: Union[TradeStatistics, None] = statistics_results.total_performance.trade_statistics
        daily_statistics: Union[StrategyDailyStatistics, DailyStatistics, None] = statistics_results.total_performance.daily_statistics
        assert(trade_statistics is not None and daily_statistics is not None and isinstance(daily_statistics, StrategyDailyStatistics))

        row: int = self.rowCount()
        self.setRowCount(row + 1)
        self.setItem(row, 0, QTableWidgetItem(key))
        self.setItem(row, 1, QTableWidgetItem(str(trade_statistics.total_number_of_trades)))
        self.setItem(row, 2, QTableWidgetItem(str(round(trade_statistics.total_net_profit, 2))))
        self.setItem(row, 3, QTableWidgetItem(str(round(trade_statistics.max_closed_trade_drawdown, 2))))
        self.setItem(row, 4, QTableWidgetItem(str(f"{round(trade_statistics.win_rate * 100, 2)}%")))
        self.setItem(row, 5, QTableWidgetItem(str(round(trade_statistics.profit_factor, 2))))
        self.setItem(row, 6, QTableWidgetItem(str(round(trade_statistics.profit_loss_ratio, 2))))
        self.setItem(row, 7, QTableWidgetItem(str(round(trade_statistics.profit_to_max_drawdown_ratio, 2))))
        self.setItem(row, 8, QTableWidgetItem(str(f"{round(daily_statistics.compounding_annual_return * 100, 2)}%")))
        self.setItem(row, 9, QTableWidgetItem(str(round(daily_statistics.alpha, 2))))
        self.setItem(row, 10, QTableWidgetItem(str(round(daily_statistics.beta, 2))))
        self.setItem(row, 11, QTableWidgetItem(str(round(daily_statistics.sharpe_ratio, 2))))
        self.setItem(row, 12, QTableWidgetItem(str(round(trade_statistics.sortino_ratio, 2))))
        self.setItem(row, 13, QTableWidgetItem(str(round(daily_statistics.information_ratio, 2))))
        self.setItem(row, 14, QTableWidgetItem(str(round(daily_statistics.tracking_error, 2))))
        self.setItem(row, 15, QTableWidgetItem(str(round(daily_statistics.treynor_ratio, 2))))

        self.resizeColumnsToContents()
        
    # -------------------------------------------------- Private Methods --------------------------------------------------

