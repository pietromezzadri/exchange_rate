from django.test import TestCase, Client
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .forms import QueryForm
from .utils.response_parser import ResponseParser
from .utils.converter import Converter
from decimal import Decimal
import json


class MockResponse:
    text = '''{
            "date": "2020-04-03",
            "base": "USD",
            "rates": {
                "EUR": 0.9272137227630969,
                "USD": 1,
                "JPY": 108.57672693555864,
                "BGN": 1.813444598980065,
                "CZK": 25.534538711172928,
                "DKK": 6.925266573945294,
                "GBP": 0.8145572554473806,
                "HUF": 338.5720908669448,
                "PLN": 4.243393602225313,
                "RON": 4.479091330551692,
                "SEK": 10.154844691701436,
                "CHF": 0.9779323133982383,
                "ISK": 144.36717663421416,
                "NOK": 10.443022716736207,
                "HRK": 7.074640704682429,
                "RUB": 76.78025034770515,
                "TRY": 6.703384330088085,
                "AUD": 1.6693555864626797,
                "BRL": 5.275197032916087,
                "CAD": 1.4185442744552619,
                "CNY": 7.09095966620306,
                "HKD": 7.753824756606399,
                "IDR": 16614.44598980065,
                "ILS": 3.6408901251738524,
                "INR": 76.23180343069076,
                "KRW": 1235.8089939731108,
                "MXN": 24.614742698191932,
                "MYR": 4.358460825220213,
                "NZD": 1.7082058414464534,
                "PHP": 50.815948076031525,
                "SGD": 1.4361613351877607,
                "THB": 33.009735744089014,
                "ZAR": 18.789244320815946
            }
            }'''


class ExchageRateTestCase(TestCase):
    def setUp(self):
        ExchangeRate.objects.create(base_currency='USD', rate_date='2023-03-16',
                                    brl_rate='5.28598395469561', eur_rate='0.9438414346389804', jpy_rate='132.3076923076923')
        ExchangeRate.objects.create(base_currency='USD', rate_date='2023-03-17',
                                    brl_rate='5.135683153306804', eur_rate='0.9475080538184576', jpy_rate='136.27060830017055')
        ExchangeRate.objects.create(base_currency='USD', rate_date='2023-03-18',
                                    brl_rate='5.135683153306804', eur_rate='0.9475080538184576', jpy_rate='136.27060830017055')

    def test_can_query_per_date(self):
        rate = ExchangeRate.objects.filter(rate_date='2023-03-16').first()
        self.assertEqual(rate.brl_rate, Decimal('5.28598395469561'))

    def test_can_query_date_range(self):
        date_range = {'initial_date': '2023-03-16', 'final_date': '2023-03-18'}
        rates = ExchangeRate.objects.filter(
            rate_date__range=[date_range['initial_date'], date_range['final_date']])
        self.assertEqual(len(rates), 3)

    def test_response_parser(self):
        example_response = MockResponse()
        response_parser = ResponseParser()
        response_parser.parse_response(example_response)
        self.assertTrue('base_currency' in response_parser.exchange_rate)
        self.assertTrue('rate_date' in response_parser.exchange_rate)
        self.assertTrue('brl_rate' in response_parser.exchange_rate)
        self.assertTrue('eur_rate' in response_parser.exchange_rate)
        self.assertTrue('jpy_rate' in response_parser.exchange_rate)
        serializer = ExchangeRateSerializer(data=response_parser.exchange_rate)
        self.assertTrue(serializer.is_valid())

    def test_exchange_rate_by_date(self):
        client = Client()
        response = client.get('/api/exchange_rate/?date=2023-03-16')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'USD')
