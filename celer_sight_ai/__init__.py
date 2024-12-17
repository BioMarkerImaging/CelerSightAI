import os
import logging
import shutil
import time
import sys

__version__ = "0.0.460"
APP_NAME = "celer_sight_ai"

# if not hasattr(sys, "frozen"):
#     from typeguard import install_import_hook

#     # Specify the module you want to check
#     install_import_hook('celer_sight_ai')
from celer_sight_ai import config as settings


logger = logging.getLogger(__name__)


def clean_exit():
    from PyQt6 import QtWidgets
    import sys

    """Clean up and exit the application"""
    logger.info("Cleaning up and exiting the application")
    # Clean up any remaining windows
    for window in QtWidgets.QApplication.topLevelWindows():
        window.close()

    # Get the QApplication instance
    app = QtWidgets.QApplication.instance()

    if app:
        # Process any pending events
        app.processEvents()
        # Quit the application
        app.quit()

    # Exit the process
    sys.exit(0)
