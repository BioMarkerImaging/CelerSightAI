import logging
import os
import tempfile
import unittest
from glob import glob

import numpy as np
import pytest

from celer_sight_ai.configHandle import getServerLogAddress
from celer_sight_ai.core.file_client import FileClient
from tests.base_test_case import BaseTestCase

logger = logging.getLogger(__name__)


@pytest.mark.online
class BaseOnlineTestCase(BaseTestCase):
    """Base class for image-related tests providing common test fixtures and utilities."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Set up class-level test fixtures."""
        from celer_sight_ai.config import start_jvm

        cls.mock_credentials = []
        if os.environ.get("USERNAME_ADMIN") and os.environ.get("PASSWORD_ADMIN"):
            cls.mock_credentials = [
                os.environ.get("USERNAME_ADMIN"),
                os.environ.get("PASSWORD_ADMIN"),
            ]
        else:
            raise ValueError("No mock credentials found, cant log in")
        assert cls.mock_credentials[0] is not None, "Username is not set"
        assert cls.mock_credentials[1] is not None, "Password is not set"
        # log user
        cls.client = FileClient("https://s1.biomarkerimaging.com")#getServerLogAddress())
        cls.client.login(cls.mock_credentials[0], cls.mock_credentials[1])

        cls.fixture_dir_abs_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )

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
    def _load_optimal_annotation_range_fixture(cls):
        return [
            ("58f00d07-caa7-4bec-8a66-39432f2e1086", [0.12, 0.16]),
            ("0888765f-f214-4e24-8cc6-c92735d03e68", None),
        ]

    @classmethod
    def tearDownClass(cls):
        from celer_sight_ai.config import stop_jvm

        stop_jvm()
