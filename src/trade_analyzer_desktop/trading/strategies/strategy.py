from typing import List, Union
from datetime import datetime as DateTime

from ..positions import PositionManager
from ...repositories import InstrumentRepository
from ...entities import Position, Instrument, Trade
from ...events import OrderFilledEvent
from ...enums import StrategyType, Side


class Strategy:
    def __init__(self, id: str, description: str, type: StrategyType) -> None:
        self.__id: str = id
        self.__description: str = description
        self.__type: StrategyType = type
        self.__position_manager: PositionManager = PositionManager()
        self.__position_manager.register_position_closed_callback(
            self.on_position_closed
        )
        self.__next_trade_int: int = 1
        self.__closed_trades: List[Trade] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def type(self) -> StrategyType:
        return self.__type

    @property
    def open_positions(self) -> List[Position]:
        return self.__position_manager.open_positions

    @property
    def closed_positions(self) -> List[Position]:
        return self.__position_manager.closed_positions

    @property
    def closed_trades(self) -> List[Trade]:
        return self.__closed_trades

    def on_order_filled(self, e: OrderFilledEvent) -> None:
        self.__position_manager.on_order_filled(e)

    def on_position_closed(self, position: Position) -> None:
        instrument: Union[Instrument, None] = InstrumentRepository.query_by_symbol(
            position.symbol
        )
        buy_fills: List[OrderFilledEvent] = position.buy_fills
        sell_fills: List[OrderFilledEvent] = position.sell_fills
        entry_time: DateTime = position.fills[0].datetime
        avg_entry_price: float = 0
        trade_size: float = position.total_entry_size
        exit_time: DateTime = position.fills[-1].datetime
        avg_exit_price: float = 0
        fee: float = sum(fill.fee for fill in position.fills)

        if position.side == Side.Long:
            avg_entry_price: float = (
                sum(fill.quantity * fill.price for fill in buy_fills)
                / position.total_entry_size
            )
            avg_exit_price: float = (
                sum(fill.quantity * fill.price for fill in sell_fills)
                / position.total_exit_size
            )
        elif position.side == Side.Short:
            avg_entry_price: float = (
                sum(fill.quantity * fill.price for fill in sell_fills)
                / position.total_entry_size
            )
            avg_exit_price: float = (
                sum(fill.quantity * fill.price for fill in buy_fills)
                / position.total_exit_size
            )

        assert instrument is not None
        gross_profit_loss: float = (
            instrument.point_value
            * position.total_buy_size
            * (avg_exit_price - avg_entry_price)
            if position.side == Side.Long
            else instrument.point_value
            * position.total_sell_size
            * (avg_entry_price - avg_exit_price)
        )

        trade: Trade = Trade(
            self.__next_trade_int,
            position.symbol,
            entry_time,
            avg_entry_price,
            position.side,
            trade_size,
            exit_time,
            avg_exit_price,
            gross_profit_loss,
            fee,
            self.id,
            position.fills,
        )
        self.__next_trade_int += 1
        self.__closed_trades.append(trade)
