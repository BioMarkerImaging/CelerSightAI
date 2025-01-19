import logging
import os
import sys
import unittest

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtTest import QTest

from celer_sight_ai import config
from tests import qttest_utils
from tests.base_gui_testcase import BaseGuiTestCase

logger = logging.getLogger(__name__)

ultra_high_res_image = "42784052-0cf6-40a8-9613-dacf5f93948f.tiff"
normal_image = "daf-2_D2_aup-1i_26.tif"
random_treatment_names = [
    "Oqid2afd",
    "VnAPf5fM7",
    "sX2x1skL",
    "U0skyanmcu",
    "BnAqCmu",
    "ImDVGDt3PF",
    "MvJJgM",
    "soAYpNk",
    "Fxnxbrxs",
    "mmdX",
    "Jw1dc7pm",
    "Iadsz6um7",
    "Zqszsif6",
    "UPvdbv",
    "5c0qvol",
    "UDhgntcN",
    "7emadvoa",
    "Soickmo",
    "sI14aPk2",
    "yUVmaaxG",
    "A4vNQs",
    "Yaytuq",
    "Leqpyz",
    "HS2jZHxESmOs",
    "6vfSqBI",
    "CWpS",
    "hWTOaCm",
    "ypQE5Yxl7V",
    "ywBZVTP0P",
    "Ypp0m",
    "S56wybdnzs",
    "Xmpwsqb",
]

# first and second points for the bounding box
bb_points_for_ultra_high_res = [
    [[8257, 10126], [8272, 10094]],
    [[8273, 10116], [8290, 10091]],
    [[7260, 10189], [7287, 10152]],
]
os.environ["CELER_SIGHT_TESTING"] = "true"

DELAY_TIME = 400  # in ms


class CelerSightTestSimple(BaseGuiTestCase):

    @pytest.mark.long
    def test_one(self):
        import time

        app = self.app

        # download assets if needed
        config.client.download_test_fixtures()
        time.sleep(0.1)
        while config.client.downloading_test_fixtures:
            time.sleep(0.03)
            QtWidgets.QApplication.processEvents()

        urls_to_be_added = [
            os.path.join(config.APP_DATA_PATH, "fixtures", ultra_high_res_image)
        ]
        QTest.qWait(DELAY_TIME * 4)
        # do magic box predict
        app.viewer.load_files_by_drag_and_drop(urls_to_be_added, auto_accept=True)
        QTest.qWait(DELAY_TIME * 3)
        # click on the first image, to make sure its loaded
        qttest_utils.click_on_image_button(app, 0)
        QTest.qWait(DELAY_TIME * 3)
        # add annotations with magic box
        for bb_point_pair in bb_points_for_ultra_high_res:
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
            QtWidgets.QApplication.processEvents()
            QTest.qWait(8 * DELAY_TIME)
        # make sure that there are 3 annotations
        assert (
            len([i for i in app.DH.BLobj.get_all_mask_objects()]) == 3
        ), f"Expected 3 annotations , got {len([i for i in app.DH.BLobj.get_all_mask_objects()])}"
        filename_save_location = os.path.join(config.APP_DATA_PATH, "temp")
        if not os.path.exists(filename_save_location):
            os.makedirs(filename_save_location)
        filename_save_location = os.path.join(
            filename_save_location, "test_file_celer_sight.bmics"
        )
        # do this 3 times to make sure no errors come up
        repeats = 1
        for i in range(repeats):
            # save file to disk
            groups_dict, filename = app.save_celer_sight_file(filename_save_location)
            QTest.qWait(600)
            qttest_utils.close_notification_dialog()
            # delete all treatments
            qttest_utils.clear_all_treatments(app)
            # reload the file
            app.load_celer_sight_file(filename_save_location)
            # make sure that the file has been read successfully
            QTest.qWait(600)

            # ui_qtbot_tools.check_data_corruption(qtbot , app)

        qttest_utils.clear_all_treatments(app)

        # open a normal image, create annotations and compare treatments
        # load 20 images for 5 treatments
        urls_to_be_added = [
            os.path.join(config.APP_DATA_PATH, "fixtures", normal_image)
        ]

        import random

        # experiment matrix -> N treatments, N images, [intensity experiment, particle experiment] ,rename the treatment, delete N images, delete N treatments
        possibility_matrix = [
            [1, 10],
            [3, 40],
            ["intensity", "particle"],
            ["yes", "no"],  # wether or not to rename the treatment
            [0, 100],  # in % of total images
            [0, 100],  # in % of total treatments
        ]
        # ui_qtbot_tools.check_data_corruption(qtbot , app)
        tot_treatments = random.randint(
            possibility_matrix[0][0], possibility_matrix[0][1]
        )
        # create random names for each treatment
        treatment_names = random.sample(random_treatment_names, tot_treatments)
        logger.info(
            f"Creating {tot_treatments} treatments with names {treatment_names}"
        )
        for i, treatment_name in enumerate(treatment_names):
            # multiply by 20
            qttest_utils.record_DH_data(app)
            total_images_to_add = random.randint(
                possibility_matrix[1][0], possibility_matrix[1][1]
            )
            logger.info(
                f"Adding {total_images_to_add} images to treatment {treatment_name}"
            )
            urls_to_be_added_multiple = urls_to_be_added * total_images_to_add
            app.viewer.load_files_by_drag_and_drop(
                urls_to_be_added_multiple, auto_accept=True
            )
            QTest.qWait(500)
            qttest_utils.wait_until_ui_settles(app)
            qttest_utils.deep_diff(config.DH_data, qttest_utils.get_data(app))
            qttest_utils.record_DH_data(app)
            current_treatment_name = app.DH.BLobj.get_current_condition()

            # ui_qtbot_tools.check_data_corruption(qtbot , app)

            # rename the treatment
            if random.sample(possibility_matrix[3], 1)[0] == "yes":
                logger.info(
                    f"Renaming treatment from {app.DH.BLobj.get_current_condition()} to {treatment_name}"
                )
                # get the current treatment name
                current_treatment_name = app.DH.BLobj.get_current_condition()
                result = qttest_utils.rename_treatment(
                    app, current_treatment_name, treatment_name
                )
                if not result:
                    logger.error("Error renaming treatment")
                    sys.exit()
                QTest.qWait(1000)

            amount_of_images_to_remove = int(
                len(urls_to_be_added)
                * random.randint(possibility_matrix[4][0], possibility_matrix[4][1])
                / 100
            )

            # ui_qtbot_tools.check_data_corruption(qtbot , app)

            # amount_of_images_to_remove = 1
            while amount_of_images_to_remove > 0:
                total_images = len([i for i in app.DH.BLobj.get_all_image_objects()])
                image_idx = random.randint(0, total_images - 1)
                logger.info(f"Deleting image at index {image_idx}")
                qttest_utils.delete_image_on_current_treatment(app, image_idx)
                QTest.qWait(200)
                amount_of_images_to_remove -= 1
            qttest_utils.deep_diff(config.DH_data, qttest_utils.get_data(app))
            qttest_utils.record_DH_data(app)

        return True


if __name__ == "__main__":
    unittest.main()
