# stock_bot

A simple stock tracking bot that allows you to view individual stocks, look at charts of a stock's performance, look at news about a certain stock and, set up a server wide watchlist

## Usage

1. Clone this repo
```bash
$ git clone https://github.com/grqphical07/stock_bot
```

2. Create a discord bot at the [Discord Developer Portal](https://discord.com/developers/applications) and get it's token

3. Create a .env file in the directory you cloned the repo to and add:
```
TOKEN=your_token_here
```
4. Create a venv (or virtualenv) and activate it
```bash
$ python -m venv bot_env
```
5. Install dependencies
```bash
(bot_env) $ pip install -r requirements.txt
```

6. Run the app
```bash
(bot_env) $ python -m stock_bot
```

7. Add the bot to your server and enjoy!
