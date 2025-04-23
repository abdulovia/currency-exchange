from urllib.parse import parse_qsl
from app.models.response import Response
from app.models.currency import Currency

class CurrencyController:
    def get_currencies(self) -> Response:
        currencies, err = Currency.fetch_currencies()
        if err != None:
            return Response(500, "Internal Server Error: database error: " + str(err))
        return Response(
            200, "OK: fetched all currencies from db", [c.__dict__ for c in currencies]
        )


    def get_currency(self, code: str="") -> Response:
        if code == "":
            return Response(400, "Bad Request: currency code is empty")
        currency, err = Currency.fetch_currency(code)
        if err != None:
            if str(err).endswith("NoneType"):
                return Response(404, "404 Not Found: currency not found: " + str(err))
            return Response(500, "Internal Server Error: database error: " + str(err))
        return Response(200, "OK: fetched one currrency from db", currency.__dict__)


    def post_currency(self, data_decoded: str) -> Response:
        data = dict(parse_qsl(data_decoded))
        print(data)
        code, name, sign = data.get("code"), data.get("name"), data.get("sign")
        if not code or not name or not sign:
            return Response(400, "Bad Request: required form field is missing")

        err = Currency.insert_currency(code, name, sign)
        if err != None:
            if str(err).startswith("UNIQUE constraint failed"):
                return Response(
                    409, "Conflict: currency was previously inserted: " + str(err)
                )
            return Response(500, "Internal Server Error: database error: " + str(err))

        return self.get_currency(code)
