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
from celer_sight_ai.configHandle import getServerLogAddress, getServerLogAddress
import logging
from requests.exceptions import ConnectionError, HTTPError, Timeout
import json
from parameterized import parameterized

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import dotenv
from PyQt6.QtTest import QTest
from tests.base_gui_testcase import BaseGuiTestCase
from tests.base_online_testcase import BaseOnlineTestCase
import pytest

# load env vars
dotenv.load_dotenv(os.path.join(p, ".env"))
# from celer_sight_ai.gui.net.errors import AuthenticationError

logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None

os.environ["CELER_SIGHT_TESTING"] = "true"

"""
How this tests works:
Use the QTest api to draw the test image from azure, use that image to create some annotations,
use the interface to submit these as autited, close and reopen the app, retrieve the image,
make adjustments, validate the adjustments, delete the annotations, validate the deletion
delete the image, validate the deletion and erase any mock images created in this test.
"""


class TestRemoteAnnotate(BaseOnlineTestCase):
    def setUp(self):
        self.currentlyUsedS1Address = getServerLogAddress()
        self.mock_credentials = [
            (os.environ.get("USERNAME_ADMIN"), os.environ.get("PASSWORD_ADMIN")),
        ]
        self.client = FileClient(getServerLogAddress())

    @pytest.mark.long
    @pytest.mark.online
    @parameterized.expand(
        [
            (
                {
                    "user_id": "manos.chaniotakis@biomarkerimaging.com",
                    "supercategory": "on_plate",
                    "categories": ["worm eggs"],
                    "amount": 1,
                    "categories_to_exclude": [],
                    "contribute_mode_retrieval": "partially_annotated",
                    "fetch_images_without_annotations": False,
                    "randomized": False,
                },
                {"image_ids": [{"image_uuid": "62c3338f-fd26-4cce-8428-632ba4faa461"}]},
            )
        ]
    )
    def test_remote_image_batch_for_annotation(self, data, expected_response):
        from celer_sight_ai.configHandle import get_remote_image_batch_for_annotation
        from celer_sight_ai.core.file_client import FileClient

        self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])

        response = self.client.remote_image_batch_for_annotation_method(data)

        self.assertEqual(response.json(), expected_response)


#     @parameterized.expand(
#         [
#             (
#                 {
#                     "user_id": "manos.chaniotakis@biomarkerimaging.com",
#                     "supercategory": "on_plate",
#                     "categories": ["worm eggs"],
#                     "amount": 1,
#                     "categories_to_exclude": [],
#                     "partial_annotation_id": None,
#                     "fetch_images_without_annotations": False,
#                     "audited": False,
#                     "randomized": False,
#                     "private": False,
#                 },
#                 {"image_ids": [{"image_uuid": "1158afdc-4c59-49f5-a419-429ff8f78e72"}]},
#             )
#         ]
#     )
#     def test_remote_image_batch_for_annotation(self, data, expected_response):
#         from celer_sight_ai.configHandle import get_remote_image_batch_for_annotation
#         from celer_sight_ai.gui.net.lib import FileClient

#         self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])

#         response = self.client.remote_image_batch_for_annotation_method(data)

#         self.assertEqual(response.json(), expected_response)

#     def test_set_remote_annotation_session_as_audited(self):
#         from celer_sight_ai import configHandle

#         self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])
#         addr = configHandle.get_set_remote_annotation_session_as_audited_address()

#         data = {
#             "image_uuids": [
#                 "1158afdc-4c59-49f5-a419-429ff8f78e72"
#             ],  # needs to be a list
#             "audited_categories": ["worm eggs"],
#             "supercategory": "on_plate",
#             "mock": True,
#         }
#         r = self.client.session.post(addr, json=data)
#         r.raise_for_status()
#         print()

#     def test_get_remote_annotations_for_image(self):
#         self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])
#         data = {
#             "image_uuid": "ce1fa147-1756-4873-b2dd-6792f10e0ea3",
#         }
#         annotations = self.client.get_remote_annotations_for_image(data)
#         return

#     def test_insert_update_remove_remote_annotation(self):
#         # log in
#         self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])
#         data = {
#             "annotation_uuid": "d9a886f0-8661-4a95-996f-bc2c5b9eb9d7",
#             "supercategory": "on_plate",
#             "category": "worm eggs",  # in text
#             "type": "polygon",
#             "data": [[[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]],  # the array
#             "image_width": 17515,  # fill in later
#             "image_height": 17239,  # fill in later
#             "image_uuid": "ce1fa147-1756-4873-b2dd-6792f10e0ea3",
#             "audited": True,
#             "state": None,
#             # "mock": True,
#         }
#         annotaion_uuid = self.client.insert_remote_annotation(data)

#         # make sure annotation has been inserted
#         data_retrieve = {
#             "image_uuid": "ce1fa147-1756-4873-b2dd-6792f10e0ea3",
#         }
#         annotations = self.client.get_remote_annotations_for_image(data_retrieve)
#         # make sure annotation_uuid exists in the annotation retrieved
#         annotation_uuids = [annotation["annotation_uuid"] for annotation in annotations]
#         self.assertIn(annotaion_uuid, annotation_uuids)

#         data_update = {
#             "annotation_uuid": annotaion_uuid,
#             "supercategory": data["supercategory"],
#             "category": data["category"],
#             "data": [[[1, 1], [0, 0], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]],
#             "image_uuid": data["image_uuid"],
#             "audited": False,
#         }

#         self.client.update_remote_annotation(data_update)

#         # validate that the data for this annotation has been updated
#         # make sure annotation has been updated
#         data_retrieve = {
#             "image_uuid": "ce1fa147-1756-4873-b2dd-6792f10e0ea3",
#         }
#         annotations = self.client.get_remote_annotations_for_image(data_retrieve)
#         annotation = [
#             annotation
#             for annotation in annotations
#             if annotation["annotation_uuid"] == annotaion_uuid
#         ][0]
#         self.assertEqual(annotation["data"], data_update["data"])

#         data_delete = {
#             "supercategory": data["supercategory"],
#             "image_uuid": data["image_uuid"],
#             "annotation_uuid": annotaion_uuid,
#             "mock": True,
#         }
#         self.client.delete_remote_annotation(data_delete)
#         return

#     def test_get_remote_image(self):
#         import cv2

#         self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])
#         # test a normal image
#         image_uuid = "ce1fa147-1756-4873-b2dd-6792f10e0ea3"
#         # get low quality image
#         image = self.client.get_remote_image(image_uuid, quality="low")
#         # save to disk
#         cv2.imwrite("test.jpg", image)
#         # make sure image is not None
#         self.assertIsNotNone(image)
#         # get high quality image
#         image = self.client.get_remote_image(image_uuid, quality="high")
#         # save to disk
#         cv2.imwrite("test.jpg", image)
#         self.assertIsNotNone(image)

#         # superresolution image

#         return


if __name__ == "__main__":
    unittest.main()
