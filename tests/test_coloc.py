import sys
import os


import unittest
import pytest
import scipy
from scipy import stats
import cv2


class colocTesting(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        IMG_PATH = "tests/test_assets/sy441.jpg"
        self.img_coloc_1 = cv2.imread(IMG_PATH)
        self.red_img_1 = self.img_coloc_1[:, :, 2]
        self.green_img_1 = self.img_coloc_1[:, :, 1]
        self.blue_img_1 = self.img_coloc_1[:, :, 0]

    def test_pearson(self):
        """
        do a pearson correlation test test if the value is as expected
        """
        # get the green channel
        img_green = self.green_img_1
        # get the red channel from img
        img_red = self.red_img_1
        # compute pearson
        opt_thresh = scipy.stats.pearsonr(img_green.ravel(), img_red.ravel())
        print(f"Pearson correlation for red vs green is {opt_thresh}")
        # assert almost equal
        self.assertAlmostEqual(opt_thresh[0], 0.656, places=2)
        opt_thresh = scipy.stats.pearsonr(img_green.ravel(), img_green.ravel())
        print(f"Pearson correlation for green vs green is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)
        opt_thresh = scipy.stats.pearsonr(img_red.ravel(), img_red.ravel())
        print(f"Pearson correlation for red vs red is {opt_thresh}")
        self.assertAlmostEqual(opt_thresh[0], 1.0, places=2)

    def test_spearman(self):
        """
        do a spearman correlation
        """
        # get the green channel
        img_green = self.green_img_1
        # get the red channel from img
        img_red = self.red_img_1
        # compute spearman
        opt_thresh = scipy.stats.spearmanr(img_green.ravel(), img_red.ravel())
        print(f"Spearman correlation for red vs green is {opt_thresh}")
        # assert almost equal
        self.assertAlmostEqual(opt_thresh[0], 0.800, places=2)
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

    def test_manders(self):
        pass


if __name__ == "__main__":
    unittest.main()
