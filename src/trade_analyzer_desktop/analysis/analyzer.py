from typing import List, Union
from datetime import date as Date 

from ..entities import Order, Instrument, Strategy as StrategyModel
from ..trading.strategies import Strategy
from ..enums import OrderStatus, StrategyType
from ..events import OrderFilledEvent
from ..repositories import OrderRepository, InstrumentRepository
from .analysis_results import AnalysisResults
from .benchmark_symbol import BenchmarkSymbol
from .statistics_builder import StatisticsBuilder

class Analyzer:


    @classmethod
    def run_analysis(cls, strategy_models: List[StrategyModel], starting_capital: float, start_date: Date, end_date: Date, benchmark_symbol: BenchmarkSymbol) -> AnalysisResults:
        results: AnalysisResults = AnalysisResults(starting_capital, start_date, end_date, benchmark_symbol)
        benchmark_statistics_results = StatisticsBuilder.build_benchmark(benchmark_symbol, starting_capital, start_date, end_date)

        # Strategy part.
        instruments: List[Instrument] = InstrumentRepository.query_all()
        for model in strategy_models:
            # Strategy instance.
            strategy: Strategy = Strategy(f"{model.id}:{model.default_report_id}", model.description, model.type)    
            # Filt orders with date range.
            orders: List[Order] = list(filter(lambda o: o.datetime.date() >= start_date and o.datetime.date() <= end_date, OrderRepository.query_by_strategy_id(strategy.id)))
            
            # Start simulation.
            for order in orders:
                instrument: Union[Instrument, None] = next(filter(lambda ins: ins.symbol == order.symbol, instruments), None)
                
                if instrument == None:
                    raise RuntimeError(f"No data avaliable for this instrument: {order.symbol}")

                assert(instrument.exchange is not None)
                order.filled_quantity = order.quantity
                order.avg_filled_price = order.price
                order.status = OrderStatus.Filled
                order.is_day_trade = True if strategy.type == StrategyType.Intraday else False
                e: OrderFilledEvent = OrderFilledEvent(order)
                e.fee = instrument.exchange.get_order_fee(e, instrument.point_value)
                strategy.on_order_filled(e)

            # Get trading results of strategy.
            key: str = f"Strategy:{model.id}:{model.default_report_id}"
            results.add(key, StatisticsBuilder.build_strategy(
                strategy.closed_trades,
                benchmark_statistics_results.total_performance.daily_statistics.returns,
                starting_capital,
                start_date,
                end_date
            ))
        results.add(f"Benchmark:{benchmark_symbol.value}", benchmark_statistics_results)
        return results
            