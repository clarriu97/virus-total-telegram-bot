"""All Bot Callbacks"""
import vt

from telegram import Update
from telegram.ext import ContextTypes

from virus_total_telegram_bot.utils import (
    request_arrived,
    check_url
)
from virus_total_telegram_bot.strings import dialogs, ENGLISH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_arrived(update, context, command="/start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['start'][ENGLISH])


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE, client: vt.Client):
    request_arrived(update, context, command="text")
    text_received = update.message.text
    if check_url(text_received):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['is_url'][ENGLISH])
        analysis = await client.scan_url_async(text_received, wait_for_completion=True)
        print(analysis.to_dict())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['is_not_url'][ENGLISH])
    # send the text back to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_received)


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE, client: vt.Client):
    request_arrived(update, context, command="file")
    # get the file received from the user
    file_received = update.message.document
    # send the file back to the user
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file_received.file_id)
