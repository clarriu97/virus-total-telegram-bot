"""All Bot Callbacks"""
import vt
import structlog
from telegram import Update
from telegram.ext import ContextTypes

from virus_total_telegram_bot.utils import (
    request_arrived,
    request_served,
    parse_url_info,
    parse_file_info,
    get_file_sha256,
    get_user_id,
    get_user_id_artifacts_path,
    add_file_data,
    Results
)
from virus_total_telegram_bot.strings import dialogs, ENGLISH
from virus_total_telegram_bot.entities import Config


logger = structlog.get_logger()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, files_max_size: int):
    """
    Callback for the /start command.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - files_max_size: int
    """
    await bot_help(update, context, files_max_size, command="/start")


async def bot_help(update: Update, context: ContextTypes.DEFAULT_TYPE, files_max_size: int, command: str = "/help"):
    """
    Callback for the /help command.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - files_max_size: int
    - command: str
    """
    request_arrived(update, context, action=command)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['help'][ENGLISH] % files_max_size)
    request_served(update, context, result=Results.SUCCESS)


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE, cfg: Config):
    """
    Callback for the text messages received by the bot.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - cfg: virus_total_telegram_bot.entities.Config object
    """
    request_arrived(update, context, action="text")

    text_received = update.message.text
    logger.info("text_received", text_received=text_received)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['analyzing'][ENGLISH])

    try:
        client = vt.Client(cfg.virus_total_apikey)
        analysis = await client.scan_url_async(text_received, wait_for_completion=True)
    except vt.error.APIError as e:
        logger.error("text_received_analysis", error=e, text_received=text_received)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['text_received']['error'][ENGLISH])
        request_served(update, context, result=Results.ERROR)
        await client.close_async()
        return

    await client.close_async()
    logger.info("text_received_analysis", analysis=analysis.to_dict())
    url_info = parse_url_info(analysis)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogs['text_received']['results'][ENGLISH] % text_received)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=url_info, parse_mode='Markdown')
    request_served(update, context, result=Results.SUCCESS)


async def file(update: Update, context: ContextTypes.DEFAULT_TYPE, cfg: Config):
    """
    Callback for the files received by the bot.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - cfg: virus_total_telegram_bot.entities.Config object
    """
    request_arrived(update, context, action="file")

    file_id = update.message.document.file_id
    new_file = await context.bot.get_file(file_id)
    file_name = update.message.document.file_name
    file_size_in_bytes = update.message.document.file_size
    file_size_in_megabytes = round(file_size_in_bytes / (1024 * 1024), 6)
    if file_size_in_megabytes > cfg.files_max_size:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['too_big'][ENGLISH] % cfg.files_max_size)
        request_served(update, context, result=Results.FILE_TOO_BIG)
        return
    user_id = str(get_user_id(update))
    user_id_artifacts_path = get_user_id_artifacts_path(cfg.artifacts_path, user_id)
    file_path = f"{user_id_artifacts_path}/{file_name}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['downloading'][ENGLISH])
    await new_file.download_to_drive(file_path)
    logger.info("file_received", file_id=file_id, file_name=file_name, file_path=file_path)

    file_sha256 = get_file_sha256(file_path)
    add_file_data(context, file_name, file_size_in_megabytes, file_sha256, file_id)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['analyzing'][ENGLISH])

    try:
        with open(file_path, 'rb') as f:
            client = vt.Client(cfg.virus_total_apikey)
            analysis = await client.scan_file_async(f, wait_for_completion=True)
    except vt.error.APIError as e:
        logger.error("file_received_analysis", error=e, file_path=file_path)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogs['file_received']['error'][ENGLISH])
        request_served(update, context, result=Results.ERROR)
        await client.close_async()
        return

    await client.close_async()
    logger.info("file_received_analysis", analysis=analysis.to_dict())
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogs['file_received']['results'][ENGLISH] % file_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=parse_file_info(analysis), parse_mode='Markdown')
    request_served(update, context, result=Results.SUCCESS)
