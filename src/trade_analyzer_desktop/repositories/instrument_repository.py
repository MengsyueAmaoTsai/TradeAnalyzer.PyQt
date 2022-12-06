from typing import List, Union

from PyQt6.QtSql import QSqlQuery

from ..entities import Instrument


class InstrumentRepository:

    QUERY_ALL_INSTRUMENTS_SQL: str = f"""
    SELECT * FROM instruments
    """

    SELECT_BY_SYMBOL_SQL: str = """
    SELECT * FROM instruments WHERE symbol = :symbol
    """
    INSERT_INSTRUMENTS_SQL: str = """
    INSERT INTO instruments (symbol, description, exchange, type, fee_pricing, point_value)
    VALUES (?, ?, ?, ?, ?, ?)
    """    

    @classmethod
    def query_all(cls) -> List[Instrument]:
        instruments: List[Instrument] = []
        query: QSqlQuery = QSqlQuery()
        query.exec(cls.QUERY_ALL_INSTRUMENTS_SQL)
        
        while (query.next()):
            instruments.append(Instrument.from_query(query))
        return instruments

    @classmethod
    def query_by_symbol(cls, symbol: str) -> Union[Instrument, None]:
        instrument: Union[Instrument, None] = None

        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.SELECT_BY_SYMBOL_SQL)
        query.bindValue(":symbol", symbol)
        query.exec()

        if (query.next()):
            instrument = Instrument.from_query(query)
        return instrument        

    @classmethod
    def insert_batch(cls, instruments: List[Instrument]) -> bool:
        query: QSqlQuery = QSqlQuery()
        query.prepare(cls.INSERT_INSTRUMENTS_SQL)

        query.addBindValue([instrument.symbol for instrument in instruments])
        query.addBindValue([instrument.description for instrument in instruments])
        query.addBindValue([instrument.exchange.id for instrument in instruments])
        query.addBindValue([instrument.type.value for instrument in instruments])
        query.addBindValue([instrument.fee_pricing for instrument in instruments])
        query.addBindValue([instrument.point_value for instrument in instruments])
        success: bool = query.execBatch()

        if not success:
            print(query.lastError().text())
        return success