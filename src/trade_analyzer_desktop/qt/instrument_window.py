from typing import Optional, List

from PyQt6.QtWidgets import QWidget, QGridLayout, QDialog

from .instrument_table import InstrumentTable
from ..entities import Instrument
from ..repositories import InstrumentRepository


class InstrumentWindow(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Instruments")
        self.resize(600, 400)

        # Widgets
        self.__instrument_table: InstrumentTable = InstrumentTable()
        self.__instrument_table.setEditTriggers(
            InstrumentTable.EditTrigger.NoEditTriggers
        )

        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(self.__instrument_table)

        # Default data
        instruments: List[Instrument] = InstrumentRepository.query_all()
        self.__instrument_table.set_instruments(instruments)
