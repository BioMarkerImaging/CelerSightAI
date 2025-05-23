# required not to crash as a first import
import os
import sys
import dotenv

# Load env vars relative to conftest.py location
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# add parent directory to path
p_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(p_dir)

from typing import Any, Callable, Literal
from unittest.mock import patch

import pytest
from ui_qtbot_tools import get_gui_main


def pytest_addoption(parser):
    parser.addoption(
        "--online", action="store_true", default=False, help="run online tests"
    )
    parser.addoption(
        "--run-long", action="store_true", default=False, help="run long tests"
    )


def pytest_collection_modifyitems(config, items):
    # Don't skip if only one test is being run
    if len(items) == 1:
        return

    # Skip online tests unless --online flag is provided
    if not config.getoption("--online"):
        skip_online = pytest.mark.skip(reason="need --online option to run")
        for item in items:
            if "online" in item.keywords:
                item.add_marker(skip_online)

    # Skip long tests unless --run-long flag is provided
    if not config.getoption("--run-long"):
        skip_long = pytest.mark.skip(reason="need --run-long option to run")
        for item in items:
            if "long" in item.keywords:
                item.add_marker(skip_long)


# get parent dir
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import dotenv

    # load env vars
    dotenv.load_dotenv(os.path.join(p, ".env"))
except Exception as e:
    print(f"Error loading env vars {e}")


@pytest.fixture
def app(qtbot) -> Any:
    return get_gui_main(qtbot)
