"""
Scene viewer class
"""

import os
import sys
import typing
from typing import Literal

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from celer_sight_ai import config
from celer_sight_ai.config import (
    BUTTON_COLS,
    BUTTON_HEIGHT,
    BUTTON_SPACING,
    BUTTON_WIDTH,
    IMAGE_PREVIEW_BOTTOM_PAD,
    IMAGE_PREVIEW_BUFFER,
    IMAGE_PREVIEW_TOP_PAD,
)

if config.is_executable:
    sys.path.append(str(os.environ["CELER_SIGHT_AI_HOME"]))

import logging

# import logging
logger = logging.getLogger(__name__)
logger.info("this is the scene")
from celer_sight_ai.gui.designer_widgets_py_files.ToolButtonsRightSceneWidget import (
    Ui_WidgetSceneTools,
)

logger.info("Ui_WidgetSceneTools imported")
from skimage.morphology import medial_axis, skeletonize, thin

logger.info("skimage morphology imported")

import os

import skimage
import skimage.draw

logger.info("Skimage imported")

logger.info("PiL imported")
import cv2
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config

print("Importing read_specialized_image")
from celer_sight_ai.io.image_reader import read_specialized_image

print(sys.path)
try:
    from skimage.draw import circle_perimeter as circle
    from skimage.draw import circle_perimeter_aa

except:
    from skimage.draw import circle, circle_perimeter_aa

# from celer_sight_ai.gui.Utilities.shape import Shape
# from celer_sight_ai.gui.Utilities.lib import distance
import mimetypes
from enum import IntEnum, auto

from shapely.geometry import Polygon


