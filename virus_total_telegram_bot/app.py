"""Entrypoint of the app"""
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from virus_total_telegram_bot.entities import Config
from virus_total_telegram_bot.callbacks import (
    start,
    text,
    file
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
    text_handler = MessageHandler(filters.TEXT, text)
    file_handler = MessageHandler(filters.Document.ALL, file)

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(file_handler)

    application.run_polling()
