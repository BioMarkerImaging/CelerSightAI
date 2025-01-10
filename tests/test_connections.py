import requests
import sys
import os

# sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

from celer_sight_ai.configHandle import *
from celer_sight_ai.core.LogTool import LogInHandler
import unittest
from celer_sight_ai.core.file_client import FileClient
from tests.base_online_testcase import BaseOnlineTestCase
import pytest

# from tests.csight_test_loader import tags
from celer_sight_ai.configHandle import getServerLogAddress
import logging
from requests.exceptions import ConnectionError, HTTPError, Timeout

# load env
from dotenv import load_dotenv

load_dotenv("../.env")
logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None
from unittest.mock import patch
from requests.exceptions import RequestException
from parameterized import parameterized


@pytest.mark.online
class TestBasicConnection(BaseOnlineTestCase):

    @parameterized.expand(BaseOnlineTestCase._load_optimal_annotation_range_fixture)
    def test_get_optimal_annotation_range(self, category, expected_result):
        result = self.client.get_optimal_annotation_range(category).get(
            "optimal_annotation_range", None
        )

        if expected_result is None:
            self.assertIsNone(result)
        else:
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertIn("max", result)
            self.assertIn("min", result)
            self.assertAlmostEqual(result["min"], expected_result["min"], places=2)
            self.assertAlmostEqual(result["max"], expected_result["max"], places=2)

    def test_get_optimal_annotation_range_results(self):
        result = requests.get(get_optimal_annotation_range_address())
        self.assertEqual(result.status_code, 200)

    def test_get_available_models(self):
        # Assuming the login method sets self.jwt and the user is already registered

        # Call the method with a valid username
        response = self.client.get_available_models()
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "models", response
        )  # Assuming the response contains a 'models' key


if __name__ == "__main__":
    unittest.main()
