
from typing import Optional, List, Union

from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QWidget, QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction

from ..entities import Trade
from .trade_detail_dialog import TradeDetialDialog


class TradeTable(QTableWidget):

    FIELDS: List[str] = [
        "#", "Symbol", "Side", "Entry Time", "Entry Price", "Size", "Exit Time", "Exit Price", "Gross P/L", "Fee", "Net P/L",
        "MAE", "MFE", "End Trade Drawdown", "Duration", "Strategy"
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setColumnCount(len(self.FIELDS))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setHorizontalHeaderLabels(self.FIELDS)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu_requested)

        self.__trades: List[Trade] = []

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def current_strategy_id(self) -> int:
        return int(self.item(self.currentRow(), 0).text().strip())

    @property
    def current_trade(self) -> Union[Trade, None]:
        return next(filter(lambda trade: trade.id == self.current_strategy_id, self.__trades), None)
    # -------------------------------------------------- Event Handlers --------------------------------------------------

    def on_context_menu_requested(self, point: QPoint) -> None:
        selected_rows: set[int] = set(index.row() for index in self.selectedIndexes())        
        if not self.selectedItems() or len(selected_rows) > 1:
            return 

        menu: QMenu = QMenu(self)
        detail_action: QAction = menu.addAction("Detail")
        detail_action.triggered.connect(self.on_detail_action_clicked)

        menu.exec(self.mapToGlobal(point))      

    def on_detail_action_clicked(self, checked: bool) -> None:
        assert(self.current_trade is not None)
        self.__trade_detail_dialog: TradeDetialDialog = TradeDetialDialog(self.current_trade)
        self.__trade_detail_dialog.exec()                  

    # -------------------------------------------------- Public Methods --------------------------------------------------
            
    def set_trades(self, trades: List[Trade]) -> None:
        self.clearContents()
        self.setRowCount(0)

        for trade in trades:
            row: int = self.rowCount()
            self.setRowCount(row + 1)
            self.setItem(row, 0, QTableWidgetItem(str(trade.id)))     
            self.setItem(row, 1, QTableWidgetItem(trade.symbol))     
            self.setItem(row, 2, QTableWidgetItem(trade.side.value))     
            self.setItem(row, 3, QTableWidgetItem(str(trade.entry_time)))     
            self.setItem(row, 4, QTableWidgetItem(str(round(trade.entry_price, 2))))     
            self.setItem(row, 5, QTableWidgetItem(str(round(trade.trade_size, 2))))     
            self.setItem(row, 6, QTableWidgetItem(str(trade.exit_time)))     
            self.setItem(row, 7, QTableWidgetItem(str(round(trade.exit_price, 2))))     
            self.setItem(row, 8, QTableWidgetItem(str(round(trade.gross_profit_loss, 2))))     
            self.setItem(row, 9, QTableWidgetItem(str(round(trade.fee, 2))))     
            self.setItem(row, 10, QTableWidgetItem(str(round(trade.net_profit_loss, 2))))     
            self.setItem(row, 11, QTableWidgetItem(str(round(trade.mae, 2))))     
            self.setItem(row, 12, QTableWidgetItem(str(round(trade.mfe, 2))))
            self.setItem(row, 13, QTableWidgetItem(str(round(trade.end_trade_drawdown, 2))))     
            self.setItem(row, 14, QTableWidgetItem(str(trade.duration)))     
            self.setItem(row, 15, QTableWidgetItem(trade.strategy_id))     

        self.resizeColumnsToContents()
        self.__trades = trades

    # -------------------------------------------------- Private Methods --------------------------------------------------
