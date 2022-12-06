from typing import List, Union, Dict, overload, Any
from datetime import date as Date 

from ..entities import Order, Instrument, Strategy as StrategyModel, BacktestReport, Trade
from ..trading.strategies import Strategy
from ..enums import OrderStatus, StrategyType
from ..events import OrderFilledEvent
from ..repositories import OrderRepository, InstrumentRepository, StrategyRepository
from .analysis_results import AnalysisResults
from .benchmark_symbol import BenchmarkSymbol
from .statistics_builder import StatisticsBuilder
from .statistics_results import StatisticsResults


class Analyzer:

    @classmethod
    def analyze_reports(
            cls, report_models: List[BacktestReport], starting_capital: float, start_date: Date, end_date: Date, benchmark_symbol: BenchmarkSymbol
        ) -> AnalysisResults:
        results: AnalysisResults = AnalysisResults(starting_capital, start_date, end_date, benchmark_symbol)
        
        # Builds benchmark results.
        benchmark_results: StatisticsResults = StatisticsBuilder.build_benchmark(benchmark_symbol, starting_capital, start_date, end_date)
        
        # Builds strategy results.
        instruments: List[Instrument] = InstrumentRepository.query_all()

        for report in report_models:
            model: Union[StrategyModel, None] = StrategyRepository.query_by_id(report.strategy_id)
            assert(model is not None)
            model.default_report_id = report.id
            strategy_id: str = f"{model.id}:{model.default_report_id}"

            # Create strategy instance by report model.
            strategy: Strategy = Strategy(strategy_id, model.description, model.type)

            # Get filted orders by date range.
            orders: List[Order] = list(filter(
                lambda order: order.datetime.date() >= start_date and order.datetime.date() <= end_date, OrderRepository.query_by_strategy_id(strategy.id))
            )
            
            # Start runtime sumulation.
            for order in orders:
                instrument: Union[Instrument, None] = next(filter(lambda instrument: instrument.symbol == order.symbol, instruments), None)
                
                if instrument is None:
                    raise RuntimeError(f"No data avaliable for this instrument: {order.symbol}")

                e: OrderFilledEvent = cls.__try_match_order(strategy, instrument, order)
                strategy.on_order_filled(e)

            # Get trading results of strategy instance.
            key: str = f"Strategy:{strategy_id}"
            results.add(key, StatisticsBuilder.build_strategy(
                strategy.closed_trades, 
                benchmark_results.total_performance.daily_statistics.returns,
                starting_capital,
                start_date,
                end_date                
            ))
        results.add(f"Benchmark:{benchmark_symbol.value}", benchmark_results)
        return results

    @classmethod
    def analyze_strategies(cls, strategies: List[StrategyModel], starting_capital: float, start_date: Date, end_date: Date, benchmark_symbol: BenchmarkSymbol) -> AnalysisResults:
        results: AnalysisResults = AnalysisResults(starting_capital, start_date, end_date, benchmark_symbol)
        
        # Builds benchmark results.
        benchmark_results: StatisticsResults = StatisticsBuilder.build_benchmark(benchmark_symbol, starting_capital, start_date, end_date)
        
        # Builds strategy results.
        instruments: List[Instrument] = InstrumentRepository.query_all()
        
        portfolio_trades: List[Trade] = []

        for model in strategies:
            strategy_id: str = f"{model.id}:{model.default_report_id}"

            # Create strategy instance by report model.
            strategy: Strategy = Strategy(strategy_id, model.description, model.type)

            # Get filted orders by date range.
            orders: List[Order] = list(filter(
                lambda order: order.datetime.date() >= start_date and order.datetime.date() <= end_date, OrderRepository.query_by_strategy_id(strategy.id))
            )
            
            cls.__mock_matching(strategy, instruments, orders)

            # Get trading results of strategy instance.
            key: str = f"Strategy:{strategy_id}"
            results.add(key, StatisticsBuilder.build_strategy(
                strategy.closed_trades, 
                benchmark_results.total_performance.daily_statistics.returns,
                starting_capital,
                start_date,
                end_date                
            ))

            if len(strategies) > 1:
                portfolio_trades.extend(strategy.closed_trades)
        
        if len(strategies):
            # Re-assign trade id for portfolio strategy.
            for i in range(len(portfolio_trades)):
                portfolio_trades[i].id = i + 1

            results.add("All", StatisticsBuilder.build_strategy(
                portfolio_trades, 
                benchmark_results.total_performance.daily_statistics.returns,
                starting_capital,
                start_date,
                end_date               
            ))
        results.add(f"Benchmark:{benchmark_symbol.value}", benchmark_results)
        return results

    @classmethod 
    def __try_match_order(cls, strategy: Strategy, instrument: Instrument, order: Order) -> OrderFilledEvent:
        order.filled_quantity = order.quantity
        order.avg_filled_price = order.price
        order.remaining_quantity -= order.filled_quantity
        order.status = OrderStatus.Filled
        order.is_day_trade = True if strategy.type == StrategyType.Intraday else False
        e: OrderFilledEvent = OrderFilledEvent(order)
        e.fee = instrument.exchange.get_order_fee(e, instrument.point_value)
        return e
    
    @classmethod
    def __mock_matching(cls, strategy: Strategy, instruments: List[Instrument], orders: List[Order]) -> None:
        # Start runtime sumulation.
        for order in orders:
            instrument: Union[Instrument, None] = next(filter(lambda instrument: instrument.symbol == order.symbol, instruments), None)
            
            if instrument is None:
                raise RuntimeError(f"No data avaliable for this instrument: {order.symbol}")

            e: OrderFilledEvent = cls.__try_match_order(strategy, instrument, order)
            strategy.on_order_filled(e)

