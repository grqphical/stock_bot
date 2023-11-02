from .scraper import *
from .embeds import *
from .watchlist import *
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import logging
import colorama

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
    if stock.price is None:
        await interaction.response.send_message(f"Stock not found")
        return

    await interaction.response.send_message(embed=stock_embed(stock))

@tree.command(name="addtowatchlist", description="Adds a stock to the watchlist", guild=discord.Object(id=1061783393718784020))
@app_commands.describe(symbol="Stock to add")
async def get_stock(interaction: discord.Interaction, symbol: str):
    stock = Stock(symbol)
    if stock.price is None:
        await interaction.response.send_message(f"Stock not found")
        return

    error = watchlists.add_to_list(stock.symbol, interaction.guild_id)
    if error != None:
        await interaction.response.send_message(error.message)
    watchlists.save()

    await interaction.response.send_message("Added to watchlist")

@tree.command(name="watchlist", description="Gets the current watchlist", guild=discord.Object(id=1061783393718784020))
async def get_stock(interaction: discord.Interaction):
    embed = watchlist_embed(watchlists.lists.get(str(interaction.guild_id), []))
    await interaction.response.send_message(embed=embed)

client.run(os.getenv("TOKEN"), log_handler=None)