"""All Bot Callbacks"""
import vt

from telegram import Update
from telegram.ext import ContextTypes

from virus_total_telegram_bot.utils import (
    request_arrived,
    parse_url_info,
)
from virus_total_telegram_bot.strings import dialogs, ENGLISH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Callback for the /start command.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    """
    request_arrived(update, context, command="/start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['start'][ENGLISH])


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE, client: vt.Client):
    """
    Callback for the text messages received by the bot.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - client: vt.Client object
    """
    request_arrived(update, context, command="text")
    text_received = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['analyzing'][ENGLISH])
    try:
        analysis = await client.scan_url_async(text_received, wait_for_completion=True)
    except vt.error.APIError as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['error'][ENGLISH])
        return
    url_info = parse_url_info(analysis)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogs['text_received']['results'][ENGLISH] % text_received)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=url_info, parse_mode='Markdown')


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE, client: vt.Client):
    """
    Callback for the files received by the bot.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - client: vt.Client object
    """
    request_arrived(update, context, command="file")
    # get the file received from the user
    file_received = update.message.document
    # send the file back to the user
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file_received.file_id)
