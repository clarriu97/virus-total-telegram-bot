"""All Bot Callbacks"""
from telegram import Update
from telegram.ext import ContextTypes

from virus_total_telegram_bot.utils import (
    request_arrived
)
from virus_total_telegram_bot.strings import dialogs, ENGLISH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_arrived(update, context, command="/start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['start'][ENGLISH])


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_arrived(update, context, command="text")
    # get the text received from the user
    text = update.message.text
    # send the text back to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_arrived(update, context, command="file")
    # get the file received from the user
    file = update.message.document
    # send the file back to the user
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file.file_id)
