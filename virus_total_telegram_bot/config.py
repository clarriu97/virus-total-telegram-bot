"""
Configuration file
"""
import os
import sys

import structlog

from virus_total_telegram_bot.entities import Configuration


def load_loggers(logs_file_path: str):
    """
    Load the loggers
    
    Parameters:
    -----------
    - logs_file_path: str
      The path where the logs file is going to be stored.
    """
    logger = structlog.get_logger()
    structlog.configure(processors=[structlog.processors.JSONRenderer(),structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
                        logger_factory=structlog.stdlib.LoggerFactory(),
                        wrapper_class=structlog.stdlib.BoundLogger,
                        cache_logger_on_first_use=True,
                        context_class=dict,
                        logger_name='virus_total_telegram_bot',
                        wrapper_kwargs={'output_file':logs_file_path}
                        )


def load_configuration():
    """
    Load configuration function
    """
    logger.info("load_configuration")
    working_directory = os.getenv("WORKING_DIRECTORY", "/tmp")
    logger.info("bot_working_directory", path=working_directory)
    artifacts_path = f"{working_directory}/artifacts"
    logs_path = f"{working_directory}/logs"
    try:
        os.makedirs(artifacts_path, exist_ok=True)
        os.makedirs(logs_path, exist_ok=True)
    except OSError:
        logger.error("make_directory", artifacts_path=artifacts_path, logs_path=logs_path)
        sys.exit(1)

    BOT_API_KEY = os.getenv("VIRUS_TOTAL_APIKEY")
    config = Configuration(
        
    )
    return config
