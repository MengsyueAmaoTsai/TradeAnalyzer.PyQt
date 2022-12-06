from typing import Optional, Union

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from .statistics_table import StatisticsTable
from ..analysis import AnalysisResults, StatisticsResults

class OverviewWindow(QWidget):
    
    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Overview")

        # Widgets


        self.__statistics_table: StatisticsTable = StatisticsTable()
        # Layout 
        layout: QGridLayout = QGridLayout(self)

        layout.addWidget(self.__statistics_table)

        # Default Data
        for key in results.keys:
            if not key.startswith("Benchmark"):
                statistics_results: Union[StatisticsResults, None] = results.get(key)
                assert(statistics_results is not None)
                self.__statistics_table.add_statistics_results(key, statistics_results)        

    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------


    # -------------------------------------------------- Private Methods --------------------------------------------------
