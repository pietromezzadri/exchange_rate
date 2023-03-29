import requests


class VatService:
    def __init__(self):
        pass

    def get_usd(self):
        return requests.get("https://api.vatcomply.com/rates?base=USD")
