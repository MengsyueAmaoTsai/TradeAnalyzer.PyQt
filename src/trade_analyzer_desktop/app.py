import qdarkstyle
from PyQt6.QtWidgets import QApplication

from .qt.main_window import MainWindow
from .database_manager import DatabaseManager


class TradeAnalyzerClientDesktop(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # DatabaseManager.reset_database()
        DatabaseManager.connect()

        self.__main_window: MainWindow = MainWindow()

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def main_window(self) -> MainWindow:
        return self.__main_window

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def launch(self) -> int:
        self.main_window.showMaximized()
        return self.exec()
