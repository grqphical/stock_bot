from stock_bot.fetcher import Stock



def test_retrieval():
    stock = Stock("MSFT")

    assert stock.currency == "USD"
    assert stock.symbol == "MSFT"
    
def test_non_existent():
    stock = Stock("FAKE")

    assert stock.exists == False