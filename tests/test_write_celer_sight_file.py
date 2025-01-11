import os
from PyQt6.QtTest import QTest
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import unittest
import pytest
from celer_sight_ai import config
import logging
import qttest_utils

logger = logging.getLogger(__name__)

os.environ["CELER_SIGHT_TESTING"] = "true"

DELAY_TIME = 200  # in ms


class TestCelerSightFile:
    def setUp(self):
        # import celer_sight_ai main module
        self.gui_main = qttest_utils.get_gui_main(offline=True)

    def test_write_read_celer_sight_file(self):
        self.write_celer_sight_file()
        self.read_celer_sight_file()

    def write_celer_sight_file(self):
        app = self.gui_main
        qttest_utils.wait_until_shown(app.MainWindow)
        qttest_utils.to_main_window(app)

        urls_to_be_added = [
            "/Users/mchaniotakis/Downloads/Day 3 egglaying/combined/Day 3/aup-1_15_3.2023-12-14-13-47-12/aup-1_15_3_Bottom Right Dish_TM_p00_0_A01f00d0.TIF"
        ]
        assert os.path.exists(urls_to_be_added[0])
        QTest.qWait(DELAY_TIME * 10)

        app.viewer.load_files_by_drag_and_drop(urls_to_be_added, auto_accept=True)
        QTest.qWait(DELAY_TIME * 10)

        app = qttest_utils.zoom_to_box(app, [12795, 9518, 12830, 9544])
        QTest.qWait(DELAY_TIME * 20)

        qttest_utils.magic_box_predict(app, [12795, 9518], [12830, 9544])
        qttest_utils.close_notification_dialog()

        filename_save_location = os.path.join(config.APP_DATA_PATH, "temp")
        if not os.path.exists(filename_save_location):
            os.makedirs(filename_save_location)
        filename_save_location = os.path.join(
            filename_save_location, "test_file_celer_sight.bmics"
        )

        groups_dict, filename = app.save_celer_sight_file(filename_save_location)
        return True

    def read_celer_sight_file(self):
        app = self.gui_main
        qttest_utils.wait_until_shown(app.MainWindow)
        qttest_utils.to_main_window(app)

        filename_save_location = os.path.join(
            config.APP_DATA_PATH, "temp", "test_file_celer_sight.bmics"
        )
        app.load_celer_sight_file(filename_save_location)
        QTest.qWait(DELAY_TIME * 100)
        return True


if __name__ == "__main__":
    unittest.main()
