from typing import Union
from .embeds import watchlist_embed
import json
import os
import logging
import discord
import math

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

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
    
    def remove_from_list(self, symbol: str, id: int):
        self.lists[str(id)].remove(symbol)
    
    def save(self):
        with open("watchlists.json", "w") as f:
            f.write(json.dumps(self.lists))

class WatchlistView(discord.ui.View):
    def __init__(self, watchlists: Watchlists, id: int):
        super().__init__()
        self.watchlist = list(split(watchlists.lists.get(str(id), []), 8))
        self.current_page = 0
        self.total_pages = len(self.watchlist)
        self.current_page_data = self.watchlist[self.current_page]
    
    async def get_current_page(self) -> discord.Embed:
        return watchlist_embed(self.current_page_data, self.current_page + 1)
    
    async def update_page(self, interaction: discord.Interaction):
        self.current_page_data = self.watchlist[self.current_page]
        await interaction.response.edit_message(embed=await self.get_current_page(), view=self)
    
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.total_pages == 1:
            await interaction.response.edit_message(view=self, embed=await self.get_current_page())
            return
        
        if self.current_page > 0:
            self.current_page -= 1
        
        await self.update_page(interaction)
    
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.total_pages == 1:
            await interaction.response.edit_message(view=self, embed=await self.get_current_page())
            return
        
        if self.current_page < self.total_pages:
            self.current_page += 1
        
        await self.update_page(interaction)
    
    async def on_timeout(self):
        # remove buttons on timeout
        message = await self.interaction.original_response()
        await message.edit(view=None)
        
