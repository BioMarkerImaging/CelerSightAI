import requests
import sys
import os

# sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

from celer_sight_ai.configHandle import *
from celer_sight_ai.core.LogTool import LogInHandler
import unittest
from celer_sight_ai.core.file_client import FileClient

# from tests.csight_test_loader import tags
from celer_sight_ai.configHandle import getServerLogAddress
import logging
from requests.exceptions import ConnectionError, HTTPError, Timeout

# load env
from dotenv import load_dotenv

load_dotenv("../.env")
logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None
import pytest
from unittest.mock import patch
from requests.exceptions import RequestException
from parameterized import parameterized


class MyTest(unittest.TestCase):
    def setUp(self):
        self.mock_credentials = []
        if os.environ.get("USERNAME_USER") and os.environ.get("PASSWORD_USER"):
            self.mock_credentials.append(
                (os.environ.get("USERNAME_USER"), os.environ.get("PASSWORD_USER"))
            )
        # log user
        self.client = FileClient(getServerLogAddress())
        self.client.login(*self.mock_credentials[0])

    @parameterized.expand(
        [
            ("58f00d07-caa7-4bec-8a66-39432f2e1086", {"min": 0.12, "max": 0.20}),
            ("0888765f-f214-4e24-8cc6-c92735d03e68", None),
        ]
    )
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

    # @pytest.mark.parametrize("status_code, expected_result", [
    #     (200, True),
    #     (404, False),
    #     (500, False)
    # ])
    # def test_get_optimal_annotation_range(self, status_code, expected_result):
    #     with patch('requests.get') as mock_get:
    #         mock_response = mock_get.return_value
    #         mock_response.status_code = status_code

    #         result = requests.get(get_optimal_annotation_range_address())

    #         assert (result.status_code == 200) == expected_result
    #         if expected_result:
    #             print(f"Connection to {get_optimal_annotation_range_address()} successful")
    #             logging.info(f"Connection to {get_optimal_annotation_range_address()} successful")
    #         else:
    #             print(f"Connection to {get_optimal_annotation_range_address()} failed with status code {status_code}")
    #             logging.error(f"Connection to {get_optimal_annotation_range_address()} failed with status code {status_code}")

    # @pytest.mark.parametrize("exception", [
    #     RequestException,
    #     ConnectionError,
    #     Timeout
    # ])
    # def test_get_optimal_annotation_range_exceptions(self, exception):
    #     with patch('requests.get', side_effect=exception):
    #         with pytest.raises(exception):
    #             requests.get(get_optimal_annotation_range_address())

    #         print(f"Connection to {get_optimal_annotation_range_address()} failed with {exception.__name__}")
    #         logging.error(f"Connection to {get_optimal_annotation_range_address()} failed with {exception.__name__}")

    def test_get_optimal_annotation_range_results(self):
        result = requests.get(get_optimal_annotation_range_address())

    # def test_login_required(self):
    #     # Mock the login method to set self.jwt
    #     self.client.login = lambda: setattr(self.client, "jwt", "test_token")

    #     # Mock the some_api_method to check if self.jwt is set
    #     @self.client.login_required
    #     def some_api_method(self):
    #         return self.jwt

    #     self.assertEqual(some_api_method(self.client), "test_token")

    #     # Test with an expired token
    #     self.client.jwt = None
    #     # self.assertRaises(A1uthenticationError, some_api_method, self.client)

    # def test_get_available_models(self):
    #     # Assuming the login method sets self.jwt and the user is already registered
    #     for email, password in self.mock_credentials:
    #         self.client.login(email, password)

    #         # Call the method with a valid username
    #         response = self.client.get_available_models(username="test_username")

    #         # Check the response
    #         self.assertIsInstance(response, dict)

    #         self.assertIn(
    #             "models", response
    #         )  # Assuming the response contains a 'models' key

    # @tags("small_test")
    def test_hello_connection(self):
        # create a request to self.currentlyUsedS1Address hello
        result = requests.get(self.currentlyUsedS1Address + "/hello")
        self.assertEqual(result.status_code, 200)
        print(f"Connection to {self.currentlyUsedS1Address} successful")
        logging.info(f"Connection to {self.currentlyUsedS1Address} successful")

    # @tags("small_test")
    def test_authenticateMain(self):
        import celer_sight_ai.configHandle as configHandle
        from celer_sight_ai.gui.lib import FileClient

        self.test_hello_connection()

        for email, password in self.mock_credentials:
            client = FileClient(configHandle.getServerLogAddress())

            return_val, exc = client.login_request(email, password)
            if not return_val:
                # case of connection error
                self.assertEqual(bool(return_val), True)
            else:
                # case of wrong credentials
                sc_json = return_val.json()
                self.assertEqual(sc_json["OK"], True)


if __name__ == "__main__":
    unittest.main()
