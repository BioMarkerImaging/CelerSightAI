print("Importing celer_sight_main")
import os
import sys


def excepthook(exc_type, exc_value, exc_tb):
    import traceback
    import logging

    logging.error("****** Exception Start *******")
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.error(tb)
    logging.error("****** Exception End *******")
    error_message = f"An error occurred: {exc_type.__name__}: {str(exc_value)}\n for more information, please check the log file at {os.path.join(getLocal(), 'celer_sight.log')}"
    config.global_signals.errorSignal.emit(error_message)


sys.excepthook = excepthook

from celer_sight_ai import config
from celer_sight_ai.configHandle import getLocal

import pathlib
import logging
from celer_sight_ai import config


if "CELER_SIGHT_INSTANCE_STARTED" not in os.environ:

    if not os.path.exists(os.path.join(getLocal())):
        try:
            os.makedirs(os.path.join(getLocal()))
        except Exception as e:
            print(f"Failed to create local directory: {e}")

    # make sure that the local folders needed exist
    dirs_to_check = [
        "experiment_configs",
        "experiment_configs/default_classes",
        "experiment_configs/default_classes/cloud",
        "experiment_configs/default_classes/local",
        "experiment_configs/user_experiments",
        "mats/mgb",
    ]
    for dir_to_check in dirs_to_check:
        if not os.path.exists(os.path.join(getLocal(), dir_to_check)):
            os.makedirs(os.path.join(getLocal(), dir_to_check))

    # setup logger
    # clear out previous handlers

    sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
    print("Local path: ", getLocal())
    print("Logger path: ", os.path.join(getLocal(), "celer_sight.log"))
    logger_path = os.path.join(getLocal(), "celer_sight.log")
    if os.path.exists(logger_path):
        os.remove(logger_path)

    import logging

    logger = logging.getLogger()

    # If you want to clear existing handlers (be cautious with this):
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(
        logger_path, maxBytes=1024 * 1024 * 5, backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("CELER_SIGHT_INSTANCE_STARTED")
else:
    logger = logging.getLogger(__name__)
logger.info("Importing celer_sight_main again")

global gui_main
os.environ["CELER_SIGHT_INSTANCE_STARTED"] = "false"

logger.info(f"CELER_SIGHT_AI_HOME: {os.environ['CELER_SIGHT_AI_HOME']}")


if config.is_executable:
    app_home = sys._MEIPASS
    # on mac os
    os.environ["CELER_SIGHT_AI_HOME"] = app_home
    os.chdir(app_home)
    logger.info("Celer Sight AI Home: " + app_home)
    sys.path.append(app_home)
    # also append the celer_sight_ai folder
    sys.path.append(os.path.join(app_home, "celer_sight_ai"))
    print(f"Running from frozen executable, setting path to {app_home}")
else:
    # get parent path of the current file
    p = pathlib.Path(__file__).parent.absolute()
    os.environ["CELER_SIGHT_AI_HOME"] = str(p)
    # get parent path
    sys.path.append(str(p))

BLNS_FILE_TO_LOAD = None  # used to instract to open a file upon login


def get_override_qapp_variable():
    """Return true if we are in testing mode, this will allow to directly import
    the UI when importing this module

    Returns:
        Bool: True if we are in testing mode
    """
    if "CelerSight_TESTING" in os.environ:
        if os.environ["CelerSight_TESTING"].lower() == "true":
            return True
    return False


def start_celer_sight_main(app, splash_window, dont_start_app=False, file_to_load=None):
    login_handler = start_celer_sight_main_part_login(app, splash_window)
    app, login_handler, gui_main = start_celer_sight_main_part_main_app(
        app,
        splash_window,
        login_handler,
        dont_start_app=dont_start_app,
        file_to_load=file_to_load,
    )
    return app, login_handler, gui_main


def start_celer_sight_main_part_login(app, splash_window=None):
    """Main method to run CelerSight app/

    Returns:
        Qt Element: Ui instance of log in handler
    """

    os.environ["CELER_SIGHT_INSTANCE_STARTED"] = "true"
    import celer_sight_ai.core.LogTool as LogTool

    logger.debug(f"Creating Application instance")

    logger.debug("Created app instance")
    # get enviromental variable ""CELER_SIGHT_TESTING"
    is_testing = os.getenv("CELER_SIGHT_TESTING", "false")
    logger.debug("Starting Splash Window")

    login_handler = LogTool.LogInHandler(splash_window)

    logger.debug(f"Checking if connection is complete.")
    return login_handler


def start_celer_sight_main_part_main_app(
    app, splash_window, login_handler, dont_start_app=False, file_to_load=None
):
    from PyQt6.QtWidgets import QApplication

    login_handler.check_connection_complete()
    if not hasattr(login_handler, "gui_main"):
        login_handler.gui_main = None
    gui_main = login_handler.gui_main
    QApplication.restoreOverrideCursor()

    if gui_main:
        login_handler.LogInDialog.hide()
        login_handler = None
        if splash_window:
            # Only finish the splash window if it exists and hasn't been deleted
            splash_window.finish(gui_main)
            splash_window.hide()

        splash_window = None
        del splash_window
        if file_to_load:
            gui_main.load_celer_sight_file(file_to_load)
    else:
        logger.info("No gui, exiting.")
        sys.exit()
    is_testing = os.getenv("CELER_SIGHT_TESTING", "false")

    # if app is not already running, start it
    if not is_testing.lower() == "true" and not dont_start_app:
        app.exec()  # start the app
    return app, login_handler, gui_main


logger.info("ok right after")


from celer_sight_ai import config


if config.is_executable:
    sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])


BLNS_FILE_TO_LOAD = None  # used to instract to open a file upon login


global seshID_server
config.user_attributes.seshIDServer = ""


if "__main__" == __name__:
    pass
