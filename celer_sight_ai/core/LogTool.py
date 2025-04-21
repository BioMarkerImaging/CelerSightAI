import os
import pathlib

os.chdir(os.environ["CELER_SIGHT_AI_HOME"])

import logging

logger = logging.getLogger(__name__)

import os
import sys

from cryptography.fernet import Fernet
from PyQt6 import QtCore, QtGui, QtWidgets

import celer_sight_ai.configHandle as configHandle
from celer_sight_ai import config
from celer_sight_ai.core.Workers import Worker
from celer_sight_ai.gui.designer_widgets_py_files.loginui1 import Ui_LogInDialog
from celer_sight_ai.gui.designer_widgets_py_files.loginuiRegistration1 import (
    Ui_Dialog as ActivationDialog,
)

global gui_main
gui_main = None
import json

import requests

from celer_sight_ai import config
from celer_sight_ai.configHandle import getLocal, getLogInAddress


class UpdateStatus:
    """Enumerated data type"""

    UNKNOWN = 0
    NO_AVAILABLE_UPDATES = 1
    UPDATE_DOWNLOAD_FAILED = 2
    EXTRACTING_UPDATE_AND_RESTARTING = 3
    UPDATE_AVAILABLE_BUT_APP_NOT_FROZEN = 4
    COULDNT_CHECK_FOR_UPDATES = 5


