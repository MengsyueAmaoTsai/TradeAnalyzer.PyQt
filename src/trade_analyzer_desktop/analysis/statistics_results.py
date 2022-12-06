
from typing import Dict, TypeVar

from .strategy_performance import StrategyPerformance
from .benchmark_performance import BenchmarkPerformance


T = TypeVar("T", StrategyPerformance, BenchmarkPerformance)

class StatisticsResults:
    """
    The class represents total/rolling/perdical statistics.
    """

    def __init__(self, total_performance: T, rolling_performance: Dict[str, T], periodical_performance: Dict[str, T]) -> None:
        self.total_performance: T = total_performance
        self.rolling_performance: Dict[str, T] = rolling_performance
        self.periodical_performance: Dict[str, T] = periodical_performance