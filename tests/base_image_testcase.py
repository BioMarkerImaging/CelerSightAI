import logging
import os
from glob import glob

import numpy as np

from tests.base_test_case import BaseTestCase

logger = logging.getLogger(__name__)


class BaseImageTestCase(BaseTestCase):
    """Base class for image-related tests providing common test fixtures and utilities."""

    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.join(
            os.path.dirname(os.environ.get("CELER_SIGHT_AI_HOME") or ""), "tests"
        )
        super().setUpClass()
        """Set up class-level test fixtures."""

        cls.fixture_dir_abs_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
        cls.path_images_tif = os.path.join(
            cls.fixture_dir_abs_path, "tests/fixtures/import_images"
        )
        cls.all_images_tif = glob(cls.path_images_tif + "/*.tif") + glob(
            cls.path_images_tif + "/*.TIF"
        )
        cls.ultra_high_res_root_path = "fixtures/import_images_high_res"

        cls.cropped_ultra_high_res_test_file = os.path.join(
            cls.fixture_dir_abs_path,
            "tests/fixtures/import_images_high_res/tiff_slide_test.tiff",
        )

        # Load test data configurations
        cls.mock_image_data = cls._load_mock_image_data()
        cls.minimal_images_tif = cls._get_short_image_data()
        cls.mock_high_res_images = cls._load_mock_high_res_images()
        cls.mock_all_images = cls._load_mock_write_load_celer_sight_file()
        cls.mock_proprietory_images = {
            "tests/fixtures/tissue_files/TCGA-HC-7820-01A-01-TS1.f9131ac5-c635-42a7-a383-634d90d212d4.svs": None
        }

    def check_key_value_pairs(self, dict1, dict2):
        """Compare two dictionaries with special handling for None and numpy arrays."""
        if isinstance(dict1, type(None)) and isinstance(dict2, type(None)):
            return

        for key in dict1.keys():
            value = dict1.get(key)
            if isinstance(value, type(None)):
                self.assertEqual(dict2[key], None)
            elif isinstance(value, list):
                self.assertIsNone(np.testing.assert_array_equal(dict2.get(key), value))
            elif isinstance(value, (float, np.floating)):
                self.assertTrue(
                    np.allclose(float(dict2[key]), value, rtol=1e-05, atol=1e-08)
                )
            else:
                self.assertEqual(dict2[key], value)

    @classmethod
    def _load_mock_coloc_data(cls):
        return [
            (
                "test_assets/sy441.jpg",  # image
                {  # values
                    "pearson": 0.656,
                    "spearman": 0.800,
                },
            )
        ]

    @classmethod
    def _load_mock_image_intensity_data(cls):
        return [
            (
                "fixtures/image_intensity/red_green.tif",  # image path
                {
                    "mean": {"green": [20.230], "red": [10.170]}
                },  # expected intensity valufves
                ["fixtures/image_intensity/red_green_tif"],  # annotations
            ),
            (
                "fixtures/image_intensity/red_brightfield.tif",
                {"mean": {"fgw": [226.177], "fbw": [276.116]}},
                ["fixtures/image_intensity/red_brightfield_tif"],
            ),
        ]

    @classmethod
    def _load_mock_write_load_celer_sight_file(cls):
        # Combine both dictionaries instead of just their keys
        return {**cls._load_mock_image_data(), **cls._load_mock_high_res_images()}

    @classmethod
    def _get_short_image_data(cls):
        short_data_names = [
            "PIR3_L1_TMRE_Image015.tif",
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif",
        ]
        return {
            os.path.join(cls.path_images_tif, key): cls.mock_image_data[
                os.path.join(cls.path_images_tif, key)
            ]
            for key in short_data_names
        }

    @classmethod
    def _load_mock_image_data(cls):
        """Load mock image data configuration."""
        # Define base dictionary with relative paths
        all_files = {
            "PIR3_L1_TMRE_Image015.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
                "readable": True,
            },
            "4D-series.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
                "readable": False,
            },
            "Cell_2.tif": {
                "channels": ["gray"],
                "size_x": 251,
                "size_y": 449,
                "readable": True,
            },
            "multi-channel-4D-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
                "readable": False,
            },
            "multi-channel-time-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
                "readable": False,
            },
            "multi-channel-z-series.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
                "readable": False,
            },
            "multi-channel.ome.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 439,
                "size_y": 167,
                "readable": True,
            },
            "N2_100x_150ms_4gain_2x2_L1_Image002.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 696,
                "size_y": 520,
                "physical_pixel_size_x": 352.77778048831453,
                "physical_pixel_size_y": 352.77778048831453,
                "readable": True,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_22.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1039,
                "size_y": 1444,
                "readable": True,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_23.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1484,
                "size_y": 1009,
                "readable": True,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_24.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1019,
                "size_y": 1672,
                "readable": True,
            },
            "neuro_rosella_D2_UA.vsi - 10x_FBW, FGW_Z_25.tif": {
                "channels": [np.array([255, 0, 0]), np.array([0, 255, 0])],
                "size_x": 1761,
                "size_y": 643,
                "physical_pixel_size_x": 0.6917064397869545,
                "physical_pixel_size_y": 0.6917997516438892,
                "readable": True,
            },
            "single-channel.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
                "readable": True,
            },
            "TMRE_D1_gsk-3_C_02.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
                "readable": True,
            },
            "TMRE_D1_gsk-3_C_10.tif": {
                "channels": ["FGW"],
                "size_x": 2457,
                "size_y": 2457,
                "readable": True,
            },
            # "TMRE_D1_gsk-3_EGTA_Overview.tif": None,
            "wt L1 TMRE_Image003.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
                "readable": True,
            },
            "z-series.ome.tif": {
                "channels": ["gray"],
                "size_x": 439,
                "size_y": 167,
                "readable": True,
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
                "readable": True,
            },
            "daf-2_D2_aup-1i.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 2740,
                "size_y": 2740,
                "readable": True,
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
                "readable": False,
            },
            # "Philips-1.tiff": { # deleted for now
            #     "channels": ["red", "green", "blue"],
            #     "size_x": 45056,
            #     "size_y": 35840,
            #     "readable": True,
            # },
            "pl_ua_1_gfp.tif": {
                "channels": ["GFP"],
                "size_x": 1992,
                "size_y": 1992,
                "readable": True,
            },
            "pl con_Top Slide_R_p01_0_A01f00d1.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 2048,
                "size_y": 1536,
                "readable": True,
            },
            "control_Bottom Slide_D_p00_0_A01f11d1.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 2048,
                "size_y": 1536,
                "physical_pixel_size_x": 1.2380542388637508,
                "physical_pixel_size_y": 1.2380542388637508,
                "readable": True,
            },
        }

        # Convert relative paths to absolute paths
        return {
            os.path.join(cls.path_images_tif, key): value
            for key, value in all_files.items()
        }

    @classmethod
    def _load_mock_high_res_images(cls):
        """Load mock high resolution images configuration."""
        # Reference to original mock_high_res_images dictionary
        # tests/test_image_import.py lines 179-212
        all_files = {
            "aup-1_13_2_Top Right Dish_TM_p00_0_A01f00d0.TIF": {
                "channels": ["red", "green", "blue"],
                "size_x": 17515,
                "size_y": 17239,
                "readable": True,
            },
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
                "readable": True,
            },
            "Philips-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 45056,
                "size_y": 35840,
                "readable": True,
            },
            # "Philips-3.tiff": { # deleted for now.
            #     "channels": ["red", "green", "blue"],
            #     "size_x": 131072,
            #     "size_y": 100352,
            # },
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
                "readable": True,
            },
        }
        return {
            os.path.join(cls.test_dir, cls.ultra_high_res_root_path, key): value
            for key, value in all_files.items()
        }

    def get_test_image_path(self, image_name):
        """Get the full path for a test image."""
        return os.path.join(self.fixture_dir_abs_path, self.path_images_tif, image_name)

    def get_high_res_image_path(self, image_name):
        """Get the full path for a high resolution test image."""
        return os.path.join(self.test_dir, self.ultra_high_res_root_path, image_name)
