import sys
import os

# append CelerSight home to system
sys.path.insert(0, os.environ["CELER_SIGHT_AI_HOME"])
import unittest
import pytest
import scipy
from scipy import stats
import cv2

from celer_sight_ai.QtAssets.Utilities.scene import get_jpeg_memory_size


class ImageProcessingTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_get_jpeg_memory_size(self):
        print(get_jpeg_memory_size((1200, 1200), 60, batch=10000) / 1024)


if __name__ == "__main__":
    unittest.main()
