import os
import tempfile
import unittest
import numpy as np
from glob import glob
import logging
from tests import qttest_utils

logger = logging.getLogger(__name__)


class BaseGuiTestCase(unittest.TestCase):
    """Base class for image-related tests providing common test fixtures and utilities."""

    @classmethod
    def setUpClass(cls, app):
        """Set up class-level test fixtures."""
        cls.app = app
        qttest_utils.wait_until_shown(cls.app.MainWindow)

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
    def tearDownClass(cls):
        cls.app.close()
