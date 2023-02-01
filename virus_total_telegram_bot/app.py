"""Entrypoint of the app"""
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from virus_total_telegram_bot.entities import Config
from virus_total_telegram_bot.callbacks import (
    start
)


def run(cfg: Config):
    """
    Entrypoint of the service.

    Parameters:
    -----------
    - cfg: virus_total_telegram_bot.entities.Config
        The Config instance for the service.
    """
    application = ApplicationBuilder().token(cfg.bot_apikey).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
