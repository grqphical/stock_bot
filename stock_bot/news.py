import yfinance as yf
import datetime

class Story:
    def __init__(self, title, publisher, url, timestamp) -> None:
        self.title = title
        self.publisher = publisher
        self.url = url
        self._publish_date = datetime.datetime.fromtimestamp(timestamp)
    
    @property
    def publish_date(self) -> str:
        return self._publish_date.strftime("%d/%m/%Y")

class News:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.stories = []

        ticker = yf.Ticker(symbol)
        news = ticker.news

        for story in news:
            story_obj = Story(story["title"], story["publisher"], story["link"], story["providerPublishTime"])
            self.stories.append(story_obj)