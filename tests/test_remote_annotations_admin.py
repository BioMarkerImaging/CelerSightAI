import logging
import os
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pytest
from parameterized import parameterized
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtTest import QTest

# import shapely
from shapely.geometry import Polygon

from celer_sight_ai import config
from tests import qttest_utils
from tests.base_gui_testcase import BaseGuiTestCase
from tests.base_online_testcase import BaseOnlineTestCase

logger = logging.getLogger(__name__)

os.environ["CELER_SIGHT_TESTING"] = "true"

ultra_high_res_image = "42784052-0cf6-40a8-9613-dacf5f93948f.tiff"
normal_image = "daf-2_D2_aup-1i_26.tif"
# first and second points for the bounding box
bb_points_for_ultra_high_res = [
    [[8257, 10126], [8272, 10094]],
    [[8273, 10116], [8290, 10091]],
    [[7260, 10189], [7287, 10152]],
]


def polygons_almost_equal(polygon1: np.ndarray, polygon2: np.ndarray, tolerance):
    """
    Check if two polygons are almost equal within a given tolerance.

    Args:
    - polygon1: The first polygon (numpy object)
    - polygon2: The second polygon (numpy object)
    - tolerance: The allowed difference in area and centroid distance

    Returns:
    - bool: True if polygons are almost equal, False otherwise
    """
    # Convert to shapely polygons
    polygon1 = Polygon(polygon1)
    polygon2 = Polygon(polygon2)

    # Check if areas are almost equal
    area_diff = abs(polygon1.area - polygon2.area)
    if area_diff > tolerance:
        return False

    # Check if centroids are almost at the same location
    centroid_diff = polygon1.centroid.distance(polygon2.centroid)
    if centroid_diff > tolerance:
        return False

    # Optionally, check if polygons overlap significantly
    intersection_area = polygon1.intersection(polygon2).area
    if intersection_area < min(polygon1.area, polygon2.area) - tolerance:
        return False

    return True


def get_remote_annotation_fixture():
    yml_path = os.path.exists(
        os.path.join(
            os.path.dirname(os.environ["CELER_SIGHT_AI_HOME"]),
            "tests",
            "fixtures",
            "user_settings_fixtures",
            "remote_annotate_fixture.yml",
        )
    )
    # read the yml file and return the contents
    with open(yml_path) as f:
        return f.read()


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
        "test_remote_process_part_1": 0,  # empty mock entries, add first one
        "test_remote_process_part_2": 1,
    }
    return order.get(test_name, 99)


