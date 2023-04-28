"""
Configuration file
"""
import os
import sys
import logging.config

from socket import gethostname
from getpass import getuser

import structlog

from virus_total_telegram_bot.entities import Config


def extract_from_record(_, __, event_dict):  # pylint: disable=invalid-name
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName

    return event_dict


def add_hostname(_, __, event_dict):  # pylint: disable=invalid-name
    """
    Add hostname to the event dict.

    Parameters:
    -----------
    - event_dict: dict
        The event dict.

    Returns:
    --------
    - event_dict: dict
        The event dict with the hostname added.
    """
    record = event_dict.get("host")
    if record is None:
        event_dict["host"] = gethostname()

    return event_dict


def add_user(_, __, event_dict):  # pylint: disable=invalid-name
    """
    Add username to the event dict.

    Parameters:
    -----------
    - event_dict: dict
        The event dict.

    Returns:
    --------
    - event_dict: dict
        The event dict with the username added.
    """
    record = event_dict.get("user")
    if record is None:
        event_dict["user"] = getuser()

    return event_dict


def _initialize_logging(log_cfg: dict, user_processors=tuple()):
    """
    Initialize logging.

    Parameters:
    -----------
    - log_cfg: dict
        The logging configuration.
    - user_processors: tuple
        The user processors.
    """
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        add_hostname,
        add_user
    ]

    if not structlog.is_configured():
        structlog.configure(
            processors=processors
            + list(user_processors)
            + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
            logger_factory=structlog.stdlib.LoggerFactory(),
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
        )

    formatter = structlog.processors.JSONRenderer() if log_cfg["log_format"] == "json" else structlog.dev.ConsoleRenderer(colors=True)
    std_formatter = structlog.stdlib.ProcessorFormatter(
        processor=formatter, foreign_pre_chain=processors
    )

    if log_cfg["log_handler"] == "stdout":
        handler = logging.StreamHandler()
    if log_cfg["log_handler"] == "file":
        handler_class = logging.handlers.RotatingFileHandler
        handler_kwargs = {
            "filename": os.path.join(log_cfg['log_folder'], log_cfg['log_filename']),
            "maxBytes": log_cfg['log_max_bytes'],
            "backupCount": log_cfg['log_backup_count']
        }
        handler = handler_class(**handler_kwargs)

    handler.setFormatter(std_formatter)

    # configure standard logging

    level = logging.getLevelName(log_cfg["log_level"])
    logger = logging.getLogger(log_cfg["log_name"])
    logger.addHandler(handler)
    logger.setLevel(level)


def initialize_loggers(logs_path: str):
    """
    Load the loggers

    Parameters:
    -----------
    - logs_path: str
      The path where the log files are going to be stored.
    """
    console_config = {
        "log_name": "",
        "log_format": "console",
        "log_level": "DEBUG",
        "log_handler": "stdout"
    }
    file_config = {
        "log_name": "",
        "log_format": "json",
        "log_handler": "file",
        "log_max_bytes": 1048576,
        "log_backup_count": 10,
        "log_folder": logs_path,
        "log_filename": "siren_scoop.log",
        "log_level": "INFO"
    }

    _initialize_logging(console_config)
    if os.getenv("PRODUCTION", "false").lower() == "true":
        _initialize_logging(file_config)


def create_application_directories(logs_path: str, artifacts_path: str):
    """
    Creates the needed directories for the application to work.

    Parameters:
    -----------
    - logs_path: str
      The path where the log files are going to be stored.
    - artifacts_path: str
      The path where the artifacts are going to be stored.
    """
    try:
        os.makedirs(artifacts_path, exist_ok=True)
        os.makedirs(logs_path, exist_ok=True)
    except OSError:
        sys.exit(1)


def load_configuration(artifacts_path: str, logs_file_path: str):
    """
    Load configuration function.

    Parameters:
    -----------
    - artifacts_path: str
        The path where the artifacts are going to be stored.
    - logs_file_path: str
        The path where the logs are going to be stored.

    Returns:
    --------
    - config: Config
      The configuration object.
    """
    logger = structlog.get_logger()
    logger.info("loading_configuration")

    VIRUS_TOTAL_BOT_APIKEY = os.getenv("VIRUS_TOTAL_BOT_APIKEY")    # pylint: disable=invalid-name
    VIRUS_TOTAL_APIKEY = os.getenv("VIRUS_TOTAL_APIKEY")            # pylint: disable=invalid-name
    FILES_MAX_SIZE = os.getenv("FILES_MAX_SIZE", "5")               # pylint: disable=invalid-name
    config = Config(
        artifacts_path=artifacts_path,
        logs_path=logs_file_path,
        bot_apikey=VIRUS_TOTAL_BOT_APIKEY,
        virus_total_apikey=VIRUS_TOTAL_APIKEY,
        files_max_size=FILES_MAX_SIZE
    )
    return config