def readImage(
    path: str = "",
    is_video=False,
    for_interactive_zoom=False,
    for_thumbnail=False,
    bbox=None,
    avoid_loading_ultra_high_res_arrays_normaly=False,
    is_pyramidal=False,
    applied_threshold=None,
    channel_names_to_filter=None,
):
    """
    path: str path to the image
    is_video: bool whether the image is a video or not
    for_interactive_zoom: bool used in ultra high res image
    bbox : [x,y,w,h] region of cropped image data to extract
    returns image, channels , dict
    """
    import numpy as np
    import tifffile
    import xmltodict

    from celer_sight_ai import config
    from celer_sight_ai.gui.custom_widgets.viewer.utils import map_value_to_dtype

    logger.debug(
        f"ReadImage for {path}, for_interactive_zoom : {for_interactive_zoom} , for_thumbnail : {for_thumbnail}"
    )
    channels = ["gray"]

    out_dict = {
        "channels": None,
        "is_ultra_high_res": False,
        "needs_pyramidal_conversion": False,
    }
    im = None
    # first handle video, since remote annotaion does not work for video anyway
    if is_video:
        from ffpyplayer.player import MediaPlayer

    # if its remote, queue for download and exit method
    if path.lower().startswith("celer_sight_ai:"):
        out_dict["is_remote"] = True
        img = None
        return img, out_dict

    if path.lower().endswith(tuple(config.SPECIALIZED_FORMATS)) and not is_pyramidal:
        # tiff is included here, read_specialized_image will handle ultra high res images
        logger.debug(f"Importing image from {path} : tiff")
        from celer_sight_ai.io.image_reader import (
            extract_tile_data_from_tiff,
            interactive_untiled_tiff_preview,
        )

        # First we attempt to read the image normally, if the image is ultra high res, handle later

        result = read_specialized_image(
            path,
            for_interactive_zoom=for_interactive_zoom,
            for_thumbnail=for_thumbnail,
            bbox=bbox,  # bbox : [x,y,w,h]
            avoid_loading_ultra_high_res_arrays_normaly=avoid_loading_ultra_high_res_arrays_normaly,
        )

        if isinstance(result, type(None)) or (
            isinstance(result[0], type(None)) and isinstance(result[1], type(None))
        ):
            logger.info(f"Could not import image from {path} : tiff")
            return None, {}
        else:
            im, tags = result
            out_dict.update(tags)

            # if the image is ultra high res and needs pyramidal conversion,
            if tags["needs_pyramidal_conversion"]:
                if (
                    bbox
                ):  # when a bbox is provided, its because we are loading a specific area from the viewport
                    im = extract_tile_data_from_tiff(path, bbox)
                    im = np.array(im)
                if applied_threshold:
                    # get channel
                    threshold_value = map_value_to_dtype(
                        applied_threshold["value"], im.dtype
                    )
                    im = cv2.threshold(im, threshold_value, 255, cv2.THRESH_BINARY)[1]
                return im, out_dict
            logger.debug(
                f"Image of shape {path} imported from {path} with channels {out_dict['channels']} : tiff"
            )

    elif (
        path.lower().endswith(tuple(config.TIFFSLIDE_FORMATS))
        or path.lower().endswith(tuple(config.SPECIALIZED_FORMATS))
        and is_pyramidal
    ):
        from celer_sight_ai.io.image_reader import (
            get_deep_zoom_by_openslide,
            get_deep_zoom_by_tiffslide,
            get_exact_tile_with_openslide,
            open_preview_with_openslide_image_reader,
            open_preview_with_tiffslide_image_reader,
        )

        if (
            bbox
        ):  # when a bbox is provided, its because we are loading a specific area from the viewport
            im = get_exact_tile_with_openslide(path, bbox)  # bbox : [x,y,w,h]
            im = np.array(im)
        # when for_interactive_zoom and for_thumbnail are both true,
        # we get a zoom out overview of the whole image
        out_dict["is_ultra_high_res"] = True

        # if there is no graphic pixmap items in the self._deepzoom_pixmaps
        if for_interactive_zoom and for_thumbnail:
            # load the full image at a lower resolution
            # with the viewport at exactly the image actuall scale
            im, out_dict = open_preview_with_openslide_image_reader(
                path  # None use the full image as the viewport
            )
            # im = im[0]
            out_dict["channels"] = ["red", "green", "blue"]

        # get standard image for tiffslide
        elif for_thumbnail:
            im, out_dict = open_preview_with_openslide_image_reader(path)
            # add entry to deepzoom pixmap
        # else, get the deep zoom image
        elif for_interactive_zoom:
            all_tiles, all_bounding_boxes = get_deep_zoom_by_openslide(
                path, config.viewport_bounding_box
            )

    elif path.lower().endswith(".npy"):
        # assume this is only during the saved / read celer sight phase, and so channels are not included in the file
        logger.info(f"Importing image from {path} : npy")
        im = np.load(path)
        if applied_threshold:
            threshold_value = map_value_to_dtype(applied_threshold, im.dtype)
            im = cv2.threshold(im, threshold_value, 255, cv2.THRESH_BINARY)[1]
        return im, {}
    else:
        logger.info(f"Importing image from {path} : normal")
        try:
            # Read image directly using cv2.imread for local files
            im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if im is None:
                # Fallback to reading as bytes if direct read fails
                with open(path, "rb") as stream:
                    bytes_data = stream.read()
                    numpyarray = np.frombuffer(bytes_data, np.uint8)
                    im = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

            if im is not None:
                # Convert from BGR to RGB color space
                if len(im.shape) == 3 and im.shape[2] == 3:
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            else:
                logger.error(f"Failed to load image: {path}")
                return None, {}

        except Exception as e:
            logger.error(f"Error loading image {path}: {str(e)}")
            return None, {}
        if (
            not not isinstance(im, type(None))
            and not for_thumbnail
            and not for_interactive_zoom
            and not bbox
        ):
            config.ram_image = im
            config.ram_image_path = path
        if bbox:
            # bbox should be in the format [x,y,w,h]
            from celer_sight_ai.io.image_reader import (
                crop_and_pad_image,
                generate_complete_spiral_tiles,
            )

            im = crop_and_pad_image(im, bbox)
        if len(im.shape) != 2:
            if im.shape[2] == 3:
                out_dict["channels"] = ["red", "green", "blue"]
            elif im.shape[2] == 4:
                out_dict["channels"] = ["red", "green", "blue", "alpha"]
            else:
                raise ValueError("Image must be grayscale or RGB or RGBA.")
        out_dict["size_x"] = im.shape[1]
        out_dict["size_y"] = im.shape[0]

    # store image to config for quick reloading
    from celer_sight_ai import config

    if im is None:
        return None, {}
    if not isinstance(channel_names_to_filter, type(None)):
        # remove channels that are not in the channel_names_to_filter
        # convert text to index
        channel_names_to_filter = [
            config.channel_names.index(i.lower()) for i in channel_names_to_filter
        ]
        # remove channels that are not in the channel_names_to_filter
        im = im[:, :, channel_names_to_filter]

    if not isinstance(im, type(None)):
        logger.debug(f"Image {im.shape} imported with channels : {channels}")

    if applied_threshold:
        threshold_value = map_value_to_dtype(applied_threshold, im.dtype)
        im = cv2.threshold(im, threshold_value, 255, cv2.THRESH_BINARY)[1]
    return im, out_dict


