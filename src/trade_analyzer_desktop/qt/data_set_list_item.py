from typing import Optional, Union, List

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox
from PyQt6.QtCore import pyqtSignal 

from .charts import AxisType, DisplayUnits, ChartPoint
from ..enums import Side
from ..analysis import StatisticsResults, StrategyPerformance, BenchmarkPerformance, TradeStatistics, DailyStatistics


class DataSetListItem(QWidget):

    checked: pyqtSignal = pyqtSignal(str, bool)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # widgets
        self.__check_box: QCheckBox = QCheckBox()
        self.__check_box.clicked.connect(self.on_check_box_clicked)
        self.__kay_label: QLabel = QLabel()

        # layout 
        layout: QGridLayout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.__check_box, 0, 0, 1, 1)
        layout.addWidget(self.__kay_label, 0, 1, 1, 9)

        # data
        self.__is_checked: bool = False
        self.__key: str = ""
        self.__statistics_results: Union[StatisticsResults, None] = None 

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def is_checked(self) -> bool:
        return self.__check_box.isChecked()
    
    @is_checked.setter
    def is_checked(self, is_checked: bool) -> None:
        self.__is_checked = is_checked
        self.__check_box.setChecked(is_checked)

    @property
    def key(self) -> str:
        return self.__kay_label.text().strip()

    @key.setter
    def key(self, key: str) -> None:
        self.__key = key
        self.__kay_label.setText(key)
    
    @property
    def statistics_results(self) -> Union[StatisticsResults, None]:
        return self.__statistics_results

    @statistics_results.setter
    def statistics_results(self, statistics_results: StatisticsResults) -> None:
        self.__statistics_results = statistics_results
        
    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_check_box_clicked(self, checked: bool) -> None:
        self.checked.emit(self.key, checked)
        
    # -------------------------------------------------- Public Methods --------------------------------------------------
    def get_equity_chart_points(self, side: Side, x_axis_type: AxisType, display_units: DisplayUnits) -> List[ChartPoint]:
        assert(self.statistics_results is not None)
        equity_chart_points: List[ChartPoint] = []
        total_performance: Optional[Union[StrategyPerformance, BenchmarkPerformance]] = None

        if side == Side.Long:
            total_performance = self.statistics_results.total_performance.long
        elif side == Side.Short:
            total_performance = self.statistics_results.total_performance.short
        else:
            total_performance = self.statistics_results.total_performance

        statistics: Optional[Union[TradeStatistics, DailyStatistics]] = None

        if x_axis_type == AxisType.DateTime:
            statistics = total_performance.daily_statistics
        else:
            statistics = total_performance.trade_statistics

        if statistics:
            if display_units == DisplayUnits.Percentage:
                equity_chart_points = [ChartPoint(x, y) for x, y in statistics.cumulative_returns.items()]
            else:
                equity_chart_points = [ChartPoint(x, y) for x, y in statistics.equity.items()]
        
        return equity_chart_points

    def get_drawdown_chart_points(self, side: Side, x_axis_type: AxisType, display_units: DisplayUnits) -> List[ChartPoint]:
        assert(self.statistics_results is not None)
        drawdown_chart_points: List[ChartPoint] = []
        total_performance: Optional[Union[StrategyPerformance, BenchmarkPerformance]] = None

        if side == Side.Long:
            total_performance = self.statistics_results.total_performance.long
        elif side == Side.Short:
            total_performance = self.statistics_results.total_performance.short
        else:
            total_performance = self.statistics_results.total_performance

        statistics: Optional[Union[TradeStatistics, DailyStatistics]] = None

        if x_axis_type == AxisType.DateTime:
            statistics = total_performance.daily_statistics
        else:
            statistics = total_performance.trade_statistics

        if statistics:
            if display_units == DisplayUnits.Percentage:
                drawdown_chart_points = [ChartPoint(x, y) for x, y in statistics.drawdown_percent.items()]
            else:
                drawdown_chart_points = [ChartPoint(x, y) for x, y in statistics.drawdown.items()]
        
        return drawdown_chart_points        

    def get_profit_loss_chart_points(self, side: Side, x_axis_type: AxisType, display_units: DisplayUnits) -> List[ChartPoint]:
        assert(self.statistics_results is not None)
        profit_loss_chart_points: List[ChartPoint] = []
        total_performance: Optional[Union[StrategyPerformance, BenchmarkPerformance]] = None

        if side == Side.Long:
            total_performance = self.statistics_results.total_performance.long
        elif side == Side.Short:
            total_performance = self.statistics_results.total_performance.short
        else:
            total_performance = self.statistics_results.total_performance

        statistics: Optional[Union[TradeStatistics, DailyStatistics]] = None

        if x_axis_type == AxisType.DateTime:
            statistics = total_performance.daily_statistics
        else:
            statistics = total_performance.trade_statistics

        if statistics:
            if display_units == DisplayUnits.Percentage:
                profit_loss_chart_points = [ChartPoint(x, y) for x, y in statistics.returns.items()]
            else:
                profit_loss_chart_points = [ChartPoint(x, y) for x, y in statistics.net_profit_loss.items()]
        
        return profit_loss_chart_points    
    # -------------------------------------------------- Private Methods --------------------------------------------------
