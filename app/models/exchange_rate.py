from typing import Optional, Tuple
from app.database import get_connection


class ExchangeRateResponse:
    def __init__(self, id: int, baseCurrency: dict, targetCurrency: dict, rate: float):
        self.id = id
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate


class ExchangeRate:
    def __init__(
        self, id: int, baseCurrencyId: int, targetCurrencyId: int, rate: float
    ):
        self.id = id
        self.baseCurrencyId = baseCurrencyId
        self.targetCurrencyId = targetCurrencyId
        self.rate = rate

    @staticmethod
    def fetch_exchange_rates() -> Tuple[list["ExchangeRate"], Optional[Exception]]:
        with get_connection() as connection:
            cursor = connection.cursor()
            exchange_rates = []
            try:
                cursor.execute("SELECT * FROM ExchangeRate;")
                for row in cursor:
                    exchange_rates.append(ExchangeRate(*row))
            except Exception as e:
                return None, e
            return exchange_rates, None

    @staticmethod
    def fetch_exchange_rate(
        base_cur_id, target_cur_id
    ) -> Tuple["ExchangeRate", Optional[Exception]]:
        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "SELECT * FROM ExchangeRate WHERE BaseCurrencyId=? AND TargetCurrencyId=?;",
                    (base_cur_id, target_cur_id),
                )
                row = cursor.fetchone()
                exchange_rate = ExchangeRate(*row)
            except Exception as e:
                return None, e
            return exchange_rate, None

    @staticmethod
    def insert_exchange_rate(base_cur_id, target_cur_id, rate) -> Exception:
        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO ExchangeRate(BaseCurrencyId, TargetCurrencyId, Rate) VALUES(?, ?, ?);",
                    (base_cur_id, target_cur_id, rate),
                )
                connection.commit()
            except Exception as e:
                return e
            return None

    @staticmethod
    def update_exchange_rate(base_cur_id, target_cur_id, rate) -> Exception:
        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE ExchangeRate SET Rate=? WHERE BaseCurrencyId=? AND TargetCurrencyId=?;",
                    (rate, base_cur_id, target_cur_id),
                )
                connection.commit()
            except Exception as e:
                return e
            return None
