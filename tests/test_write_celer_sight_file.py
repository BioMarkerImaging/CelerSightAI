import logging
import os
import unittest

import numpy as np
import pytest
import qttest_utils
from parameterized import parameterized
from PyQt6.QtTest import QTest
from tqdm import tqdm

from celer_sight_ai import config
from tests.base_gui_testcase import BaseGuiTestCase
from tests.base_image_testcase import BaseImageTestCase

logger = logging.getLogger(__name__)

os.environ["CELER_SIGHT_TESTING"] = "true"

DELAY_TIME = 200  # in ms


class TestCelerSightFile(BaseGuiTestCase, BaseImageTestCase):
    @pytest.mark.skip(reason="There is an issue with the test")
    @pytest.mark.long
    def test_write_read_celer_sight_file(self):
        for image_path, image_info in tqdm(self.mock_all_images.items()):
            if not image_info.get("readable"):
                continue
            self.write_celer_sight_file((image_path,))
            self.read_celer_sight_file()

    def write_celer_sight_file(self, image_paths: tuple = ()):
        import math

        qttest_utils.to_main_window(self.app)

        urls_to_be_added = image_paths
        for image_path in urls_to_be_added:
            assert os.path.exists(image_path), f"File does not exist: {image_path}"
        QTest.qWait(DELAY_TIME * 10)

        self.app.viewer.load_files_by_drag_and_drop(urls_to_be_added, auto_accept=True)
        QTest.qWait(DELAY_TIME * 10)

        current_image_uuid = self.app.DH.BLobj.get_current_image_uuid()
        current_image_object = self.app.DH.BLobj.get_image_object_by_uuid(
            current_image_uuid
        )
        current_image_size = current_image_object.SizeX, current_image_object.SizeY

        center = [current_image_size[0] // 2, current_image_size[1] // 2]
        # generate a polygon with 6 points in the center of the image
        point_array = [
            [
                center[0] + 40 * math.cos(2 * math.pi * i / 6),
                center[1] + 40 * math.sin(2 * math.pi * i / 6),
            ]
            for i in range(6)
        ]
        qttest_utils.draw_mask_by_array(self.app, np.array(point_array))
        QTest.qWait(DELAY_TIME * 10)

        filename_save_location = os.path.join(config.APP_DATA_PATH, "temp")
        if not os.path.exists(filename_save_location):
            os.makedirs(filename_save_location)
        filename_save_location = os.path.join(
            filename_save_location, "test_file_celer_sight.bmics"
        )

        groups_dict, filename = self.app.save_celer_sight_file(filename_save_location)
        qttest_utils.close_notification_dialog()
        self.app.quit_project(without_prompt=True)
        return True

    @pytest.mark.long
    def read_celer_sight_file(self):
        qttest_utils.to_main_window(self.app)

        filename_save_location = os.path.join(
            config.APP_DATA_PATH, "temp", "test_file_celer_sight.bmics"
        )
        self.app.load_celer_sight_file(filename_save_location)
        QTest.qWait(DELAY_TIME)
        # make sure there is one image loaded
        assert (
            len(self.app.DH.BLobj.get_all_image_objects()) == 1
        ), "There should be one image loaded"
        self.app.quit_project(without_prompt=True)

        return True


if __name__ == "__main__":
    unittest.main()
