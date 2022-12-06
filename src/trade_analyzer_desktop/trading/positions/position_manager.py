from typing import List, Union, Callable

from ...entities import Position
from ...events import OrderFilledEvent
from ...enums import Side, Action, PositionStatus

class PositionManager:

    def __init__(self) -> None:
        self.__positions: List[Position] = []
        self.__next_position_id: int = 1
        self.__position_closed_callbacks: List[Callable[[Position], None]] = []

    @property
    def open_positions(self) -> List[Position]:
        return list(filter(lambda pos: pos.status == PositionStatus.Opened, self.__positions))

    @property
    def closed_positions(self) -> List[Position]:
        return list(filter(lambda pos: pos.status == PositionStatus.Closed, self.__positions))

    def on_order_filled(self, e: OrderFilledEvent) -> None:
        open_position: Union[Position, None] = next(
            filter(lambda pos: pos.symbol == e.symbol and pos.strategy_id  == e.strategy_id and pos.status == PositionStatus.Opened, self.__positions), 
            None
        )

        if not open_position:
            new_position: Position = Position(
                self.__next_position_id, 
                e.symbol,
                Side.Long if e.action == Action.Buy else Side.Short,
                e.strategy_id
            )

            new_position.add_fill(e)
            self.__positions.append(new_position)
            self.__next_position_id += 1
            return
        else:
            if e.action == open_position.fills[0].action:
                open_position.add_fill(e)
            else:
                open_position.add_fill(e)
                if open_position.total_entry_size - open_position.total_exit_size == 0:
                    self.close_position(open_position)
                    
    def close_position(self, position: Position) -> None:
        position.status = PositionStatus.Closed

        for callback in self.__position_closed_callbacks:
            callback(position)

    def register_position_closed_callback(self, callback: Callable[[Position], None]) -> None:
        self.__position_closed_callbacks.append(callback)