from typing import Dict
from datetime import date as Date


class DailyStatistics:
    """
    The class represents a set of statistics calculated from equity and benchmark samples
    """

    def __init__(self) -> None:
        # Series
        self.net_profit_loss: Dict[Date, float] = {}
        self.returns: Dict[Date, float] = {}
        self.equity: Dict[Date, float] = {}
        self.cumulative_returns: Dict[Date, float] = {}
        self.drawdown: Dict[Date, float] = {}
        self.drawdown_percent: Dict[Date, float] = {}

        # Metrix
        self.total_returns: float = 0  # The total net profit percentage.
        self.sharpe_ratio: float = 0  # Sharpe ratio with respect to risk free instrest rate: measures excess of return per unit of risk.
        self.max_drawdown: float = 0
        self.max_drawdown_percent: float = 0  # Drawdown maximum percentage.
        self.average_win_rate: float = 0  # Average rate of return for winning trades.
        self.average_loss_rate: float = 0  # Average rate of return for losing trades.
        self.profit_loss_ratio: float = (
            0  # The ratio of the average win rate to the average loss rate.
        )
        self.win_rate: float = (
            0  # The ratio of the number of winnig trades to the total number of trades.
        )
        self.expectancy: float = 0  # The expected value of the rate of return
        self.compounding_annual_return: float = 0  # Annual compounded returns statistic based on the final-starting capital and years.
        self.annual_standard_deviation: float = 0  # Annualized standard deviation.
        self.annual_variance: float = 0  # Annualized variance statistic calculation using the daily performance variance and trading days per year.
