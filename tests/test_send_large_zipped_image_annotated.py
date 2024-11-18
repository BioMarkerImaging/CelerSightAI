import unittest
import os
import sys
from celer_sight_ai.configHandle import (
    get_send_large_zipped_image_annotated_address,
)
from celer_sight_ai.QtAssets.lib import FileClient
from celer_sight_ai.configHandle import getServerAddress, getServerLogAddress

import json
# Custom callback for monitoring progress
def callback(bytes_read, total_size):
    progress_percentage = (bytes_read / total_size) * 100
    end_percentage = 100
    start_percentage = 0
    percentage = (
        progress_percentage * (end_percentage - start_percentage) / 100
    ) + start_percentage
    print(
        int(percentage)
    )
def file_generator(file_path):
    total_size = os.path.getsize(file_path)
    uploaded = 0
    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)  # Read in chunks of 4KB
            if not data:
                break
            uploaded += len(data)
            if callback:
                callback(uploaded, total_size)  # Update progress
            yield data

class TestSendLargeZippedImageAnnotated(unittest.TestCase):

    def setUp(self):
        self.mock_credentials = []
        if os.environ.get("USERNAME_USER") and os.environ.get("PASSWORD_USER"):
            self.mock_credentials.append((os.environ.get("USERNAME_USER"), os.environ.get("PASSWORD_USER")))
        # log user
        self.client = FileClient(getServerAddress())
        self.client.login(*self.mock_credentials[0])


    def test_send_large_zipped_image_annotated(self):
    
        # create a dictionary object of 10MB in size
        dict_to_send = {"large_data": "a" * 1_000_000 }#1024 * 1024* 10} #
        send_large_zipped_image_annotated_url = get_send_large_zipped_image_annotated_address()

        resp = self.client.session.post(
                send_large_zipped_image_annotated_url,
                data=None,
                headers={
                    'User-Agent': 'python-requests/2.31.0',
                    "Connection": "keep-alive",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/octet-stream",
                    "Metadata": json.dumps(dict_to_send),
                    "mock" : "true"
                },
            )

if __name__ == "__main__":
    unittest.main()
