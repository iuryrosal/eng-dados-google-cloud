import requests


class APIFreeCurrency:
    def __init__(self, token) -> None:
        self.token = token
        self.url_base = "https://api.freecurrencyapi.com/v1/"

    def _add_token(self, url):
        return url + f"?apikey={self.token}"

    def _make_request(self, url, method):
        try:
            response = requests.request(method=method,
                                        url=url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            print("Http Error:", error)
        except requests.exceptions.ConnectionError as error:
            print("Error Connecting:", error)
        except requests.exceptions.Timeout as error:
            print("Timeout Error:", error)
        except requests.exceptions.RequestException as error:
            print("OOps: Something Else", error)

    def get_currencies(self):
        url = self.url_base + "currencies"
        url = self._add_token(url)
        return self._make_request(url, method="get")

    def get_latest_exchange_rates(self, base_currency=None):
        url = self.url_base + "latest"
        url = self._add_token(url)
        if base_currency:
            url += f"&base_currency={base_currency}"
        return self._make_request(url, method="get")
