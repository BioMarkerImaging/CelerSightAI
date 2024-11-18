import requests
import sys
import os

# sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai import config

from celer_sight_ai.configHandle import *
from celer_sight_ai.QtAssets.Utilities.LogTool import LogInHandler
import unittest
from celer_sight_ai.QtAssets.lib import FileClient

from celer_sight_ai.configHandle import getServerAddress

import logging

logger = logging.getLogger(__name__)

unittest.TestLoader.sortTestMethodsUsing = None


class MyTest(unittest.TestCase):
    def setUp(self):
        self.currentlyUsedS1Address = getServerAddress()
        self.mock_credentials = []
        self.client = FileClient()

        # def test_get_cloud_classes(self):
        #     # log in first
        #     r = self.client.login(self.mock_credentials[0][0], self.mock_credentials[0][1])
        #     print(r)
        #     r = self.client.get_cloud_classes()

        # print(response)


if __name__ == "__main__":
    unittest.main()
