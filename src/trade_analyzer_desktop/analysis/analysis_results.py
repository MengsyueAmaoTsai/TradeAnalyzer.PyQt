from typing import Dict, List, Union
from datetime import date as Date

from ..entities import Trade
from .benchmark_symbol import BenchmarkSymbol
from .statistics_results import StatisticsResults


class AnalysisResults:
    def __init__(
        self,
        starting_capital: float,
        start_date: Date,
        end_date: Date,
        benchmark_symbol: BenchmarkSymbol,
    ) -> None:
        self.__starting_capital: float = starting_capital
        self.__start_date: Date = start_date
        self.__end_date: Date = end_date
        self.__benchmark_symbol: BenchmarkSymbol = benchmark_symbol
        self.__results: Dict[str, StatisticsResults] = {}

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def starting_capital(self) -> float:
        return self.__starting_capital

    @property
    def start_date(self) -> Date:
        return self.__start_date

    @property
    def end_date(self) -> Date:
        return self.__end_date

    @property
    def benchmark_symbol(self) -> BenchmarkSymbol:
        return self.__benchmark_symbol

    @property
    def keys(self) -> List[str]:
        return list(self.__results.keys())

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def add(self, key: str, statistics_results: StatisticsResults) -> None:
        self.__results[key] = statistics_results

    def get(self, key: str) -> Union[StatisticsResults, None]:
        return self.__results.get(key, None)

    # -------------------------------------------------- Private Methods --------------------------------------------------
