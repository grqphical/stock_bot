from stock_bot.watchlist import Watchlists, WATCHLIST_FILE


watchlists = Watchlists()

def test_addition_to_list():
    watchlists.create_list(1)

    watchlists.add_to_list("MSFT", 1)

    assert watchlists.lists["1"][0] == "MSFT"

def test_removal_from_list():
    watchlists.remove_from_list("MSFT", 1)

    assert len(watchlists.lists["1"]) == 0

def test_saving():
    watchlists.add_to_list("MSFT", 1)

    watchlists.save()

    with open(WATCHLIST_FILE, "r") as f:
        data = f.read()
    
    assert data == '{"1": ["MSFT"]}'