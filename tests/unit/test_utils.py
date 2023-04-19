"""Unit tests for the utils module."""
import pytest
from unittest.mock import MagicMock, patch

from telegram import Update
from telegram.ext import CallbackContext

from virus_total_telegram_bot.utils import (
    get_username,
    get_user_id,
    get_user_language,
    add_request_arrived_data,
    add_file_data,
    current_milliseconds,
    save_request_data,
    get_event_info,
    clear_user_data
)
from virus_total_telegram_bot.strings import ENGLISH


@pytest.mark.unit
def test_get_username():
    update = MagicMock(spec=Update)
    update.message.from_user.username = "johndoe"
    username = get_username(update)
    assert username == "johndoe"


@pytest.mark.unit
def test_get_username_callback_query():
    update = MagicMock(spec=Update)
    update.message = None
    update.callback_query.message.chat.username = "janedoe"
    username = get_username(update)
    assert username == "janedoe"


@pytest.mark.unit
def test_get_user_id():
    update = MagicMock(spec=Update)
    update.message.from_user.id = 123456789
    user_id = get_user_id(update)
    assert user_id == 123456789


@pytest.mark.unit
def test_get_user_id_callback_query():
    update = MagicMock(spec=Update)
    update.message = None
    update.callback_query.message.chat.id = 987654321
    user_id = get_user_id(update)
    assert user_id == 987654321


@pytest.mark.unit
def test_get_user_language():
    assert get_user_language(None) == ENGLISH
    assert get_user_language("foo") == ENGLISH


@pytest.mark.unit
def test_add_request_arrived_data():
    with patch("virus_total_telegram_bot.utils.current_milliseconds") as mock_current_milliseconds:
        mock_current_milliseconds.return_value = 123456789
        context = MagicMock(spec=CallbackContext)
        context.user_data = {}
        add_request_arrived_data(context, "scan", "johndoe", "123456", "abcdef")
        assert context.user_data == {
            "event_info": {
                "metadata": {
                    "service": "virus total telegram bot",
                    "integrator": "clarriu97"
                },
                "request": {
                    "action": "scan",
                    "username": "johndoe",
                    "user_id": "123456",
                    "result": None,
                    "request_id": "abcdef",
                    "start_time": 123456789,
                    "end_time": None,
                    "elapsed": None
                }
            }
        }


@pytest.mark.unit
def test_add_file_data():
    context = MagicMock(spec=CallbackContext)
    context.user_data = {"event_info": {}}
    add_file_data(context, "file.txt", 123456, "abcdef", "123456")
    assert context.user_data == {
        "event_info": {
            "file": {
                "name": "file.txt",
                "size": 123456,
                "hash": "abcdef",
                "id": "123456"
            }
        }
    }


@pytest.mark.unit
def test_current_milliseconds():
    assert isinstance(current_milliseconds(), int)


@pytest.mark.unit
def test_save_request_data():
    context = MagicMock(spec=CallbackContext)
    random_start_time = 123456789
    random_end_time = 7654321
    context.user_data = {
        "event_info": {
            "request": {
                "action": "scan",
                "username": "johndoe",
                "user_id": "123456",
                "result": None,
                "request_id": "abcdef",
                "start_time": random_start_time,
                "end_time": None,
                "elapsed": None
            }
        }
    }
    with patch("virus_total_telegram_bot.utils.current_milliseconds") as mock_current_milliseconds:
        mock_current_milliseconds.return_value = random_end_time
        save_request_data(context, "result")
        assert context.user_data == {
            "event_info": {
                "request": {
                    "action": "scan",
                    "username": "johndoe",
                    "user_id": "123456",
                    "result": "result",
                    "request_id": "abcdef",
                    "start_time": random_start_time,
                    "end_time": random_end_time,
                    "elapsed": random_end_time - random_start_time
                }
            }
        }


@pytest.mark.unit
def test_get_event_info():
    context = MagicMock(spec=CallbackContext)
    context.user_data = {
        "event_info": {
            "metadata": {
                "service": "virus total telegram bot",
                "integrator": "clarriu97"
            },
            "request": {
                "action": "scan",
                "username": "johndoe",
                "user_id": "123456",
                "result": None,
                "request_id": "abcdef",
                "start_time": 123456789,
                "end_time": None,
                "elapsed": None
            }
        }
    }
    event_info = get_event_info(context)
    assert event_info == {
        "metadata": {
            "service": "virus total telegram bot",
            "integrator": "clarriu97"
        },
        "request": {
            "action": "scan",
            "username": "johndoe",
            "user_id": "123456",
            "result": None,
            "request_id": "abcdef",
            "start_time": 123456789,
            "end_time": None,
            "elapsed": None
        }
    }


@pytest.mark.unit
def test_clear_user_data():
    context = MagicMock(spec=CallbackContext)
    context.user_data = {
        "event_info": {
            "metadata": {
                "service": "virus total telegram bot",
                "integrator": "clarriu97"
            },
            "request": {
                "action": "scan",
                "username": "johndoe",
                "user_id": "123456",
                "result": None,
                "request_id": "abcdef",
                "start_time": 123456789,
                "end_time": None,
                "elapsed": None
            }
        }
    }
    clear_user_data(context)
    assert context.user_data == {}
