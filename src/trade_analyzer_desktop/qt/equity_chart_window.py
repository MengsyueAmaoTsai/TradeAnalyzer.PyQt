from typing import Optional, Union, List

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QRadioButton, QComboBox, QButtonGroup
from PyQt6.QtCore import Qt

from .data_set_list import DataSetList
from .data_set_list_item import DataSetListItem
from .charts import EquityChart, DrawdownChart, ChartPoint, AxisType, DisplayUnits
from ..enums import Side
from ..analysis import AnalysisResults, StatisticsResults


class EquityChartWindow(QWidget):
    
    def __init__(self, results: AnalysisResults, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Equity Chart")

        # Widgets
        self.__data_set_list: DataSetList = DataSetList()
        self.__data_set_list.setResizeMode(DataSetList.ResizeMode.Adjust)
        self.__data_set_list.item_checked.connect(self.on_data_list_item_checked)
        
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

        self.__side_button_group: QButtonGroup = QButtonGroup()
        self.__side_button_group.addButton(self.__all_side_button, 1)
        self.__side_button_group.addButton(self.__long_side_button, 2)
        self.__side_button_group.addButton(self.__short_side_button, 3)

        self.__by_time_button: QRadioButton = QRadioButton("By Time")
        self.__by_time_button.setChecked(True)
        self.__by_time_button.clicked.connect(self.on_by_time_button_clicked)

        self.__by_trade_button: QRadioButton = QRadioButton("By Trade")
        self.__by_trade_button.clicked.connect(self.on_by_trade_button_clicked)

        self.__display_units_combo: QComboBox = QComboBox()
        self.__display_units_combo.currentIndexChanged.connect(self.on_display_units_combo_currenct_index_changed)

        self.__equity_chart: EquityChart = EquityChart()
        self.__drawdown_chart: DrawdownChart = DrawdownChart()
        
        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(self.__data_set_list, 0, 0, 20, 2)

        side_label: QLabel = QLabel("Side")
        side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(side_label, 0, 2, 1, 2)
        layout.addWidget(self.__all_side_button, 0, 4, 1, 2)
        layout.addWidget(self.__long_side_button, 0, 6, 1, 2)
        layout.addWidget(self.__short_side_button, 0, 8, 1, 2)

        axis_label: QLabel = QLabel("X Axis")
        axis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(axis_label, 0, 10, 1, 2)
        layout.addWidget(self.__by_time_button, 0, 12, 1, 2)
        layout.addWidget(self.__by_trade_button, 0, 14, 1, 2)

        display_units_label: QLabel = QLabel("Display Units")
        display_units_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(display_units_label, 0, 16, 1, 2)
        layout.addWidget(self.__display_units_combo, 0, 18, 1, 2)

        layout.addWidget(self.__equity_chart, 1, 2, 15, 18)
        layout.addWidget(self.__drawdown_chart, 16, 2, 4, 18)
        
        # Data
        for i, units in enumerate(DisplayUnits):
            self.__display_units_combo.addItem(units.value, units)

        # Add data set to data set list.
        self.__equity_chart.set_x_axis_type(self.x_axis_type)

        for key in results.keys:
            statistics_results: Union[StatisticsResults, None] = results.get(key)
            assert(statistics_results is not None)
            self.__data_set_list.add_data(key, statistics_results)
            self.add_series(key)

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def side(self) -> Side:
        if self.__long_side_button.isChecked():
            return Side.Long
        elif self.__short_side_button.isChecked():
            return Side.Short
        else:
            return Side.All

    @property
    def x_axis_type(self) -> AxisType:
        axis_type: AxisType = AxisType.DateTime
        if self.__by_time_button.isChecked():
            axis_type = AxisType.DateTime
        elif self.__by_trade_button.isChecked():
            axis_type = AxisType.Value
        return axis_type

    @property
    def display_units(self) -> DisplayUnits:
        return self.__display_units_combo.currentData()            

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_data_list_item_checked(self, key: str, checked: str) -> None:
        self.add_series(key) if checked else self.remove_series(key)

    def on_all_side_button_clicked(self, checked: bool) -> None:
        self.reload_charts()          

    def on_long_side_button_clicked(self, checked: bool) -> None:
        self.reload_charts()          

    def on_short_side_button_clicked(self, checked: bool) -> None:
        self.reload_charts()          

    def on_by_time_button_clicked(self, checked: bool) -> None:
        self.reload_charts()          

    def on_by_trade_button_clicked(self, checked: bool) -> None:
        self.reload_charts()          

    def on_display_units_combo_currenct_index_changed(self, index: int) -> None:
        self.reload_charts()          

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def reload_charts(self) -> None:
        """
        Reload series which data sets on charts. 
        """
        existing_items: List[DataSetListItem] = list(filter(lambda item: item.is_checked, self.__data_set_list.items)) 
        self.__equity_chart.set_x_axis_type(self.x_axis_type)
        self.__drawdown_chart.set_x_axis_type(self.x_axis_type)
        
        for item in existing_items:
            self.remove_series(item.key)
            self.add_series(item.key)   

    def add_series(self, name: str) -> None:
        """
        Add a series to equity/drawdown chart.
        """
        equity_chart_points: List[ChartPoint] = self.__data_set_list.get_item(name).get_equity_chart_points(self.side, self.x_axis_type, self.display_units)
        drawdown_chart_points: List[ChartPoint] = self.__data_set_list.get_item(name).get_drawdown_chart_points(self.side, self.x_axis_type, self.display_units)

        if name.startswith("Benchmark") and self.x_axis_type == AxisType.Value:
            benchmark_item: DataSetListItem = self.__data_set_list.get_item(name)
            self.remove_series(name)
            benchmark_item.is_checked = False
        else:
            self.__equity_chart.add_series(name, equity_chart_points, self.x_axis_type, self.display_units)    
            self.__drawdown_chart.add_series(name, drawdown_chart_points, self.x_axis_type, self.display_units)  

    def remove_series(self, name: str) -> None:
        """
        Remove series by name from equity/drawdown chart.
        """
        self.__equity_chart.remove_series(name)
        self.__drawdown_chart.remove_series(name)

       
    # -------------------------------------------------- Private Methods --------------------------------------------------        


    