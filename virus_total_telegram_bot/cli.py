"""
Command-line interface that acts as the entrypoint from which the server can be started.
"""
import os

import click

from virus_total_telegram_bot import __version__
from virus_total_telegram_bot import config
from virus_total_telegram_bot import app


@click.command()
def virus_total():
    """
    Entrypoint of the app.

    To run it, simply put this command in your terminal:

    ```bash
    python virus_total_telegram_bot/cli.py
    ```
    """
    logs_path = os.getenv("LOGS_PATH", "/tmp")
    artifacts_path = os.getenv("ARTIFACTS_PATH", "/tmp")
    config.initialize_loggers()
    config.create_application_directories(logs_path, artifacts_path)
    cfg = config.load_configuration(artifacts_path, logs_path)
    app.run(cfg)


if __name__ == "__main__":  # pragma: no cover
    virus_total()
