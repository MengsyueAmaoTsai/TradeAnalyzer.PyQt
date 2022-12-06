from typing import List, Dict
from datetime import date as Date

from .trade_statistics import TradeStatistics
from .strategy_daily_statistics import StrategyDailyStatistics
from .trade_statistics_builder import TradeStatisticsBuilder
from .daily_statistics_builder import DailyStatisticsBuilder
from ..entities import Trade
from ..enums import Side


class StrategyPerformance():

    def __init__(self, trades: List[Trade], benchmark_returns: Dict[Date, float], starting_capital: float, start_date: Date, end_date: Date) -> None:
        self.__closed_trades: List[Trade] = trades
        self.__starting_capital: float = starting_capital
        self.__start_date: Date = start_date
        self.__end_date: Date = end_date
        self.__benchmark_returns: Dict[Date, float] = benchmark_returns
        self.__trade_statistics: TradeStatistics = TradeStatisticsBuilder.build(trades, starting_capital, start_date, end_date)
        self.daily_statistics: StrategyDailyStatistics = DailyStatisticsBuilder.build_strategy(trades, benchmark_returns, starting_capital, start_date, end_date)

    @property
    def long(self) -> "StrategyPerformance":
        long_trades: List[Trade] = list(filter(lambda trade: trade.side == Side.Long, self.__closed_trades))
        return StrategyPerformance(long_trades, self.__benchmark_returns, self.__starting_capital, self.__start_date, self.__end_date) 

    @property
    def short(self) -> "StrategyPerformance":
        long_trades: List[Trade] = list(filter(lambda trade: trade.side == Side.Short, self.__closed_trades))
        return StrategyPerformance(long_trades, self.__benchmark_returns, self.__starting_capital, self.__start_date, self.__end_date)     

    @property
    def trade_statistics(self) -> TradeStatistics:
        return self.__trade_statistics

    @property
    def closed_trades(self) -> List[Trade]:
        return self.__closed_trades