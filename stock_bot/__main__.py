from .fetcher import Stock
from .embeds import *
from .watchlist import *
from .news import *
from .prices import *
from .logging import setup_logger
import discord
from discord import app_commands
from dotenv import load_dotenv
import os

# Load the token from the .env file
load_dotenv()

# Setup the discord bot and the discord.py logger and the StockCord logger
setup_logger("discord")
logger = logger = setup_logger("StockCord")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

watchlists = Watchlists()

@client.event
async def on_ready():
    await tree.sync()
    logger.info(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Markets 📈"))

"""Gets information about a given stock but if that stock doesn't exist it will send an error instead

Args:
    interaction (discord.Interaction): Discord API Interaction
    symbol (str): The stock to lookup
"""
@tree.command(name="stock", description="Gets stats for a given stock")
@app_commands.describe(symbol="Stock to lookup")
async def get_stock(interaction: discord.Interaction, symbol: str):
    stock = Stock(symbol)
    if stock == None:
        await interaction.response.send_message(embed=error_embed("Stock Not Found", f"Stock with symbol '{symbol}' not found. \
                                                                  Try putting the exchange after the stock if it's a foreign stock. \
                                                                  For example AC on the TSX would be AC.TO"))
        return

    await interaction.response.send_message(embed=stock_embed(stock))
"""Adds a stock to the server's watchlist. If the stock doesn't exist, send the user an error message

Args:
    interaction (discord.Interaction): Discord API Interaction
    symbol (str): The stock to add
"""
@tree.command(name="addtowatchlist", description="Adds a stock to the watchlist")
@app_commands.describe(symbol="Stock to add")
async def get_stock(interaction: discord.Interaction, symbol: str):
    stock = Stock(symbol)
    if stock == None:
        await interaction.response.send_message(embed=error_embed("Stock Not Found", f"Stock with symbol '{symbol}' not found. \
                                                                  Try putting the exchange after the stock if it's a foreign stock. \
                                                                  For example AC on the TSX would be AC.TO"))
        return

    error = watchlists.add_to_list(stock.symbol, interaction.guild_id)
    if error != None:
        await interaction.response.send_message(embed=error_embed("Error adding to watchlist", error.message))
    watchlists.save()

    await interaction.response.send_message(embed=info_embed("Added", f"Added '{symbol}' to watchlist"))

"""Removes a stock from the server's watchlist

Args:
    interaction (discord.Interaction): Discord API Interaction
    symbol (str): The stock to lookup
"""
@tree.command(name="removefromwatchlist", description="Remove a stock from the watchlist")
@app_commands.describe(symbol="Stock to remove")
async def get_stock(interaction: discord.Interaction, symbol: str):
    if symbol not in watchlists.lists[str(interaction.guild_id)]:
        await interaction.response.send_message(embed=error_embed("Watchlist Removal Error", f"{symbol} not in watchlist"))
        return
    
    watchlists.remove_from_list(symbol, interaction.guild_id)
    watchlists.save()
    await interaction.response.send_message(embed=info_embed("Removed", f"{symbol} Removed from watchlist"))

"""Gets news from Yahoo Finance about a stock

Args:
    interaction (discord.Interaction): Discord API Interaction
    symbol (str): The stock to lookup
"""
@tree.command(name="news", description="Gets news stories for a certain stock")
@app_commands.describe(symbol="Stock to get news for")
async def get_news(interaction: discord.Interaction, symbol: str):
    news = News(symbol)

    if news == None:
        await interaction.response.send_message(embed=error_embed(error_embed("Stock Not Found", f"Stock with symbol '{symbol}' not found. \
                                                                  Try putting the exchange after the stock if it's a foreign stock. \
                                                                  For example AC on the TSX would be AC.TO")))
        return

    await interaction.response.send_message(embed=news_embed(news))

"""Charts a stock's price history over the past day

Args:
    interaction (discord.Interaction): Discord API Interaction
    symbol (str): The stock to lookup
"""
@tree.command(name="chart", description="Shows a chart of the daily history of a stock")
@app_commands.describe(symbol="Stock to get chart for")
async def get_chart(interacton: discord.Interaction, symbol: str):
    await interacton.response.defer()
    img = get_chart_img(symbol)
    await interacton.followup.send(file=discord.File(fp=img, filename='chart.png'), embed=chart_embed(symbol), ephemeral=True)

"""Sends the server's watchlist

Args:
    interaction (discord.Interaction): Discord API Interaction
"""
@tree.command(name="watchlist", description="Gets the current watchlist")
async def watchlist(interaction: discord.Interaction):
    current_watchlist = watchlists.lists[str(interaction.guild_id)]
    if len(current_watchlist) <= 8:
        await interaction.response.send_message(embed=watchlist_embed(current_watchlist, 1))
    else:
        view = WatchlistView(watchlists, interaction.guild_id)
        await interaction.response.send_message(embed=await view.get_current_page(), view=view)

# Run the bot using the token defined in a .ENV file
client.run(os.getenv("TOKEN"), log_handler=None)