class LogInHandler(Ui_LogInDialog):
    def __init__(self, splash=None, is_main_window_launched=False):
        super(LogInHandler, self).__init__()
        # if splash UI is not provided then we are probably testing, so
        # skiping all of the UI initialization stuff.

        self._is_logged_in = False

        self.connection_complete = False
        logger.debug("loggin handler initializing")
        self.LogInDialog = QtWidgets.QDialog()
        # Make the dialog modal
        self.LogInDialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.splash = splash
        self._is_main_window_launched = is_main_window_launched

        self.setupUi(self.LogInDialog)
        self.retranslateUi(self.LogInDialog)
        self.during_log_in = False
        from celer_sight_ai import config
        from celer_sight_ai.gui.custom_widgets.widget_spinner import WaitingSpinner
        from celer_sight_ai.updater import launch_update

        # spinner that runs while we are logging in.
        self.spinner_log_in = WaitingSpinner(
            self.LogInDialog,
            roundness=100.0,
            # opacity=1.0,
            fade=10.0,
            radius=17,
            lines=52,
            line_length=11,
            line_width=18,
            speed=0.5,
            color=QtGui.QColor(0, 255, 35),
        )

        config.global_signals.shut_down_signal.connect(lambda: sys.exit(0))
        config.global_signals.update_signal.connect(launch_update)

        config.global_signals.start_log_in_spinner.connect(
            lambda: self.spinner_log_in.start()
        )
        config.global_signals.stop_log_in_spinner.connect(
            lambda: self.spinner_log_in.stop()
        )
        config.global_signals.launch_main_window_after_log_in_signal.connect(
            self.Lunch_application_after_authentication
        )

        config.global_signals.lunch_APP_LINK_FILE_downloader.connect(
            lambda: self.launch_app_link_notification_dialog()
        )
        config.global_signals.set_text_log_in_error_signal.connect(
            self.set_log_in_error_text
        )
        config.global_signals.show_log_in_dialog_signal.connect(
            lambda: self.show_login_dialog()
        )
        config.global_signals.hide_log_in_dialog_signal.connect(
            lambda: self.LogInDialog.hide()
        )
        config.global_signals.hide_splash_screen_signal.connect(
            lambda: self.splash.hide()
        )

        config.global_signals.show_splash_screen_signal.connect(
            lambda: self.splash.show()
        )

        self.APP_LINK_save_loc = (
            False  # indicates there is a file waiting for us form the app
        )
        self.APP_LINK_download_size = 0  # in MB
        self.app_link_notification_dialog = None
        if self.splash:
            config.global_signals.setSplashText.connect(self.splash.showMessage)

        try:
            iconWin1 = QtGui.QIcon("data/celer_sight_icons/app_logo_celer_sight.png")
            # iconWin1.setIconSize(QtCore.QSize(50, 50))
            self.LogInDialog.setWindowIcon(iconWin1)

        except Exception as e:
            print(e)
            logger.error("cant load appicon! ", e)

        self.updateWindow = None

        self.LogInThreadPool = QtCore.QThreadPool()

        self.pushButton_2.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.pushButton.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )

        self.label_2.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label_4.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label_5.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        config.global_signals.lunchUpdaterWindowSignal.connect(self.lunchUpdatingWindow)
        self.pushButton_2.clicked.connect(lambda: self.spinner_log_in.start())
        self.pushButton_2.clicked.connect(lambda: self.LogInDialog.setEnabled(False))
        self.pushButton_2.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.pushButton_2.clicked.connect(lambda: self.AuthenticationRunner())
        self.pushButton.clicked.connect(lambda: self.LunchRegistrationWindow())
        self.OfflineModeButton.clicked.connect(lambda: self.log_in_with_offline_mode())
        self.LogInDialog.closeEvent = self.closeEvent
        self.attempt_to_auto_login()  # only runs if the user has set the automatic log in
        self.initialize_log_in_dialog()
        self.lineEdit = self.setup_username_autocomplete(self.lineEdit)

    def attempt_to_auto_login(self):
        # if the user has set the automatic log in, check past jwt
        # token and try to get new ones, if we fail, then log in
        # if its offline mode, skip this
        if config.user_cfg["OFFLINE_MODE"]:
            self.splash.hide()
            return
        if (
            config.settings.value("AutoLogIn")
            and config.settings.value("AutoLogIn").lower() == "true"
        ):
            previous_username = configHandle.get_stored_username()
            jwt_refresh_token = configHandle.get_jwt_token_for_auto_login()
            if not jwt_refresh_token:
                logger.info("JWT refresh token not found, cant auto login.")
                return
            self.AuthenticationRunner(
                provided_username=previous_username, jwt_refresh_token=jwt_refresh_token
            )
        else:
            self.splash.hide()

    def setup_username_autocomplete(self, lineEdit):
        """Set up autocomplete for the username input field"""
        # Get recent users list
        recent_users = configHandle.get_recent_users()

        # Create and configure completer
        completer = QtWidgets.QCompleter(recent_users)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)

        # Set completer on the lineEdit
        lineEdit.setCompleter(completer)
        return lineEdit

    def log_in_with_offline_mode(self):
        # Start local session without the online features
        config.user_cfg["OFFLINE_MODE"] = True  # force offline mode
        self.pushButton_2.click()

    # on close event, close app
    def closeEvent(self, event):
        logger.info("Closing application")
        from celer_sight_ai import clean_exit

        try:
            clean_exit()
        except Exception as e:
            logger.error(e)
        sys.exit()

    def set_log_in_error_text(self, text):
        """Shows the error to the user in the log in dialog
        in case of a failed log in attepmt"""
        self.label_ThatshowsError.setText(text)
        return

    def check_connection_complete(self):
        import time

        while not self.connection_complete:  # sucessfully connected to server
            QtWidgets.QApplication.processEvents()
            time.sleep(0.0001)
        logger.debug("connection complete")
        return self.connection_complete

    def show_login_dialog(self):
        if not hasattr(self, "LogInDialog"):
            from celer_sight_ai.gui.custom_widgets.widget_spinner import WaitingSpinner

            self.LogInDialog = QtWidgets.QDialog()
            self.setupUi(self.LogInDialog)
            self.retranslateUi(self.LogInDialog)
            # spinner that runs while we are logging in.
            self.spinner_log_in = WaitingSpinner(
                self.LogInDialog,
                roundness=100.0,
                # opacity=1.0,
                fade=10.0,
                radius=17,
                lines=52,
                line_length=11,
                line_width=18,
                speed=0.5,
                color=QtGui.QColor(0, 255, 35),
            )
        self.LogInDialog.show()

    def initialize_log_in_dialog(self):
        QtWidgets.QApplication.processEvents()
        logger.info("initializing log in dialog.")
        settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        username, password = None, None

        if config.user_cfg["OFFLINE_MODE"]:
            if self.splash:
                self.splash.finish(self.LogInDialog)
            self.LogInDialog.hide()
            self.Lunch_application_after_authentication(
                {"result": "OK", "offline_mode": True}
            )
        elif (
            settings.value("isUserSignedOut")
            and settings.value("isUserSignedOut").lower() == "true"
        ):
            return
        else:
            if settings.value("LoadFromLastLogIn") != None:
                if settings.value("LoadFromLastLogIn").lower() == "true":
                    logger.info("Loading last log in settings")
                    logger.info("past loaded value is ")
                    from celer_sight_ai.configHandle import (
                        get_stored_password,
                        get_stored_username,
                    )

                    username = get_stored_username()
                    if username:
                        password = get_stored_password(username)
                    if username:
                        self.lineEdit.setText(username)
                    if password:
                        self.lineEdit_2.setText(password)
            if (
                settings.contains("AutoLogIn")
                and not config.user_cfg["FORCE_REJECT_AUTO_LOGIN"]
                and not self._is_logged_in
            ):

                if settings.value("AutoLogIn").lower() == "true":
                    logger.info("Auto log in is enabled")

                    self.LogInDialog.hide()
                    self.splash.showMessage("Signing in...")
                    self.AuthenticationRunner()
                    QtWidgets.QApplication.processEvents()
                    return

        self.splash.finish(self.LogInDialog)
        self.LogInDialog.show()
        self.LogInDialog.raise_()

    @config.threaded
    def AuthenticationRunner(
        self, provided_username=None, provided_password=None, jwt_refresh_token=None
    ):
        from celer_sight_ai import config

        username, password = None, None
        if config.user_cfg["OFFLINE_MODE"]:
            if not self._is_main_window_launched:
                config.global_signals.launch_main_window_after_log_in_signal.emit({})
            return
        logger.info(f"Starting log in worker {self.during_log_in}")
        if self.during_log_in == False:
            self.during_log_in = True
            logger.info("Athentification running")
            if provided_username:
                username = provided_username
            else:
                username = self.lineEdit.text()
            if provided_password:
                password = provided_password
            else:
                password = self.lineEdit_2.text()
            self.Authenticate(
                {
                    "username": username,
                    "password": password,
                    "jwt_refresh_token": jwt_refresh_token,
                }
            )

    def lunchUpdatingWindow(self):
        """
        lunches update window and starts updating, not sure if this works or not
        """
        # TODO: make sure this runs correctly.
        logger.info("Lunching updater window.")
        config.global_signals.warningSignal("Updating and restaring\n do not cancel.")
        self.updateWindow.WarningDialForm.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowType.WindowTitleHint
            | QtCore.Qt.CustomizeWindowHint
        )
        self.updateWindow.WarningDialForm.activateWindow()
        self.updateWindow.WarningDialForm.setWindowTitle("Updating")
        self.updateWindow.WarningDialForm.show()
        self.LogInDialog.hide()
        QtWidgets.QApplication.processEvents()

    def setUpdaterPercent(self, value):
        """updates the string on the splash window to reflect the percent of bytes downloaded from the total update.

        Args:
            value (float): The current percentage of the ongoing download
        """
        logger.debug("percent is ", value)
        if self.updateWindow:
            self.splash.showMessage("Updating: " + str(int(value)) + " %")
            pass
        else:
            logger.error("There was an error updating the percentage, exiting.")
            sys.exit()

    def sendUpdateSignalToUpdateDialog(self, status):
        """Sends signal that connects to the setUpdaterPercent() method

        Args:
            status (dict): dictionary containing the % complete of the update.
        """
        zz = float(status["percent_complete"])
        from celer_sight_ai import config

        try:
            config.global_signals.UpdaterWindowPercentSignal.emit(zz)
        except Exception as e:
            logger.error(e)
            sys.exit()

    def updateCurrentVersion(self, progress_callback=None):
        """
        Check for updates.

        Channel options are stable, beta & alpha
        Patches are only created & applied on the stable channel
        """
        from celer_sign_ai import __version__
        from pyupdater.client import Client

        from celer_sight_ai import config

        if config.user_cfg.OVERRIDE_VERSION:
            version = config.user_cfg.OVERRIDE_VERSION_NUMBER
        else:
            version = __version__

        from client_config import ClientConfig  # pylint: disable=import-error

        CLIENT_CONFIG = ClientConfig()
        logger.debug(f"Config public key is  {CLIENT_CONFIG.PUBLIC_KEY}")
        logger.debug(f"Config HTTP_TIMEOUT is {CLIENT_CONFIG.HTTP_TIMEOUT}")
        logger.debug(
            f"Config MAX_DOWNLOAD_RETRIES is {CLIENT_CONFIG.MAX_DOWNLOAD_RETRIES}"
        )
        logger.debug(f"Config UPDATE_URLS are {CLIENT_CONFIG.UPDATE_URLS}")
        from celer_sight_ai import config

        try:
            assert CLIENT_CONFIG.PUBLIC_KEY is not None
        except Exception as e:
            logger.error(e)
        client = Client(CLIENT_CONFIG, refresh=True)

        if "b" in config.APP_VERSION:
            logger.info(f"Downloading beta version : {config.APP_VERSION}")
            appUpdate = client.update_check(
                CLIENT_CONFIG.APP_NAME, config.APP_VERSION, channel="beta"
            )
        else:
            logger.info(f"Downloading production version : {config.APP_VERSION}")
            appUpdate = client.update_check(
                CLIENT_CONFIG.APP_NAME, config.APP_VERSION, channel="stable"
            )
        logger.info("Update is ")
        if appUpdate:
            if config.is_executable:
                config.global_signals.lunchUpdaterWindowSignal.emit()
                appUpdate.progress_hooks.append(self.sendUpdateSignalToUpdateDialog)
                downloaded = appUpdate.download()
                logger.info("download complete")
                if downloaded:
                    status = UpdateStatus.EXTRACTING_UPDATE_AND_RESTARTING
                    appUpdate.extract_restart()
                else:
                    status = UpdateStatus.UPDATE_DOWNLOAD_FAILED
            else:
                status = UpdateStatus.UPDATE_AVAILABLE_BUT_APP_NOT_FROZEN
        else:
            status = UpdateStatus.NO_AVAILABLE_UPDATES
        logger.info("finished updating with status ")
        return status

    def onUpdateCurrentVersionFINISH(self):
        """Runs when updateCurrentVersion() method is completed."""
        try:
            self.updateWindow.WarningDialForm.hide()
            self.updateWindow.WarningDialForm.close()
        except Exception as e:
            logger.error(e)
            pass
        self.LogInDialog.show()
        logger.info("Update comple")
        self.initialize_log_in_dialog()

    def setBluredBackground(self):
        self.blur = QtWidgets.QGraphicsBlurEffect(blurRadius=5)
        self.widget.setGraphicsEffect(self.blur)

    def AddShadowToWidget(self, widget, intensity=90):
        BR = 40  # blur radius
        xo = +5  # xoffset
        yo = 7  # yoffset
        colorGUI = QtGui.QColor(0, 0, 0, intensity)
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=BR, xOffset=xo, yOffset=yo, color=colorGUI
        )
        widget.setGraphicsEffect(shadow)

    def LunchRegistrationWindow(self):
        """Opens the registration window on the browser."""
        address = "https://www.biomarkerimaging.com/register"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(address))

    @staticmethod
    def authenticateMain(user, password):
        """
        It sends a request to the main server with the username and password, and returns the response

        :param user: The username of the user
        :param password: The password to authenticate with
        :return: The responce from the server
        """
        return config.sch.logIn(user, password)

    def Authenticate(self, creds, progress_callback=None):
        """
        The function Authenticate() is called when the user clicks the "Log In" button. It takes the
        username and password from the GUI and sends them to the server. If the server accepts the
        credentials, it returns a JWT token. The token is saved in the environment variable CelerSight_JWT

        :param creds: a dict that can contain username, password and jwt_refresh_token
        :param progress_callback: A callback function that will be called with the progress of the
        download. The callback function should take two parameters: the number of bytes downloaded so far,
        and the total number of bytes to download
        """
        self.during_log_in = True
        logger.info("Authenticating")
        from celer_sight_ai.core.file_client import FileClient

        client = FileClient(configHandle.getServerLogAddress())
        result = client.login(
            creds.get("username"), creds.get("password"), creds.get("jwt_refresh_token")
        )
        client.download_category_images()

        self.during_log_in = False
        if "error" in result:
            # this means we have an error code return to handle
            config.global_signals.set_text_log_in_error_signal.emit(result["error"])
            logger.error(result["error"])
            config.global_signals.show_log_in_dialog_signal.emit()
            config.global_signals.hide_splash_screen_signal.emit()
            self.LogInDialog.setEnabled(True)
            # show the log in dialog again
            return
        else:
            self._is_logged_in = True
            if self.remember_me_checkbox.isChecked():
                logger.info("Enabling remember me")
                # save the credentials
                from celer_sight_ai.configHandle import store_password, store_username

                # save the username
                if creds.get("username"):
                    store_username(creds.get("username"))
                if creds.get("password"):
                    store_password(creds.get("username"), creds.get("password"))
            if self.log_in_automatically_checkbox.isChecked():
                logger.info("Enabling auto log in")
                config.settings.setValue("AutoLogIn", "true")
                configHandle.store_jwt_token_for_auto_login(result["JWT_refresh"])
            else:
                logger.info("Disabling auto log in")
                config.settings.setValue("AutoLogIn", "false")

        if not self._is_main_window_launched:
            config.global_signals.launch_main_window_after_log_in_signal.emit(result)

    def Lunch_application_after_authentication(self, result: dict) -> None:
        """
        The function is called when the user presses the log in button. It checks if the credentials are
        correct and if they are it launches the main window

        :param result: The result of the login attempt
        """
        import celer_sight_ai.configHandle as configHandle
        from celer_sight_ai import __version__, config
        from celer_sight_ai.core import file_client

        logger.debug("Lunching main window after authentication")

        logger.debug(f"Log in result: {result}")

        # Hide log in window since we are successfully authenticated
        self.LogInDialog.hide()
        from celer_sight_ai import config

        if config.user_cfg["OFFLINE_MODE"]:
            config.cloud_user_variables = None

        # hide the log in window
        self.LogInDialog.hide()
        # show splash screen
        self.splash.show()
        # set message for loading assets
        self.splash.showMessage("Loading assets")
        # Load MainWindow

        from celer_sight_ai.celer_sight_core import Master_MainWindow

        self.gui_main = Master_MainWindow()
        from celer_sight_ai import config

        # instantiate client on config
        config.client = file_client.FileClient(
            configHandle.getServerLogAddress(), MainWindow=self.gui_main
        )
        if not config.user_cfg["OFFLINE_MODE"]:
            # set the jwt tokens from the login result
            config.client._update_jwt_tokens(result)

        logger.info("Mainwindow is running")
        self.gui_main.FinalizeMainWindow()
        logger.info("Mainwindow finalized")
        self.gui_main.ApplyStyleSheet()
        logger.info("Stylesheet applied to main window")
        self.gui_main.MainWindow.setWindowIcon(
            QtGui.QIcon(
                os.path.join("data", "celer_sight_icons", "app_logo_celer_sight.png")
            )
        )
        self.splash.hide()
        self.gui_main.MainWindow.show()
        self.LogInDialog.hide()
        logger.info("Window icon added")

        # normal log in, without loading a file
        logger.info("Showing organism selection dialog")
        self.gui_main.organism_selection.myDialog.show()
        self.gui_main.organism_selection.myDialog.setWindowModality(
            QtCore.Qt.WindowModality.ApplicationModal
        )
        self.gui_main.organism_selection.myDialog.raise_()
        if config.user_cfg["ANNOTATE_DATA_MODE"]:
            # automatically log in, set supercategory and categroy and load some images.
            self.gui_main.start_remote_annotation_session(without_prompt=True)
        QtWidgets.QApplication.processEvents()

        self.splash.hide()
        self.LogInDialog.setEnabled(True)
        self.connection_complete = True
        return

    def verify_folder_against_txt(self, version) -> bool:
        # make a connection to the server and get that file path
        import hashlib
        import platform

        import requests

        from celer_sight_ai import configHandle

        if config.user_cfg["OFFLINE_MODE"]:
            return True
        os = platform.system()

        connection_address = configHandle.get_files_hash_list_address() + f"/{version}"
        # request the file form the server
        response = requests.get(connection_address)
        if response.status_code != 200:
            logger.error(
                "Failed to validate files , skipping validation."
            )  # TODO: possible raise a fatal error here in the future.
            return

        # Read the expected hash dictionary from the .txt file

        expected_hash_dict = response.json()
        # celer sght ai folder
        # get the file location of the current file
        current_file_loc = os.path.dirname(os.path.realpath(__file__))
        # get the 3rd parent path
        folder_path = os.path.abspath(
            os.path.join(current_file_loc, os.pardir, os.pardir)
        )
        if config.user_cfg.FORCE_UPDATE:
            folder_path = config.user_cfg.FORCE_UPDATE_LOCATION
        # Iterate through the expected hash dictionary to verify each file
        for file_name, expected_hash in expected_hash_dict.items():
            # Construct the absolute path to the file in the folder
            file_path = os.path.join(folder_path, file_name)

            # Check if the file exists in the folder
            if not os.path.exists(file_path):
                print(f"File {file_name} does not exist in the folder.")
                return False

            # Generate the SHA256 hash for the file
            with open(file_path, "rb") as f:
                file_data = f.read()
                actual_hash = hashlib.sha256(file_data).hexdigest()

            # Compare the generated hash with the expected hash
            if expected_hash != actual_hash:
                print(f"Hash mismatch for file {file_name}.")
                return False

        # If all files are verified, return True
        return True


if __name__ == "__main__":
    import sys
