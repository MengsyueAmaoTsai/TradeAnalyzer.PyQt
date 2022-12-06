
from .fee_model import FeeModel
from ...enums import Action
from ...events import OrderFilledEvent


class TwseFeeModel(FeeModel):
    
    TAX_RATE: float = 0.003

    def __init__(self, fee_pricing: float) -> None:
        super().__init__(fee_pricing)

    def get_order_fee(self, e: OrderFilledEvent, point_value: float) -> float:
        commission: float = 0
        tax: float = 0
        trade_volume: float = (e.filled_quantity * e.avg_filled_price * point_value)
        commission = trade_volume * self.fee_pricing
        
        if e.action == Action.Sell:
            tax = trade_volume * self.TAX_RATE
    
            if e.is_day_trade: 
                tax /= 2
        return commission + tax  