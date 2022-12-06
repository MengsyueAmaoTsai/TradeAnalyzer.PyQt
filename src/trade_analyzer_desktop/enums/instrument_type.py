from enum import Enum

class InstrumentType(Enum):
    Unknown = "Unknown"
    Equity = "Equity"
    Bond = "Bond"
    Commodity = "Commodity"
    Cash = "Cash"
    Cryptocurrency = "Cryptocurrency"
    Forex = "Forex"
    Future = "Future"
    Option = "Option"
    Swap = "Swap"
    Forward = "Forward"
    CDF = "CFD"
    Warrant = "Warrant"
    ETF = "ETF"
    MutualFund = "MutualFund"

