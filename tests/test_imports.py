# from aicsimageio import AICSImage
# import sys
# import os

# append CelerSight home to system
# from celer_sight_ai import config

import unittest
import logging

logger = logging.getLogger(__name__)
# import pytest
# from . from celer_sight_ai import config


class importTesting(unittest.TestCase):
    def test_imports(self):
        try:
            # from dask.core import flatten
            # import dask.array as da
            import time

            print("aicsimageio")
            from aicsimageio import AICSImage

            print("tufup")
            import tufup
            from celer_sight_ai import config

            config.add_open_slide_and_vips_to_sys(test_imports=True)
            print("roi file")
            import roifile

            print("zstandard")
            import zstandard

            print("requests_toolbelt")
            import requests_toolbelt

            start = time.time()
            print("lazy_import")
            import lazy_import

            start = time.time()
            print("xsdata.formats.dataclass.compat")
            from xsdata.formats.dataclass.compat import class_types

            # from ome_types._conversion import from_tiff, from_xml, to_dict, to_xml, validate_xml
            print(f"ome_types import took {time.time() - start} seconds")

            logger.info("TEST")
            print(f"Lazy import took {time.time() - start} seconds")
            start = time.time()
            print("dask.sizeof")
            from dask.sizeof import sizeof

            print(
                f"dask.sizeof import sizeof import took {time.time() - start} seconds"
            )
            print("numpy")
            import numpy as np

            import sys
            import os

            print("openslide")
            import openslide  # make sure libraries linked

            # import pyvis  # make sure libraries are linked
            print("shapely")
            import shapely

            print("webcolors")
            import webcolors
            from celer_sight_ai import config, __version__

            print("imageio")
            import imageio

            print("dask")
            import dask

            print("zarr")
            import zarr

            if config.is_executable:
                sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
            print("PyQt6")
            from PyQt6 import QtGui, QtCore, QtWidgets

            print("itertools")
            import itertools

            print("statistics")
            import statistics

            print("pyometiff")
            import pyometiff

            print("tiffslide")
            import tiffslide

            if os.name == "nt":
                print("win32con")
                import win32con

                print("win32gui")
                from win32gui import SetWindowPos
            print("opencv")
            import cv2

            print("scipy")
            import scipy.stats as stats
            from celer_sight_ai.historyStack import AddPolygonCommand

            import logging

            print("skimage")
            from skimage.segmentation import watershed, random_walker
            from skimage.feature import peak_local_max
            from scipy import ndimage as ndi
            from PyQt6 import QtCore, QtGui, QtWidgets
            from skimage.morphology import binary_closing, disk
            import scipy.ndimage as nd
            import scipy
            import cv2

            print("seaborn")
            import seaborn

            print("pandas")
            import pandas as pd

            print("matplotlib")
            import matplotlib.pyplot as plt
            import pickle
            from cv2 import resize

            print("sklearn")
            import sklearn
            import sklearn.decomposition
            import scipy.ndimage as ndi

            print("tqdm")
            import tqdm
            from scipy import ndimage
            from skimage.transform import rescale, resize, downscale_local_mean
            from skimage.morphology import medial_axis, skeletonize, thin

            print("Pillow")
            from PIL import Image
            from skimage.draw import polygon_perimeter
            from scipy import ndimage
            import skimage
            import skimage.draw

            print("Natsort")
            import natsort

            print("cryptography")
            import cryptography

            print("xmltodict")
            import xmltodict

            print("azure.storage.blob")
            from azure.storage.blob import BlobServiceClient, BlobClient

            print("skimage.draw import circle_perimeter as circle")
            from skimage.draw import circle_perimeter as circle

            print("onnxruntime")
            import onnxruntime
            from cv2 import resize
            from celer_sight_ai.core.magic_box_tools import get_largest_area
            from celer_sight_ai.QtAssets.UiFiles.ExitSaveDialog import (
                Ui_Dialog as exitSaveDialog_UI,
            )

        except ImportError as e:
            assert False, f"Import error raised {e}"


if __name__ == "__main__":
    unittest.main()
