import os
from PyQt6.QtTest import QTest
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import sys
import unittest

from celer_sight_ai import config

config.user_cfg["OFFLINE_MODE"] = True
from tests.base_image_testcase import BaseImageTestCase
from tests.base_gui_testcase import BaseGuiTestCase

import logging
from tests import qttest_utils
from unittest.mock import patch
import numpy as np

# import shapely
from shapely.geometry import Polygon
from parameterized import parameterized

logger = logging.getLogger(__name__)

os.environ["CELER_SIGHT_TESTING"] = "true"

ultra_high_res_image = "42784052-0cf6-40a8-9613-dacf5f93948f.tiff"
normal_image = "daf-2_D2_aup-1i_26.tif"


DELAY_TIME = 200


def run_single_test_suite():
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = custom_test_order
    suite = loader.loadTestsFromTestCase(CelerSightRemoteAnnotationAdminTest)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()


# Function to run the test suite multiple times
def run_tests_multiple_times(num_runs):
    for i in range(num_runs):
        print(f"Run {i + 1}/{num_runs}")
        if not run_single_test_suite():
            print(f"Errors or failures encountered in run {i + 1}")
            break
    else:
        print("All test runs completed successfully")


def custom_test_order(test_name, num):
    order = {
        "test_image_intensity_2D_rgb": 0,  # empty mock entries, add first one
        "test_remote_process_part_2": 1,
    }
    return order.get(test_name, 99)


class TestImageIntensityWithGUI(BaseGuiTestCase, BaseImageTestCase):
    def setUp(self):
        super().setUp()  # This ensures parent class setUp methods are called

    @parameterized.expand(BaseImageTestCase._load_mock_image_intensity_data)
    def test_image_intensity_2D_rgb(
        self,
        image_path,  # Will receive the fixture's "image_path"
        mean,  # Will receive the fixture's "mean"
        annotations,  # Will receive the fixture's "annotations"
    ):
        # start ui
        app = self.app
        # wait for app to start
        # go to mainwindow
        qttest_utils.to_main_window(app, organism="worm", model_button_names=["body"])
        urls_to_be_added = [os.path.join(self.test_dir, image_path)]
        for i in range(len(urls_to_be_added)):
            assert os.path.exists(
                urls_to_be_added[i]
            ), f"File / fixture {urls_to_be_added[i]} does not exist"
        app.viewer.load_files_by_drag_and_drop(
            urls_to_be_added,
            channel_pattern=False,
            treatment_pattern=False,
            auto_accept=True,
        )
        QTest.qWait(1000)
        # add imagej annotations
        for anno in annotations:
            qttest_utils.read_imagej_roi_with_polygon_tool(
                app, os.path.join(self.test_dir, anno)
            )
            QTest.qWait(DELAY_TIME)
        qttest_utils.do_analysis(app)
        QTest.qWait(DELAY_TIME)
        # go to Data tab of app
        qttest_utils.go_to_data_tab(app)
        # test if the values are as expected
        qttest_utils.assert_data_equals(app, roi_name="body", values_to_check=mean)

        # quit to the main window
        app.quit_project(without_prompt=True)


if __name__ == "__main__":

    # Number of times to run the tests
    num_runs = 1

    # Run the test suite multiple times
    run_tests_multiple_times(num_runs)
