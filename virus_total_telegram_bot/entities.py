"""
All the entities needed for the bot. Here you will find all data structires.
"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Config(BaseModel):
    """
    Class to store the application configuration
    """
    artifacts_path: str
    logs_path: str
    bot_apikey: str
    virus_total_apikey: str
