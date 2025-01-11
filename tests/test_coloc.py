import sys
import os


import unittest
import pytest
import scipy
from scipy import stats
import cv2
from tests.base_image_testcase import BaseImageTestCase
from parameterized import parameterized


class colocTesting(BaseImageTestCase):

    @parameterized.expand(BaseImageTestCase._load_mock_coloc_data)
    def test_pearson(self, image_path, data):
        """
        do a pearson correlation test test if the value is as expected
        """
        abs_path = os.path.join(self.test_dir, image_path)
        image_data = cv2.imread(abs_path)
        # get the green channel
        img_green = image_data[:, :, 1]
        # get the red channel from img
        img_red = image_data[:, :, 2]
        # compute pearson
        opt_thresh = scipy.stats.pearsonr(img_green.ravel(), img_red.ravel())
        print(f"Pearson correlation for red vs green is {opt_thresh}")
        # assert almost equal
        self.assertAlmostEqual(opt_thresh[0], data["pearson"], places=2)
        opt_thresh = scipy.stats.pearsonr(img_green.ravel(), img_green.ravel())
        print(f"Pearson correlation for green vs green is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)
        opt_thresh = scipy.stats.pearsonr(img_red.ravel(), img_red.ravel())
        print(f"Pearson correlation for red vs red is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)

    @parameterized.expand(BaseImageTestCase._load_mock_coloc_data)
    def test_spearman(self, image_path, data):
        """
        do a spearman correlation
        """
        abs_path = os.path.join(self.test_dir, image_path)
        image_data = cv2.imread(abs_path)
        # get the green channel
        img_green = image_data[:, :, 1]
        # get the red channel from img
        img_red = image_data[:, :, 2]
        # compute spearman
        opt_thresh = scipy.stats.spearmanr(img_green.ravel(), img_red.ravel())
        print(f"Spearman correlation for red vs green is {opt_thresh}")
        # assert almost equal
        self.assertAlmostEqual(opt_thresh[0], data["spearman"], places=2)
        opt_thresh = scipy.stats.spearmanr(img_green.ravel(), img_green.ravel())
        print(f"Spearman correlation for green vs green is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)
        opt_thresh = scipy.stats.spearmanr(img_red.ravel(), img_red.ravel())
        print(f"Spearman correlation for red vs red is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)

    # def test_kendals_tau(self):
    #     """
    #     Do kendals tau correlation tests
    #     """
    #     img_green = self.green_img_1
    #     img_red = self.red_img_1
    #     opt_thresh = scipy.stats.kendalltau(img_green.ravel(), img_red.ravel())
    #     print(f"Kendals tau correlation for red vs green is {opt_thresh}")
    #     # assert almost equal
    #     self.assertAlmostEqual(opt_thresh[0], 0.76310, places=2)
    #     opt_thresh = scipy.stats.kendalltau(img_green.ravel(), img_green.ravel())
    #     print(f"Kendals tau correlation for green vs green is {opt_thresh}")
    #     self.assertAlmostEqual(opt_thresh[0], 0.76310, places=2)
    #     opt_thresh = scipy.stats.kendalltau(img_red.ravel(), img_red.ravel())
    #     print(f"Kendals tau correlation for red vs red is {opt_thresh}")
    #     self.assertAlmostEqual(opt_thresh[0], 0.76310, places=2)

    # def test_manders(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
