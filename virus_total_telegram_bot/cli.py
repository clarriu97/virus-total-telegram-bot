"""
Command-line interface that acts as the entrypoint from which the server can be started.
"""
import click

from virus_total_telegram_bot import __version__
from virus_total_telegram_bot import config
from virus_total_telegram_bot import app


@click.group()
@click.version_option(version=__version__)
def voice_alive_telegram_bot_cli():
    """
    Run the server from CLI
    """


@voice_alive_telegram_bot_cli.command("run")
def run():
    """Runs the Flask development server"""
    cfg = config.load_configuration()
    app.run(cfg)


def main():  # pragma: no cover
    """The main entrypoint for this application"""
    voice_alive_telegram_bot_cli()


if __name__ == "__main__":  # pragma: no cover
    main()
