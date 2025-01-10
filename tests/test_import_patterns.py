import os
from PyQt6.QtTest import QTest
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import sys
import unittest
import pytest
from celer_sight_ai import config
import logging
from tests import qttest_utils
from unittest.mock import patch
import numpy as np

# import shapely
from shapely.geometry import Polygon
from parameterized import parameterized
from tests.base_gui_testcase import BaseGuiTestCase

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
        "test_import_pattern": 0,  # empty mock entries, add first one
        "test_remote_process_part_2": 1,
    }
    return order.get(test_name, 99)


class CelerSightImportPatternsTest(BaseGuiTestCase):

    def setUp(self):
        celer_sight_home = os.environ.get("CELER_SIGHT_AI_HOME")
        assert celer_sight_home is not None, "CELER_SIGHT_AI_HOME is not set"
        self.test_dir = os.path.join(os.path.dirname(celer_sight_home), "tests")
        qttest_utils.wait_until_shown(self.app.MainWindow)

    @parameterized.expand(
        [
            (
                [
                    "fixtures//pattern_single_channel_per_folder"
                ],  # imported image paths , can be a directory
                {
                    "aup-": 3,
                },  # treatment name with expected loaded image amount
                ["red", "green", "blue"],  # channels
                "one treatment",  # action
            ),
            (
                ["fixtures//channel_pattern//image_urls"],
                {
                    "pl_ua": 5,
                },
                ["gfp", "dsred"],
                "yes, combine them",
            ),
            (
                ["fixtures//channel_pattern//multi_dir_urls"],
                {
                    "multi_dir_urls": 7,
                },
                ["GFP", "Texas Red"],
                "yes, combine them",
            ),
            (
                ["fixtures//channel_pattern//single_dir_url"],
                {
                    "pl_ua": 5,
                },
                ["gfp", "dsred"],
                "yes, combine them",
            ),
        ]
    )
    def test_import_pattern(
        self, image_paths, expected_loaded_image_amount, expected_channels, action
    ):
        from celer_sight_ai import configHandle, config
        import time

        # start ui
        app = self.app
        # wait for app to start
        # go to mainwindow
        qttest_utils.to_main_window(app, organism="worm", model_button_names=["body"])

        urls_to_be_added = []
        for image_path in image_paths:
            if not os.path.exists(os.path.join(self.test_dir, image_path)):
                raise FileNotFoundError(f"File {image_path} not found")
            urls_to_be_added.append(os.path.join(self.test_dir, image_path))
        app.viewer.load_files_by_drag_and_drop(urls_to_be_added)
        QTest.qWait(DELAY_TIME * 3)
        qttest_utils.click_on_action_dialog_with_button(app, action)
        QTest.qWait(DELAY_TIME * 3)
        # make sure that the treatments specified exist and the amount of images loaded is as expected
        current_group = app.DH.BLobj.get_current_group()
        for treatment_name, expected_amount in expected_loaded_image_amount.items():
            assert treatment_name in app.DH.BLobj.groups[current_group].conds
            assert (
                len(app.DH.BLobj.groups[current_group].conds[treatment_name].images)
                == expected_amount
            )
            for image_object in (
                app.DH.BLobj.groups[current_group].conds[treatment_name].images
            ):
                # wait until the image has channel list with timeout
                start = time.time()
                while isinstance(image_object.channel_list, type(None)):
                    QTest.qWait(DELAY_TIME)
                    if time.time() - start > 10:
                        break
                assert set(image_object.channel_list) == set(expected_channels)

        # # quit to the main window
        app.quit_project(without_prompt=True)


if __name__ == "__main__":
    unittest.main()
