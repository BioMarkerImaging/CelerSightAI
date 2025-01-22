import logging
import os
import tempfile
import unittest
from glob import glob

import numpy as np
import pytest

from tests import qttest_utils
from tests.base_test_case import BaseTestCase

logger = logging.getLogger(__name__)


class BaseOnlineGuiTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = qttest_utils.get_gui_main(offline=False)
        qttest_utils.wait_until_shown(cls.app.MainWindow)

    def check_key_value_pairs(self, dict1, dict2):
        """Compare two dictionaries with special handling for None and numpy arrays."""
        if isinstance(dict1, type(None)) and isinstance(dict2, type(None)):
            return
        for key in dict1.keys():
            value = dict1.get(key)
            self.assertEqual(dict2[key], value)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.app.closeApp()


class BaseGuiTestCase(BaseTestCase):
    """Base class for image-related tests providing common test fixtures and utilities."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level test fixtures."""
        try:
            # os.environ["QT_QPA_PLATFORM"] = "offscreen"
            super().setUpClass()
            cls.app = qttest_utils.get_gui_main(offline=True)
            qttest_utils.wait_until_shown(cls.app.MainWindow)
        except Exception as e:
            logger.error(f"Failed to set up test class: {str(e)}", exc_info=True)
            raise

    def setUp(self):
        """Set up test-level fixtures."""
        try:
            super().setUp()
        except Exception as e:
            logger.error(f"Failed to set up test: {str(e)}", exc_info=True)
            raise

    def tearDown(self):
        """Clean up after each test."""
        try:
            super().tearDown()
        except Exception as e:
            logger.error(f"Failed to tear down test: {str(e)}", exc_info=True)
            raise

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
        """Clean up class-level fixtures."""
        try:
            super().tearDownClass()
            cls.app.closeApp()
        except Exception as e:
            logger.error(f"Failed to tear down test class: {str(e)}", exc_info=True)
            raise
