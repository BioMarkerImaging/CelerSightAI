import os
import tempfile
import unittest
import numpy as np
from glob import glob
import logging

logger = logging.getLogger(__name__)


class BaseImageTest(unittest.TestCase):
    """Base class for image-related tests providing common test fixtures and utilities."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level test fixtures."""
        from celer_sight_ai.config import start_jvm

        start_jvm()

        cls.fixture_dir_abs_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
        cls.path_images_tif = os.path.join(
            cls.fixture_dir_abs_path, "tests/fixtures/import_images"
        )
        cls.all_images_tif = glob(cls.path_images_tif + "/*.tif") + glob(
            cls.path_images_tif + "/*.TIF"
        )
        cls.ultra_high_res_root_path = "tests/fixtures/import_images_high_res"

        # Load test data configurations
        cls.mock_image_data = cls._load_mock_image_data()
        cls.mock_high_res_images = cls._load_mock_high_res_images()
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
                self.assertTrue(np.allclose(dict2[key], value, rtol=1e-05, atol=1e-08))
            else:
                self.assertEqual(dict2[key], value)

    @classmethod
    def _load_mock_image_data(cls):
        """Load mock image data configuration."""
        # Reference to original mock_image_data dictionary
        # tests/test_image_import.py lines 39-177
        return {
            "PIR3_L1_TMRE_Image015.tif": {
                "channels": ["red", "green", "blue"],
                "size_x": 1392,
                "size_y": 1040,
            },
            # ... rest of the mock_image_data dictionary
        }

    @classmethod
    def _load_mock_high_res_images(cls):
        """Load mock high resolution images configuration."""
        # Reference to original mock_high_res_images dictionary
        # tests/test_image_import.py lines 179-212
        return {
            "CMU-1.tiff": {
                "channels": ["red", "green", "blue"],
                "size_x": 46000,
                "size_y": 32914,
            },
            # ... rest of the mock_high_res_images dictionary
        }

    def get_test_image_path(self, image_name):
        """Get the full path for a test image."""
        return os.path.join(self.fixture_dir_abs_path, self.path_images_tif, image_name)

    def get_high_res_image_path(self, image_name):
        """Get the full path for a high resolution test image."""
        return os.path.join(
            self.fixture_dir_abs_path, self.ultra_high_res_root_path, image_name
        )

    @classmethod
    def tearDownClass(cls):
        from celer_sight_ai.config import stop_jvm

        import shutil

        shutil.rmtree(self.temp_dir)

        stop_jvm()
