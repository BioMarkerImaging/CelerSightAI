import logging
import os
import unittest
from unittest.mock import patch

import pytest
import qttest_utils
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtTest import QTest

from celer_sight_ai import config
from celer_sight_ai.core.file_client import FileClient
from tests.base_gui_testcase import BaseOnlineGuiTestCase

logger = logging.getLogger(__name__)

DELAY_TIME = 200  # in ms


class TestLoginDuringAnalysis(BaseOnlineGuiTestCase):

    @pytest.mark.long
    @pytest.mark.online
    def test_login_during_analysis(self):
        app = self.app

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
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget.objectName() == "LogInDialog":
                login_dialog = widget
                break
        self.assertTrue(login_dialog.isVisible())

        # Perform login
        app.login_handler.lineEdit.setText(os.environ.get("USERNAME_ADMIN"))
        app.login_handler.lineEdit_2.setText(os.environ.get("PASSWORD_ADMIN"))
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
