from typing import Union
from .embeds import watchlist_embed
from .logging import setup_logger
import json
import os
import logging
import discord

WATCHLIST_FILE = "watchlists.json"

"""Splits a list into even chunks"""
def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

class WatchlistError:
    def __init__(self, message: str) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.message}"

"""Represents all the watchlists in the bot"""
class Watchlists:
    def __init__(self) -> None:
        # Check if the bot already has data on the disk and if so load it
        if os.path.exists(WATCHLIST_FILE) and os.path.getsize(WATCHLIST_FILE) > 0:
            with open(WATCHLIST_FILE, "r") as f:
                try:
                    self.lists = json.load(f)
                except:
                    self.lists = {}
                    logger = logging.getLogger('discord')
                    logger.warning("Unable to read JSON file")
        else:
            # Otherwise start from scratch
            self.lists = {}
    """Adds a list for a server
    
    Args:
        id (int): Server ID"""
    def create_list(self, id: int):
        self.lists[str(id)] = []
    
    """Adds a symbol to the server's watchlist
    
    Args:
        symbol (str): Stock to add
        id (int): Server ID
    
    Returns:
        Union[WatchlistError, None]: Returns an error if one occured otherwise nothing gets returned"""
    def add_to_list(self, symbol: str, id: int) -> Union[WatchlistError, None]:        
        if symbol in self.lists.get(str(id), []):
            return WatchlistError("Stock already in watchlist")
        
        if self.lists.get(str(id), []) == []:
            self.lists[str(id)] = []

        if len(self.lists.get(str(id), [])) == 25:
            return WatchlistError("WatchList Full")
        
        self.lists[str(id)].append(symbol)
    
    """Removes a symbol from the server's list
    
    Args:
        symbol (str): Stock to remove
        id (int): Server ID"""
    def remove_from_list(self, symbol: str, id: int):
        self.lists[str(id)].remove(symbol)
    
    """Saves the watchlists to disk"""
    def save(self):
        logger = setup_logger("StockCord")
        with open(WATCHLIST_FILE, "w") as f:
            f.write(json.dumps(self.lists))
        
        logger.info("Saved watchlists to disk")

"""View used to add pagination to watchlist embed"""
class WatchlistView(discord.ui.View):
    def __init__(self, watchlists: Watchlists, id: int):
        super().__init__()
        # Split the watchlist into chunks of 8 (3 fields per stock, 25 max fields on embed means we can have at most 8 stocks on a page)
        self.watchlist = list(split(watchlists.lists.get(str(id), []), 8))
        self.current_page = 0
        self.total_pages = len(self.watchlist)
        self.current_page_data = self.watchlist[self.current_page]
    
    """Gets the embed for the current page"""
    async def get_current_page(self) -> discord.Embed:
        return watchlist_embed(self.current_page_data, self.current_page + 1)
    
    """Updates the message to the current page"""
    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.watchlist[self.current_page]
        await interaction.response.edit_message(embed=await self.get_current_page(), view=self)
    
    """Button used to go back a page"""
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(view=self, embed=await self.get_current_page())
            return
        
        # If the user is not at the beginning, decrease the page count by 1
        if self.current_page > 0:
            self.current_page -= 1
        
        # Finally update the page
        await self.update_page(interaction)
    
    """Button used to go forward a page"""
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # If we only have one page just set the pages contents to be the same as we don't need to change them
        if self.total_pages == 1:
            await interaction.response.edit_message(view=self, embed=await self.get_current_page())
            return
        
        # If the user is not at the end, increase the page count by 1
        if self.current_page < self.total_pages:
            self.current_page += 1
        
        # Finally update the page
        await self.update_page(interaction)
    
    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)
        
