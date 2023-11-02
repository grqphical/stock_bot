from .fetcher import get_stock_page
from bs4 import BeautifulSoup

class Stock:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

        data, success = get_stock_page(self.symbol)
        if not success:
            self.price = None
            self.point_change = None
            self.percent_change = None
            return

        soup = BeautifulSoup(data, 'html.parser')

        tickers = soup.select("fin-streamer")
        valid_tickers = []

        for ticker in tickers:
            if ticker.attrs.get("data-symbol", "") == self.symbol:
                valid_tickers.append(ticker)
        
        price = valid_tickers[0].contents
        point_change = valid_tickers[1].find("span").contents
        percent_change = valid_tickers[2].find("span").contents

        self.price = float(price[0])
        self.point_change = point_change[0]
        self.percent_change = percent_change[0].replace("(", "").replace(")", "")