@config.threaded_with_registers("convert_pyramidal")
def create_pyramidal_tiff_for_image_object(image_object):
    """
    Creates a locked variable, that gets released when the process completes.
    The .tif file is converted to an svs file using pyvips. The source file is changed to
    .svs
    """
    import random

    logger.debug(f"Creating pyramidal tiff for {image_object.get_path()}")
    out_file = os.path.basename(image_object.get_path())
    out_file = os.path.join(
        config.cache_dir,
        out_file.split(".")[0] + str(random.randint(0, 1000000)) + ".svs",
    )
    image_object._during_pyramidal_conversion = True
    from celer_sight_ai.io.image_reader import (
        create_pyramidal_tiff,
    )

    result = create_pyramidal_tiff(image_object.get_path(), out_file)
    if result:
        image_object.set_path(out_file)
    else:
        config.global_signals.error("Could not create pyramidal tiff")
        image_object._failed_creating_pyramidal = True
    image_object._during_pyramidal_conversion = False
    image_object.set_pyramidal_path(out_file)
    image_object._is_pyramidal = True
    # update the viewport once finished
    # config.global_signals.check_and_update_high_res_slides_signal.emit()
    if hasattr(config, "current_photo_viewer") and config.current_photo_viewer:
        config.current_photo_viewer.request_debounced_high_res_update(force_update=True)


def find_treatment_patterns_within_filepaths(filepaths):
    import re
    from collections import defaultdict
    from os.path import basename, splitext

    # remove trailing "_" or " " or "-" or "." from the filenames
    filepaths_stripped = [
        os.path.splitext(i)[0].rstrip(" _-.") + os.path.splitext(i)[1]
        for i in filepaths
    ]
    grouped_files = defaultdict(list)
    if not filepaths_stripped:
        return grouped_files
    # convert to filenames
    filenames = [basename(i) for i in filepaths_stripped]
    for i in range(len(filenames)):
        filename = basename(filenames[i])
        # Extracting the grouping pattern from the file name using regex.
        match = re.match(r"(.+?)_\d+\.\w+$", filename)

        if match:
            # Using the extracted grouping pattern as a key to group the file paths.
            key = match.group(1)
            grouped_files[key].append(filepaths[i])

    return grouped_files


# image, channels


class QMask(QtGui.QPolygonF):
    def __init__(self):
        super().__init__()
        self._IncludedInAnalysis = True
        self.Visibility = True
        self.Color = 1  # rgb r = 0 , g = 1, b = 2
        self.Attribute = None


class BackgroundGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, pixmap=None):
        super().__init__(pixmap)


class ZoomToolsSideScene(Ui_WidgetSceneTools):
    def __init__(self, viewer) -> None:
        super().__init__()
        self.Myviewer = viewer
        self.MyWidget = QtWidgets.QWidget()
        self.setupUi(self.MyWidget)
        self.retraslateUi(self.MyWidget)
        self.MyWidget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.MyWidget.move(viewer.width(), 20)

        self.FitbuttonTool
        self.ZoomInButtonTool
        self.ZoomOutButtonTool


class SceneViewer(QtWidgets.QGraphicsScene):
    def __init__(self, viewer=None):
        super().__init__()
        self.viewer = viewer
        self.Main = self.viewer.MainWindow
        self.installEventFilter(self)
        self.PreviousSelectedItemList = []
        self.CurrentlyAdjustingItem = False
        self.lastItem = None
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.ItemIndexMethod.NoIndex)
        self.current_instruction = 0

    def removeItemSafely(self, itemQGraphics):
        for child_item in itemQGraphics.childItems():
            self.removeItem(child_item)
        self.removeItem(itemQGraphics)


class mgcClick_cursor_cls(QtWidgets.QGraphicsItemGroup):
    def __init__(self, px=None, py=None, w=None, mode="box"):
        QtWidgets.QGraphicsItemGroup.__init__(self)
        # center rect to cursor
        self.myW = w  # width of the
        self.mode = mode
        if mode == "box":
            # px - int(w/2),py- int(w/2), w, w))
            self.current_rect = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0, 0, w, w))
        elif mode == "circle":
            self.current_rect = QtWidgets.QGraphicsEllipseItem(
                QtCore.QRectF(0, 0, w, w)
            )  # px - int(w/2),py- int(w/2), w, w))

        self.current_rect.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
        )
        self.current_rect.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False
        )
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        pen_width = 3
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0, 255))
        pen.setWidth(pen_width)
        pen.setCosmetic(True)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)
        # pen.setDashPattern([5, 5])
        self.current_rect.setPen(pen)
        self.addToGroup(self.current_rect)
        # self.show()
        self.current_rect.show()

    def moveToC(self, x, y):
        # custom move method to correct offset
        self.setPos(x - int(self.myW / 2), y - int(self.myW / 2))

    def updateSize(self, radius=None):
        self.current_rect.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
        )
        self.current_rect.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False
        )
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        print(f"setting radius to {radius}")
        self.myW = radius
        if self.current_rect:
            self.current_rect.setRect(
                QtCore.QRectF(
                    self.current_rect.pos().x(),
                    self.current_rect.pos().y(),
                    radius,
                    radius,
                )
            )


