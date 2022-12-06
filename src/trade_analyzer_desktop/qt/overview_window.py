
from typing import Optional

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from ..analysis import AnalysisResults

class OverviewWindow(QWidget):
    
    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Overview")

        # Widgets

        # Layout 
        layout: QGridLayout = QGridLayout(self)

        # Default Data
        self.__analysis_results: AnalysisResults = results

    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------

    # -------------------------------------------------- Private Methods --------------------------------------------------
