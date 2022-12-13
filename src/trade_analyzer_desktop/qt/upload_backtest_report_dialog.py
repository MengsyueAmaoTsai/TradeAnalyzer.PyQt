from typing import Optional, List, Union
from datetime import date as Date

from PyQt6.QtWidgets import QDialog, QWidget, QGridLayout, QMessageBox, QPushButton, QLineEdit, QLabel, QDateEdit
from PyQt6.QtCore import QDate, pyqtSignal

from ..entities import BacktestReport, Order, Instrument
from ..repositories import BacktestReportRepository, OrderRepository, InstrumentRepository
from .text_file_order_provider import TextFileOrderProvider
from .instrument_table import InstrumentTable
from ..enums import InstrumentType


class UploadBacktestReportDialog(QDialog):

    DATE_FORMAT: str = "yyyy-MM-dd"

    backtest_report_uploaded: pyqtSignal = pyqtSignal()

    def __init__(self, path: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Upload Backtest Report")
        self.resize(800, 600)

        # Widgets
        self.__strategy_id_input: QLineEdit = QLineEdit()
        self.__strategy_id_input.setReadOnly(True)

        self.__backtest_report_id_input: QLineEdit = QLineEdit()
        self.__backtest_report_id_input.textChanged.connect(self.on_backtest_report_id_text_changed)

        self.__description_input: QLineEdit = QLineEdit()

        self.__start_date_input: QDateEdit = QDateEdit()
        self.__start_date_input.setCalendarPopup(True)
        self.__start_date_input.setDisplayFormat(self.DATE_FORMAT)
        
        self.__end_date_input: QDateEdit = QDateEdit()
        self.__end_date_input.dateChanged.connect(self.on_end_date_changed)
        self.__end_date_input.setCalendarPopup(True)
        self.__end_date_input.setDisplayFormat(self.DATE_FORMAT)
        
        self.__new_instruments_label: QLabel = QLabel()
        self.__instruments_table: InstrumentTable = InstrumentTable()
        
        self.__upload_button: QPushButton = QPushButton("Upload")
        self.__upload_button.clicked.connect(self.on_upload_button_clicked)
        self.__upload_button.setEnabled(False)

        self.__cancel_button: QPushButton = QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.on_cancel_button_clicked)

        # Layout
        layout: QGridLayout = QGridLayout(self)

        layout.addWidget(QLabel("Strategy Id"), 0, 0, 1, 1)
        layout.addWidget(self.__strategy_id_input, 0, 1, 1, 3)

        layout.addWidget(QLabel("Backtest Report Id"), 1, 0, 1, 1)
        layout.addWidget(self.__backtest_report_id_input, 1, 1, 1, 3)

        layout.addWidget(QLabel("Description"), 1, 4, 1, 1)
        layout.addWidget(self.__description_input, 1, 5, 1, 6)

        layout.addWidget(QLabel("Start Date"), 2, 0, 1, 1)
        layout.addWidget(self.__start_date_input, 2, 1, 1, 2)

        layout.addWidget(QLabel("End Date"), 2, 3, 1, 1)
        layout.addWidget(self.__end_date_input, 2, 4, 1, 2)

        layout.addWidget(self.__new_instruments_label, 3, 0, 1, 4)
        layout.addWidget(self.__instruments_table, 4, 0, 4, 10)

        layout.addWidget(self.__upload_button, 9, 0, 1, 1)
        layout.addWidget(self.__cancel_button, 9, 1, 1, 1)

        # Default Data
        self.__start_date_input.setDate(QDate(2020, 1, 1))
        self.__end_date_input.setDate(QDate.currentDate())

        self.__orders_from_file: List[Order] = TextFileOrderProvider.read(path)

        # New instruments
        new_symbols: List[str] = []
        for order in self.__orders_from_file:
            if order.symbol not in new_symbols:
                new_symbols.append(order.symbol)
        instruments: List[Instrument] = [self.__guess_instrument(symbol) for symbol in new_symbols if not (InstrumentRepository.query_by_symbol(symbol))]
        self.__instruments_table.set_instruments(instruments)
        self.__new_instruments_label.setText(f"New instruments: {len(instruments)}")
        del instruments

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def strategy_id(self) -> str:
        return self.__strategy_id_input.text().strip()
    
    @strategy_id.setter
    def strategy_id(self, strategy_id: str) -> None:
        self.__strategy_id_input.setText(strategy_id)

    @property
    def backtest_report_id(self) -> str:
        return self.__backtest_report_id_input.text().strip()
    
    @backtest_report_id.setter
    def backtest_report_id(self, backtest_report_id: str) -> None:
        self.__backtest_report_id_input.setText(backtest_report_id)

    @property
    def description(self) -> str:
        return self.__description_input.text().strip()

    @property
    def start_date(self) -> Date:
        return self.__start_date_input.date().toPyDate()
    
    @property
    def end_date(self) -> Date:
        return self.__end_date_input.date().toPyDate()
    
    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_backtest_report_id_text_changed(self, backtest_report_id: str) -> None:
        self.__upload_button.setEnabled(False) if backtest_report_id.isspace() or backtest_report_id.__eq__(str()) else self.__upload_button.setEnabled(True)

    def on_end_date_changed(self, date: QDate) -> None:
        if date.toPyDate() > QDate.currentDate().toPyDate():
            self.__end_date_input.setDate(QDate.currentDate())

    def on_upload_button_clicked(self, checked: bool) -> None:
        backtest_report: Union[BacktestReport, None] = next(
            filter(lambda report: report.id == self.backtest_report_id, BacktestReportRepository.query_by_strategy_id(self.strategy_id)), None
        )

        if backtest_report:
            QMessageBox.warning(self, "WARN", f"Backtest report with {self.backtest_report_id} of strategy: {self.strategy_id} already exists.")
            return 
            
        report_created: bool = self.__create_backtest_report(
            self.backtest_report_id,
            self.description,
            self.start_date,
            self.end_date,
            self.strategy_id
        )
        if not report_created:
            QMessageBox.warning(self, "WARN", "Error on create report.")
            return
        
        # Insert instruments
        instruments_created: bool = self.__create_instruments(self.__instruments_table.instruments)
        if not instruments_created:
            QMessageBox.warning(self, "WARN", "Error on create instruments.")
            return            

        # Insert orders
        filted_orders: List[Order] = list(filter(lambda order: order.datetime.date() >= self.start_date and order.datetime.date() <= self.end_date, self.__orders_from_file))
        
        orders_created: bool = self.__create_orders(filted_orders)

        if not orders_created:
            QMessageBox.warning(self, "WARN", "Error on create orders.")
            return            
            
        QMessageBox.information(self, "INFO", "Backtest report uploaded.")
        self.close()
        self.backtest_report_uploaded.emit()
        return

    def on_cancel_button_clicked(self, checked: bool) -> None:
        self.close()
    # -------------------------------------------------- Public Methods --------------------------------------------------

    # -------------------------------------------------- Private Methods --------------------------------------------------
    @classmethod
    def __create_backtest_report(cls, id: str, description: str, start_date: Date, end_date: Date, strategy_id: str) -> bool:
        backtest_report: BacktestReport = BacktestReport(id, description, start_date, end_date, strategy_id)
        return BacktestReportRepository.insert(backtest_report)

    def __create_instruments(self, instruments: List[Instrument]) -> bool:
        return InstrumentRepository.insert_batch(instruments)

    def __create_orders(self, orders_from_file: List[Order]) -> bool:
        orders: List[Order] = []
        for order in orders_from_file:
            order.strategy_id = f"{self.strategy_id}:{self.backtest_report_id}"
            orders.append(order)
        return OrderRepository.insert_batch(orders)

    @classmethod
    def __guess_instrument(cls, symbol: str) -> Instrument:
        exchange_id: str = ""
        instrument_type: InstrumentType = InstrumentType.Unknown
        fee_pricing: float = 0
        point_value: float = 0

        if symbol.lower().endswith(".tw"):
            exchange_id = "TWSE"
            instrument_type = InstrumentType.Equity
            fee_pricing = 0.0004
            point_value = 1000

        elif symbol.lower().endswith(".tf"):
            exchange_id = "TAIFEX"
            instrument_type = InstrumentType.Option if "TXO" in symbol else InstrumentType.Future
            point_value = 200

        return Instrument(
            symbol,
            "",
            exchange_id,
            instrument_type,
            fee_pricing,
            point_value  
        )