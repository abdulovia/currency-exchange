from app.database import get_connection


class Currency:
    def __init__(
        self, id: int = None, code: str = None, name: str = None, sign: str = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.sign = sign

    @staticmethod
    def fetch_currencies():
        with get_connection() as connection:
            cursor = connection.cursor()
            currencies, err = [], None
            try:
                cursor.execute("SELECT * FROM Currency;")
                for currency in cursor:
                    currencies.append(Currency(*currency))
            except Exception as e:
                err = e
            return currencies, err

    @staticmethod
    def fetch_currency(code):
        with get_connection() as connection:
            cursor = connection.cursor()
            currency, err = None, None
            try:
                cursor.execute("SELECT * FROM Currency WHERE Code=?;", (code,))
                row = cursor.fetchone()
                currency = Currency(*row)
            except Exception as e:
                err = e
            return currency, err

    @staticmethod
    def insert_currency(code, name, sign):
        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Currency(Code, FullName, Sign) VALUES(?, ?, ?);",
                    (code, name, sign),
                )
                connection.commit()
            except Exception as e:
                return e
            return None

    @staticmethod
    def get_currency_by_id(id):
        with get_connection() as connection:
            cursor = connection.cursor()
            currency, err = None, None
            try:
                cursor.execute("SELECT * FROM Currency WHERE ID=?;", (id,))
                row = cursor.fetchone()
                currency = Currency(*row)
            except Exception as e:
                err = e
            return currency, err
