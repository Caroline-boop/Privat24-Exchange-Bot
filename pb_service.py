import requests
import json


class PBService:
    API_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

    def get_exchanges(self):
        return json.loads(requests.get(self.API_URL).text)

    def get_exchange_by_currency(self, currency):
        for exchange in self.get_exchanges():
            if exchange['ccy'] == currency:
                return exchange

        return None
