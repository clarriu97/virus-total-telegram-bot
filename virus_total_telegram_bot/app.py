"""Entrypoint of the app"""
from functools import partial

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from virus_total_telegram_bot.entities import Config
from virus_total_telegram_bot.callbacks import (
    start,
    bot_help,
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

    start_handler = CommandHandler('start', partial(start, files_max_size=cfg.files_max_size))
    help_handler = CommandHandler('help', partial(bot_help, files_max_size=cfg.files_max_size))
    text_handler = MessageHandler(filters.TEXT, partial(text, cfg=cfg))
    file_handler = MessageHandler(filters.Document.ALL, partial(file, cfg=cfg))

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(text_handler)
    application.add_handler(file_handler)

    application.run_polling()
