import logging
import os
import sys
import time

# from tests.csight_test_loader import tags
import unittest
from glob import glob

import cv2
import numpy as np
import tifffile
import xmltodict

from tests.base_image_testcase import BaseImageTestCase

logger = logging.getLogger(__name__)


class TestUltraHighResCrop(BaseImageTestCase):

    def test_ultra_high_res_image_crop(self):
        from celer_sight_ai.io.image_reader import crop_ultra_high_res

        tile_xywh = [6500, 6200, 19700, 15100]
        croped_image = crop_ultra_high_res(
            self.cropped_ultra_high_res_test_file, tile_xywh
        )


if __name__ == "__main__":
    unittest.main()
