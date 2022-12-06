from typing import Dict, Union
from datetime import datetime as DateTime, timedelta as TimeDelta



class TradeStatistics():
    """
    The class represents a set of statistics calculated from a list of closed trades.
    """

    def __init__(self) -> None:
        self.net_profit_loss: Dict[int, float] = {}
        self.returns: Dict[int, float] = {}
        self.equity: Dict[int, float] = {}
        self.cumulative_returns: Dict[int, float] = {}
        self.drawdown: Dict[int, float] = {}
        self.drawdown_percent: Dict[int, float] = {} 
        
        self.start_datetime: Union[DateTime, None] = None # The entry date/time of the first trade.
        self.end_datetime: Union[DateTime, None] = None # The exit date/time of the last trade.

        self.total_number_of_trades: int = 0 # The total number of trades.
        self.number_of_winning_trades: int = 0 # The total number of winning trades.
        self.number_of_lossing_trades: int = 0 # The total number of lossing trades.
        
        self.total_net_profit: float = 0 # Total profit/loss for all trades (as symbol currency)
        self.total_profit: float = 0 # Total profit for all winning trades
        self.total_loss: float = 0 # Total loss for all lossing trades.
        self.total_fees: float = 0 # Sum of fees for all trades.
        
        self.largest_profit: float = 0 # Largest profit in a single trade.
        self.largest_loss: float = 0 # Largest loss in a single trades.
        self.largest_mae: float = 0 # The largest Maximum Adverse Excursion in a single trade.    
        self.largest_mfe: float = 0 # The largest Maximum Favorable Excursion in a single trade.    
        
        self.average_profit_loss: float = 0 # Average profit/loss for all trades.
        self.average_profit: float = 0 # Average profit for all winning trades.
        self.average_loss: float = 0 # Average loss for all lossing treades.
        self.average_mae: float = 0 # The average Maximum Adverse Excursion for all trades.
        self.average_mfe: float = 0 # The average Maximum Favorable Excursion for all trades.
        
        self.avearage_trade_duration: TimeDelta = TimeDelta() # Average duration for all trades.
        self.average_winning_trade_duration: TimeDelta = TimeDelta() # Average duration for all winning trades.
        self.average_lossing_trade_duration: TimeDelta = TimeDelta() # Average duration for all lossing trades.
        self.average_end_trade_drawdown: float = 0 # Average amount of profit given back y a single trade before exit.
        
        self.max_consecutive_winning_trades: int = 0 # The max number of consecutive winning trades.
        self.max_consecutive_lossing_trades: int = 0 # The max number of consecutive lossing trades.
        self.max_closed_trade_drawdown: float = 0 # Maximum closed-trade drawdown for all trades.
        self.max_intra_trade_drawdown: float = 0 # Maximum intra-trade drawdown for all trades.
        self.max_end_trade_drawdown: float = 0 # Maximum amount of profit given back y a single trade before exit.
        self.max_drawdown_duration: TimeDelta = TimeDelta() # Maximum amount of time to recover from a drawdown.
        
        self.profit_loss_ratio: float = 0 # The ratio of the average profit per trade to the average loss per trade.
        self.win_rate: float = 0 # Ratio of the number of winning trades to the number of trades.         
        self.profit_factor: float = 0 # Ratio of the total profit to the total loss.
        self.profit_to_max_drawdown_ratio: float = 0 # Ratio of total profit/loss to the maximum closed-trade drawdown.

        self.profit_loss_standard_deviation: float = 0 # The standard deviation of the profits/losses for all trades.
        self.profit_loss_downside_deviation: float = 0 # The downside deviation of the profits/losses for all trades.
        self.sharpe_ratio: float = 0 # Ratio of the average profit/loss to the standard deviation.
        self.sortino_ratio: float = 0 # Ratio of the average profit/loss to the downside deviation.

   
   