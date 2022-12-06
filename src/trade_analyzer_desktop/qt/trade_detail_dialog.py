from typing import Optional

from PyQt6.QtWidgets import QDialog, QWidget, QGridLayout

from ..entities import Trade
from .fill_table import FillTable


class TradeDetialDialog(QDialog):

    def __init__(self, trade: Trade, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.resize(800, 600)
        self.setWindowTitle("Trade Details")
        
        # Widgets
        self.__fill_table: FillTable = FillTable()

        # Layout 
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(self.__fill_table)

        # Data
        self.__fill_table.set_fills(trade.fills)