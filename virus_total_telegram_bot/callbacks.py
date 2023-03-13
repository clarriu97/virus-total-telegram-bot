"""All Bot Callbacks"""
import vt

from telegram import Update
from telegram.ext import ContextTypes

from virus_total_telegram_bot.utils import (
    request_arrived,
    parse_url_info,
    parse_file_info,
    get_file_size_and_sha256
)
from virus_total_telegram_bot.strings import dialogs, ENGLISH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, files_max_size: int):
    """
    Callback for the /start command.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - files_max_size: int
    """
    request_arrived(update, context, command="/start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['start'][ENGLISH] % files_max_size)


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


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE, client: vt.Client, files_max_size: int):
    """
    Callback for the files received by the bot.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - client: vt.Client object
    - files_max_size: int
    """
    request_arrived(update, context, command="file")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['analyzing'][ENGLISH])
    file_id = update.message.document.file_id
    new_file = await context.bot.get_file(file_id)
    file_name = update.message.document.file_name
    await new_file.download_to_drive(file_name)

    file_size, file_hash = get_file_size_and_sha256(file_name)
    if file_size > files_max_size:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['too_big'][ENGLISH] % files_max_size)
        return

    try:
        with open(file_name, 'rb') as f:
            analysis = await client.scan_file_async(f, wait_for_completion=True)
    except vt.error.APIError as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['error'][ENGLISH])
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogs['file_received']['results'][ENGLISH] % file_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=parse_file_info(analysis), parse_mode='Markdown')
