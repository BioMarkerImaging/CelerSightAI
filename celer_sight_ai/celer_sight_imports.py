import os
from celer_sight_ai.configHandle import getLocal
from aicsimageio import AICSImage

import numpy as np

import sys
import logging
import pathlib
import cv2
import PyQt6
import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets
import skimage.data
import skimage.transform
from skimage.transform import resize
import skimage.data._fetchers
import skimage.filters
import skimage.filters.edges
from celer_sight_ai import config

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from celer_sight_ai.gui.custom_widgets.splash_widget import loadingWindowAnimation
from random import randint

from celer_sight_ai.gui.custom_widgets.celer_sight_main_window_ui_extended import (
    CelerSightMainWindow,
)
from threading import Thread
import cv2
import numpy as np
import copy
from celer_sight_ai import config

from pathlib import Path
from celer_sight_ai.core import ML_tools
from celer_sight_ai import aa_toolbar_2
import celer_sight_ai.core.image_button_handler as image_button_handler
import celer_sight_ai.inference_handler as inference_handler
from celer_sight_ai import config

import cs_updater_binary
import CustomMovement
import DockSizeHandle
import getSettings
import historyStack
import MultiChannellImports
import NewAnalysisSetUp
import celer_sight_ai.gui.custom_widgets.pg1_widget_mask_settings as pg1_widget_mask_settings
import selection_tool
import SplineTool
import celer_sight_ai.gui.custom_widgets.celer_sight_main_window_ui_extended as celer_sight_main_window_ui_extended
import UpdaterMain
from celer_sight_ai.QtAssets import *
from celer_sight_ai.gui.net import *
from celer_sight_ai.gui.Utilities import *
import scipy
import scipy.stats as stats
from scipy import ndimage
import skimage
import skiamge.draw
import pandas
import sklearn
import matplotlib
import glob
import aicsimageio
import statistics
import PIL


if "__main__" == __name__:
    import celer_sight_main

    gui_main, MyLogInHandler, app = celer_sight_main.start()
