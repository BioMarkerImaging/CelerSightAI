import tifffile
import xmltodict
from glob import glob
import cv2
import numpy as np
import os
import sys
import time

# from tests.csight_test_loader import tags
import unittest

from celer_sight_ai.io.image_reader import read_specialized_image
import logging

logger = logging.getLogger(__name__)


class MyTest(unittest.TestCase):
    def setUp(self):
        self.ultra_high_res_root_path = "tests/fixtures/import_images_high_res"

    def test_ultra_high_res_image_crop(self):
        from celer_sight_ai.io.image_reader import crop_ultra_high_res

        image_path = os.path.join(self.ultra_high_res_root_path, "tiff_slide_test.tiff")
        # tile = [6500, 6200, 14200, 13300]
        tile_xywh = [6500, 6200, 19700, 15100]
        croped_image = crop_ultra_high_res(image_path, tile_xywh)
        print(croped_image.shape)
        cv2.imwrite("test.jpg", croped_image)


if __name__ == "__main__":
    unittest.main()
