from typing import Optional
from datetime import date as Date

from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QDateEdit,
    QGridLayout,
)
from PyQt6.QtCore import pyqtSignal

from ..analysis import BenchmarkSymbol


class AnalysisSettingsDialog(QDialog):
    DATE_FORMAT: str = "yyyy-MM-dd"

    analysis_settings_confirmed: pyqtSignal = pyqtSignal(
        float, Date, Date, BenchmarkSymbol
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Widgets
        self.__starting_capital_input: QDoubleSpinBox = QDoubleSpinBox()
        self.__starting_capital_input.setMaximum(999999999)
        self.__starting_capital_input.setMinimum(100000)
        self.__starting_capital_input.setSingleStep(1000)

        self.__start_date_input: QDateEdit = QDateEdit()
        self.__start_date_input.setDisplayFormat(self.DATE_FORMAT)

        self.__end_date_input: QDateEdit = QDateEdit()
        self.__end_date_input.setDisplayFormat(self.DATE_FORMAT)

        self.__benchmark_combo: QComboBox = QComboBox()

        self.__confirm_button: QPushButton = QPushButton("Confirm")
        self.__confirm_button.clicked.connect(self.on_confirm_button_clicked)

        self.__cancel_button: QPushButton = QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.on_cancel_button_clicked)

        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(QLabel("Starting Capital"), 0, 0, 1, 1)
        layout.addWidget(self.__starting_capital_input, 0, 1, 1, 3)

        layout.addWidget(QLabel("Start Date"), 1, 0, 1, 1)
        layout.addWidget(self.__start_date_input, 1, 1, 1, 3)

        layout.addWidget(QLabel("End Date"), 2, 0, 1, 1)
        layout.addWidget(self.__end_date_input, 2, 1, 1, 3)

        layout.addWidget(QLabel("Benchmark"), 3, 0, 1, 1)
        layout.addWidget(self.__benchmark_combo, 3, 1, 1, 3)

        layout.addWidget(self.__confirm_button, 4, 0, 1, 2)
        layout.addWidget(self.__cancel_button, 4, 2, 1, 2)
        # Data
        for i, symbol in enumerate(BenchmarkSymbol):
            self.__benchmark_combo.addItem(symbol.value, symbol)

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def starting_capital(self) -> float:
        return self.__starting_capital_input.value()

    @starting_capital.setter
    def starting_capital(self, starting_capital: float) -> None:
        self.__starting_capital_input.setValue(starting_capital)

    @property
    def start_date(self) -> Date:
        return self.__start_date_input.date().toPyDate()

    @start_date.setter
    def start_date(self, date: Date) -> None:
        self.__start_date_input.setDate(date)

    @property
    def end_date(self) -> Date:
        return self.__end_date_input.date().toPyDate()

    @end_date.setter
    def end_date(self, date: Date) -> None:
        self.__end_date_input.setDate(date)

    @property
    def benchmark_symbol(self) -> BenchmarkSymbol:
        return self.__benchmark_combo.currentData()

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_confirm_button_clicked(self, checked: bool) -> None:
        self.close()
        self.analysis_settings_confirmed.emit(
            self.starting_capital, self.start_date, self.end_date, self.benchmark_symbol
        )

    def on_cancel_button_clicked(self, checked: bool) -> None:
        self.close()

    # -------------------------------------------------- Public Methods --------------------------------------------------

    # -------------------------------------------------- Private Methods --------------------------------------------------
