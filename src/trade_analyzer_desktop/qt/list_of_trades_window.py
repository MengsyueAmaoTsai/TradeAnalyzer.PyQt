from typing import Optional, List

from PyQt6.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel, QPushButton

from .trade_table import TradeTable
from ..analysis import AnalysisResults
from ..entities import Trade
from ..enums import Side

class ListOfTradesWindow(QWidget):

    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("List of Trades")

        # Widgets
        self.__data_set_combo: QComboBox = QComboBox()
        self.__data_set_combo.currentIndexChanged.connect(self.on_data_set_combo_current_index_changed)

        self.__all_side_button: QPushButton = QPushButton("All")
        self.__all_side_button.setAutoExclusive(True)
        self.__all_side_button.setCheckable(True)
        self.__all_side_button.setChecked(True)
        self.__all_side_button.clicked.connect(self.on_all_side_button_clicked)

        self.__long_side_button: QPushButton = QPushButton("Long")
        self.__long_side_button.setAutoExclusive(True)
        self.__long_side_button.setCheckable(True)
        self.__long_side_button.clicked.connect(self.on_long_side_button_clicked)

        self.__short_side_button: QPushButton = QPushButton("Short")
        self.__short_side_button.setAutoExclusive(True)
        self.__short_side_button.setCheckable(True)
        self.__short_side_button.clicked.connect(self.on_short_side_button_clicked)
        
        self.__trade_table: TradeTable = TradeTable(self)
        
        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(QLabel("Data Set"), 0, 0, 1, 1)
        layout.addWidget(self.__data_set_combo, 0, 1, 1, 3)
        layout.addWidget(QLabel("Side"), 0, 4, 1, 1)
        layout.addWidget(self.__all_side_button, 0, 5, 1, 1)
        layout.addWidget(self.__long_side_button, 0, 6, 1, 1)
        layout.addWidget(self.__short_side_button, 0, 7, 1, 1)
        layout.addWidget(self.__trade_table, 1, 0, 9, 10)

        # Data
        self.__analysis_results: AnalysisResults = results

        for key in results.keys:
            if key.startswith("Benchmark:"):
                continue
            self.__data_set_combo.addItem(key, results.get(key)) 
        self.__trade_table.set_trades(self.current_trade_list)
        
    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def current_trade_list(self) -> List[Trade]:
        return self.__data_set_combo.currentData().total_performance.closed_trades

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_data_set_combo_current_index_changed(self, index: int) -> None:
        self.__trade_table.set_trades(self.current_trade_list)

    def on_all_side_button_clicked(self, checked: bool) -> None:
        if checked:
            self.__trade_table.set_trades(self.current_trade_list)

    def on_long_side_button_clicked(self, checked: bool) -> None:
        if checked:
            long_trades: List[Trade] = list(filter(lambda trade: trade.side == Side.Long, self.current_trade_list))
            self.__trade_table.set_trades(long_trades)

    def on_short_side_button_clicked(self, checked: bool) -> None:
        if checked:
            long_trades: List[Trade] = list(filter(lambda trade: trade.side == Side.Short, self.current_trade_list))
            self.__trade_table.set_trades(long_trades)

    # -------------------------------------------------- Public Methods --------------------------------------------------

    # -------------------------------------------------- Private Methods -------------------------------------------------- 