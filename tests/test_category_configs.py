from glob import glob
import cv2
import numpy as np
import os
import sys
import time

# from tests.csight_test_loader import tags
import unittest

sys.path.append(os.environ["CELER_SIGHT_AI_HOME"])
from celer_sight_ai.QtAssets.Utilities.image_reader import get_specialized_image
import logging
from celer_sight_ai.QtAssets.grid_button_image_selector import (
    gather_cfgs,
    process_cfg_for_grid_button_image_selector,
    validate_cfg,
)

logger = logging.getLogger(__name__)


class TestCategoryConfigs(unittest.TestCase):
    def setUp(self):
        self.cfgs_paths = gather_cfgs()
        assert self.cfgs_paths != [], "Could not gather any configs"
        self.cfgs = [c for c in self.cfgs_paths]
        assert len(self.cfgs) == len(self.cfgs_paths), "Could not read all configs"

    def test_validate_cfg(self):
        for i, p in enumerate(self.cfgs_paths):
            assert validate_cfg(self.cfgs[i]), f"Could not validate config {p}"



if __name__ == "__main__":
    unittest.main()
