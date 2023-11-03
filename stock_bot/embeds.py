import discord
from .fetcher import Stock
from .news import News
import io

def stock_embed(stock: Stock) -> discord.Embed:
    embed = discord.Embed(title=f"Stock Result for {stock.symbol}", url=f"https://finance.yahoo.com/quote/{stock.symbol}", color=discord.Color.blue())
    embed.add_field(name="Price", value=f"```fix\n${stock.price} {stock.currency}```")
    embed.add_field(name="Point Change", value=f"```diff\n{stock.point_change}```")
    embed.add_field(name="Percent Change", value=f"```diff\n{stock.percent_change}```")
    embed.add_field(name="Previous Close Price", value=f"```fix\n${stock.last_close:.2f} {stock.currency}```")
    embed.add_field(name="Open Price", value=f"```fix\n${stock.open:.2f} {stock.currency}```")

    return embed

def watchlist_embed(watchlist: list) -> discord.Embed:
    embed = discord.Embed(title=f"Watchlist", color=discord.Color.blue())
    for symbol in watchlist:
        stock = Stock(symbol)
        embed.add_field(name=f"**{symbol}:** Price", value=f"```fix\n${stock.price}```")
        embed.add_field(name=f"Point Change", value=f"```diff\n{stock.point_change}```")
        embed.add_field(name=f"Percent Change", value=f"```diff\n{stock.percent_change}```")
    
    return embed

def news_embed(news: News) -> discord.Embed:
    embed = discord.Embed(title=f"News for {news.symbol}", color=discord.Color.blue())

    for story in news.stories:
        embed.add_field(name=f"**'{story.title}'** by *{story.publisher}*. *{story.publish_date}*", value=f"[Read More]({story.url})", inline=False)
    
    return embed

def chart_embed(symbol: str) -> discord.Embed:
    embed = discord.Embed(title=f"Chart for {symbol}", color=discord.Color.blue())
    embed.set_image(url="attachment://chart.png")

    return embed

def error_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(title=f"{title}", color=discord.Color.red())
    embed.description = f"❌ {message}"
    return embed

def info_embed(title: str, message: str) -> discord.Embed:
    embed = discord.Embed(title=f"{title}", color=discord.Color.blue())
    embed.description = f"ℹ️ {message}"
    return embed