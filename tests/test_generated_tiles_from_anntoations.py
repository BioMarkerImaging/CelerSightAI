from glob import glob
from PyQt6.QtTest import QTest
from PyQt6 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import os
import sys
import time
import copy
import unittest
from tests import qttest_utils
from parameterized import parameterized

sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai.io.image_reader import read_specialized_image
import logging
from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
    gather_cfgs,
    process_cfg_for_grid_button_image_selector,
    validate_cfg,
)
from celer_sight_ai.io.data_handler import (
    overlaps,
    build_graph,
    get_tile_range_from_annotation_size,
    find_minimum_groups,
    get_tile_range_from_group,
)

logger = logging.getLogger(__name__)
DELAY_TIME = 200


def validate_all_intervals_overlap(
    grouped_keys: list = None, intervals: dict = None
) -> bool:
    # get all relevant intervals
    intervals = [intervals[key] for key in grouped_keys]
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            if not overlaps(intervals[i], intervals[j]):
                print(f"Error: {intervals[i]} and {intervals[j]}")
                return False
            else:
                print(f"Ok: {intervals[i]} and {intervals[j]}")
    return True


os.environ["CELER_SIGHT_TESTING"] = "true"
ultra_high_res_image = "42784052-0cf6-40a8-9613-dacf5f93948f.tiff"
normal_image = "daf-2_D2_aup-1i_26.tif"
# first and second points for the bounding box
bb_points_for_ultra_high_res = [
    [[8257, 10126], [8272, 10094]],
    [[8273, 10116], [8290, 10091]],
    [[7260, 10189], [7287, 10152]],
]


class TestCategoryConfigs(unittest.TestCase):
    def test_case_1(self):
        MIN_PERCENTAGE = 0.03  # 3%
        MAX_PERCENTAGE = 0.14  # 24%
        widths = {
            "c1": 100,
            "c2": 30,
            "c3": 120,
            "c4": 200,
            "c5": 50,
            "c6": 220,
            "c7": 300,
        }
        # convert to percentage
        widths = {
            w: get_tile_range_from_annotation_size(
                widths[w], MIN_PERCENTAGE, MAX_PERCENTAGE
            )
            for w in widths
        }
        print(widths)
        min_groups = find_minimum_groups(copy.deepcopy(widths))
        # convert intervals back to width
        print(widths)
        for group in min_groups:
            print("------------Interval: ", group, "----------------")
            group_values = [widths[key] for key in group]
            print(get_tile_range_from_group(group_values))
            assert validate_all_intervals_overlap(group, intervals=widths)
        # determin the groups required for the rest of the items


class TestAnnotationSizeForInfereceFromUI(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        # start the app
        cls.app = qttest_utils.get_gui_main()
        qttest_utils.wait_until_shown(cls.app.MainWindow)

    @parameterized.expand(
        [
            (
                ultra_high_res_image,
                bb_points_for_ultra_high_res,
                17229,  # width
                17526,  # height
                56013527,  # image_size
            ),
        ]
    )
    def test_case_1(self, image_path, bb_points, width, height, image_size):
        from celer_sight_ai import configHandle, config
        import time

        app = self.app
        # wait for app to start
        # go to mainwindow
        qttest_utils.to_main_window(
            app, organism="on_plate", model_button_names=["worm eggs"]
        )
        # load up an image
        urls_to_be_added = [os.path.join(config.APP_DATA_PATH, "fixtures", image_path)]
        QTest.qWait(DELAY_TIME)
        app.viewer.load_files_by_drag_and_drop(urls_to_be_added, auto_accept=True)
        QTest.qWait(DELAY_TIME)
        # do magic box predict
        # add annotations with magic box
        for bb_point_pair in bb_points:
            print(f"Adding annotation with magic box {bb_point_pair}")
            app = qttest_utils.zoom_to_box(
                app,
                [
                    bb_point_pair[0][0],
                    bb_point_pair[0][1],
                    bb_point_pair[1][0],
                    bb_point_pair[1][1],
                ],
            )
            qttest_utils.magic_box_predict(app, bb_point_pair[0], bb_point_pair[1])


if __name__ == "__main__":
    unittest.main()
