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


def extract_from_record(_, __, event_dict):
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName

    return event_dict


def add_hostname(_, __, event_dict):
    """
    Add hostname to the event dict.

    Parameters:
    -----------
    - logger: structlog.stdlib.BoundLogger
    - method_name: str
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


def add_user(_, __, event_dict):
    """
    Add username to the event dict.

    Parameters:
    -----------
    - logger: structlog.stdlib.BoundLogger
    - method_name: str
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


def initialize_loggers(logs_path: str):
    """
    Load the loggers

    Parameters:
    -----------
    - logs_path: str
      The path where the log files are going to be stored.
    """
    log_file = os.path.join(logs_path, "virus_total_telegram_bot.log")
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        timestamper,
    ]

    logging.config.dictConfig({
      "version": 1,
      "disable_existing_loggers": False,
      "formatters": {
          "json": {
              "()": structlog.stdlib.ProcessorFormatter,
              "processors": [
                add_hostname,
                add_user,
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer()
              ],
              "foreign_pre_chain": pre_chain,
          },
          "console": {
              "()": structlog.stdlib.ProcessorFormatter,
              "processors": [
                add_hostname,
                add_user,
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
              ],
              "foreign_pre_chain": pre_chain,
          },
      },
      "handlers": {
          "default": {
              "level": "DEBUG",
              "class": "logging.StreamHandler",
              "formatter": "console",
          },
          "file": {
              "level": "INFO",
              "class": "logging.handlers.WatchedFileHandler",
              "filename": log_file,
              "formatter": "json",
          },
      },
      "loggers": {
          "": {
              "handlers": ["default", "file"],
              "level": "DEBUG",
              "propagate": True,
          },
      }
    })

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )


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
