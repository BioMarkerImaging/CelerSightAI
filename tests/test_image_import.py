import tifffile
import xmltodict
from glob import glob
import cv2
import numpy as np
import os
import sys
import time
import logging
import tempfile

logger = logging.getLogger(__name__)
# from tests.csight_test_loader import tags
import unittest

from celer_sight_ai.io.image_reader import read_specialized_image
import logging


class MyTest(unittest.TestCase):
    def setUp(self):

        from celer_sight_ai.config import start_jvm

        start_jvm()
        self.fixture_dir_abs_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
        self.path_images_tif = os.path.join(
            self.fixture_dir_abs_path, "tests/fixtures/import_images"
        )
        self.all_images_tif = glob(self.path_images_tif + "/*.tif") + glob(
            self.path_images_tif + "/*.TIF"
        )
        self.mock_proprietory_images = {
            "tests/fixtures/tissue_files/TCGA-HC-7820-01A-01-TS1.f9131ac5-c635-42a7-a383-634d90d212d4.svs": None
        }
        self.temp_dir = tempfile.mkdtemp()
        self.mock_image_data = {
            "PIR3_L1_TMRE_Image015.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
            },
            "4D-series.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
            },
            "Cell_2.tif": {
                "channels": ["gray"],
                "size_x": 251,
                "size_y": 449,
            },
            "multi-channel-4D-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "multi-channel-time-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "multi-channel-z-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "multi-channel.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
            },
            "N2_100x_150ms_4gain_2x2_L1_Image002.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 696,
                "size_y": 520,
                "physical_pixel_size_x": 352.77778048831453,
                "physical_pixel_size_y": 352.77778048831453,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1039,
                "size_y": 1444,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_23.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1484,
                "size_y": 1009,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_24.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1019,
                "size_y": 1672,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_25.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1761,
                "size_y": 643,
                "physical_pixel_size_x": 0.6917064397869545,
                "physical_pixel_size_y": 0.6917997516438892,
            },
            "single-channel.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
            },
            "TMRE_D1_gsk-3_C_02.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "TMRE_D1_gsk-3_C_10.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            # "TMRE_D1_gsk-3_EGTA_Overview.tif": None,
            "wt L1 TMRE_Image003.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
            },
            "z-series.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
            },
            # "TMRE_D1_gsk-3_UA+EGTA_06.tif": { # does not exists?
            #     "channels": ["FGW"],
            #     "size_x": 2457,
            #     "size_y": 2457,
            # },
            "neuronal_rosella_D5_C_05.tif": {
                "channels": ["FBW", "FGW"],
                "size_x": 2457,
                "size_y": 2457,
            },
            "daf-2_D2_aup-1i.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 2740,
                "size_y": 2740,
            },
            "20211005_LHE042_plane1_-324.425_raw-092_Cycle00001_Ch1_000001.ome.tif": {
                "size_x": 512,
                "size_y": 512,
                "channels": ["Ch1", "Ch2"],
                "is_ultra_high_res": False,
                "physical_pixel_size_x": 352.77777777777777,
                "physical_pixel_size_y": 352.77777777777777,
                "physical_pixel_unit_x": "µm",
                "physical_pixel_unit_y": "µm",
            },
            "Philips-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 45056,
                "size_y": 35840,
            },
            "pl_ua_1_gfp.tif": {
                "channels": ["GFP"],
                "size_x": 1992,
                "size_y": 1992,
            },
            "pl con_Top Slide_R_p01_0_A01f00d1.TIF": {
                "channels": ["gray"],
                "size_x": 2048,
                "size_y": 1536,
            },
            "control_Bottom Slide_D_p00_0_A01f11d1.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 2048,
                "size_y": 1536,
                "physical_pixel_size_x": 1.2380542388637508,
                "physical_pixel_size_y": 1.2380542388637508,
            },
        }

        self.mock_high_res_images = {
            # "20211005_LHE042_plane1_-324.425_raw-092_Cycle00001_Ch1_000001.ome.tif": None,
            # "CMU-1.ndpi": {
            #     "channels": ["red", "green", "blue"],
            #     "size_x": 51200,
            #     "size_y": 38144,
            # },
            "CMU-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 46000,
                "size_y": 32914,
            },
            "Philips-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 45056,
                "size_y": 35840,
            },
            "Philips-3.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 131072,
                "size_y": 100352,
            },
            # Needs to be converted to a pyramidal tiff first
            # "aup-1_13_Top Left Dish_TM_p00_0_A01f00d0.TIF": {
            #     "channels": ["red", "green", "blue"],
            #     "size_x": 17229,
            #     "size_y": 17526,
            # },
            "KPA01_2_13_Top Right Dish_TM_p00_0_A01f00d0.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 17231,
                "size_y": 17525,
            },
        }
        self.ultra_high_res_root_path = "tests/fixtures/import_images_high_res"

    def check_key_value_pairs(self, dict1, dict2):
        if isinstance(dict1, type(None)) and isinstance(dict2, type(None)):
            return
        # check that all key value pairs in dict1 are in dict2
        for key in dict1.keys():
            value = dict1.get(key)
            if isinstance(value, type(None)):
                self.assertEqual(dict2[key], None)
                self.assertEqual(dict2[key], None)
            elif isinstance(value, list):
                self.assertIsNone(np.testing.assert_array_equal(dict2.get(key), value))
                self.assertIsNone(np.testing.assert_array_equal(dict2.get(key), value))
            # Add special handling for floating point numbers
            elif isinstance(value, (float, np.floating)):
                self.assertTrue(np.allclose(dict2[key], value, rtol=1e-05, atol=1e-08))
            else:
                self.assertEqual(dict2[key], value)

    def test_extract_tile_data_from_tiff(self):
        from celer_sight_ai.io.image_reader import (
            extract_tile_data_from_tiff,
        )

        for img_path in self.mock_high_res_images:
            if not os.path.basename(img_path) in self.mock_image_data.keys():
                print("Skipping image: " + img_path)
                continue
            if not (
                os.path.basename(img_path).lower().endswith(".tiff")
                or os.path.basename(img_path).lower().endswith(".tif")
            ):
                print(os.path.basename(img_path))
                continue
            print("Testing image: " + img_path)
            try:
                result = extract_tile_data_from_tiff(
                    os.path.join(
                        self.fixture_dir_abs_path,
                        self.ultra_high_res_root_path,
                        img_path,
                    )
                )
                self.assertIsNotNone(result)
            except Exception as e:
                import traceback

                print(traceback.format_exc())
                print(e)
                self.fail()

    def tearDown(self):
        from celer_sight_ai.config import stop_jvm

        import shutil

        shutil.rmtree(self.temp_dir)

        stop_jvm()

    def test_tifffile_loader(self):
        # test that all of the images that should be loaded are loaded correctly and the ones that should not are not
        for img_path in self.all_images_tif:
            if not os.path.basename(img_path) in self.mock_image_data.keys():
                logger.info("Skipping image: " + img_path)
                continue
            if not "PIR3_L1_TMRE_Image015.tif" in img_path:
                continue
            logger.info("Testing image: " + img_path)
            try:
                result, arr_metadata = read_specialized_image(
                    os.path.join(self.fixture_dir_abs_path, img_path)
                )

            except Exception as e:
                import traceback

                print(traceback.format_exc())
                print(e)
                self.fail()
            self.check_key_value_pairs(
                self.mock_image_data[os.path.basename(img_path)], arr_metadata
            )
            logger.info("Testing image: " + img_path)
            if arr_metadata:
                logger.info(
                    "Shape: "
                    + str(arr_metadata["size_x"])
                    + str(arr_metadata["size_y"])
                )
                logger.info("Channels: " + str(arr_metadata["channels"]))
            else:
                logger.info("Invalid image.")

    def test_write_read_ome_tiff(self):
        """
        Write every tiff file and record its channels, read it back again and
        validate that the channels and shape are the same.
        """
        from celer_sight_ai.io.image_reader import write_ome_tiff
        from celer_sight_ai.io.image_reader import read_specialized_image

        skip_images = [
            "4D-series.ome.tif",
            "multi-channel-time-series.ome.tif",
            "multi-channel-4D-series.ome.tif",
            "multi-channel-z-series.ome.tif",
            "multi-channel.ome.tif",
            "z-series.ome.tif",
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif",  # channel is an array of color
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_23.tif",  # channel is an array of color
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_24.tif",  # channel is an array of color
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_25.tif",  # channel is an array of color
            "Cell_2.tif",
        ]
        for img_path in self.mock_image_data.keys():
            if img_path in skip_images:
                logger.info(f"Skipping image: {img_path}")
                continue
            # read it normaly
            logger.info(f"Testing image: {img_path}")
            arr, arr_metadata = read_specialized_image(
                os.path.join(self.path_images_tif, img_path)
            )
            logger.info(f"Shape: {arr.shape}")
            logger.info(f"Channels: {self.mock_image_data[img_path]['channels']}")
            # write it to ome-tiff
            logger.info(f"Writing to ome-tiff")
            result = write_ome_tiff(
                arr=arr,
                channels=self.mock_image_data[img_path]["channels"],
                tif_path=os.path.join(self.temp_dir, "test.tiff"),
                physical_pixel_size_x=self.mock_image_data[img_path].get(
                    "physical_pixel_size_x", None
                ),
                physical_pixel_size_y=self.mock_image_data[img_path].get(
                    "physical_pixel_size_y", None
                ),
                physical_pixel_unit_x=self.mock_image_data[img_path].get(
                    "physical_pixel_unit_x", None
                ),
                physical_pixel_unit_y=self.mock_image_data[img_path].get(
                    "physical_pixel_unit_y", None
                ),
            )
            logger.info("Reading it back.")
            self.assertTrue(result)
            # read it back
            result, arr_metadata = read_specialized_image(
                os.path.join(self.temp_dir, "test.tiff")
            )
            logger.info(f"Shape: {arr.shape}")
            logger.info(f"Channels: {self.mock_image_data[img_path]['channels']}")

            self.check_key_value_pairs(
                self.mock_image_data[os.path.basename(img_path)], arr_metadata
            )

    # def test_ultra_high_res_preview(self):
    #     from celer_sight_ai import config
    #     from celer_sight_ai.gui.custom_widgets.scene import readImage
    #     from celer_sight_ai.io.image_reader import (
    #         open_preview_with_tiffslide_image_reader,
    #         open_preview_with_openslide_image_reader,
    #         get_deep_zoom_by_tiffslide,
    #         create_pyramidal_tiff,
    #     )
    #     import time

    #     config.user_cfg["USER_WORKERS"] = False
    #     # test that all of the images that should be loaded are loaded correctly and the ones that should not are not
    #     for img_path in self.mock_high_res_images.keys():
    #         expected_val_key_pairs = self.mock_high_res_images[img_path]
    #         print("Testing image: " + os.path.basename(img_path))

    #         try:
    #             start = time.time()
    #             #  test thumbnail first
    #             result = readImage(
    #                 os.path.join(self.ultra_high_res_root_path, img_path),
    #                 for_interactive_zoom=False,
    #                 for_thumbnail=True,
    #                 avoid_loading_ultra_high_res_arrays_normaly=True,  # Interactive methods, quick loading etc
    #             )
    #             time_taken = time.time() - start
    #             print(
    #                 f"{os.path.basename(img_path)} Image read in {time_taken} seconds"
    #             )
    #             assert (
    #                 time_taken < 1
    #             ), f"{os.path.basename(img_path)} took {time_taken} seconds to load thumbnail"
    #             if isinstance(result, type(None)) or (
    #                 isinstance(result[0], type(None))
    #                 and isinstance(result[1], type(None))
    #             ):
    #                 self.assertEqual(expected_val_key_pairs, None)
    #                 continue
    #             self.check_key_value_pairs(expected_val_key_pairs, result[1])
    #             # test loading for interactive zoom
    #             start = time.time()
    #             result = readImage(
    #                 os.path.join(self.ultra_high_res_root_path, img_path),
    #                 for_interactive_zoom=True,
    #                 for_thumbnail=True,
    #                 avoid_loading_ultra_high_res_arrays_normaly=True,  # Interactive methods, quick loading etc
    #             )
    #             time_taken = time.time() - start
    #             print(
    #                 f"{os.path.basename(img_path)} Image read in {time_taken} seconds"
    #             )
    #             assert (
    #                 time_taken < 1
    #             ), f"{os.path.basename(img_path)} took {time_taken} seconds to load interactive zoom"
    #             print()
    #         except Exception as e:
    #             print(e)
    #             self.fail()

    #         im, arr_metadata = open_preview_with_openslide_image_reader(
    #             os.path.join(self.ultra_high_res_root_path, img_path)
    #         )
    #         self.check_key_value_pairs(expected_val_key_pairs, arr_metadata)

    #         print("Testing image: " + img_path)

    # def test_crop_ultra_high_res(self):
    #     from celer_sight_ai.gui.Utilities.scene import readImage

    #     img_path = "CMU-1.tiff"
    #     bbox = [17612, 21320, 17637, 21340]  # in x1 , y1 , x2 , y2
    #     # to x, y, w, h
    #     bbox = [
    #         bbox[0],
    #         bbox[1],
    #         bbox[2] - bbox[0],
    #         bbox[3] - bbox[1],
    #     ]
    #     result = readImage(
    #         os.path.join(self.ultra_high_res_root_path, img_path),
    #         for_interactive_zoom=False,
    #         for_thumbnail=False,
    #         bbox=bbox,
    #         avoid_loading_ultra_high_res_arrays_normaly=True,  # Interactive methods, quick loading etc
    #     )
    #     # save image result to disk to check it visually
    #     cv2.imwrite("test.jpg", result[0])

    # # def test_pattern_signle_channel_per_folder(self):
    # # tests/fixtures/pattern_single_channel_per_folder

    # def test_find_treatment_patterns_within_filepaths(self):
    #     from celer_sight_ai.gui.Utilities.scene import (
    #         find_treatment_patterns_within_filepaths,
    #     )

    #     file_list = self.get_file_list(5)
    #     # test 1 speretely
    #     file_list = self.get_file_list(1)
    #     # should find these patterns
    #     pats = [
    #         "TMRE_D1_mcu-1_C",
    #         "TMRE_D1_N2_UA",
    #         "TMRE_D1_gsk-3_UA",
    #         "TMRE_D1_gsk-3_UA+EGTA",
    #         "TMRE_D1_gsk-3_EGTA",
    #         "TMRE_D1_mcu-1_UA+EGTA",
    #         "TMRE_D1_mcu-1_UA",
    #         "TMRE_D1_mcu-1_EGTA",
    #         "TMRE_D1_N2_C",
    #         "TMRE_D1_N2_EGTA",
    #         "TMRE_D1_gsk-3_C",
    #         "TMRE_D1_N2_UA+EGTA",
    #     ]
    #     res = find_treatment_patterns_within_filepaths(file_list)
    #     assert set(list(res)) == set(pats)
    #     assert len(list(res)) == len(pats)

    #     # test 2 separetely
    #     file_list = self.get_file_list(2)
    #     pats = ["UroA N2 OPO50 DAY 4", "N2 OPO50 DAY 4"]
    #     res = find_treatment_patterns_within_filepaths(file_list)
    #     assert set(list(res.keys())) == set(pats)
    #     assert len(list(res.keys())) == len(pats)

    #     # test 2 + 3 together
    #     file_list = self.get_file_list(2) + self.get_file_list(3)
    #     pats = [
    #         "UroA N2 OPO50 DAY 4",
    #         "N2 OPO50 DAY 4",
    #         "UroA N2 OP50 DAY 8",
    #         "N2 OP50 DAY 8",
    #     ]
    #     res = find_treatment_patterns_within_filepaths(file_list)
    #     assert set(list(res.keys())) == set(pats)
    #     assert len(list(res.keys())) == len(pats)

    #     file_list = self.get_file_list(4)
    #     # remove all dsred
    #     file_list = [i for i in file_list if "dsred" not in i]
    #     file_list = file_list + [i.replace("drp-1(i)", "drp-3(i)") for i in file_list]
    #     file_list = [i.replace("gfp", "") for i in file_list]
    #     res = find_treatment_patterns_within_filepaths(file_list)

    #     print()

    #     return True

    def get_file_list(self, list_name=1):
        # return the list of filename within the fixture folder "path_fixtures"
        p = os.path.dirname(__file__)
        fix_dir = os.path.join(p, "fixtures", "path_fixtures")
        with open(os.path.join(fix_dir, str(list_name) + ".txt")) as f:
            file_list = f.read().splitlines()
        return file_list


if __name__ == "__main__":
    unittest.main()
