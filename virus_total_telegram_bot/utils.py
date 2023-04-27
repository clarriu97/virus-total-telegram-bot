"""
Utils to be used around the bot
"""
import os
import hashlib
import time
import uuid

import structlog
import vt

from telegram import Update
from telegram.ext import CallbackContext

from virus_total_telegram_bot.strings import ENGLISH


logger = structlog.get_logger()


class Results():
    """
    Events to finallize requests
    """
    SUCCESS = "success"
    CANCELLED = "cancelled"
    ERROR = "error"
    FILE_TOO_BIG = "file_too_big"


def get_username(update: Update):
    """
    Get the username from the update object.

    Parameters:
    -----------
    - update: telegram.Update object

    Returns:
    --------
    - username: str
        The username of the user that sent the message.
    """
    try:
        username = update.message.from_user.username
    except AttributeError:
        username = update.callback_query.message.chat.username
    return username


def request_arrived(update: Update, context: CallbackContext, action: str):
    """
    Performs the configuration needed for every request that arrives.

    Parameters:
    -----------
    - update: telegram.Update object
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - action: str
        The action that the user sent to the bot.
    """
    username = get_username(update)
    user_id = get_user_id(update)
    request_id = str(uuid.uuid4())
    context.user_data['request_id'] = request_id
    context.user_data['username'] = username
    context.user_data['id'] = user_id
    add_request_arrived_data(context, action, username, user_id, request_id)
    logger.info("request_arrived", action=action, username=username, user_id=user_id, request_id=request_id)


def get_user_id(update: Update):
    """
    Get the telegram user id from the update object.

    Parameters:
    -----------
    - update: telegram.Update object

    Returns:
    --------
    - user_id: str
        The user id of the user that sent the message.
    """
    try:
        return update.message.from_user.id
    except AttributeError:
        return update.callback_query.message.chat.id


def get_user_language(update: Update):  # pylint: disable=unused-argument
    """
    Get the language in which the user wants to be addressed.

    Parameters:
    -----------
    - update: telegram.Update object

    Returns:
    --------
    - lang: str
        The user id of the user that sent the message.
    """
    lang = ENGLISH
    return lang


def add_request_arrived_data(context: CallbackContext, action: str, username: str, user_id: str, request_id: str):
    """
    Add request arrived data and application metadata to the context.

    Parameters:
    -----------
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - action: str
        The action that the user sent to the bot.
    - username: str
        The username of the user that sent the message.
    - user_id: str
        The telegram id of the user that sent the message.
    """
    context.user_data['event_info'] = {
        "metadata": {
            "service": "virus total telegram bot",
            "integrator": "clarriu97"
        },
        "request": {
            "action": action,
            "username": username,
            "user_id": user_id,
            "result": None,
            "request_id": request_id,
            "start_time": current_milliseconds(),
            "end_time": None,
            "elapsed": None,
        }
    }


def add_file_data(context: CallbackContext, file_name: str, file_size: int, file_hash: str, file_id: str):
    """
    Add file data to the context.

    Parameters:
    -----------
    - context: telegram.ext.ContextTypes.DEFAULT_TYPE object
    - file_name: str
        The name of the file.
    - file_size: int
        The size of the file.
    - file_hash: str
        The hash of the file.
    - file_id: str
        The id that Telegram gives to the file.
    """
    context.user_data['event_info']['file'] = {}
    context.user_data['event_info']['file']['name'] = file_name
    context.user_data['event_info']['file']['size'] = file_size
    context.user_data['event_info']['file']['hash'] = file_hash
    context.user_data['event_info']['file']['id'] = file_id


def current_milliseconds():
    """
    Get the current time in milliseconds.

    Returns:
    --------
    - current_time: int
    """
    return round(time.time() * 1000)


def save_request_data(context: CallbackContext, result: str):
    event_info = get_event_info(context)
    end_time = current_milliseconds()
    event_info['request']['end_time'] = end_time
    elapsed = end_time - event_info['request']['start_time']
    event_info['request']['elapsed'] = elapsed
    event_info['request']['result'] = result


def request_served(update: Update, context: CallbackContext, result: str, save_artifacts: bool = False):  # pylint: disable=unused-argument
    """Request served function"""
    if 'request_id' not in context.user_data:
        logger.warning('request_served_no_request_id')
        return
    request_id = context.user_data['request_id']
    save_request_data(context, result)
    logger.info("request_served", request_id=request_id, user_data=context.user_data)
    clear_user_data(context)


def get_event_info(context: CallbackContext):
    return context.user_data['event_info']


def clear_user_data(context: CallbackContext):
    context.user_data.clear()


def parse_url_info(analysis: vt.object.Object):
    """
    Parse the url info from the analysis object.

    Parameters:
    -----------
    - analysis: vt.object.Object object
        The analysis object returned by the VirusTotal API.

    Returns:
    --------
    - url_info: str
        The url info in a human readable format.
    """
    analysis_dict = analysis.to_dict()
    harmless = analysis_dict['attributes']['stats']['harmless']
    malicious = analysis_dict['attributes']['stats']['malicious']
    suspicious = analysis_dict['attributes']['stats']['suspicious']
    undetected = analysis_dict['attributes']['stats']['undetected']
    url_info = (
        f"🟢 **Harmless**: {harmless}\n"
        f"🔴 **Malicious**: {malicious}\n"
        f"🟡 **Suspicious**: {suspicious}\n"
        f"🟣 **Undetected**: {undetected}\n"
    )
    return url_info


def parse_file_info(analysis: vt.object.Object):
    """
    Parse the file info from the analysis object.

    Parameters:
    -----------
    - analysis: vt.object.Object object
        The analysis object returned by the VirusTotal API.

    Returns:
    --------
    - file_info: str
        The file info in a human readable format.
    """
    analysis_dict = analysis.to_dict()
    harmless = analysis_dict['attributes']['stats']['harmless']
    malicious = analysis_dict['attributes']['stats']['malicious']
    suspicious = analysis_dict['attributes']['stats']['suspicious']
    undetected = analysis_dict['attributes']['stats']['undetected']
    type_unsupported = analysis_dict['attributes']['stats']['type-unsupported']
    file_info = (
        f"🟢 **Harmless**: {harmless}\n"
        f"🔴 **Malicious**: {malicious}\n"
        f"🟡 **Suspicious**: {suspicious}\n"
        f"🟣 **Undetected**: {undetected}\n"
        f"⚪ **Type unsupported**: {type_unsupported}\n"
    )
    return file_info


def get_file_sha256(file_path: str):
    """
    Get the file sha256 hash of the file.

    Parameters:
    -----------
    - file_path: str
        The path of the file.

    Returns:
    --------
    - sha256: str
        The sha256 hash of the file.
    """
    with open(file_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    return sha256


def get_user_id_artifacts_path(artifacts_path: str, user_id: str):
    """
    Get the path of the artifacts folder of the user.

    Parameters:
    -----------
    - artifacts_path: str
        The path of the artifacts folder.
    - user_id: str
        The telegram id of the user.

    Returns:
    --------
    - user_id_artifacts_path: str
        The path of the artifacts folder of the user.
    """
    user_id_artifacts_path = os.path.join(artifacts_path, user_id)
    if not os.path.exists(user_id_artifacts_path):
        os.makedirs(user_id_artifacts_path)
    return user_id_artifacts_path
