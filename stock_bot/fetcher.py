from typing import Union
import requests

def get_stock_page(symbol: str) -> Union[str, bool]:
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}")
    if not response.ok:
        return "", False
    return response.text, True
