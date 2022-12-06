from abc import ABC, abstractmethod

from ...events import OrderFilledEvent

class FeeModel(ABC):

    def __init__(self, fee_pricing: float) -> None:
        self.__fee_pricing: float = fee_pricing
    
    # -------------------------------------------------- Properties -------------------------------------------------- 
    @property
    def fee_pricing(self) -> float:
        return self.__fee_pricing

    # -------------------------------------------------- Public Methods -------------------------------------------------- 
    @abstractmethod
    def get_order_fee(self, e: OrderFilledEvent, point_value: float) -> float: ...

