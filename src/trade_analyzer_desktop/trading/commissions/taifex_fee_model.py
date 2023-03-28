from .fee_model import FeeModel
from ...events import OrderFilledEvent


class TaiFexFeeModel(FeeModel):
    def __init__(self, fee_pricing: float) -> None:
        super().__init__(fee_pricing)

    def get_order_fee(self, e: OrderFilledEvent) -> float:
        """ """
        order_fee: float = e.filled_quantity * self.fee_pricing
        return order_fee
