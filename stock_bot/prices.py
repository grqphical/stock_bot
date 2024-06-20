import yfinance as yf
import matplotlib.pyplot as plt
import pandas
import mplcyberpunk
import pandas
from matplotlib.dates import DateFormatter, MinuteLocator
from matplotlib.ticker import FuncFormatter
from .fetcher import Stock
import io
import datetime

"""Formats a float as a dollar value. Example: 8.6512753 => $8.65"""
def dollar_format(x: float, pos) -> str:
    return "${:.2f}".format(x)

"""Charts a stock and returns a bytes buffer of the image data

Args:
    symbol (str): Stock to chart

Returns:
    io.BytesIO: buffer of image data to be sent over Discord
"""
def get_chart_img(symbol: str) -> io.BytesIO:
    today = datetime.datetime.today()

    # Set the start date to today's market open (9:30 AM) and download the data
    start_date = today.replace(hour=9, minute=30, second=0, microsecond=0)
    history = yf.download(symbol, period="1d", interval="1m", start=start_date)
    stock = Stock(symbol)
    change = stock._point_change

    # We only want the close price
    data: pandas.DataFrame = history['Close']
    data.asfreq('D')

    dates = data.index

    # Style the plot
    plt.style.use("cyberpunk")
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=24)

    # Make the colour red if the change in price is negative, green if it is positive
    if change < 0:
        colour = "#FF0000"
    else:
        colour = "#00FF00"
        
    plt.figure(figsize=(35, 14))
    plt.title(f"Today's Price Change for {symbol} ({stock.currency})", fontdict={'fontsize': 64})
    plt.plot(dates, data.values, color=colour)
    plt.gca().xaxis.set_major_locator(MinuteLocator(byminute=[0, 30]))
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(dollar_format))
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S', tz="Eastern Standard Time"))
    plt.xticks(rotation=45)
    
    mplcyberpunk.add_glow_effects()

    # Save the data as a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='PNG', transparent=True)
    buffer.seek(0)
    return buffer
