from .daily_statistics import DailyStatistics

class StrategyDailyStatistics(DailyStatistics):
    """ 
    The class represents a set of statistics calculated from equity and benchmark samples 
    """

    def __init__(self) -> None:
        super().__init__()
        self.alpha: float = 0 # Strategy 'alpha' - abnormal returns over the risk free intrest rate and the relationshio with the benchmark returns.
        self.beta: float = 0 # Strategy 'beta' statistic - the covariance between the strategy and benchmark performance, divided by benchmark's variance.
        self.information_ratio: float = 0 # Risk-adjusted return.
        self.tracking_error: float = 0 # Tracking error volatility (TEV) statistic - a measure of how closely a portfolio follows the index to which it is benchmarked.
        self.treynor_ratio: float = 0 # Treynor ratio statistic is a measurement of the returns earned in excess of that which could have been earned on an investment that has np doversofiable risk.
        