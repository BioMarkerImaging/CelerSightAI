import requests
import sys
import os
from celer_sight_ai import config
from celer_sight_ai.configHandle import *
from celer_sight_ai.core.LogTool import LogInHandler
import unittest
from celer_sight_ai.core.file_client import FileClient
from celer_sight_ai.configHandle import getServerLogAddress
import logging
from requests.exceptions import ConnectionError, HTTPError, Timeout


from parameterized import parameterized
from dotenv import load_dotenv

load_dotenv("../.env")

logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None


def add(x, y):
    return x + y


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.empty_mock_objects(cls)  # remove all mock objects

    @classmethod
    def tearDownClass(cls):
        cls.empty_mock_objects(cls)

    def empty_mock_objects(self):
        ## Delete all mock category objects from the server ##
        from celer_sight_ai import configHandle

        self.currentlyUsedS1Address = getServerLogAddress()
        self.client = FileClient()
        empty_mock_categtory_objects_address = (
            configHandle.getServerLogAddress()
            + "/api/v1/admin/empty_mock_category_objects"
        )
        if os.environ.get("USERNAME_ADMIN") and os.environ.get("PASSWORD_ADMIN"):
            self.client.login(
                os.environ["USERNAME_ADMIN"], os.environ["PASSWORD_ADMIN"]
            )
            response = self.client.session.post(empty_mock_categtory_objects_address)
            assert response.status_code == 200
        else:
            logger.warning(
                "No admin credentials provided. Cannot delete mock category objects."
            )

    def setUp(self):
        self.currentlyUsedS1Address = getServerLogAddress()
        self.client = FileClient()

        # data = {
        #     "category" : "tail", # check case this already exists on public, or current private
        #     "text" : "Tail", # check case this already exists on public or current private
        #     "parent_category_uuid" : "0888765f-f214-4e24-8cc6-c92735d03e68", # check case this doesnt exists
        #     "supercategory" : "worm", # check case this doesnt exists
        #     "username" : self.mock_credentials[0][0], # Make sure its the same as the provided tokken
        #     "type" : "Global",  # or "Private"
        #     "mock" : True,
        # }

    @parameterized.expand(
        [
            # This will fail as category == parent category
            (
                0,
                "test_body",  # category
                "test_body-1",
                "test_body",  # parent category
                "worm",
                os.environ["USERNAME_PAID"],
                "Global",
                True,  # is mock
                os.environ["PASSWORD_PAID"],
                "add",  # action
                "Parent category cannot be the same as the category",
            ),
            # Same as above but creates the category sucessfully
            (
                0,
                "test_body",  # will be converted to a custom category, based on the community category
                "test_body-1",
                None,  # no parent
                "worm",  # supercategory
                os.environ["USERNAME_PAID"],
                "Global",  # available for everyone, but handled by the organization
                True,
                os.environ["PASSWORD_PAID"],
                "add",
                None,  # no error
            ),
            # test_body will raise error as it exists already
            (
                15,  # wait period because the cache needs to update
                "test_body",  # already exists above, it will fail
                "test_body-1",
                None,
                "worm",
                os.environ["USERNAME_PAID"],
                "Global",
                True,  # mock
                os.environ["PASSWORD_PAID"],
                "add",
                "Category already exists.\nChoose a different, unique name.",
            ),
            # Parent class doesnt exists, will raise error
            (
                0,
                "new",  # new class
                "new",
                "invalid parent category",  # parent category will raise error because it does not exist
                "worm",
                os.environ["USERNAME_PAID"],
                "Private",
                True,
                os.environ["PASSWORD_PAID"],
                "add",
                "Parent category not found",
            ),  # No error because its private
            # Supercateogory doesnt exist, will raise error
            (
                0,
                "new",  # new category
                "new",
                "body",
                "invalid supercategory",  # will raise error as it does not exist
                os.environ["USERNAME_PAID"],
                "Private",
                True,
                os.environ["PASSWORD_PAID"],
                "add",
                "Supercategory not found",
            ),
            # No error because its private, and it will be created
            (
                0,
                "head",  # head already exists, but the custom category doesn't
                # and so it can be created
                "Head",
                "test_body",  # parent category , exists
                "worm",
                os.environ[
                    "USERNAME_PAID"
                ],  # only paid user can create custom categories
                "Private",
                True,  # Add it to db, to test later
                os.environ["PASSWORD_PAID"],
                "add",
                None,
            ),
            # Error because it already exists
            (
                15,
                "head",
                "Head",
                "test_body",
                "worm",
                os.environ["USERNAME_PAID"],
                "Global",
                True,
                os.environ["PASSWORD_PAID"],
                "add",
                "Category already exists.\nChoose a different, unique name.",
            ),
            # Remove community category it will fail
            (
                0,
                "worm",
                None,
                None,
                "on_plate",
                os.environ["USERNAME_PAID"],
                None,
                True,
                os.environ["PASSWORD_PAID"],
                "remove",
                "Cannot delete a community category.",
            ),
            # Error because the user is not in a lab (and is not paid)
            (
                0,
                "head",
                None,
                None,
                "worm",
                os.environ["USERNAME_USER"],
                None,
                True,
                os.environ["PASSWORD_USER"],
                "remove",
                "Custom active learning models are only available for Lab members. For free members, please request new categories / models at manos.chaniotakis@biomarkerimaing.com if you think that they will benefitial to the greater community.",
            ),
            # Remove private category (only private categories can be removed)
            (
                0,
                "head",
                None,
                None,
                "worm",
                os.environ["USERNAME_PAID"],
                None,
                True,
                os.environ["PASSWORD_PAID"],
                "remove",
                None,
            ),
            # Error Because its private and we have already added it
            # (
            #     "tail_1",
            #     "Tail",
            #     "0888765f-f214-4e24-8cc6-c92735d03e68",
            #     "worm",
            #     os.environ["USERNAME_ADMIN"],
            #     "Private",
            #     True,
            #     os.environ["PASSWORD_ADMIN"],
            #     "add",
            #     "Category already exists.\nChoose a different, unique name.",
            # ),
        ]
    )
    def test_add_remove_cloud_categories(
        self,
        wait_period,
        category,
        text,
        parent_category,
        supercategory,
        username,
        type,
        is_mock,
        password,
        action,
        error_message,
    ):
        # setup, login
        r = self.client.login(username, password)
        import time

        logger.info(f"Waiting for {wait_period} seconds")
        time.sleep(wait_period)
        print(
            f"Testing : category : {category}, text : {text}, parent_category : {parent_category}, supercategory : {supercategory}, username : {username}, type : {type}, is_mock : {is_mock}, password : {password}"
        )
        if action == "add":
            # Act
            data = {
                "category": category,  # check case this already exists on public, or current private
                "text": text,  # check case this already exists on public or current private
                "parent_category": parent_category,  # check case this doesnt exists
                "supercategory": supercategory,  # check case this doesnt exists
                "username": username,  # Make sure its the same as the provided tokken
                "type": type,  # or "Private"
                "mock": is_mock,
            }
            response = self.client.create_new_category_cloud(data)
        elif action == "remove":
            data = {
                "supercategory": supercategory,
                "category": category,
                "username": username,
                "type": type,
                "mock": is_mock,
            }
            response = self.client.remove_category_cloud(data)
        print(response)
        assert response == error_message


if __name__ == "__main__":
    unittest.main()
