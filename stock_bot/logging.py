import logging
from logging.handlers import TimedRotatingFileHandler

"""Creates/gets a logger and changes it so it shows all logs at the info level and formats it nicely"""
def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler =TimedRotatingFileHandler(
        filename="logs/discord.log",
        encoding="utf-8",
        interval=1,
        when="D",
        backupCount=5
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(f'[{{asctime}}] [{{levelname}}] {{name}}: {{message}}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger