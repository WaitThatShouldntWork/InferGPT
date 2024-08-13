# conftest.py
import pytest
import os

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Set an environment variable to indicate pytest is running
    os.environ["PYTEST_RUNNING"] = "1"