class bbox_drawing_cls(QtWidgets.QGraphicsItemGroup):
    # graphics item for the magic roi mode
    def __init__(self, p_width=None, px=None, py=None, pw=None, ph=None):
        # p_width = width of the circle object at the endges of the squares
        # px : x position
        # py : y poosition
        # pw : bbox width
        # py : bbox height
        QtWidgets.QGraphicsItemGroup.__init__(self)
        self.below_rect = QtWidgets.QGraphicsRectItem(QtCore.QRectF(px, py, pw, ph))
        self.above_rect = QtWidgets.QGraphicsRectItem(QtCore.QRectF(px, py, pw, ph))
        w = p_width
        # on windows these are offset
        if os.name == "nt":
            hw = w // 2
            self.c1 = QtWidgets.QGraphicsEllipseItem(px - hw, py - hw, w, w)
            self.c2 = QtWidgets.QGraphicsEllipseItem(px + pw - hw, py - hw, w, w)
            self.c3 = QtWidgets.QGraphicsEllipseItem(px + pw - hw, py + ph - hw, w, w)
            self.c4 = QtWidgets.QGraphicsEllipseItem(px - hw, py + ph - hw, w, w)
        else:
            hw = w // 2

            self.c1 = QtWidgets.QGraphicsEllipseItem(px - hw, py - hw, w, w)
            self.c2 = QtWidgets.QGraphicsEllipseItem(px + pw - hw, py - hw, w, w)
            self.c3 = QtWidgets.QGraphicsEllipseItem(px + pw - hw, py + ph - hw, w, w)
            self.c4 = QtWidgets.QGraphicsEllipseItem(px - hw, py + ph - hw, w, w)
        self.addToGroup(self.below_rect)
        # self.addToGroup(self.above_rect)
        self.addToGroup(self.c1)
        self.addToGroup(self.c2)
        self.addToGroup(self.c3)
        self.addToGroup(self.c4)
        self.drawRectItems()

    def moveRects(self):
        pass

    def drawRectItems(self):
        pen_width = 2
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255))
        pen.setWidth(pen_width)
        pen.setCosmetic(True)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)

        # pen.setStyle(QtCore.Qt.PenStyle.DashLine)
        # pen.setDashPattern([5, 5])

        self.below_rect.setPen(pen)
        self._brush = QtGui.QBrush(
            QtGui.QColor(255, 255, 255, 255), QtCore.Qt.BrushStyle.SolidPattern
        )
        self.c1.setBrush(self._brush)
        self.c2.setBrush(self._brush)
        self.c3.setBrush(self._brush)
        self.c4.setBrush(self._brush)
        self.c1.setPen(pen)
        self.c2.setPen(pen)
        self.c3.setPen(pen)
        self.c4.setPen(pen)
        # self.c1.setFlag(
        #     QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        # )
        # self.c2.setFlag(
        #     QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        # )
        # self.c3.setFlag(
        #     QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        # )
        # self.c4.setFlag(
        #     QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        # )

        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255))
        pen.setWidth(pen_width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setCosmetic(True)
        # pen.setDashPattern([5, 5])
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)
        # self._brush = QtGui.QBrush(
        #     QtGui.QColor(255, 255, 255, 25), QtCore.Qt.BrushStyle.SolidPattern
        # )
        # self.above_rect.setPen(pen)
        # self.above_rect.setBrush(self._brush)


class CropItem(QtWidgets.QGraphicsPathItem):
    # This is the auto tool scene item
    def __init__(self, pixmap, rect1, rect2):
        QtWidgets.QGraphicsPathItem.__init__(self)
        self.extern_rect = rect1
        self.intern_rect = rect2
        # self.intern_rect.moveCenter(self.extern_rect.center())
        self.setBrush(QtGui.QColor(10, 0, 0, 255))
        self.setPen(QtGui.QPen(QtCore.Qt.PenStyle.NoPen))
        self.create_path()

    def create_path(self):
        self._path = QtGui.QPainterPath()
        self._path.addRect(self.extern_rect)
        self._path.moveTo(self.intern_rect.topLeft())
        self._path.addRect(self.intern_rect)
        self.setPath(self._path)

    def rect(self):
        return self.intern_rect

    def setRect(self, rect):
        self._intern = rect
        self.create_path()


logger.info("completed loading scene")

if __name__ == "__main__":
    pass