class CelerSightRemoteAnnotationAdminTest(BaseGuiTestCase, BaseOnlineTestCase):

    @pytest.mark.long
    @pytest.mark.online
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
    def test_remote_process_part_1(
        self, image_path, bb_points, width, height, image_size
    ):
        import time

        from celer_sight_ai import config, configHandle

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
            qttest_utils.magic_box_predict(
                app,
                [
                    bb_point_pair[0][0],
                    bb_point_pair[0][1],
                    bb_point_pair[1][0],
                    bb_point_pair[1][1],
                ],
            )
        # contribute the images through the ui
        qttest_utils.contribute_images(app)

        ## Delete all mock obbjects from the server ##

        empty_mock_objects_address = (
            configHandle.getServerLogAddress()
            + "/api/v1/admin/empty_mock_image_objects"
        )
        response = config.client.session.post(empty_mock_objects_address)
        assert response.status_code == 200

        # wait 10 seconds for the effects to take place on the
        # server side
        time.sleep(13)
        # TODO validate the images were contributed through the admin api
        # # get the current objects in the mock directory
        get_mock_objects_address = (
            configHandle.getServerLogAddress() + "/api/v1/admin/get_mock_image_objects"
        )
        response = config.client.session.get(get_mock_objects_address)
        assert response.status_code == 200
        image_objects_on_server = response.json()["image_objects"]
        if not len(image_objects_on_server) == 1:
            # wait another 5 seconds
            time.sleep(5)
            response = config.client.session.get(get_mock_objects_address)
            image_objects_on_server = response.json()["image_objects"]
        # # make sure that the image has been added to the server as mock
        assert len(image_objects_on_server) == 1
        # make sure that the image size matches the original image
        assert image_objects_on_server[0]["width"] == width
        assert image_objects_on_server[0]["height"] == height
        assert image_objects_on_server[0]["image_size"] == image_size

    def test_remote_process_part_2(self):
        # import celer_sight_ai
        from celer_sight_ai import config, configHandle

        # patch the .yml imported file so that we activate the remote annotation
        os.environ["CELER_SIGHT_ALTERNATIVE_SETTINGS"] = os.path.join(
            os.path.dirname(os.environ["CELER_SIGHT_AI_HOME"]),
            "tests/fixtures/user_settings_fixtures/remote_annotate_fixture.yml",
        )
        config.USER_CONFIG_LOADED = False
        # start ui
        app = self.app  # qttest_utils.get_gui_main()

        # wait for app to start
        # qttest_utils.wait_until_shown(app.MainWindow)
        # reload user settings
        app.reload_config_user_settings()
        app.start_remote_annotation_session(without_prompt=True)
        QTest.qWait(1000)
        # make sure that there is one image in the scene
        assert len(app.DH.BLobj.groups["default"].conds["images"].images) == 1
        assert app.DH.BLobj.groups["default"].conds["images"].images[0]._is_remote
        QTest.qWait(DELAY_TIME)
        qttest_utils.wait_until_current_remote_image_has_been_downloaded(app)
        # get all annotation in the current image
        mask_object = next(
            app.DH.BLobj.get_all_mask_objects_for_image(
                group_name="default", condition_name="images", image_idx=0
            )
        )
        mask_object_uuid = mask_object.unique_id
        image_uuid = app.DH.BLobj.groups["default"].conds["images"].images[0].unique_id
        # get the coordinates of the mask object (just the outer ones with [0])
        mask_object_coords = mask_object.get_array_for_storing()[0]
        # get the image object uuid

        # delete mask object
        annotetion_mask_item = mask_object.get_annotation_item()
        annotetion_mask_item.DeleteMask()
        QTest.qWait(DELAY_TIME)

        #### verify that the cloud annotation is deleted ####

        # draw cloud annotations
        get_mock_objects_address = (
            configHandle.getServerLogAddress() + "/api/v1/admin/get_mock_image_objects"
        )
        response = config.client.session.get(get_mock_objects_address)
        assert response.status_code == 200
        image_objects_on_server = [
            i for i in response.json()["image_objects"] if i["image_uuid"] == image_uuid
        ]
        assert len(image_objects_on_server) == 1
        image_object_on_server = image_objects_on_server[0]
        # make sure annotation is deleted
        assert (
            len(
                [
                    anno
                    for anno in image_object_on_server["annotations"]
                    if anno["annotation_uuid"] == mask_object_uuid
                ]
            )
            == 0
        )

        # create a new annotation and make sure that it is added to the server
        added_annotation_uuid = qttest_utils.draw_mask_by_array(app, mask_object_coords)
        QTest.qWait(1500)
        # get the mask object from the server
        response = config.client.session.get(get_mock_objects_address)
        assert response.status_code == 200
        # get all annotation arrays
        annotation_data = [
            [i["data"][0] for i in x["annotations"]]
            for x in response.json()["image_objects"]
        ][0]
        matched_annotations = [
            i
            for i in annotation_data
            if polygons_almost_equal(
                np.array(mask_object_coords.round(), dtype=np.uint32),
                np.array(i, dtype=np.uint32),
                200,
            )
        ]
        # make sure no matched annotation found, since we deleted the annotations
        assert len(matched_annotations) == 1


if __name__ == "__main__":

    # Number of times to run the tests
    num_runs = 10

    # Run the test suite multiple times
    run_tests_multiple_times(num_runs)
