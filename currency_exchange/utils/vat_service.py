import requests


class VatService:
    def __init__(self):
        pass

    def get_daily(self):
        return requests.get("https://api.vatcomply.com/rates?base=USD")

    def get_by_date(self, date):
        return requests.get(f"https://api.vatcomply.com/rates?base=USD&date={date}")
