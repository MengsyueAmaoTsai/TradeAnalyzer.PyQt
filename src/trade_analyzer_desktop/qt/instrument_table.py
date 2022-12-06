from typing import Optional, List 

from PyQt6.QtWidgets import QTableWidget, QWidget, QHeaderView, QTableWidgetItem, QComboBox

from ..entities import Instrument, Exchange
from ..enums import InstrumentType


class InstrumentTable(QTableWidget):

    FIELDS: List[str] = [
        "Symbol", "Description", "Exchange", "Type", "Fee Pricing", "Point Value"
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setColumnCount(len(self.FIELDS))
        self.setHorizontalHeaderLabels(self.FIELDS)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)        

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def instruments(self) -> List[Instrument]:
        instruments: list[Instrument] = [Instrument(
            self.item(row, 0).text().strip(),
            self.item(row, 1).text().strip(),
            self.cellWidget(row, 2).currentData(),
            self.cellWidget(row, 3).currentData(),
            float(self.item(row, 4).text().strip()),
            float(self.item(row, 5).text().strip())
        ) for row in range(self.rowCount())]
        return instruments
    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_instruments(self, instruments: List[Instrument]) -> None:
        self.clearContents()
        self.setRowCount(0)

        for instrument in instruments:
            self.add_instrument(instrument)

    def add_instrument(self, instrument: Instrument) -> None:
        row: int = self.rowCount()
        self.setRowCount(row + 1)

        self.setItem(row, 0, QTableWidgetItem(instrument.symbol))
        self.setItem(row, 1, QTableWidgetItem(instrument.description))
        
        exchange_combo: QComboBox = QComboBox()
        for id in Exchange.SUPPORTS_EXCHANGES:
            exchange_combo.addItem(id, id)

        assert(instrument.exchange is not None)
        exchange_combo.setCurrentIndex(Exchange.SUPPORTS_EXCHANGES.index(instrument.exchange.id))
        self.setCellWidget(row, 2, exchange_combo)

        instrument_type_combo: QComboBox = QComboBox()
        for index, type in enumerate(InstrumentType):
            instrument_type_combo.addItem(type.value, type)
        instrument_type_combo.setCurrentIndex(list(InstrumentType).index(instrument.type))
        self.setCellWidget(row, 3, instrument_type_combo)
        
        self.setItem(row, 4, QTableWidgetItem(str(instrument.fee_pricing)))
        self.setItem(row, 5, QTableWidgetItem(str(instrument.point_value)))

        if self.editTriggers() == QTableWidget.EditTrigger.NoEditTriggers:
            exchange_combo.setEnabled(False)
            instrument_type_combo.setEnabled(False)
    # -------------------------------------------------- Private Methods --------------------------------------------------

    