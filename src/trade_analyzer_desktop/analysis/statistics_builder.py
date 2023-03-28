from typing import List, Dict
from datetime import date as Date

from .benchmark_symbol import BenchmarkSymbol
from .statistics_results import StatisticsResults
from .benchmark_performance import BenchmarkPerformance
from .strategy_performance import StrategyPerformance
from ..entities import Trade


class StatisticsBuilder:
    @classmethod
    def build_benchmark(
        cls,
        benchmark_symbol: BenchmarkSymbol,
        starting_capital: float,
        start_date: Date,
        end_date: Date,
    ) -> StatisticsResults:
        """
        Builds the statistics and returns the results of benchmark.
        """
        benchmark_performance = BenchmarkPerformance(
            benchmark_symbol, starting_capital, start_date, end_date
        )
        return StatisticsResults(benchmark_performance, None, None)

    @classmethod
    def build_strategy(
        cls,
        trades: List[Trade],
        benchmark_returns: Dict[Date, float],
        starting_capital: float,
        start_date: Date,
        end_date: Date,
    ) -> StatisticsResults:
        """
        Generates the statistics and returns the results of strategy.
        """
        strategy_performance: StrategyPerformance = StrategyPerformance(
            trades, benchmark_returns, starting_capital, start_date, end_date
        )
        return StatisticsResults(strategy_performance, None, None)
