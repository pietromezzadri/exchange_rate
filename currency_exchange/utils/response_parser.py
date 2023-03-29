import json


class ResponseParser:
    exchange_rate = {
        'base_currency': '',
        'brl_rate': '',
        'eur_rate': '',
        'jpy_rate': '',
        'rate_date': '',
    }

    def parse_response(self, response):
        raw_exchange_rate = json.loads(response.text)
        self.exchange_rate['base_currency'] = raw_exchange_rate['base']
        self.exchange_rate['brl_rate'] = raw_exchange_rate['rates']['BRL']
        self.exchange_rate['eur_rate'] = raw_exchange_rate['rates']['EUR']
        self.exchange_rate['jpy_rate'] = raw_exchange_rate['rates']['JPY']
        self.exchange_rate['rate_date'] = raw_exchange_rate['date']
