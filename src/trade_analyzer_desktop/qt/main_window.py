from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTabWidget,
    QGridLayout,
    QMenuBar,
    QMenu,
)
from PyQt6.QtGui import QAction

from .strategy_window import StrategyWindow
from .create_strategy_dialog import CreateStrategyDialog
from .instrument_window import InstrumentWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Trade Analyzer Desktop [Version 0.1.0]")

        # Menu
        # Menu - File
        file_menu: QMenu = self.menuBar().addMenu("File")
        new_menu: QMenu = file_menu.addMenu("New")

        new_strategy_action: QAction = new_menu.addAction("New Strategy")
        new_strategy_action.triggered.connect(self.on_new_strategy_action_clicked)

        # Menu - View
        view_menu: QMenu = self.menuBar().addMenu("View")

        instruments_action: QAction = view_menu.addAction("Instruments")
        instruments_action.triggered.connect(self.on_instruments_action_clicked)

        # Main
        self.__strategy_window: StrategyWindow = StrategyWindow()
        self.__tab: QTabWidget = QTabWidget()
        self.__tab.addTab(self.__strategy_window, self.__strategy_window.windowTitle())
        self.__tab.addTab(QWidget(), "Portfolios")
        self.setCentralWidget(self.__tab)

    # -------------------------------------------------- Properties --------------------------------------------------
    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_new_strategy_action_clicked(self, checked: bool) -> None:
        self.__strategy_form: CreateStrategyDialog = CreateStrategyDialog(self)
        self.__strategy_form.setWindowTitle("Create Strategy")
        self.__strategy_form.strategy_created.connect(
            self.__strategy_window.on_strategy_created
        )
        self.__strategy_form.exec()

    def on_instruments_action_clicked(self, checked: bool) -> None:
        self.__instrument_window: InstrumentWindow = InstrumentWindow(self)
        self.__instrument_window.exec()

    # -------------------------------------------------- Public Methods --------------------------------------------------
    # -------------------------------------------------- Private Methods --------------------------------------------------
