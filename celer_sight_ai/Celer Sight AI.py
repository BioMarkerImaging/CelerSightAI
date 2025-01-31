from multiprocessing import freeze_support  # noqa

freeze_support()  # noqa
# if frozen
import sys

# if not hasattr(sys, "frozen"):
#     import typeguard
#     from typeguard import TypeCheckConfiguration

#     # Configure typeguard to ignore javabridge
#     config = TypeCheckConfiguration(exclude_modules=("javabridge", "bioformats"))
#     typeguard.install_import_hook("celer_sight_ai", config)  # For the package

print("Running Celer Sight AI")
import time

start = time.time()

import argparse
import os

import bioformats
import imagecodecs
import javabridge
import networkx
import numcodecs
import openslide
import tufup
import zarr
import zarr.storage
from azure.storage.blob import BlobClient, BlobServiceClient

from celer_sight_ai import config
from celer_sight_ai.gui.custom_widgets.splash_widget import CustomSplashScreenWithText

print("Importing Splash")
from PyQt6.QtWidgets import QApplication, QWidget

print("Importing QApplication, QWidget")
os.environ["PYTHONDEVMODE"] = "0"
os.environ["PYTHONTYPECHECKINGPDB"] = "0"
os.environ["PYTHONTYPECHECKING"] = "0"


def start_celer_sight_ai():
    print("Starting Celer Sight AI")
    # if pytest is not used
    # if not os.getenv("CELER_SIGHT_TESTING", False) == "true":
    # check if any arguments provided
    # if is instance pytest, dont read arguments
    args = None  # no args for testing
    from celer_sight_ai import config

    config.start_jvm()
    if not os.environ.get("CELER_SIGHT_TESTING", False):
        parser = argparse.ArgumentParser()
        # Filter out macOS-specific arguments before parsing
        if hasattr(sys, "frozen") and sys.platform == "darwin":
            sys.argv = [arg for arg in sys.argv if arg not in ["-B", "-S", "-I", "-c"]]

        # check if celer sight ai file is provided
        parser.add_argument("--load-from-file", type=str, help="Celer Sight AI file")
        # check if --run-tests-short is provided
        parser.add_argument(
            "--run-tests-short", help="Run short tests", action="store_true"
        )
        # add an argument to supply a particular test file
        parser.add_argument(
            "--test-file", type=str, help="Test file to run", default=None
        )
        # add argument that allow us to not relunch after the update, normally it will relaunch
        parser.add_argument(
            "--no-relunch-after-update",
            help="Do not relaunch after the update",
            action="store_true",
        )
        # check if --run-tests-short is provided
        parser.add_argument(
            "--update-host", type=str, default=None, help="Change the update host url"
        )
        # get version
        parser.add_argument("--version", help="Get the version", action="store_true")
        # force offline mode
        parser.add_argument(
            "--offline", help="Run the application offline", action="store_true"
        )
        parser.add_argument(
            "--empty-local-dir", help="Empty the local directory", action="store_true"
        )
        # any other arguments, ignore
        parser.add_argument("args", nargs=argparse.REMAINDER)
        args = parser.parse_args()
        if args.empty_local_dir:
            import shutil

            from celer_sight_ai.configHandle import getLocal

            shutil.rmtree(os.path.join(getLocal()), ignore_errors=True)
            # re-create the local directories
            from celer_sight_ai.config import make_sure_local_dirs_exist

            make_sure_local_dirs_exist()

        if args.version:
            from celer_sight_ai import __version__, clean_exit

            print(f"Celer Sight version: {__version__}")
            clean_exit()
        if args.update_host:
            os.environ["CELER_SIGHT_UPDATE_HOST"] = args.update_host
        # if testing
        if args.run_tests_short:

            os.environ["CELER_SIGHT_TESTING"] = "true"
            app_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"App dir is {app_dir}")
            sys.argv = sys.argv[:1]
            if hasattr(sys, "frozen"):
                import unittest

                # remove all args
                if args.test_file:
                    unittest.main(module="celer_sight_ai.tests." + args.test_file)
                else:
                    unittest.main(module="celer_sight_ai.tests.test_small_suite")
                sys.exit()
            else:
                import unittest

                unittest.main(module="tests.test_small_suite")
                sys.exit()
        if args.no_relunch_after_update:
            os.environ["CELER_SIGHT_NO_RELUNCH_AFTER_UPDATE"] = "true"
        if args.offline:
            # config has already loaded
            from celer_sight_ai import config

            config.user_cfg["OFFLINE_MODE"] = True  # force offline mode

    print("Before QApplication")
    # This runs on the firs time CelerSight module is imported
    # app = QApplication(sys.argv)
    app = QApplication.instance()

    print("App is: ", app)
    if app is None:
        app = QApplication(sys.argv)
    app.setApplicationName("CelerSight")
    app.setOrganizationName("BioMarkerImaging")

    splashWindow = CustomSplashScreenWithText()
    splashWindow.show()
    # create a widget
    w = QWidget()
    w.show()
    w.hide()
    w.deleteLater()
    QApplication.processEvents()
    splashWindow.showMessage("Loading modules...")
    print(f"Importing Celer Sight AI took {time.time() - start} seconds")

    if os.name == "nt":
        from ctypes import wintypes

        import win32api
        import win32con
        import win32gui
    from celer_sight_ai import celer_sight_main

    load_from_file = args.load_from_file if args else None
    gui_main, MyLogInHandler, app = celer_sight_main.start_celer_sight_main(
        app, splashWindow, file_to_load=load_from_file
    )  # pass in the splash window to delete it later
    return gui_main, MyLogInHandler, app, splashWindow


if "__main__" == __name__:
    (
        gui_main,
        MyLogInHandler,
        app,
        splashWindow,
    ) = start_celer_sight_ai()  # pass in the splash window to delete it later
