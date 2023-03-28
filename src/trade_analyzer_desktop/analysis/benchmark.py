import time
from typing import Dict, List
from datetime import (
    date as Date,
    datetime as DateTime,
    timezone as TimeZone,
    timedelta as TimeDelta,
)

from yfinance import Ticker
from pandas import DataFrame, Timestamp

from .benchmark_symbol import BenchmarkSymbol


class Benchmark:
    @staticmethod
    def get_historical_prices(
        benchmark_symbol: BenchmarkSymbol,
        start_date: Date = Date.min,
        end_date: Date = Date.today(),
    ):
        benchmark_prices: Dict[Date, float] = {}
        data_frame: DataFrame = Ticker(benchmark_symbol.value).history(
            interval="1d",
            start=start_date.strftime("%Y-%m-%d") if start_date else None,
            end=end_date.strftime("%Y-%m-%d") if end_date else None,
        )
        prices: Dict[Timestamp, float] = data_frame["Close"].to_dict()

        for timestamp, price in prices.items():
            original_timestamp = time.mktime(timestamp.timetuple())
            dt = DateTime.fromtimestamp(original_timestamp)
            utc_timestamp = dt.replace(tzinfo=TimeZone.utc).timestamp()
            benchmark_prices[Date.fromtimestamp(utc_timestamp)] = price

        return Benchmark.daily_returns(benchmark_prices, start_date, end_date)

    @staticmethod
    def daily_returns(
        prices: Dict[Date, float], start_date: Date, end_date: Date
    ) -> Dict[Date, float]:
        returns: Dict[Date, float] = {}
        periods: List[Date] = list(
            filter(
                lambda date: date >= start_date and date <= end_date,
                list(prices.keys()),
            )
        )
        returns[periods[0]] = 0
        prev_date: Date = periods[0] - TimeDelta(days=1)

        for current_date in periods:
            prev_price: float = 0
            has_previous: bool = False

            prev_price = prices.get(prev_date, 0)

            if prev_price != 0:
                has_previous = True

            if has_previous and prev_price != 0:
                daily_returns: float = (prices[current_date] - prev_price) / prev_price
                returns[current_date] = daily_returns

            elif has_previous:
                returns[current_date] = 0
            prev_date = current_date
        return returns
