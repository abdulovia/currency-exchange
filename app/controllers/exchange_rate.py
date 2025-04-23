from urllib.parse import parse_qsl
from app.models.response import Response
from app.models.currency import Currency
from app.models.exchange_rate import ExchangeRate, ExchangeRateResponse

class ExchangeRateController:
    def get_exchange_rates(self) -> Response:
        exchange_rates_raw, err = ExchangeRate.fetch_exchange_rates()
        if err:
            return Response(500, "Internal Server Error: database error: " + str(err))
        exchange_rates = []
        for er in exchange_rates_raw:
            base_cur, err1 = Currency.get_currency_by_id(er.baseCurrencyId)
            target_cur, err2 = Currency.get_currency_by_id(er.targetCurrencyId)
            if err1 or err2:
                return Response(400, "Bad Request: currency not found in database")
            exchange_rates.append(
                ExchangeRateResponse(er.id, base_cur.__dict__, target_cur.__dict__, er.rate)
            )
        return Response(
            200, "OK: fetched all exchange rates", [er.__dict__ for er in exchange_rates]
        )

    def get_exchange_rate(self, codes: str = "") -> Response:
        if len(codes) != 6:
            return Response(400, "Bad Request: currency value pair not found in path")
        base_code, target_code = codes[:3], codes[3:]
        base_cur, err1 = Currency.fetch_currency(base_code)
        target_cur, err2 = Currency.fetch_currency(target_code)
        if err1 or err2:
            return Response(400, "Bad Request: currency not found in database")
        er_raw, err = ExchangeRate.fetch_exchange_rate(base_cur.id, target_cur.id)
        if err:
            if str(err).endswith("NoneType"):
                return Response(404, "404 Not Found: exchange rate not found: " + str(err))
            return Response(500, "Internal Server Error: database error: " + str(err))
        exchange_rate = ExchangeRateResponse(
            er_raw.id, base_cur.__dict__, target_cur.__dict__, er_raw.rate
        )
        return Response(200, "OK: fetched exchange rate", exchange_rate.__dict__)

    def post_exchange_rate(self, data_decoded: str) -> Response:
        data = dict(parse_qsl(data_decoded))
        print(data)
        base_code = data.get("baseCurrencyCode")
        target_code = data.get("targetCurrencyCode")
        rate = data.get("rate")
        if not base_code or not target_code or not rate:
            return Response(400, "Bad Request: required form field is missing")
        base_cur, err1 = Currency.fetch_currency(base_code)
        target_cur, err2 = Currency.fetch_currency(target_code)
        if err1 != None or err2 != None:
            return Response(404, "Bad Request: currency code not found in database")
        err = ExchangeRate.insert_exchange_rate(base_cur.id, target_cur.id, rate)
        if err != None:
            return Response(
                409, "Conflict: exchange rate was previously inserted" + str(err)
            )
        return self.get_exchange_rate(base_code + target_code)

    def patch_exchange_rate(self, data_decoded: str, codes: str = "") -> Response:
        data = dict(parse_qsl(data_decoded))
        print(data)
        if "rate" not in data or len(codes) != 6:
            return Response(400, "Bad Request: form field or value pair missing")
        base_code, target_code, rate = codes[:3], codes[3:], data["rate"]
        base_cur, err1 = Currency.fetch_currency(base_code)
        target_cur, err2 = Currency.fetch_currency(target_code)
        if err1 or err2:
            return Response(400, "Bad Request: currency not found in database")
        err = ExchangeRate.update_exchange_rate(base_cur.id, target_cur.id, rate)
        if err != None:
            return Response(404, "404 Not Found: exchange rate not found: " + str(err))
        return self.get_exchange_rate(base_code + target_code)

    def get_exchange(self, query) -> Response:
        query_dct = dict(parse_qsl(query))
        amount = int(query_dct["amount"])
        resp = self.get_exchange_rate(query_dct["from"] + query_dct["to"])
        if resp.code == 200:
            rate = resp.body["rate"]
            converted_amount = rate * amount
        else:
            resp = self.get_exchange_rate(query_dct["to"] + query_dct["from"])
            if resp.code == 200:
                rate = 1 / resp.body["rate"]
                converted_amount = rate * amount
            else:
                resp1 = self.get_exchange_rate("USD" + query_dct["from"])
                resp2 = self.get_exchange_rate("USD" + query_dct["to"])
                if resp1.code == 200 and resp2.code == 200:
                    rate = resp2.body["rate"] / resp1.body["rate"]
                    converted_amount = rate * amount
                else:
                    return Response(
                        404, "404 Not Found: exchange rate to convert not found"
                    )
        base_cur, err1 = Currency.fetch_currency(query_dct["from"])
        target_cur, err2 = Currency.fetch_currency(query_dct["to"])
        if err1 or err2:
            return Response(400, "Bad Request: currency not found in database")
        result_dct = {
            "baseCurrency": base_cur.__dict__,
            "targetCurrency": target_cur.__dict__,
            "rate": round(rate, 3),
            "amount": amount,
            "convertedAmount": round(converted_amount, 3),
        }
        return Response(200, "OK: successfully exchanged currencies", result_dct)
