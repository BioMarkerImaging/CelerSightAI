import logging
import os
import sys
import unittest

import pytest
import requests

# load env
from dotenv import load_dotenv
from parameterized import parameterized
from requests.exceptions import ConnectionError, HTTPError, Timeout

# sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

# from tests.csight_test_loader import tags
from celer_sight_ai.configHandle import (
    get_optimal_annotation_range_address,
    getServerLogAddress,
)
from celer_sight_ai.core.file_client import FileClient
from celer_sight_ai.core.LogTool import LogInHandler
from tests.base_online_testcase import BaseOnlineTestCase

load_dotenv("../.env")
logger = logging.getLogger(__name__)


class TestBasicConnection(BaseOnlineTestCase):

    @parameterized.expand(BaseOnlineTestCase._load_optimal_annotation_range_fixture)
    @pytest.mark.online
    def test_get_optimal_annotation_range(self, category, expected_result):
        result = self.client.get_optimal_annotation_range(category).get(
            "optimal_annotation_range", None
        )

        if expected_result is None:
            self.assertIsNone(result)
        else:
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            self.assertAlmostEqual(result[0], expected_result[0], places=2)
            self.assertAlmostEqual(result[1], expected_result[1], places=2)

    @pytest.mark.skip(reason="This test is not implemented")
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
