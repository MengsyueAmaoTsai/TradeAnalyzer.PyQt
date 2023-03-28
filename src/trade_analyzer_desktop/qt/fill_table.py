from typing import Optional, List

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from PyQt6.QtCore import Qt

from ..events import OrderFilledEvent


class FillTable(QTableWidget):
    FIELDS: List[str] = [
        "DateTime",
        "Action",
        "Filled Quantity",
        "Avg Filled Price",
        "Fee",
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setColumnCount(len(self.FIELDS))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setHorizontalHeaderLabels(self.FIELDS)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def set_fills(self, fills: List[OrderFilledEvent]) -> None:
        self.clearContents()
        self.setRowCount(0)

        for fill in fills:
            row: int = self.rowCount()
            self.setRowCount(row + 1)

            self.setItem(row, 0, QTableWidgetItem(str(fill.datetime)))
            self.setItem(row, 1, QTableWidgetItem(fill.action.value))
            self.setItem(row, 2, QTableWidgetItem(str(round(fill.filled_quantity, 2))))
            self.setItem(row, 3, QTableWidgetItem(str(round(fill.avg_filled_price))))
            self.setItem(row, 4, QTableWidgetItem(str(round(fill.fee, 2))))
        self.resizeColumnsToContents()
