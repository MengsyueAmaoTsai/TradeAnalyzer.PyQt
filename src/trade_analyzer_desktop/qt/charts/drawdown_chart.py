from typing import List, Dict, Optional, Union
from datetime import datetime as DateTime

from PyQt6.QtCharts import QChartView, QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import QDateTime, Qt, QPointF
from PyQt6.QtGui import QPainter 

from .chart_point import ChartPoint
from .axis_type import AxisType
from .display_units import DisplayUnits

class DrawdownChart(QChartView):
    """
    A line chart to display equity/total returns.
    """

    DATE_FORMAT: str = "yyyy-MM-dd"

    def __init__(self) -> None:
        super().__init__()
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create chart.
        chart: QChart = QChart()
        chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.setChart(chart)

        # Create axes default x by time, y by percentage
        self.x_axis: QDateTimeAxis = self.__create_datetime_axis()
        
        self.y_axis: QValueAxis = QValueAxis()
        self.y_axis.setTickCount(3)
        self.y_axis.setGridLineVisible(False)
        chart.addAxis(self.x_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.y_axis, Qt.AlignmentFlag.AlignLeft)

        # Data
        self.__series: Dict[str, QLineSeries] = {}

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def all_points(self) -> List[QPointF]:
        points: List[QPointF] = []
        for series in self.__series.values():
            points.extend(series.points())
        return points

    @property
    def max_y(self) -> float:
        return max(point_f.y() for point_f in self.all_points) if len(self.all_points) != 0 else 0
    
    @property
    def min_y(self) -> float:
        return min(point_f.y() for point_f in self.all_points) if len(self.all_points) != 0 else 0
    # -------------------------------------------------- Event Handlers --------------------------------------------------

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def set_x_axis_type(self, axis_type: AxisType) -> None:
        if self.x_axis: 
            self.chart().removeAxis(self.x_axis)

        axis: Optional[Union[QDateTimeAxis, QValueAxis]] = None

        if axis_type == AxisType.DateTime:
            axis = QDateTimeAxis()
            axis.setFormat(self.DATE_FORMAT)
            axis.setLabelsAngle(45)
        else:
            axis = QValueAxis()

        axis.setTickCount(10)
        axis.setGridLineVisible(False)             
        self.x_axis = axis
        self.chart().addAxis(axis, Qt.AlignmentFlag.AlignBottom)

    def add_series(self, name: str, points: List[ChartPoint], x_axis_type: AxisType, display_units: DisplayUnits) -> None:
        series: QLineSeries = self.create_series(name, points, x_axis_type)
        self.__series[name] = series

        if self.x_axis:
            if x_axis_type == AxisType.DateTime:
                self.x_axis.setRange(DateTime.fromtimestamp(points[0].x), DateTime.fromtimestamp(points[-1].x))
            else:
                self.x_axis.setRange(points[0].x, points[-1].x)

        self.y_axis.setRange(self.min_y, self.max_y)
        self.chart().addSeries(series)
        series.attachAxis(self.x_axis)
        series.attachAxis(self.y_axis)
        
    def create_series(self, name: str, points: List[ChartPoint], x_axis_type: AxisType) -> QLineSeries:
        series: QLineSeries = QLineSeries()
        series.setName(name)
        for point in points:
            if x_axis_type == AxisType.DateTime: 
                datetime: QDateTime = QDateTime(DateTime.fromtimestamp(point.x))
                series.append(datetime.toMSecsSinceEpoch(), point.y)
            else:
                series.append(point.x, point.y)
        return series

    def remove_series(self, name: str) -> None:
        series: QLineSeries = self.__series.pop(name, None)
        if series:
            self.chart().removeSeries(series)

        # Adjust axis range.
        self.y_axis.setRange(self.min_y, self.max_y)  


    # -------------------------------------------------- Private Methods --------------------------------------------------        

    def __create_datetime_axis(self) -> QDateTimeAxis:
        axis: QDateTimeAxis = QDateTimeAxis()
        axis.setFormat(self.DATE_FORMAT)
        axis.setTickCount(10)
        axis.setLabelsAngle(45)
        axis.setGridLineVisible(False)         
        return axis