from typing import Optional, Union

from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QButtonGroup, QLabel, QComboBox

from .charts import DisplayUnits
from .statistics_view import StatisticsView
from .statistics_table import StatisticsTable
from ..analysis import AnalysisResults, StatisticsResults, TradeStatistics, DailyStatistics, StrategyPerformance, BenchmarkPerformance


class OverviewWindow(QWidget):
    
    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Overview")

        # Widgets
        self.__all_side_button: QPushButton = QPushButton("All")
        self.__all_side_button.setAutoExclusive(True)
        self.__all_side_button.setCheckable(True)
        self.__all_side_button.setChecked(True)
        self.__all_side_button.clicked.connect(self.on_all_side_button_clicked)

        self.__long_side_button: QPushButton = QPushButton("Long")
        self.__long_side_button.setAutoExclusive(True)
        self.__long_side_button.setCheckable(True)
        self.__long_side_button.clicked.connect(self.on_long_side_button_clicked)

        self.__short_side_button: QPushButton = QPushButton("Short")
        self.__short_side_button.setAutoExclusive(True)
        self.__short_side_button.setCheckable(True)
        self.__short_side_button.clicked.connect(self.on_short_side_button_clicked)
        
        self.side_button_group: QButtonGroup = QButtonGroup()
        self.side_button_group.addButton(self.__all_side_button, 1)
        self.side_button_group.addButton(self.__long_side_button, 2)
        self.side_button_group.addButton(self.__short_side_button, 3)

        self.__display_units_combo: QComboBox = QComboBox()
        self.__display_units_combo.currentIndexChanged.connect(self.on_display_units_combo_currenct_index_changed)

        self.__statistics_view: StatisticsView = StatisticsView(results)
        self.__statistics_table: StatisticsTable = StatisticsTable()
        self.__statistics_table.results_selected.connect(self.on_result_selected)
        
        # Layout 
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(QLabel("Side"), 0, 0, 1, 1)
        layout.addWidget(self.__all_side_button, 0, 1, 1, 1)
        layout.addWidget(self.__long_side_button, 0, 2, 1, 1)
        layout.addWidget(self.__short_side_button, 0, 3, 1, 1)

        layout.addWidget(QLabel("Display Units"), 0, 4, 1, 1)
        layout.addWidget(self.__display_units_combo, 0, 5, 1, 1)
        
        layout.addWidget(self.__statistics_view, 1, 0, 6, 10)
        layout.addWidget(self.__statistics_table, 7, 0, 3, 10)

        # Default Data
        for i, units in enumerate(DisplayUnits):
            self.__display_units_combo.addItem(units.value, units)    

        for key in results.keys:
            if not key.startswith("Benchmark"):
                statistics_results: Union[StatisticsResults, None] = results.get(key)
                assert(statistics_results is not None)
                self.__statistics_table.add_statistics_results(key, statistics_results)        

        self.__results: AnalysisResults = results
        
    # -------------------------------------------------- Properties --------------------------------------------------

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_all_side_button_clicked(self, checked: bool) -> None:
        pass
    
    def on_long_side_button_clicked(self, checked: bool) -> None:
        pass
    
    def on_short_side_button_clicked(self, checked: bool) -> None:
        pass

    def on_display_units_combo_currenct_index_changed(self, index: int) -> None:
        pass

    def on_result_selected(self, key: str) -> None:
        results: Union[StatisticsResults, None] = self.__results.get(key)
        assert(results is not None)
        performance: Union[StrategyPerformance, BenchmarkPerformance, None] = results.total_performance
        assert(isinstance(performance, StrategyPerformance))
        self.__statistics_view.set_performance(performance)
                
    # -------------------------------------------------- Public Methods --------------------------------------------------


    # -------------------------------------------------- Private Methods --------------------------------------------------
