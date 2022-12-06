

from datetime import date as Date

from .benchmark_symbol import BenchmarkSymbol
from .daily_statistics import DailyStatistics
from .daily_statistics_builder import DailyStatisticsBuilder

class BenchmarkPerformance():

    def __init__(self, benchmark_symbol: BenchmarkSymbol, starting_capital: float, start_date: Date, end_date: Date):
        self.__daily_statistics: DailyStatistics = DailyStatisticsBuilder.build_benchmark(benchmark_symbol, starting_capital, start_date, end_date)

    @property
    def daily_statistics(self) -> DailyStatistics:
        return self.__daily_statistics

    @property
    def trade_statistics(self) -> None:
        return None

    @property
    def long(self) -> "BenchmarkPerformance":
        return self

    @property
    def short(self) -> "BenchmarkPerformance":
        return self        
