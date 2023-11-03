import yfinance as yf
import matplotlib.pyplot as plt
import pandas
import mplcyberpunk
import pandas
from matplotlib.dates import DateFormatter
from PIL import Image
import io

def get_chart_img(symbol: str) -> io.BytesIO:
    ticker = yf.Ticker(symbol)

    history = ticker.history(period="1d", interval="2m")

    data: pandas.DataFrame = history['Close']

    dates = data.index.values

    plt.style.use("cyberpunk")
        
    plt.figure(figsize=(10, 6))
    plt.plot(dates, data.values, color="#00FFFF")
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    mplcyberpunk.add_glow_effects()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='PNG')
    buffer.seek(0)
    return buffer
