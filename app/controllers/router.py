from app.controllers.currency import CurrencyController
from app.controllers.exchange_rate import ExchangeRateController


class Router:
    currencyController = CurrencyController()
    exchangeRateController = ExchangeRateController()
    routes = {
        "GET": [
            ("/currencies", currencyController.get_currencies),
            ("/currency", currencyController.get_currency),
            ("/exchangeRates", exchangeRateController.get_exchange_rates),
            ("/exchangeRate", exchangeRateController.get_exchange_rate),
            ("/exchange", exchangeRateController.get_exchange),
        ],
        "POST": [
            ("/currencies", currencyController.post_currency),
            ("/exchangeRates", exchangeRateController.post_exchange_rate),
        ],
        "PATCH": [
            ("/exchangeRate", exchangeRateController.patch_exchange_rate),
        ],
    }

    def match_path2route(self, method: str, path: str):
        route_list = self.routes[method]
        path_list = path.split("/")
        if len(path_list) < 2:
            return None, None
        for route in route_list:
            if route[0] == "/" + path_list[1]:
                return route[1], None if len(path_list) == 2 else path_list[2]
        return None, None
