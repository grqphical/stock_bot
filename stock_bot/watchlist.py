from typing import Union
import json
import os
import logging

class WatchlistError:
    def __init__(self, message: str) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.message}"

class Watchlists:
    def __init__(self) -> None:
        if os.path.exists("watchlists.json") and os.path.getsize("watchlists.json") > 0:
            with open("watchlists.json", "r") as f:
                try:
                    self.lists = json.load(f)
                except:
                    self.lists = {}
                    logger = logging.getLogger('discord')
                    logger.warning("Unable to read JSON file")
        else:
            self.lists = {}
    
    def create_list(self, id: int):
        self.lists[str(id)] = []
    
    def add_to_list(self, symbol: str, id: int) -> Union[WatchlistError, None]:        
        if symbol in self.lists.get(str(id), []):
            return WatchlistError("Stock already in watchlist")
        
        if self.lists.get(str(id), []) == []:
            self.lists[str(id)] = []

        if len(self.lists.get(str(id), [])) == 25:
            return WatchlistError("WatchList Full")
        
        self.lists[str(id)].append(symbol)
        return None
    
    def remove_from_list(self, symbol: str):
        self.lists[str(id)].remove(symbol)
    
    def save(self):
        with open("watchlists.json", "w") as f:
            f.write(json.dumps(self.lists))