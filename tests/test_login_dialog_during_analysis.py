import os
from PyQt6.QtTest import QTest
from PyQt6 import QtCore, QtWidgets
import unittest
import logging
import qttest_utils
from unittest.mock import patch
from celer_sight_ai.core.file_client import FileClient
from celer_sight_ai import config
from tests.base_gui_testcase import BaseGuiTestCase
from tests.base_online_testcase import BaseOnlineTestCase

logger = logging.getLogger(__name__)

DELAY_TIME = 200  # in ms


class TestLoginDuringAnalysis(BaseGuiTestCase, BaseOnlineTestCase):

    def test_login_during_analysis(self):
        app = self.app
        qttest_utils.wait_until_shown(app.MainWindow)
        qttest_utils.to_main_window(app)

        # Load some test image
        test_image_path = (
            "/path/to/test/image.tif"  # Replace with actual test image path
        )
        if os.path.exists(test_image_path):
            app.viewer.load_files_by_drag_and_drop([test_image_path], auto_accept=True)
            QTest.qWait(DELAY_TIME * 2)

        config.client.jwt = None
        config.client.jwt_long = None

        # Trigger an action that requires authentication
        # This should cause the login dialog to appear
        config.client.get_available_models()
        QTest.qWait(DELAY_TIME)

        # Verify login dialog is shown
        login_dialog = app.login_handler.LogInDialog
        self.assertTrue(login_dialog.isVisible())

        # Perform login
        app.login_handler.lineEdit.setText(os.environ.get("USERNAME_USER"))
        app.login_handler.lineEdit_2.setText(os.environ.get("PASSWORD_USER"))
        QTest.qWait(DELAY_TIME)

        # Click login button
        app.login_handler.pushButton_2.click()
        QTest.qWait(DELAY_TIME * 2)

        # Verify login dialog is hidden
        self.assertFalse(login_dialog.isVisible())

        # Verify main window is still visible and active
        self.assertTrue(app.MainWindow.isVisible())
        self.assertTrue(app.MainWindow.isActiveWindow())

        # Verify the viewer still has the image loaded
        if os.path.exists(test_image_path):
            self.assertGreater(len(app.viewer.layers), 0)


if __name__ == "__main__":
    unittest.main()
