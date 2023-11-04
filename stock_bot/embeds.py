"""Embed builder functions to be used by the bot"""
import discord
from .fetcher import Stock
from .news import News

"""Generates an embed for a stock with important price information such as current price, point change and percent change since last close price

Args:
    stock (Stock): The stock to generate the embed from

Returns:
    Embed: The embed to send on Discord
"""
def stock_embed(stock: Stock) -> discord.Embed:
    embed = discord.Embed(title=f"Stock Result for {stock.symbol}", url=f"https://finance.yahoo.com/quote/{stock.symbol}", color=discord.Color.blue())
    embed.add_field(name="Price", value=f"```fix\n${stock.price} {stock.currency}```")
    embed.add_field(name="Point Change", value=f"```diff\n{stock.point_change}```")
    embed.add_field(name="Percent Change", value=f"```diff\n{stock.percent_change}```")
    embed.add_field(name="Previous Close Price", value=f"```fix\n${stock.last_close:.2f} {stock.currency}```")
    embed.add_field(name="Open Price", value=f"```fix\n${stock.open:.2f} {stock.currency}```")

    return embed

"""Generates an embed for a stock with important price information such as current price, point change and percent change since last close price

Args:
    stock (Stock): The stock to generate the embed from

Returns:
    Embed: The embed to send on Discord
"""
def watchlist_embed(watchlist: list[str], page: int) -> discord.Embed:
    embed = discord.Embed(title=f"Watchlist Page {page}", color=discord.Color.blue())
    for symbol in watchlist:
        stock = Stock(symbol)
        embed.add_field(name=f"**{symbol}:** Price", value=f"```fix\n${stock.price}```")
        embed.add_field(name=f"Point Change", value=f"```diff\n{stock.point_change}```")
        embed.add_field(name=f"Percent Change", value=f"```diff\n{stock.percent_change}```")
    
    return embed

"""Generates an embed for a stock's news, gathered from Yahoo Finance. The embed has fields with the name of the article, the publisher and the release date with the url being
in the value of the field

Args:
    news (News): The news gathered about a stock

Returns:
    Embed: The embed to send on Discord
"""
def news_embed(news: News) -> discord.Embed:
    embed = discord.Embed(title=f"News for {news.symbol}", color=discord.Color.blue())

    for story in news.stories:
        embed.add_field(name=f"**'{story.title}'** by *{story.publisher}*. *{story.publish_date}*", value=f"[Read More]({story.url})", inline=False)
    
    return embed

"""Charts a stock and sends an embed with the chart embedded as an image inside of it

Args:
    symbol (str): The symbol that has been charted

Returns:
    Embed: The embed to send on Discord
"""
def chart_embed(symbol: str) -> discord.Embed:
    embed = discord.Embed(title=f"Chart for {symbol}", color=discord.Color.blue())
    embed.set_image(url="attachment://chart.png")

    return embed

"""A generic error embed

Args:
    title (str): Title of the error embed
    message (str): Additional info about the error

Returns:
    Embed: The embed to send on Discord
"""
def error_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(title=f"{title}", color=discord.Color.red())
    embed.description = f"❌ {message}"
    return embed

"""A generic embed

Args:
    title (str): Title of the embed
    message (str): Additional info

Returns:
    Embed: The embed to send on Discord
"""
def info_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(title=f"{title}", color=discord.Color.blue())
    embed.description = f"ℹ️ {message}"
    return embed