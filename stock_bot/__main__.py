from .fetcher import Stock
from .embeds import *
from .watchlist import *
from .news import *
from .prices import *
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import logging
import colorama
import io
from PIL import Image

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(f'[{{asctime}}] [{{levelname}}] {colorama.Fore.CYAN}{{name}}{colorama.Fore.RESET}: {{message}}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

watchlists = Watchlists()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1061783393718784020))
    logger.info(f"Logged in as {client.user}")

@tree.command(name="stock", description="Gets stats for a given stock", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to lookup")
async def get_stock(interaction: discord.Interaction, symbol: str):
    stock = Stock(symbol)
    if stock.not_found:
        await interaction.response.send_message(embed=error_embed("Stock Not Found", f"Stock with symbol '{symbol}' not found. \
                                                                  Try putting the exchange after the stock if it's a foreign stock. \
                                                                  For example AC on the TSX would be AC.TO"))
        return

    await interaction.response.send_message(embed=stock_embed(stock))

@tree.command(name="addtowatchlist", description="Adds a stock to the watchlist", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to add")
async def get_stock(interaction: discord.Interaction, symbol: str):
    stock = Stock(symbol)
    if stock.not_found:
        await interaction.response.send_message(embed=error_embed("Stock Not Found", f"Stock with symbol '{symbol}' not found. \
                                                                  Try putting the exchange after the stock if it's a foreign stock. \
                                                                  For example AC on the TSX would be AC.TO"))
        return

    error = watchlists.add_to_list(stock.symbol, interaction.guild_id)
    if error != None:
        await interaction.response.send_message(embed=error_embed("Error adding to watchlist", error.message))
    watchlists.save()

    await interaction.response.send_message(embed=info_embed("Added", f"Added '{symbol}' to watchlist"))

@tree.command(name="removefromwatchlist", description="Remove a stock from the watchlist", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to remove")
async def get_stock(interaction: discord.Interaction, symbol: str):
    if symbol not in watchlists.lists[str(interaction.guild_id)]:
        await interaction.response.send_message(embed=error_embed("Watchlist Removal Error", f"{symbol} not in watchlist"))
        return
    
    watchlists.remove_from_list(symbol, interaction.guild_id)
    await interaction.response.send_message(embed=info_embed("Removed", f"{symbol} Removed from watchlist"))

@tree.command(name="news", description="Gets news stories for a certain stock", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to get news for")
async def get_news(interaction: discord.Interaction, symbol: str):
    news = News(symbol)

    await interaction.response.send_message(embed=news_embed(news))

@tree.command(name="chart", description="Shows a chart of the daily history of a stock", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to get chart for")
async def get_chart(interacton: discord.Interaction, symbol: str):
    await interacton.response.defer()
    img = get_chart_img(symbol)
    await interacton.followup.send(file=discord.File(fp=img, filename='chart.png'), embed=chart_embed(symbol), ephemeral=True)

@tree.command(name="watchlist", description="Gets the current watchlist", guild=discord.Object(id=1061783393718784020))
async def watchlist(interaction: discord.Interaction):
    embed = watchlist_embed(watchlists.lists.get(str(interaction.guild_id), []))
    await interaction.response.send_message(embed=embed)

client.run(os.getenv("TOKEN"), log_handler=None)