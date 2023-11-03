import requests
import urllib

class Stock:
    """Creates a new stock object
    
    :param symbol: the stock symbol to gather data from
    :type symbol: str
    """
    def __init__(self, symbol) -> None:
        info = Ticker(symbol).info

        if info == None:
            self.not_found = True
            return

        self.symbol = symbol
        self.price = info["currentPrice"]
        self.last_close = info["previousClose"]
        self.open = info["open"]
        self._point_change = self.price - self.last_close
        self.currency = info["currency"]
        self._percent_change = (self._point_change / self.price) * 100

        self.not_found = False
    
    @property
    def percent_change(self):
        if self._percent_change < 0:
            return f"-{self._percent_change:.2f} %"
        else:
            return f"+{self._percent_change:.2f} %"
    
    @property
    def point_change(self):
        if self._point_change < 0:
            return f"-{self._point_change:.2f}"
        else:
            return f"+{self._point_change:.2f}"
        

class Ticker:
    user_agent_key = "User-Agent"
    user_agent_value = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/58.0.3029.110 Safari/537.36")
    
    def __init__(self, ticker):
        self.yahoo_ticker = ticker

    def __str__(self):
        return self.yahoo_ticker

    def _get_yahoo_cookie(self):
        cookie = None

        headers = {self.user_agent_key: self.user_agent_value}
        response = requests.get("https://fc.yahoo.com",
                                headers=headers,
                                allow_redirects=True)

        if not response.cookies:
            raise Exception("Failed to obtain Yahoo auth cookie.")

        cookie = list(response.cookies)[0]

        return cookie

    def _get_yahoo_crumb(self, cookie):
        crumb = None

        headers = {self.user_agent_key: self.user_agent_value}

        crumb_response = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=headers,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
        )
        crumb = crumb_response.text

        if crumb is None:
            raise Exception("Failed to retrieve Yahoo crumb.")

        return crumb

    @property
    def info(self):
        # Yahoo modules doc informations :
        # https://cryptocointracker.com/yahoo-finance/yahoo-finance-api
        cookie = self._get_yahoo_cookie()
        crumb = self._get_yahoo_crumb(cookie)
        info = {}
        ret = {}

        headers = {self.user_agent_key: self.user_agent_value}

        yahoo_modules = ("summaryDetail,"
                         "financialData,"
                         "indexTrend,"
                         "defaultKeyStatistics")

        url = ("https://query1.finance.yahoo.com/v10/finance/"
               f"quoteSummary/{self.yahoo_ticker}"
               f"?modules={urllib.parse.quote_plus(yahoo_modules)}"
               f"&ssl=true&crumb={urllib.parse.quote_plus(crumb)}")

        info_response = requests.get(url,
                                     headers=headers,
                                     cookies={cookie.name: cookie.value},
                                     allow_redirects=True)
        
        if not info_response.ok:
            return None

        info = info_response.json()
        info = info['quoteSummary']['result'][0]

        for mainKeys in info.keys():
            for key in info[mainKeys].keys():
                if isinstance(info[mainKeys][key], dict):
                    try:
                        ret[key] = info[mainKeys][key]['raw']
                    except (KeyError, TypeError):
                        pass
                else:
                    ret[key] = info[mainKeys][key]

        return ret

