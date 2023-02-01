"""
Configuration file
"""
import os
import sys
import logging

import structlog

from virus_total_telegram_bot.entities import Config


logger = structlog.get_logger()


def load_loggers(logs_path: str):
    """
    Load the loggers

    Parameters:
    -----------
    - logs_path: str
      The path where the log files are going to be stored.
    """
    log_file_path = f"{logs_path}/virus_total.log"
    # Configure terminal output
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.JSONRenderer()
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    # Configure json file output
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    structlog.get_logger().addHandler(file_handler)


def create_application_directories(working_directory: str):
    """
    Creates the needed directories for the application to work.

    Parameters:
    -----------
    - working_directory: str
      The work directory of the bot. From this root, all artefacts will be organized and saved.

    Returns:
    --------
    - artifacts_path: str
      The path where the application artifacts will be saved.
    - logs_path: str
      The path where the applications log files will be saved.
    """
    logger.info("bot_working_directory", path=working_directory)
    artifacts_path = f"{working_directory}/artifacts"
    logs_path = f"{working_directory}/logs"
    try:
        os.makedirs(artifacts_path, exist_ok=True)
        os.makedirs(logs_path, exist_ok=True)
    except OSError:
        logger.error("make_directory", artifacts_path=artifacts_path, logs_path=logs_path)
        sys.exit(1)
    return artifacts_path, logs_path


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
