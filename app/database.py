import sqlite3
from config import DB_PATH
from contextlib import contextmanager


@contextmanager
def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def initialize():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Currency"
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT, Code VARCHAR NOT NULL, FullName VARCHAR NOT NULL, Sign VARCHAR NOT NULL);"
        )
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS code_index ON Currency(Code);"
        )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS ExchangeRate"
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT, BaseCurrencyId INTEGER NOT NULL, TargetCurrencyId INTEGER NOT NULL, Rate DECIMAL(6, 6) NOT NULL,"
            "FOREIGN KEY (BaseCurrencyId) REFERENCES Currency(ID), FOREIGN KEY (TargetCurrencyId) REFERENCES Currency(ID));"
        )
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS currencies_index ON ExchangeRate(BaseCurrencyId, TargetCurrencyId);"
        )
