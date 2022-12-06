import math
from typing import List, Dict
from datetime import date as Date

from .benchmark import Benchmark
from .benchmark_symbol import BenchmarkSymbol
from .daily_statistics import DailyStatistics
from .strategy_daily_statistics import StrategyDailyStatistics
from ..entities import Trade


class DailyStatisticsBuilder:

    RISK_FREE_INTEREST: float = 0.01 # Risk-free interest rate
    TRADING_DAYS_PER_YEAR: int = 252
    
    @classmethod
    def build_benchmark(cls, benchmark_symbol: BenchmarkSymbol, starting_capital: float, start_date: Date, end_date: Date) -> DailyStatistics:
        # Get benchmark daily returns from yahoo finance
        returns: Dict[Date, float] = Benchmark.get_historical_prices(benchmark_symbol, start_date, end_date)

        # Calculate daily pnl/equity as $, cumulative return as %
        first_date: Date = list(returns.keys())[0]
        
        net_profit_loss: Dict[Date, float] = { first_date: 0 }
        equity: Dict[Date, float] = { first_date: starting_capital }
        cumulative_returns: Dict[Date, float] = { first_date: 0 }        
        drawdown: Dict[Date, float] = { first_date: 0 } 
        drawdown_percent: Dict[Date, float] = { first_date: 0 }                
        
        max_equity: float = starting_capital

        prev_date: Date = first_date

        for i in range(0, len(returns)):
            current_date: Date = list(returns.keys())[i]
            net_profit_loss[current_date] = equity[prev_date] * returns[current_date]
            benchmark_current_equity: float = equity[prev_date] + net_profit_loss[current_date]
            equity[current_date] = benchmark_current_equity
            max_equity = max(max_equity, benchmark_current_equity)            
            cumulative_returns[current_date] = benchmark_current_equity / starting_capital - 1
            drawdown[current_date] = benchmark_current_equity - max_equity
            drawdown_percent[current_date] = drawdown[current_date] / max_equity            
            prev_date = current_date    

        daily_statistics: DailyStatistics = DailyStatistics()
        daily_statistics.net_profit_loss = net_profit_loss
        daily_statistics.returns = returns
        daily_statistics.equity = equity
        daily_statistics.cumulative_returns = cumulative_returns
        daily_statistics.drawdown = drawdown
        daily_statistics.drawdown_percent = drawdown_percent
        return daily_statistics

    @classmethod
    def build_strategy(
        cls, trades: List[Trade], benchmark_returns: Dict[Date, float], starting_capital: float, start_date: Date, end_date: Date
    ) -> StrategyDailyStatistics:
        daily_statistics: StrategyDailyStatistics = StrategyDailyStatistics()

        first_date: Date = list(benchmark_returns.keys())[0]
        
        daily_trades: Dict[Date, List[Trade]] = { first_date: [] }
        profit_loss: Dict[Date, float] = { first_date: 0 }
        returns: Dict[Date, float] = { first_date: 0 }
        equity: Dict[Date, float] = { first_date: starting_capital }
        cumulative_returns: Dict[Date, float] = { first_date: 0 }
        drawdown: Dict[Date, float] = { first_date: 0 }
        drawdown_percent: Dict[Date, float] = { first_date: 0 }
        max_equity: float = starting_capital
        prev_date: Date = first_date
        
        for i in range(0, len(benchmark_returns)):
            current_date: Date = list(benchmark_returns.keys())[i]
            daily_trades[current_date] = list(filter(lambda trade: trade.exit_time.date() == current_date, trades))
            profit_loss[current_date] = sum(trade.net_profit_loss for trade in daily_trades[current_date])
            returns[current_date] = profit_loss[current_date] / equity[prev_date]
            current_equity: float = equity[prev_date] + profit_loss[current_date]
            equity[current_date] = current_equity
            max_equity = max(max_equity, current_equity)
            cumulative_returns[current_date] = (current_equity / starting_capital) - 1
            drawdown[current_date] = current_equity - max_equity
            drawdown_percent[current_date] = drawdown[current_date] / max_equity
            prev_date = current_date

        daily_statistics.net_profit_loss = profit_loss
        daily_statistics.returns = returns
        daily_statistics.equity = equity
        daily_statistics.cumulative_returns = cumulative_returns
        daily_statistics.drawdown = drawdown
        daily_statistics.drawdown_percent = drawdown_percent
       
        # Min amount of samples to calculate variance. 
        if (starting_capital == 0 or len(benchmark_returns) < 2 or len(returns) < 2):
            return StrategyDailyStatistics()

        running_capital: float = starting_capital
        total_profit: float = 0
        total_loss: float = 0
        number_of_winning_days: int = 0
        number_of_lossing_days: int = 0

        for pnl in profit_loss.values():
            trade_profit_loss: float = pnl

            if (pnl > 0):
                total_profit += trade_profit_loss / running_capital
                number_of_winning_days += 1
            else:
                total_loss += trade_profit_loss / running_capital
                number_of_lossing_days += 1
            running_capital += trade_profit_loss

        daily_statistics.average_win_rate = total_profit / number_of_winning_days if number_of_winning_days != 0 else 0 # -> avg profit
        daily_statistics.average_loss_rate = total_loss / number_of_lossing_days if number_of_lossing_days != 0 else 0 # -> avg loss
        daily_statistics.profit_loss_ratio = daily_statistics.average_win_rate / abs(daily_statistics.average_loss_rate) if daily_statistics.average_loss_rate != 0 else 0
        daily_statistics.win_rate = number_of_winning_days / len(profit_loss) if len(profit_loss) != 0 else 0
        
        daily_statistics.expectancy = daily_statistics.win_rate * daily_statistics.profit_loss_ratio - (1 - daily_statistics.win_rate)

        if (starting_capital != 0):
            daily_statistics.total_returns = list(equity.values())[-1] / starting_capital - 1

        fraction_of_years: float = (list(equity.keys())[-1] - list(equity.keys())[0]).days / 365

        daily_statistics.compounding_annual_return = cls.compounding_annual_returns(starting_capital, list(equity.values())[-1], fraction_of_years)
        
        # daily_statistics.max_drawdown_pct = cls.drawdown_percent(equity, 3)
        daily_statistics.max_drawdown = min(drawdown.values())
        daily_statistics.max_drawdown_percent = min(drawdown_percent.values())

        daily_statistics.annual_variance  = cls.annual_variance(list(returns.values()), cls.TRADING_DAYS_PER_YEAR)
        daily_statistics.annual_standard_deviation = math.sqrt(daily_statistics.annual_variance)
       
        benchmark_annual_returns: float = cls.annual_returns(list(benchmark_returns.values()), cls.TRADING_DAYS_PER_YEAR)
        benchmark_variance: float = cls.annual_variance(list(benchmark_returns.values()))

        annaul_returns: float = cls.annual_returns(list(returns.values()), cls.TRADING_DAYS_PER_YEAR) 
        
        daily_statistics.sharpe_ratio = annaul_returns - cls.RISK_FREE_INTEREST / daily_statistics.annual_standard_deviation \
            if daily_statistics.annual_standard_deviation != 0 else 0

        daily_statistics.beta = cls.covariance(list(returns.values()), list(benchmark_returns.values())) / benchmark_variance if benchmark_variance != 0 else 0

        daily_statistics.alpha = annaul_returns - (cls.RISK_FREE_INTEREST + daily_statistics.beta * (benchmark_annual_returns - cls.RISK_FREE_INTEREST)) \
            if daily_statistics.beta != 0 else 0

        daily_statistics.tracking_error = cls.tracking_error(list(returns.values()), list(benchmark_returns.values()), cls.TRADING_DAYS_PER_YEAR)

        daily_statistics.information_ratio = (annaul_returns - benchmark_annual_returns) / daily_statistics.tracking_error \
            if daily_statistics.tracking_error != 0 else 0

        daily_statistics.treynor_ratio = (annaul_returns - cls.RISK_FREE_INTEREST) / daily_statistics.beta if daily_statistics.beta != 0 else 0
        return daily_statistics

    @classmethod
    def tracking_error(cls, returns: List[float], benchmark_returns: List[float], trading_days_per_year: int = 252):
        if (len(returns) != len(benchmark_returns)):
            return 0
        performance_difference: List[float] = []

        for i in range(0, len(returns)):
            performance_difference.append(returns[i] - benchmark_returns[i])

        annual_performance: float = cls.annual_returns(performance_difference, trading_days_per_year)
        return math.sqrt(annual_performance) if annual_performance >= 0 else 0    

    @classmethod
    def compounding_annual_returns(cls, starting_capital: float, final_capital: float, years: float) -> float:
        if (years == 0 or starting_capital == 0):
            return 0
        power: float = 1 / years
        base_number: float = final_capital / starting_capital
        return math.pow(base_number, power) - 1        

    @classmethod
    def drawdown_percent(cls, equity: Dict[Date, float], rounding: int = 2) -> float:
        prices: List[float] = list(equity.values())

        if (len(prices) == 0):
            return 0
        drawdowns: List[float] = list()
        high: float = prices[0]
        
        for price in prices:
            if (price > high):
                high = price
            if (high > 0):
                drawdowns.append(price / high - 1)
        return round(abs(min(drawdowns)), rounding)

    @classmethod
    def annual_returns(cls, return_list: List[float], trading_days_per_year: int = 252) -> float:
        return math.pow(DailyStatisticsBuilder.get_mean(return_list) + 1, trading_days_per_year) - 1

    @classmethod
    def annual_variance(cls, return_list: List[float], trading_days_per_year: int = 252) -> float:
        length: int = int(len(return_list))
        mean: float = sum(return_list) / length 
        variance: float = sum((i - mean) ** 2 for i in return_list) / length
        return variance * trading_days_per_year if variance != 0 else 0

    @classmethod
    def get_mean(cls, values: List[float]) -> float:
        return sum(values) / len(values)

    @classmethod
    def covariance(cls, series1: List[float], series2: List[float]) -> float:
        if len(series1) != len(series2):
            length = min([len(series1), len(series2)])
            new_list1: List[float] = series1[0 : length - 1]
            new_list2: List[float] = series2[0 : length - 1]
            return sum((new_list1[i] - cls.get_mean(new_list1)) * (new_list2[i] - cls.get_mean(new_list2)) for i in range(0, len(new_list1))) / len(new_list2)
        length = min([len(series1), len(series2)])
        return sum((series1[i] - cls.get_mean(series1)) * (series2[i] - cls.get_mean(series2)) for i in range(0, length)) / length
        