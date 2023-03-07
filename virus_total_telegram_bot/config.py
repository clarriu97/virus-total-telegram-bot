"""
Configuration file
"""
import os
import sys
import logging

import structlog

from virus_total_telegram_bot.entities import Config


def load_loggers():
    """
    Load the loggers

    Parameters:
    -----------
    - logs_path: str
      The path where the log files are going to be stored.
    """
    # configure structlog to work with two loggers: one for the console and one for a json file
    # the console logger will have plain text and the json logger will have json
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
    logger = structlog.get_logger()
    try:
        os.makedirs(artifacts_path, exist_ok=True)
        os.makedirs(logs_path, exist_ok=True)
        logger.info("paths_created", artifacts_path=artifacts_path, logs_path=logs_path)
    except OSError:
        logger.error("make_path", artifacts_path=artifacts_path, logs_path=logs_path)
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
    config = Config(
        artifacts_path=artifacts_path,
        logs_path=logs_file_path,
        bot_apikey=VIRUS_TOTAL_BOT_APIKEY,
        virus_total_apikey=VIRUS_TOTAL_APIKEY
    )
    return config
