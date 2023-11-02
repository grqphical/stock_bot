import discord
from .scraper import Stock

def stock_embed(stock: Stock) -> discord.Embed:
    embed = discord.Embed(title=f"Stock Result for {stock.symbol}", url=f"https://finance.yahoo.com/quote/{stock.symbol}", color=discord.Color.blue())
    embed.add_field(name="Price:", value=f"```fix\n${stock.price}```")
    embed.add_field(name="Point Change:", value=f"```diff\n{stock.point_change}```")
    embed.add_field(name="Percent Change:", value=f"```diff\n{stock.percent_change}```")

    return embed

def watchlist_embed(watchlist: list) -> discord.Embed:
    embed = discord.Embed(title=f"Watchlist", color=discord.Color.blue())
    for symbol in watchlist:
        stock = Stock(symbol)
        embed.add_field(name=f"**{symbol}:** Price", value=f"```fix\n${stock.price}```")
        embed.add_field(name=f"Point Change", value=f"```diff\n{stock.point_change}```")
        embed.add_field(name=f"Percent Change", value=f"```diff\n{stock.percent_change}```")
    
    return embed