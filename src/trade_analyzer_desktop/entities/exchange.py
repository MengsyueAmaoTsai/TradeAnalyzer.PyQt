from typing import Union, List

from ..trading.commissions import FeeModel, TaiFexFeeModel, TwseFeeModel
from ..events import OrderFilledEvent


class Exchange:
    SUPPORTS_EXCHANGES: List[str] = ["TWSE", "TAIFEX"]

    def __init__(self, id: str, description: str, fee_model: FeeModel) -> None:
        self.__id: str = id
        self.__description: str = description
        self.__fee_model: FeeModel = fee_model

    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def id(self) -> str:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def fee_model(self) -> FeeModel:
        return self.__fee_model

    # -------------------------------------------------- Public Methods --------------------------------------------------
    @classmethod
    def create(cls, exchange_id: str, fee_pricing: float) -> Union["Exchange", None]:
        if exchange_id.__eq__("TWSE"):
            return cls.twse(fee_pricing)

        elif exchange_id.__eq__("TAIFEX"):
            return cls.taifex(fee_pricing)
        else:
            raise ValueError("Unsupported exchange.")

    @classmethod
    def twse(cls, fee_pricing: float) -> "Exchange":
        return cls("TWSE", "Taiwan Security Exchange", TwseFeeModel(fee_pricing))

    @classmethod
    def taifex(cls, fee_pricing: float) -> "Exchange":
        return cls("TAIFEX", "Taiwan Futures Exchange", TaiFexFeeModel(fee_pricing))

    def get_order_fee(self, e: OrderFilledEvent, point_value: float) -> float:
        return self.fee_model.get_order_fee(e, point_value)
