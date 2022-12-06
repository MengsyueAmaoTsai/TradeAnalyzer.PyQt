import math
from typing import List, Dict
from datetime import datetime as DateTime, timedelta as TimeDelta, date as Date

from .trade_statistics import TradeStatistics
from ..entities import Trade


class TradeStatisticsBuilder:

    @staticmethod
    def build(trades: List[Trade], starting_capital: float, start_date: Date, end_date: Date) -> TradeStatistics:
        trade_statistics: TradeStatistics = TradeStatistics()

        net_profit_loss: Dict[int, float] = { 0: 0}
        returns: Dict[int, float] = { 0: 0}
        equity: Dict[int, float] = { 0: starting_capital}
        cumulative_returns: Dict[int, float] = { 0: 0}
        drawdown: Dict[int, float] = { 0: 0}
        drawdown_percent: Dict[int, float] = { 0: 0} 

        max_consecutive_winners: int = 0
        max_consecutive_losers: int = 0
        max_total_profit_loss: float = 0
        max_total_profit_loss_with_mfe: float = 0
        sum_for_variance: float = 0
        sum_for_downside_variance: float = 0
        last_peak_time = DateTime.min
        is_in_drawdown: bool = False
        max_equity: float = starting_capital

        for trade in trades:
            net_profit_loss[trade.id] = trade.net_profit_loss
            returns[trade.id] = trade.net_profit_loss / equity[trade.id - 1]
            current_equity: float = equity[trade.id - 1] + trade.net_profit_loss 
            equity[trade.id] = current_equity
            cumulative_returns[trade.id] = current_equity / starting_capital - 1
            
            if trade.net_profit_loss > 0:
                max_equity = max(max_equity, current_equity)

            drawdown[trade.id] = current_equity - max_equity
            drawdown_percent[trade.id] = drawdown[trade.id] / max_equity

            if (last_peak_time == DateTime.min):
                last_peak_time = trade.entry_time

            if (trade_statistics.start_datetime == None or trade.entry_time < trade_statistics.start_datetime):
                trade_statistics.start_datetime = trade.entry_time

            if (trade_statistics.end_datetime == None or trade.exit_time > trade_statistics.end_datetime):
                trade_statistics.end_datetime = trade.exit_time

            trade_statistics.total_number_of_trades += 1

            if (trade_statistics.total_profit_loss + trade.mfe > max_total_profit_loss_with_mfe):
                max_total_profit_loss_with_mfe = trade_statistics.total_profit_loss + trade.mfe

            if (trade_statistics.total_profit_loss + trade.mae - max_total_profit_loss_with_mfe < trade_statistics.max_intra_trade_drawdown):
                trade_statistics.max_intra_trade_drawdown = trade_statistics.total_profit_loss + trade.mae - max_total_profit_loss_with_mfe
            
            if (trade.net_profit_loss > 0):
                trade_statistics.number_of_winning_trades += 1
                trade_statistics.total_profit_loss += trade.net_profit_loss
                trade_statistics.total_profit += trade.net_profit_loss
                trade_statistics.average_profit += (trade.net_profit_loss - trade_statistics.average_profit) / trade_statistics.number_of_winning_trades
                trade_statistics.average_winning_trade_duration += TimeDelta(seconds = (trade.duration.total_seconds() - trade_statistics.average_winning_trade_duration.total_seconds()) / trade_statistics.number_of_winning_trades)

                if (trade.net_profit_loss > trade_statistics.largest_profit):
                    trade_statistics.largest_profit = trade.net_profit_loss
                
                max_consecutive_winners += 1
                max_consecutive_losers = 0

                if (max_consecutive_winners > trade_statistics.max_consecutive_winning_trades):
                    trade_statistics.max_consecutive_winning_trades = max_consecutive_winners
                
                if (trade_statistics.total_profit_loss > max_total_profit_loss):
                    max_total_profit_loss = trade_statistics.total_profit_loss

                    if (is_in_drawdown and (trade.exit_time - last_peak_time) > trade_statistics.max_drawdown_duration):
                        trade_statistics.max_drawdown_duration = trade.exit_time - last_peak_time

                    last_peak_time = trade.exit_time
                    is_in_drawdown = False
            else:
                trade_statistics.number_of_lossing_trades += 1
                trade_statistics.total_profit_loss += trade.net_profit_loss
                trade_statistics.total_loss += trade.net_profit_loss
                
                prev_average_loss: float = trade_statistics.average_loss
                trade_statistics.average_loss += (trade.net_profit_loss - trade_statistics.average_loss) / trade_statistics.number_of_lossing_trades

                sum_for_downside_variance += (trade.net_profit_loss - prev_average_loss) * (trade.net_profit_loss - trade_statistics.average_loss)                
                
                downside_variance: float = sum_for_downside_variance / (trade_statistics.number_of_lossing_trades - 1) if trade_statistics.number_of_lossing_trades > 1 else 0
                trade_statistics.profit_loss_downside_deviation = math.sqrt(downside_variance)
                trade_statistics.average_lossing_trade_duration += TimeDelta(seconds = (trade.duration.total_seconds() - trade_statistics.average_lossing_trade_duration.total_seconds()) / trade_statistics.number_of_lossing_trades)

                if (trade.net_profit_loss < trade_statistics.largest_loss):
                    trade_statistics.largest_loss = trade.net_profit_loss

                max_consecutive_winners = 0
                max_consecutive_losers += 1

                if (max_consecutive_losers > trade_statistics.max_consecutive_lossing_trades):
                    trade_statistics.max_consecutive_lossing_trades = max_consecutive_losers

                if (trade_statistics.total_profit_loss - max_total_profit_loss < trade_statistics.max_closed_trade_drawdown):
                    trade_statistics.max_closed_trade_drawdown = trade_statistics.total_profit_loss - max_total_profit_loss
                
                is_in_drawdown = True

            prev_average_profit_loss: float = trade_statistics.average_profit
            trade_statistics.average_profit_loss += (trade.net_profit_loss - trade_statistics.average_profit_loss) / trade_statistics.total_number_of_trades

            sum_for_variance += (trade.net_profit_loss - prev_average_profit_loss) * (trade.net_profit_loss - trade_statistics.average_profit_loss)
            variance: float = sum_for_variance / (trade_statistics.total_number_of_trades - 1) if trade_statistics.total_number_of_trades > 1 else 0 
            trade_statistics.profit_loss_standard_deviation = math.sqrt(variance) if variance > 0 else 0

            trade_statistics.avearage_trade_duration += TimeDelta(seconds = (trade.duration.total_seconds() - trade_statistics.avearage_trade_duration.total_seconds()) / trade_statistics.total_number_of_trades)
            trade_statistics.average_mae += (trade.mae - trade_statistics.average_mae) / trade_statistics.total_number_of_trades
            trade_statistics.average_mfe += (trade.mfe - trade_statistics.average_mfe) / trade_statistics.total_number_of_trades

            if (trade.mae < trade_statistics.largest_mae):
                trade_statistics.largest_mae = trade.mae

            if (trade.mfe > trade_statistics.largest_mfe):
                trade_statistics.largest_mfe = trade.mfe
            
            if (trade.end_trade_drawdown < trade_statistics.max_end_trade_drawdown):
                trade_statistics.max_end_trade_drawdown = trade.end_trade_drawdown
            
            trade_statistics.total_fees += trade.net_profit_loss

        trade_statistics.profit_loss_ratio = trade_statistics.average_profit / abs(trade_statistics.average_loss) if trade_statistics.average_loss != 0 else 0 
        trade_statistics.win_rate = trade_statistics.number_of_winning_trades / trade_statistics.total_number_of_trades if trade_statistics.total_number_of_trades != 0 else 0
        trade_statistics.profit_factor = trade_statistics.total_profit / abs(trade_statistics.total_loss) if trade_statistics.total_loss != 0 else 0 if trade_statistics.total_profit != 0 else 0
        trade_statistics.sharpe_ratio = trade_statistics.average_profit_loss / trade_statistics.profit_loss_standard_deviation if trade_statistics.profit_loss_standard_deviation != 0 else 0
        trade_statistics.sortino_ratio = trade_statistics.average_profit_loss / trade_statistics.profit_loss_downside_deviation if trade_statistics.profit_loss_downside_deviation != 0 else 0
        trade_statistics.profit_to_max_drawdown_ratio = trade_statistics.total_profit_loss / abs(trade_statistics.max_closed_trade_drawdown) if trade_statistics.max_closed_trade_drawdown != 0 else 0
        trade_statistics.average_end_trade_drawdown = trade_statistics.average_profit_loss - trade_statistics.average_mae
        
        trade_statistics.net_profit_loss = net_profit_loss
        trade_statistics.returns = returns
        trade_statistics.equity = equity
        trade_statistics.cumulative_returns = cumulative_returns
        trade_statistics.drawdown = drawdown
        trade_statistics.drawdown_percent = drawdown_percent

        return trade_statistics