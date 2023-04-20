"""
This file is used to configure pytest.
"""
import pytest

from virus_total_telegram_bot.config import load_configuration


@pytest.fixture(scope="session")
def test_config():
    """
    Dictionary with all test configuration to parametrize
    """
    return load_configuration(None, None)
