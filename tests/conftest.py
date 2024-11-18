# required not to crash as a first import
import aicsimageio
import os
import sys

# add parent directory to path
p_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(p_dir)

import pytest
from unittest.mock import patch
from celer_sight_ai.configHandle import get_stored_password, get_stored_username
from typing import Literal, Any, Callable
from ui_qtbot_tools import get_gui_main

# get parent dir
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import dotenv
    # load env vars
    dotenv.load_dotenv(os.path.join(p, ".env"))
except Exception as e:
    print(f"Error loading env vars {e}")

def mock_password_fail() -> str:
    return "ASojnaAJO"


def mock_correct_password() -> str:
    return os.environ.get("PASSWORD")


def mock_correct_username() -> str:
    return os.environ["USERNAME"]


@pytest.fixture
def app(qtbot, mock_correct_creds) -> Any:
    return get_gui_main(qtbot)


@pytest.fixture
def mock_correct_creds(monkeypatch) -> None:
    # Patch the get_stored_password function to return a mock settings object
    monkeypatch.setattr(
        "celer_sight_ai.configHandle.get_stored_username", mock_correct_username
    )
    monkeypatch.setattr(
        "celer_sight_ai.configHandle.get_stored_password", mock_correct_password
    )


@pytest.fixture
def mock_failed_creds(monkeypatch) -> None:
    # Patch the get_stored_password function to return a mock settings object
    monkeypatch.setattr(
        "celer_sight_ai.configHandle.get_stored_password", mock_password_fail
    )
