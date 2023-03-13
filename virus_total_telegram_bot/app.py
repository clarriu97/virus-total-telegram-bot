"""Entrypoint of the app"""
from functools import partial

import vt
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
    client = vt.Client(cfg.virus_total_apikey)

    start_handler = CommandHandler('start', partial(start, files_max_size=cfg.files_max_size))
    text_handler = MessageHandler(filters.TEXT, partial(text, client=client))
    file_handler = MessageHandler(filters.Document.ALL, partial(file, client=client, files_max_size=cfg.files_max_size))

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(file_handler)

    application.run_polling()
