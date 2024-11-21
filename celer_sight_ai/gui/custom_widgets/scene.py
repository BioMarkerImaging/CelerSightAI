"""
Scene viewer class
"""

import os
import sys
import typing

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from celer_sight_ai import config

from celer_sight_ai.config import (
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_SPACING,
    BUTTON_COLS,
    IMAGE_PREVIEW_TOP_PAD,
    IMAGE_PREVIEW_BOTTOM_PAD,
    IMAGE_PREVIEW_BUFFER,
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
import skimage.draw
import skimage

logger.info("Skimage imported")
from PIL.ImageColor import getrgb as GetRGB_FromHex

logger.info("PiL imported")
import numpy as np
import cv2
from celer_sight_ai import config

from PyQt6 import QtCore, QtGui, QtWidgets

print("Importing get_specialized_image")
from celer_sight_ai.io.image_reader import get_specialized_image

print(sys.path)
try:
    from skimage.draw import circle_perimeter as circle
    from skimage.draw import circle_perimeter_aa

except:
    from skimage.draw import circle
    from skimage.draw import circle_perimeter_aa

# from celer_sight_ai.gui.Utilities.shape import Shape
# from celer_sight_ai.gui.Utilities.lib import distance
from enum import IntEnum, auto
from shapely.geometry import Polygon
import mimetypes


def is_video_file(filename):
    # Guess the type of a file based on its filename
    filetype, _ = mimetypes.guess_type(filename)

    # Check if the file type is a video
    return filetype is not None and filetype.startswith("video/")


def get_jpeg_memory_size(output_image_size, jpeg_quality, batch=1):
    # returns in mb
    # create a random image to encode
    image = np.random.randint(
        0, 256, (output_image_size[1], output_image_size[0], 3), dtype=np.uint8
    )

    # encode the image using cv2.imencode
    _, encoded_img = cv2.imencode(
        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    )

    # calculate the size of the encoded image in bytes
    memory_size = len(encoded_img)

    return (batch * memory_size) / 1_000_000


def image_to_uint8(image, min_val, max_val):
    """
    > The function takes an image, a maximum value, and a minimum value, and returns an image with
    values scaled to the range [0, 255]

    Args:
      image: The image to be converted.
      max_val: The maximum value of the image.
      min_val: The minimum value of the image.

    Returns:
      The image is being returned as a uint8 array.
    """
    diff_val = max_val - min_val
    image = image - min_val
    return ((image / diff_val) * 255).astype(np.uint8)


def map_value_to_dtype(value: float = 0.5, dtype=np.uint8):
    """
    Given a value in the range between 0-1
    calculate the int value from the dtype.
    ex. given 0.5 and np.uint8, return 128
    Parameters:
    - value : float : value between 0-1
    - dtype : numpy.dtype : dtype to convert to

    Returns:
    - int : value in the dtype

    """
    if value < 0 or value > 1:
        logger.warning("Value must be between 0 and 1, cliping")
        value = np.clip(value, 0, 1)
    return np.iinfo(dtype).max * value


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
    import tifffile
    import numpy as np
    import xmltodict
    from celer_sight_ai import config

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
        # tiff is included here, get_specialized_image will handle ultra high res images
        logger.debug(f"Importing image from {path} : tiff")
        from celer_sight_ai.io.image_reader import (
            interactive_untiled_tiff_preview,
            extract_tile_data_from_tiff,
        )

        # First we attempt to read the image normally, if the image is ultra high res, handle later

        result = get_specialized_image(
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
            open_preview_with_tiffslide_image_reader,
            open_preview_with_openslide_image_reader,
            get_deep_zoom_by_tiffslide,
            get_deep_zoom_by_openslide,
            get_exact_tile_with_openslide,
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
        if not not isinstance(im, type(None)) and not for_thumbnail:
            config.ram_image = im
            config.ram_image_path = path
        if bbox:
            # bbox should be in the format [x,y,w,h]
            from celer_sight_ai.io.image_reader import (
                generate_complete_spiral_tiles,
                crop_and_pad_image,
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
        # remove                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        hannels that are not in the channel_names_to_filter
        # convert text to index
        channel_names_to_filter = [
            config.channel_names.index(i.lower()) for i in channel_names_to_filter
        ]
        # remove channels that are not in the channel_names_to_filter
        im = im[:, :, channel_names_to_filter]
    if (
        not isinstance(im, type(None))
        and not for_thumbnail
        and not for_interactive_zoom
        and isinstance(bbox, type(None))
    ):
        config.ram_image = im
        config.ram_image_path = path
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
    config.global_signals.check_and_update_high_res_slides_signal.emit()


def find_treatment_patterns_within_filepaths(filepaths):
    import re
    from collections import defaultdict
    from os.path import splitext, basename

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

CURSOR_DEFAULT = QtCore.Qt.CursorShape.ArrowCursor
CURSOR_POINT = QtCore.Qt.CursorShape.PointingHandCursor
CURSOR_DRAW = QtCore.Qt.CursorShape.CrossCursor
CURSOR_MOVE = QtCore.Qt.CursorShape.ClosedHandCursor
CURSOR_GRAB = QtCore.Qt.CursorShape.OpenHandCursor


class QMask(QtGui.QPolygonF):
    def __init__(self):
        super(QMask, self).__init__()
        self._IncludedInAnalysis = True
        self.Visibility = True
        self.Color = 1  # rgb r = 0 , g = 1, b = 2
        self.Attribute = None


class BackgroundGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, pixmap=None):
        super().__init__(pixmap)


class ZoomToolsSideScene(Ui_WidgetSceneTools):
    def __init__(self, viewer):
        super(ZoomToolsSideScene, self).__init__()
        self.Myviewer = viewer
        self.MyWidget = QtWidgets.QWidget()
        self.setupUi(self.MyWidget)
        self.retraslateUi(self.MyWidget)
        self.MyWidget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.MyWidget.move(viewer.width(), 20)

        self.FitbuttonTool
        self.ZoomInButtonTool
        self.ZoomOutButtonTool


class DragEventType(IntEnum):
    start = auto()
    stop = auto()
    move = auto()
    repaint = auto()


class ColorPrefsPhotoViewer:
    """
    This class is responsible for getting all of the colors and color preferences associated with the graphics view
    """

    def __init__(self, MainWindow=None):
        super(ColorPrefsPhotoViewer, self).__init__()
        self.Main = MainWindow
        self.AvailabelChannels = {"RED": 0, "GREEN": 1, "BLUE": 2}
        self.ChannelsInUse = [0]
        self.NonSelectedColorDivider = (
            0.5  # to get from pg1_settings_mask_opasity_slider
        )
        self.FillerAlpha = 50
        self.NotSelectedMaskColor = QtGui.QColor(0, 0, 255)
        self.SelectedColor = QtGui.QColor(0, 255, 255)
        self.ChannelGreenColor = QtGui.QColor(0, 0, 255)
        self.ChannelRedColor = QtGui.QColor(0, 0, 255)
        self.ChannelBlueColor = QtGui.QColor(0, 0, 255)
        self.MaskWidth = 2
        self.CurrentPenCapStyle = "RoundCap"
        self.CurrentPenStyle = "SolidLine"
        self.CurrentBrushStyle = "SolidPattern"
        self.MyStyles = {
            "SolidLine": QtCore.Qt.PenStyle.SolidLine,
            "DashLine": QtCore.Qt.PenStyle.DashLine,
            "DotLine": QtCore.Qt.PenStyle.DotLine,
            "DashDotLine": QtCore.Qt.PenStyle.DashDotLine,
            "DashDotDotLine": QtCore.Qt.PenStyle.DashDotDotLine,
            "CustomDashLine": QtCore.Qt.PenStyle.CustomDashLine,
            "SquareCap": QtCore.Qt.PenCapStyle.SquareCap,
            "FlatCap": QtCore.Qt.PenCapStyle.FlatCap,
            "RoundCap": QtCore.Qt.PenCapStyle.RoundCap,
            "SolidPattern": QtCore.Qt.BrushStyle.SolidPattern,
        }

    def GetChannelsInUse(self):
        """
        function To aquiar the current channells
        """
        # get call from pg1_settings_all_masks_color_button
        # get colour from pg1_settings_selected_mask_color_button
        pass

    def setCurrentStyle(self, StyleStr="SolidLine"):
        self.CurrentStyle = str(StyleStr)

    def setCurrentCap(self, CapStyleStr="RoundCap"):
        self.CurrentCapStyle = str(CapStyleStr)

    def setBrushToViewer(self, viewer):
        viewer.setBursh(self.MyStyles[self.CurrentBrushStyle], self.SelectedColor)

    def getPenSelection(self):
        pen = QtGui.QPen(
            self.Main.pg1_settings_all_masks_color_button.palette().button().color()
        )
        pen.setWidth(self.MaskWidth)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getPenStartingPoint(self, color="blue"):
        pen = QtGui.QPen(QtGui.QPen(QtGui.QColor(color), 0.3))
        pen.setWidth(2)
        return pen
        # pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        # pen.setStyle(self.MyStyles[self.CurrentPenStyle])

    def getPen(self, ForMask=False, class_id=None):
        """
        if we has assigned a region to the masks then choose that, otherwise take from the settings quick tools
        """
        color = None
        if class_id:
            color = self.Main.custom_class_list_widget.classes[class_id].color
            if not isinstance(color, type(None)):
                color = QtGui.QColor(*color)
        else:
            color = (
                self.Main.pg1_settings_all_masks_color_button.palette().button().color()
            )
        if not color:
            # generate one temporarily
            color = QtGui.QColor([0, 255, 0])
        pen = QtGui.QPen(color)
        pen.setWidth(self.Main.viewer.QuickTools.lineWidthSpinBoxPolygonTool.value())
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getColorSkGc(self):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 255, 70))
        pen.setWidth(2)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        return pen

    def getBrush(self, class_id=None):
        if class_id:
            Color = self.Main.get_mask_color_from_class(class_id)
        else:
            Color = self.GetColorSelected()
        brush = QtGui.QBrush(
            QtGui.QColor(Color[0], Color[1], Color[2], self.FillerAlpha)
        )
        return brush

    def CreatePen(self, viewer):
        """
        Creates a pen with the appropriate styles
        """
        pen = QtGui.QPen(self.SelectedColor)
        pen.setWidth(self.MaskWidth)
        pen.setCapStyle(self.MyStyles[self.CurrentPenCapStyle])
        pen.setStyle(self.MyStyles[self.CurrentPenStyle])
        viewer.setPen(pen)

    def FillRect(self, painter=None, style=None, widget=None):
        painter.fillRect(self.scene_rect, self._brush)

    def GetColorNotSelected(self):
        return GetRGB_FromHex(self.SelectedColor.name()) / self.NonSelectedColorDivider

    def GetColorSelected(self):
        return np.asarray(GetRGB_FromHex(self.NotSelectedMaskColor.name()))


class ImagePreviewGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None, MainWindow=None):
        super(ImagePreviewGraphicsView, self).__init__(parent)
        from PyQt6.QtOpenGLWidgets import QOpenGLWidget

        self.setMouseTracking(True)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        # use OpenGL for gpu acceleration if available

        # gl_widget = QOpenGLWidget()
        # self.setViewport(gl_widget)

        self.MainWindow = MainWindow
        self.button_container = []
        self.visible_buttons = []
        self.visible_buttons_ids = []
        self.previous_update_pos = None  # update prediodically when scrolling, with spacing of sel.update_spacing
        config.global_signals.ensure_current_image_button_visible_signal.connect(
            self.ensure_current_image_button_visible
        )
        config.global_signals.next_image_signal.connect(self.next_image)
        config.global_signals.previous_image_signal.connect(self.previous_image)
        config.global_signals.ensure_current_image_button_visible_signal.connect(
            self.ensure_current_image_button_visible
        )
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.verticalScrollBar().hide()
        self.verticalScrollBar().resize(0, 0)

        config.global_signals.refresh_image_preview_graphicsscene_signal.connect(
            self.update_visible_buttons
        )
        self.setScene(QtWidgets.QGraphicsScene())

        # show the first 30 buttons by default
        self.start_button_i_to_show = 0
        self.end_button_i_to_show = 30
        self.scene_width = self.get_scene_width()
        # self.MainWindow.splitterImagesRight.setSizes([400, width])
        self.scene().setSceneRect(QtCore.QRectF(0, 0, self.scene_width, 50000))
        # self.MainWindow.statistical_analysis_widget_4.setMinimumWidth(self.scene_width)
        # self.scene().setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self._is_updating_buttons = False

    def reset_state(self):
        self.clear_out_visible_buttons()
        self._is_updating_buttons = False

    def set_updating_buttons(self, value):
        self._is_updating_buttons = value

    def next_image(self):
        """
        Moves the image on the viewr to the next image
        """
        # Make sure that the self.MainWindow.current_imagenumber is not out of bounds
        # Because it will cause an error on get_current_image_object()
        self.MainWindow.current_imagenumber = min(
            self.MainWindow.current_imagenumber,
            len(
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images
            )
            - 1,
        )

        # Move to the next image of the same condition
        if any(
            [
                i.is_suggested
                for i in self.MainWindow.DH.BLobj.get_current_image_object().masks
            ]
        ):
            self.MainWindow.ai_model_settings_widget.prompt_user_to_save_or_delete_suggestions()
            return
        # if mask generation is running, but no images found above ^,
        # then stop the mask generation, and clear up any masks generated while doing so
        if config.group_running.get("start_suggested_mask_generator"):
            # stop and wait to stop all threads
            logger.info("Stopping mask generation as we move on to the next image.")
            self.MainWindow.sdknn_tool.magic_box_2.stop_mask_suggestion_generator_process()
        self.MainWindow.sdknn_tool.magic_box_2.cleanup_memory()
        self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
        self.MainWindow.current_imagenumber += 1
        self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        # iter through visible buttons and set label to white
        for i in self.MainWindow.images_preview_graphicsview.visible_buttons:
            if i.image_number == self.MainWindow.current_imagenumber:
                i.button_instance.setChecked(True)
                i.button_instance.set_label_color()
            else:
                if i.button_instance is not None:
                    i.button_instance.setChecked(False)
                    i.button_instance.set_label_color()
        config.global_signals.ensure_current_image_button_visible_signal.emit()

    def previous_image(self):
        if any(
            [
                i.is_suggested
                for i in self.MainWindow.DH.BLobj.get_current_image_object().masks
            ]
        ):
            self.MainWindow.ai_model_settings_widget.prompt_user_to_save_or_delete_suggestions()
            return
        # if mask generation is running, but no images found above ^,
        # then stop the mask generation, and clear up any masks generated while doing so
        if config.group_running.get("start_suggested_mask_generator"):
            # stop and wait to stop all threads
            logger.info("Stopping mask generation as we move on to the next image.")
            self.MainWindow.sdknn_tool.magic_box_2.stop_mask_suggestion_generator_process()
        self.MainWindow.sdknn_tool.magic_box_2.cleanup_memory()
        self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
        self.MainWindow.current_imagenumber -= 1
        self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        # iter through visible buttons and set label to white
        for i in self.MainWindow.images_preview_graphicsview.visible_buttons:
            if i.image_number == self.MainWindow.current_imagenumber:
                i.button_instance.setChecked(True)
                i.button_instance.set_label_color()
            else:
                if i.button_instance is not None:
                    i.button_instance.setChecked(False)
                    i.button_instance.set_label_color()
        config.global_signals.ensure_current_image_button_visible_signal.emit()

    def ensure_current_image_button_visible(self):
        # scroll to ensure visible
        # if lower than the current scroll position, scroll up to button Y + height - button height

        visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        button_y_pos = (BUTTON_SPACING + BUTTON_HEIGHT) * (
            self.MainWindow.current_imagenumber // BUTTON_COLS
        )
        if button_y_pos < visible_rect.y():
            self.verticalScrollBar().setValue(int(button_y_pos))
        elif (button_y_pos + BUTTON_HEIGHT) > (
            visible_rect.y() + visible_rect.height()
        ):
            # if higher than the current scroll position, scroll down to button Y
            self.verticalScrollBar().setValue(
                int((button_y_pos - visible_rect.height()) + BUTTON_HEIGHT)
            )

    def get_scene_width(self):
        return (BUTTON_WIDTH * (BUTTON_COLS)) + ((BUTTON_COLS + 1) * BUTTON_SPACING)

    def uncheck_all_buttons_except_current(self):
        [
            i.button_instance.set_checked_to_false()
            for i in self.visible_buttons
            if i.image_number != self.MainWindow.current_imagenumber
            and i.button_instance
        ]

    def clear_out_visible_buttons(self):
        # When changing conditions, delete all the buttons of the current condition
        currentCondition = self.MainWindow.DH.BLobj.get_current_condition()
        currentGroup = self.MainWindow.DH.BLobj.get_current_group()
        logger.debug(f"Deleting Current condition : {currentCondition}")
        all_graphic_items = self.scene().items()
        for item in all_graphic_items:
            if isinstance(item, QtWidgets.QGraphicsProxyWidget):
                button_holder = item.widget().ButtonHolder
                button_holder.button_instance = None
                self.scene().removeItem(item)
                item.deleteLater()
        self.visible_buttons_ids = []
        self.visible_buttons = []

    def substract_from_all_buttons(self, reference_id=None, amount=1):
        # remove the amount form all buttons (for image_id), is usually triggered when deleting an image
        # only affect images larger than reference_id

        for b in self.MainWindow.DH.get_all_buttons(
            self.MainWindow.DH.BLobj.get_current_group(),
            self.MainWindow.DH.BLobj.get_current_condition(),
        ):
            if b.image_number > reference_id:
                b.image_number -= amount
                b.button_instance.set_label_number(b.image_number + 1)
        for im, image in enumerate(
            self.MainWindow.DH.BLobj.groups[
                self.MainWindow.DH.BLobj.get_current_group()
            ]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images
        ):
            if image.imgID > reference_id:
                self.MainWindow.DH.BLobj.groups[
                    self.MainWindow.DH.BLobj.get_current_group()
                ].conds[self.MainWindow.DH.BLobj.get_current_condition()].images[
                    im
                ].imgID -= amount

    def place_all_image_buttons_to_correct_positions(self):
        """
        Updates every button image widget to its correct position by its id
        """
        for b in self.visible_buttons:
            p = self.MainWindow.DH.BLobj.get_box_position(b.image_number)
            b.button_instance_proxy.setPos(p[0], p[1])

    def update_visible_buttons(self, condition=None, force_update=False):
        """
        This method is progressivly spawning and despawning buttons as needed within the
        overview_tabs_image -> image_preview_graphicsview.
        """
        try:
            if self._is_updating_buttons:
                return
            self._is_updating_buttons = True

            if condition is None:
                condition = self.MainWindow.DH.BLobj.get_current_condition()
            if condition is None:
                return
            condition_object = self.MainWindow.DH.BLobj.groups["default"].conds[
                condition
            ]
            condition_uuid = condition_object.unique_id

            visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()
            # make it so that the rect has much less space for intersection
            visible_rect = QtCore.QRectF(
                visible_rect.left(),
                visible_rect.top() - IMAGE_PREVIEW_TOP_PAD,
                visible_rect.width(),
                visible_rect.height()
                + IMAGE_PREVIEW_BOTTOM_PAD
                + IMAGE_PREVIEW_BOTTOM_PAD,
            )

            self.start_button_i_to_show = int(
                (visible_rect.top() - BUTTON_SPACING) / (BUTTON_HEIGHT // BUTTON_COLS)
            )
            self.end_button_i_to_show = int(
                (visible_rect.bottom() - BUTTON_SPACING)
                / (BUTTON_HEIGHT // BUTTON_COLS)
            )
            center = visible_rect.center()
            if not center:
                self._is_updating_buttons = False
                return

            # # check if number of buttons // cols is less than height, if it is, update image viewport anyway
            if not len(self.visible_buttons) <= self.end_button_i_to_show:
                # get the difference of the visible rect bottom point and top point and find if its greater than the update spacing
                if not force_update and self.previous_update_pos is not None:
                    # get the center point of the visible rect

                    if (
                        abs(center.y() - self.previous_update_pos)
                        < IMAGE_PREVIEW_BUFFER
                    ):
                        self._is_updating_buttons = False
                        return

            self.previous_update_pos = center.y()
            currentCondition = self.MainWindow.DH.BLobj.get_current_condition()
            currentGroup = self.MainWindow.DH.BLobj.get_current_group()
            # TODO: This needs to become faster, as it is currently blocking the UI
            # iterate over all existsing buttons and hide the ones that are not visible
            for button in self.visible_buttons:
                if button.image_number not in range(
                    max(self.start_button_i_to_show, 0), self.end_button_i_to_show
                ):
                    idx = self.visible_buttons_ids.index(button.image_number)
                    print(f"removing button id {button.image_number} at index {idx}")
                    if (
                        button.button_instance_proxy is not None
                        and button.button_instance_proxy in self.scene().items()
                    ):
                        self.scene().removeItem(button.button_instance_proxy)
                    self.visible_buttons.remove(button)

                    self.visible_buttons_ids.pop(idx)
                    button.button_instance = None
                    button.button_instance_proxy = None

            # show buttons needed
            all_buttons_to_create_instance = []
            total_buttons_len = len(
                self.MainWindow.DH.get_all_buttons(currentGroup, currentCondition)
            )
            for i in range(
                max(self.start_button_i_to_show, 0), self.end_button_i_to_show
            ):
                if i < 0:
                    continue
                if i in self.visible_buttons_ids:
                    continue
                if total_buttons_len <= i:
                    continue
                all_buttons_to_create_instance.append(i)
                button = self.MainWindow.DH.get_button(
                    currentGroup, currentCondition, i
                )

                print(f"Adding button id {button.image_number}")
                self.visible_buttons.append(button)
                self.visible_buttons_ids.append(i)
            # start threaded function that sends signals to create buttons instances

            height = (
                (BUTTON_SPACING + BUTTON_SPACING + BUTTON_HEIGHT)
                * total_buttons_len
                // BUTTON_COLS
            )

            self.scene().setSceneRect(
                QtCore.QRectF(0, 0, self.scene_width, max(500, height))
            )

            all_objects = [
                [
                    currentGroup,
                    condition_uuid,
                    i,
                    True if i == all_buttons_to_create_instance[-1] else None,
                ]
                for i in all_buttons_to_create_instance
            ]
            if len(all_objects) == 0:
                self._is_updating_buttons = False

            per_chunk = 5

            # group objects in a list of 5 if possible
            all_objects = [
                all_objects[i : i + per_chunk]
                for i in range(0, len(all_objects), per_chunk)
            ]

            # Loop through each chunk
            for i in range(len(all_objects)):
                config.global_signals.create_button_instance_signal.emit(all_objects[i])

        except Exception as e:
            print(e)

    def scrollContentsBy(self, dx, dy):
        self.update_visible_buttons()
        super(ImagePreviewGraphicsView, self).scrollContentsBy(dx, dy)

    def mousePressEvent(self, event):
        # get position in scene of the press event
        pos = self.mapToScene(event.pos())
        # get the item at that location
        item = self.itemAt(pos.toPoint())
        # if item is not None, then it is the item you want
        if item is not None:
            # item.click()
            print("item clicked")
        super(ImagePreviewGraphicsView, self).mousePressEvent(event)

    def contextMenuEvent(self, event):
        """
        Conetext menu for Images inside the image preview area that runs on right click
        """
        menu = QtWidgets.QMenu()
        event_pos = self.mapToGlobal(event.pos())
        self.DeleteAction = QtGui.QAction("Delete", None)
        self.DeleteAction.triggered.connect(
            lambda: self.delete_image(proxy_item, widget_item)
        )
        proxy_item = self.scene().itemAt(
            self.mapToScene(event.pos()), QtGui.QTransform()
        )
        widget_item = proxy_item.widget()
        menu.addAction(self.DeleteAction)
        menu.exec(event_pos)

    def delete_image(self, proxy, widget):
        logger.info(f"Deleted image preview item : {widget.image_number}")
        self.scene().removeItem(proxy)
        widget.deleteCurrentImage()
        # TODO: reorder the rest of the items
        return

    def displace_image_preview_widgets_after_delete(self):
        pass


class ArrowChangeImageButton(QtWidgets.QPushButton):
    valueChangedSignal = QtCore.pyqtSignal(int)

    def __init__(
        self,
        imageLocation=None,
        Viewer=None,
        StartingPositionXMOD=0,
        StartingPositionYMOD=0,
        MODE="left",
    ):
        super(ArrowChangeImageButton, self).__init__()
        self.ViewerRef = Viewer
        self.setParent(self.ViewerRef)
        import cv2

        self.installEventFilter(self)
        self.StartingPosY = self.ViewerRef.height() / 2
        self.StartingPosX = self.ViewerRef.width()
        self.StartingPosX_MODIFIER = StartingPositionXMOD
        self.StartingPosY_MODIFIER = StartingPositionYMOD
        self.duringAnim = False
        self.posVisible = False
        self.MODE = MODE
        # Add arrow left and right
        # self = QtWidgets.QPushButton(self.ViewerRef)
        if self.MODE == "left":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX_MODIFIER),
                    int(self.StartingPosY + self.StartingPosY_MODIFIER),
                )
            )

        if self.MODE == "right":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX + self.StartingPosX_MODIFIER),
                    int(self.StartingPosY + self.StartingPosY_MODIFIER),
                )
            )
        self.setMaximumSize(QtCore.QSize(75, 75))
        self.setMinimumSize(QtCore.QSize(75, 75))
        pixmap = QtGui.QPixmap(imageLocation)
        size = QtCore.QSize(60, 60)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)
        self.setStyleSheet(
            """
        QPushButton{
            background-color:rgba(0,0,0,50);
            border-radius: 35;
        }
        QPushButton:hover{
            background-color:rgba(0,0,0,20);
            border-color: rgba(0,0,0,0);
        }
        """
        )
        self.valueChangedSignal.connect(self.onValueChanged)
        # self.sf = QtWidgets.QGraphicsDropShadowEffect()
        # self.sf.setColor(QtGui.QColor(0,0,0,220))
        # self.sf.setBlurRadius(30)
        # self.setGraphicsEffect(self.sf)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        if MODE == "left":
            animationStart = self.StartingPosX_MODIFIER
            animationEnd = self.StartingPosX_MODIFIER + 50
        elif MODE == "right":
            animationStart = self.ViewerRef.width() + self.StartingPosX_MODIFIER
            animationEnd = self.ViewerRef.width() + self.StartingPosX_MODIFIER - 50
        self.show_animation = QtCore.QVariantAnimation(
            self,
            startValue=animationStart,
            endValue=animationEnd,
            # valueChanged=self.valueChangedSignal,
            duration=200,
            easingCurve=QtCore.QEasingCurve.Type.InOutCubic,
        )
        self.hide_animation = QtCore.QVariantAnimation(
            self,
            startValue=animationEnd,
            endValue=animationStart,
            # valueChanged=self.valueChangedSignal,
            duration=1000,
            easingCurve=QtCore.QEasingCurve.Type.InOutCubic,
        )
        self.show_animation.finished.connect(lambda: self.setPosVisible(True))
        self.hide_animation.finished.connect(lambda: self.setPosVisible(False))
        if self.MODE == "right":
            self.hide_animation.setStartValue(self.pos().x())
            self.hide_animation.setEndValue(
                self.ViewerRef.width() + self.StartingPosX_MODIFIER
            )
            self.duringAnim = True
            self.posVisible = False
            self.hide_animation.start()
        if self.MODE == "left":
            self.hide_animation.setStartValue(self.pos().x())
            self.hide_animation.setEndValue(self.StartingPosX_MODIFIER)

            self.duringAnim = True
            self.posVisible = False
            self.hide_animation.start()

        # self.hide_animation.start()

    # @QtCore. pyqtSlot(bool)
    # def onToggled(self, checked):
    #     self.m_animation.setDirection(
    #         QtCore.QAbstractAnimation.Forward
    #         if checked
    #         else QtCore.QAbstractAnimation.Backward
    #     )
    #     self.m_animation.start()
    def setPosVisible(self, Viz):
        print("SETTING VISIBLE")
        self.posVisible = Viz
        self.duringAnim = False

    @QtCore.pyqtSlot(int)
    def onValueChanged(self, value):
        self.move(
            QtCore.QPoint(
                int(value),
                int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
            )
        )
        # print(value)

    def updatePositionViewer(self):
        if self.MODE == "left":
            self.move(
                QtCore.QPoint(
                    int(self.StartingPosX_MODIFIER),
                    int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
                )
            )
        if self.MODE == "right":
            self.move(
                QtCore.QPoint(
                    int(self.ViewerRef.width() + self.StartingPosX_MODIFIER),
                    int(self.ViewerRef.height() / 2 + self.StartingPosY_MODIFIER),
                )
            )

    def leaveEvent(self, event):
        if self.MODE == "right":
            if self.duringAnim == True:
                self.show_animation.stop()
                self.duringAnim = False
            if self.duringAnim == False:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER
                )
                self.duringAnim = True
                self.posVisible = False
                self.hide_animation.start()
        if self.MODE == "left":
            if self.duringAnim == True:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(self.StartingPosX_MODIFIER - 50)
                # self.show_animation.stop()
                self.duringAnim = False
                self.hide_animation.start()
            if self.duringAnim == False:
                self.hide_animation.setStartValue(self.pos().x())
                self.hide_animation.setEndValue(self.StartingPosX_MODIFIER)
                self.duringAnim = True
                self.posVisible = False
                self.hide_animation.start()
        return super(ArrowChangeImageButton, self).leaveEvent(event)

    def enterEvent(self, event):
        if self.duringAnim == True:
            # self.show_animation.stop()
            self.hide_animation.stop()
            self.duringAnim = False
        if self.MODE == "left":
            if self.duringAnim == False:
                self.show_animation.setStartValue(self.StartingPosX_MODIFIER)
                self.show_animation.setEndValue(self.StartingPosX_MODIFIER + 40)
                self.duringAnim = True
                self.show_animation.start()
        if self.MODE == "right":
            if self.duringAnim == False:
                self.show_animation.setStartValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER
                )
                self.show_animation.setEndValue(
                    self.ViewerRef.width() + self.StartingPosX_MODIFIER - 40
                )
                self.duringAnim = True
                self.show_animation.start()
        return super(ArrowChangeImageButton, self).enterEvent(event)


class PhotoViewer(QtWidgets.QGraphicsView):
    """Image viewer for celer sight. The main viewer that displays and annotates images.

    Args:
        QtWidgets (UiMainWindow): The reference to the main window

    Returns:
        PhotoViewer: the qgraphicsview viewer
    """

    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    object_signal = QtCore.pyqtSignal()
    zoomRequest = QtCore.pyqtSignal(int)
    scrollRequest = QtCore.pyqtSignal(int, int)
    newShape = QtCore.pyqtSignal()
    selectionChanged = QtCore.pyqtSignal(bool)
    shapeMoved = QtCore.pyqtSignal()
    drawingPolygon = QtCore.pyqtSignal(bool)
    finishDraw = QtCore.pyqtSignal(bool)
    CREATE, EDIT = 0, 1
    epsilon = 11.0

    WHEEL_STEP = 15 * 8  # degrees

    __slots__ = (
        "app",
        "angleRemainder",
        "zoomValue",
    )

    mouseMoved = QtCore.pyqtSignal(QtGui.QMouseEvent)
    mousePressed = QtCore.pyqtSignal(QtGui.QMouseEvent)
    mouseReleased = QtCore.pyqtSignal(QtGui.QMouseEvent)
    wheelScrolled = QtCore.pyqtSignal(int)
    dragEvent = QtCore.pyqtSignal(DragEventType)
    drag_mode: QtWidgets.QGraphicsView.DragMode

    underReload = False
    last_positions = (0, 0)

    autofit = False

    def __init__(self, MainWindow=None):
        super(PhotoViewer, self).__init__()
        # super(Ui_MainWindow, self).__init__()
        from celer_sight_ai import config
        from celer_sight_ai.gui.custom_widgets.scene import BackgroundGraphicsItem

        from PyQt6.QtOpenGLWidgets import QOpenGLWidget

        gl_widget = QOpenGLWidget()
        self.setViewport(gl_widget)

        self.previousTool = None
        self.scene_rect = None  # to be deleted
        self.app = QtWidgets.QApplication.instance()
        self.angleRemainder = 0
        self.zoomValue = 0.0
        self.currentZoom = 0.0
        self.old_mouse_position = None

        self.drag_mode = self.dragMode()

        self.setMinimumHeight(50)
        self.setMinimumWidth(50)
        self.setMaximumHeight(100000)
        self.setMaximumWidth(100000)

        # Particle analysis specfic
        self._is_particle_settled = (
            False  # => wether or not the particle analysis settings have been set
        )
        self._is_particle_ui_spawned = False
        # On a particle analysis these are either set by clicking on the particles class / ROI in the class
        # widget item or by clicking on the analysis button

        # Polygon Add or Remove MODE:
        self.POLYGON_MODIFY_MODE = None
        self.POLYGON_MODIFY_ADD = 1
        self.POLYGON_MODIFY_REMOVE = 2
        self.moving_line = None

        # MAGIC BOX tool attributes
        self.aa_tool_draw = False
        # Indicates if we are currently drawing an auto tool (for the event filter) bbox = bounding box
        self.during_drawing_bbox = False
        self.FG_add = True  # adding aatool state
        self.BG_add = False  # removing brush aatool state
        # the state that activates after we have drawn the aa_tool(Grab cut / auto cut) box and  we want to review the mask
        self.aa_review_state = False

        # ai inference bbox graphics item reference
        self.inference_tile_box_graphic_items = {}
        # config -> interrupt_mask_suggestion_process variable to control the process
        self.during_mask_suggestion_cleanup = (
            False  # On when cleanup to avoid race conditions
        )

        # ML brush draw forground an background
        self.brushMask_STATE = False
        self.brushMask_DuringDrawing = False

        # remove masks brush
        self.rm_Masks_STATE = False
        self.rm_Masks_tool_draw = False
        self.rm_Masks_during_drawing = False
        self.rm_Masks_BrushSize = 5  # in pixels

        # tool for spliting cells
        # CELL_SPLIT_SEED
        self.CELL_SPLIT_TOOL_STATE = False
        self.CELL_SPLIT_DRAWING = False
        self.CELL_SPLIT_SPOTS = []
        self.CELL_SPLIT_FIRST_SPOT_PLACED = False
        self.sceneCELL_SPLIT_ITEMS = []

        self.ML_past_X_train = None
        self.ML_past_Y_train = None

        # scale bar tool
        self.scaleBarDraw_STATE = False
        self.scaleBarDraw_duringDraw_STATE = False
        self.scaleBar_FirstPoint = []
        self.scaleBarWhileLine = None
        self.scaleBarFinalDistance = None
        # cell random forrest machine learning: CELL_RM_

        self.ML_brush_tool_object_state = False
        self.ML_brush_tool_object_during_inference = False
        # First boolean that allows to draw with machine learning
        self.ML_brush_tool_draw_is_active = False
        # Indicates if we are currently drawing an auto tool (for the event filter) bbox = bounding box
        self.ML_brush_tool_draw_during_draw = False
        self.ML_brush_tool_draw_foreground_add = True  # adding aatool state
        self.ML_brush_tool_draw_background_add = False  # removing brush aatool state
        # the state that activates after we have drawn the aa_tool(Grab cut / auto cut) box and  we want to review the mask
        self.ML_brush_tool_draw_mode_review = False  # user reviews drawing
        self.ML_brush_tool_draw_foreground_array = (
            None  # the canvas that we draw Forground
        )
        self.ML_brush_tool_draw_background_array = (
            None  # the canvas that we draw background
        )
        self.ML_brush_tool_draw_brush_size = 2  # in pixels
        self.ML_brush_tool_draw_background_added = False
        self.ML_brush_tool_draw_foreground_added = False
        self.ML_brush_tool_draw_refreshed = False
        self.ML_brush_tool_draw_scene_items = []
        # this becomes true after 1st model, and if true we ask to apply the model to the new loaded image
        self.ML_brush_tool_draw_continous_inference = False
        self.ML_brush_tool_draw_last_model = None
        # normal is the first time, also retrain to train on top of new
        self.ML_brush_tool_draw_training_mode = "NORMAL"

        self.ML_brush_tool_object = None

        # Focus widget list contaning all of the widgets that make our scene darker
        self.sceneFocusWidgetList = []

        # skeleton grub cut variation
        self.SkGb_during_drawing = False  # if we are currently drawing
        self.SkGb_STATE = False  # if tool is active
        self.SkGb_points = []  # points to form polyline
        # allof the lines in the scene, we delete after completion
        self.SkBG_allLineScene = []
        self.SkGb_whileLine = 0  # here not to make errors later

        # magic Click Tool
        self.mgcClick_STATE = False  # if tool is active
        self.mgcClick_points = []  # points to form polyline
        self.mgcBrushT_Pos = 0
        self.magic_brush_cursor = None  # scene item for magic_brush_move
        self.mgcClickWidth = 120  # default

        # magic Brush move Tool:
        self.mgcBrushT = False  # if we are currently drawing
        self.MAGIC_BRUSH_STATE = False  # if tool is active
        self.MAGIC_BRUSH_DURING_DRAWING = False  # points to form polyline
        self.mgcBrushT_i_am_drawing_state = False  # points to form polyline
        self.magic_brush_pos_a = 0

        self.magic_brush_radious = 70
        self.magic_brush_points_set_A = []

        self._deepzoom_pixmaps = []  # temporary storage for deepzoom pixmaps LIFO

        self.polyTmpItems = []  # tempopral items to delete later

        self.myScene_worm_mask_points_x_slot = []
        self.myScene_worm_mask_points_y_slot = []

        self.loading_tile_inference_graphic_items = (
            {}
        )  # list of current scene loading tile inference graphic items
        # these indicate the current position in the scene is being processed.

        self.MoveTool = False  # from actionMoveTool when its in use its true

        self.sceneItemsListUndo = []
        self.moving_lineItemsList = []

        # This is the current position on screen during drawing, for keypressevent
        self.CurrentPosOnScene = None
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.SmartViewportUpdate
        )
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        # self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.ExtBounds = 500  # amound with which to extend the bounds

        self.base_step = 0.05

        self.buttonPress = False  # indicates if button is pressed to replace
        self.global_pos_x = 0
        self.global_pos_y = 0
        self.SelectionStateRegions = False
        # Indicates when the Pop up menu is visible for the user to select a tool (popup_tool_menu.py)
        self.pop_up_tool_choosing_state = False
        self.MainWindow = MainWindow

        # Rubberband Properties
        self.rubberBandOrigin = 0  # origin
        self.sceneRubberband = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Shape.Rectangle, self
        )  # rubberband
        self.rubberBandActive = True
        self.duringRubberbandDrawing = False
        # this is to be used to clear the scene only on the first drag frame
        self.firstRubberBandDrag = True
        self.startPointDrawingS = None
        self.startPointDrawingL = None

        from celer_sight_ai.gui.custom_widgets.popup_tool_menu_Handler import (
            Ui_tool_selection_onscreen_menu,
        )

        self.ui_tool_selection = Ui_tool_selection_onscreen_menu(MainWindow)
        config.global_signals.tool_signal_to_main.connect(
            lambda: self.disable_aa_tool()
        )

        ##########################
        ######## SIGNALS #########
        ##########################

        # self.scrollContentsBy = self.scrollContentsByNew
        from celer_sight_ai import config

        config.global_signals.spawnLoadedMLModelSignal.connect(
            lambda: self.spawnModelLoadedText()
        )
        config.global_signals.removeLoadedMLModelSignal.connect(
            lambda: self.removeModelLoadedText()
        )
        config.global_signals.add_inference_tile_graphics_item_signal.connect(
            self.add_inference_tile_graphics_item
        )
        config.global_signals.remove_inference_tile_graphics_item_signal.connect(
            self.remove_inference_tile_graphics_item
        )
        config.global_signals.remove_all_inference_tile_graphics_items_signal.connect(
            self.remove_all_inference_tile_graphics_items
        )
        config.global_signals.spawn_inference_tile_graphics_items_signal.connect(
            self.spawn_inference_tile_graphics_items
        )

        # during drag mode only
        self.leftMouseBtn_autoRepeat = False

        # QGraphics Polygon tempStore variable
        self.QpolygonsSaved_Y = []
        self.QpolygonsSaved_X = []

        # Menus:
        self.menus = (QtWidgets.QMenu(), QtWidgets.QMenu())
        self.Cpixmap = None
        self.drop_urls = self.object_signal
        self._zoom = 0
        self._empty = True
        self._scene = SceneViewer(self)
        self._photo = BackgroundGraphicsItem()
        self._photo.setZValue(-50)
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setMouseTracking(True)

        # AUTO MASK TOOL WITH BOUNDING BOX
        self.add_mask_btn_state = False
        self.during_drawing = False
        self.i_am_drawing_state = False
        self.i_am_drawing_state_bbox = False
        self.polyPreviousSelectedItems = []
        self.polygon_graphic_grip_items = []  # grip items ad polygon is created
        guide_pen = QtGui.QPen(
            QtGui.QColor(255, 255, 255, 255), 1, QtCore.Qt.PenStyle.DashLine
        )
        guide_pen.setCosmetic(True)

        self.guide_magic_tool_is_spawned = False
        self.h_guide_magic_tool = self.scene().addLine(
            -100, 0, 200, 0, guide_pen
        )  # horizontal guide line
        self.v_guide_magic_tool = self.scene().addLine(
            0, -100, 0, 200, guide_pen
        )  # vertical guide line

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(15, 15, 15)))
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.setMouseTracking(True)
        self.installEventFilter(self)

        # Label at topleft position indicating current image number

        self.LabelNumberViewer = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.LabelNumberViewer.sizePolicy().hasHeightForWidth()
        )
        self.LabelNumberViewer.setSizePolicy(sizePolicy)
        self.LabelNumberViewer.setMaximumSize(QtCore.QSize(16777215, 100))
        self.LabelNumberViewer.setMinimumSize(QtCore.QSize(100, 60))
        font = QtGui.QFont()
        font.setPointSize(44)
        self.LabelNumberViewer.setFont(font)
        self.LabelNumberViewer.setObjectName("LabelNumberViewer")
        self.LabelNumberViewer.setText("-")
        self.LabelNumberViewer.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        # self.gridLayout_18.addWidget(self.pg1_settings_brightness_label, 2, 0, 1, 1)
        self.LabelNumberViewer.setStyleSheet(
            """color:rgba(255,255,255,180);
        background-color:rgba(0,0,0,0);
        margin-left:10px;"""
        )
        self.LabelNumberViewer.move(0, -10)
        self.LabelMasksNumber = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.LabelMasksNumber.sizePolicy().hasHeightForWidth()
        )
        self.LabelMasksNumber.setSizePolicy(sizePolicy)
        self.LabelMasksNumber.setMaximumSize(QtCore.QSize(16777215, 100))
        self.LabelMasksNumber.setMinimumSize(QtCore.QSize(100, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LabelMasksNumber.setFont(font)
        self.LabelMasksNumber.setObjectName("LabelMasksNumber")
        self.LabelMasksNumber.setText("Masks : " + "0")
        # self.gridLayout_18.addWidget(self.pg1_settings_brightness_label, 2, 0, 1, 1)
        self.LabelMasksNumber.setStyleSheet(
            """color:rgba(255,255,255,180);
        background-color:rgba(0,0,0,0);
        margin-left:10px;"""
        )
        self.LabelMasksNumber.move(55, -10)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.LeftArrowChangeButton = ArrowChangeImageButton(
            MODE="left",
            imageLocation="data\\NeedsAttribution\\LeftPageArrow.png",
            Viewer=self,
            StartingPositionXMOD=-45,
            StartingPositionYMOD=0,
        )
        self.RightArrowChangeButton = ArrowChangeImageButton(
            MODE="right",
            imageLocation="data\\NeedsAttribution\\RightPageArrow.png",
            Viewer=self,
            StartingPositionXMOD=-30,
            StartingPositionYMOD=0,
        )

        self.LeftArrowChangeButton.hide()
        self.RightArrowChangeButton.hide()

        self.LeftArrowChangeButton.clicked.connect(lambda: self.MoveRightImage())
        self.RightArrowChangeButton.clicked.connect(lambda: self.MoveLeftImage())

        from celer_sight_ai.gui.custom_widgets.QitemTools import quickToolsUi

        self.QuickTools = quickToolsUi(self)

    def removeItemByUuid(self, uuid):
        for item in self.scene().items():
            if hasattr(item, "uuid"):
                if item.uuid == uuid:
                    self.scene().removeItem(item)

    def getML_brush_tool_draw_brush_size(self):
        # get the size of the ML Brush
        gl = config.global_params
        an = self.MainWindow.new_analysis_object
        return self.QuickTools.BrushRadiusCellRandomForestSlider.value()
        if gl.area == an.scratch:
            return 4
        else:
            return 2

        # Button to change from drag/pan to getting pixel info

    def updateAllPolygonPen(self):
        # Make sure that existing annotations are updated with the new pen
        # iterate over all elements in the scene
        # Set the opacity of the color of the current condition
        class_id = (
            self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id
        )
        self.MainWindow.custom_class_list_widget.classes[class_id].set_opacity(
            int(self.MainWindow.pg1_settings_mask_opasity_slider.value())
        )
        # update only the current class items
        for item in self.scene().items():
            if isinstance(item, (PolygonAnnotation, BitMapAnnotation)):
                if class_id == item.class_id:
                    # update color
                    item.update_annotations_color()

    # @config.threaded
    # def update_scene_partial_image(self, object):
    #     """
    #     Updates the scene progressivily from a partial image file
    #     object : dict
    #         {
    #             "image_uuid": str,
    #             "image_position": [int, int], centerpoint of the image
    #             "image_size": [int, int], width and height of the image
    #         }
    #     """

    #     image_position = object.get("image_position", None)
    #     image_size = object.get("image_size", None)
    #     image_uuid = object.get("image_uuid", None)
    #     if image_uuid is None:
    #         # get the current image object
    #         image_object = (
    #             self.MainWindow.DH.BLobj.groups["default"]
    #             .conds[self.MainWindow.DH.BLobj.get_current_condition()]
    #             .images[self.MainWindow.current_imagenumber]
    #         )
    #     else:
    #         # get image by uuid
    #         image_object = (
    #             self.MainWindow.DH.BLobj.groups["default"]
    #             .conds[self.MainWindow.DH.BLobj.get_current_condition()]
    #             .get_image_by_uuid(image_uuid)
    #         )
    #         if not image_object:
    #             logger.info("Image uuid could not be retrieved")

    #     # make sure its the same image uuid with the same image uuid
    #     # get current image uuid
    #     current_image_uuid = (
    #         self.MainWindow.DH.BLobj.groups["default"]
    #         .conds[self.MainWindow.DH.BLobj.get_current_condition()]
    #         .images[self.MainWindow.current_imagenumber]
    #         .uuid
    #     )
    #     if current_image_uuid != image_object.uuid:
    #         logger.info("Image uuid does not match")
    #         return

    def add_inference_tile_graphics_item(self, object):
        """
        Object is {
        "tile_box" : [x,y,w,h]
        "inference_uuid" : str
        "image_uuid" : str
        }
        adds graphics item object to scene and appends it to add_inference_tile_graphics_item
        Return: graphics scene item, so that it can be removed without re-indexing
        """
        from celer_sight_ai.gui.custom_widgets.animate_processing_bbox import (
            ProcessingBox,
        )

        tile = object["tile_box"]
        inference_uuid = object.get("inference_uuid")
        image_uuid = object.get("image_uuid")
        is_animated = object.get("is_animated", False)
        # get current image object
        current_io = self.MainWindow.DH.BLobj.get_current_image_object()
        if current_io.unique_id == image_uuid:
            # add the annotation to the scene
            graphics_item = ProcessingBox(tile, self.scene(), is_animated=is_animated)
            # QtWidgets.QGraphicsRectItem(tile[0], tile[1], tile[2], tile[3])
            self.scene().addItem(graphics_item)
            # white pen
            # pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255))
            # # set pen comsetic
            # graphics_item.setPen(pen)
            self.loading_tile_inference_graphic_items[inference_uuid] = graphics_item
        # get the image object
        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(image_uuid)
        # add inference id to image object
        image_object.graphics_tile_items[inference_uuid] = tile
        self.inference_tile_box_graphic_items[inference_uuid] = {
            "tile_box": tile,
            "image_uuid": image_uuid,
        }

    def remove_inference_tile_graphics_item(self, object):
        """
        Object is a tile item, index from mask_suggestion_bbox_scene_items to get the graphics
        item to remove
        """
        inference_uuid = object.get("inference_uuid")
        full_cleanup = object.get("full_cleanup")
        # if its partial, we only remove the graphics item (bbox of the tile and shperes)
        self.during_mask_suggestion_cleanup = True
        # get image object by uuid
        # delete from the list of the current used graphic items
        if inference_uuid in self.loading_tile_inference_graphic_items:
            inference_graphics_item = self.loading_tile_inference_graphic_items.get(
                inference_uuid
            )
            if (
                inference_graphics_item
                and inference_graphics_item in self.scene().items()
            ):
                # if the graphics item is in the scene, remove it
                inference_graphics_item.cleanup()
            del self.loading_tile_inference_graphic_items[inference_uuid]
        # delete from dict used by viewer to update the scene when we switch images
        if inference_uuid in self.inference_tile_box_graphic_items:
            image_uuid = self.inference_tile_box_graphic_items[inference_uuid].get(
                "image_uuid"
            )
            # get image object
            image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(image_uuid)
            # delete the inference uuid from image_object.graphics_tile_items
            if inference_uuid in image_object.graphics_tile_items:
                del image_object.graphics_tile_items[inference_uuid]
            del self.inference_tile_box_graphic_items[inference_uuid]
        if full_cleanup:
            for (
                inference_uuid,
                graphics_item,
            ) in self.loading_tile_inference_graphic_items.items():
                if graphics_item and graphics_item in self.scene().items():
                    graphics_item.cleanup()
            self.remove_all_suggested_annotations_from_current_image()
        self.during_mask_suggestion_cleanup = False

    def remove_all_inference_tile_graphics_items(self):
        # Remove all inference tile graphics items from the scene
        for graphics_item in list(self.loading_tile_inference_graphic_items.values()):
            if graphics_item and graphics_item in self.scene().items():
                graphics_item.cleanup()
        # iterate over all image objects and remove the graphics items
        for image_object in self.MainWindow.DH.BLobj.get_all_image_objects():
            image_object.graphics_tile_items.clear()
        # Clear the dictionaries to remove references to the graphics items
        self.loading_tile_inference_graphic_items.clear()
        self.inference_tile_box_graphic_items.clear()

    def spawn_inference_tile_graphics_items(self):
        """
        Spawn all the inference tile graphics items
        """
        from celer_sight_ai.gui.custom_widgets.animate_processing_bbox import (
            ProcessingBox,
        )

        if not self.inference_tile_box_graphic_items:
            return
        self.MainWindow.during_load_main_scene_display = True
        try:
            # get current image object and only spawn tiles for that object
            current_io = self.MainWindow.DH.BLobj.get_current_image_object()
            for inference_uuid, value in self.inference_tile_box_graphic_items.items():
                if value.get("image_uuid") == current_io.unique_id:
                    graphics_item = ProcessingBox(value.get("tile_box"), self.scene())
                    self.scene().addItem(graphics_item)
                    self.loading_tile_inference_graphic_items[inference_uuid] = (
                        graphics_item
                    )
        except Exception as e:
            logger.error(e)
        finally:
            self.MainWindow.during_load_main_scene_display = False

    def remove_all_suggested_annotations_from_current_image(self):
        # get all masks in the scene
        all_masks_in_scene = [
            i for i in self.scene().items() if isinstance(i, (PolygonAnnotation))
        ]
        masks_to_remove = [i for i in all_masks_in_scene if i.is_suggested]
        for m in masks_to_remove:
            self.scene().removeItem(m)

    # add the partial image
    @config.threaded
    @config.group_task("update_scene_ultra_high_res_plane")
    def update_scene_ultra_high_res_plane(self, object):
        """
        image_uuid: str
        image_position: [int, int]
        image_size: [int, int]
        """
        logger.info(
            f"Updating scene ultra high res plane with bbox {config.viewport_bounding_box}"
        )
        # # get image object by uuid
        image_object = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[object.get("image_uuid", None)]
        )
        if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
            return
        # image_object._during_scene_update = True
        try:
            from celer_sight_ai.io.image_reader import (
                get_deep_zoom_by_tiffslide,
                get_deep_zoom_by_openslide,
            )

            get_deep_zoom_by_openslide(
                image_object.get_path(), config.viewport_bounding_box
            )

        except Exception as e:
            logger.error(e)
            pass
        # image_object._during_scene_update = False
        if config.group_stop_flags.get("update_scene_ultra_high_res_plane"):
            return
        # run update once more at the end
        if object.get("update_again", False):
            # The above code is setting the `_during_scene_update` attribute of the `image_object` to
            # `False`.
            object["update_again"] = False
            config.global_signals.update_scene_ultra_high_res_plane_signal.emit(object)

    def add_partial_slide_images_to_scene(self, object):
        """
        Adds a partial slide image to the scene.

        This method takes a dictionary object containing image data and image bounding box (of the silde) information.
        It converts the image data to a QPixmap and adds it to the scene.
        The image is positioned according to the bounding box information.
        The method also ensures that the number of deepzoom pixmaps does not exceed 2 by removing the oldest one if necessary.

        Parameters:
        object (dict): A dictionary containing the following keys:
            - "image_data" (bytes): The image data in JPEG format.
            - "image_bounding_box" (QtCore.QPoint, optional): The position of the image in the scene. Defaults to QtCore.QPoint(0, 0).

        Returns:
        None
        """
        from celer_sight_ai.io.image_reader import DEEPZOOM_TILE_SIZE
        import heapq

        logger.info("Adding deepview images to scene")
        image_objects = object.get("image_data", None)
        bbox_objects = object.get("image_bounding_box", None)
        image_name = object.get("image_name", None)
        items_added = []
        idx = 0
        # remove large objects
        if len(config._deepzoom_pixmaps) > config.MAX_DEEPZOOM_OBJECTS:
            # Use a heap to find the largest items
            largest_items = heapq.nlargest(
                config.MAX_DEEPZOOM_OBJECTS,
                config._deepzoom_pixmaps,
                key=lambda x: x[3],
            )

            items_to_remove = [
                item
                for item in config._deepzoom_pixmaps
                if item not in largest_items
                and item[2] != config._current_deep_zoom_downsample_level
            ]
            for item in items_to_remove:
                config._deepzoom_pixmaps.remove(item)
                try:
                    self.scene().removeItem(item[0])
                except Exception as e:
                    logger.error(e)
        image_object = image_objects[0]
        bbox = bbox_objects[0]
        idx += 1

        photo = QtWidgets.QGraphicsPixmapItem()
        logger.debug(f"Pixmap width is {image_object.width()}")
        scale = bbox[2] / image_object.width()
        photo.setPos(bbox[0], bbox[1])
        photo.setScale(scale)
        photo.setPixmap(image_object)
        photo.setCacheMode(
            QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache
        )  # DeviceCoordinateCache
        downsample = 1 / scale
        # make sure current image is the same as the objects unique id
        condition_object = self.MainWindow.DH.BLobj.get_current_condition_object()
        if not condition_object:
            return
        try:
            current_image_object = condition_object.images[
                self.MainWindow.current_imagenumber
            ]
            if not current_image_object:
                return
            if (
                current_image_object.fileName != image_name
                or self.MainWindow.during_load_main_scene_display
                or self.MainWindow.during_scene_refresh
            ):
                logger.debug("Got a differnt image object while updating deep maps")
                return
            self.scene().addItem(photo)
            items_added.append(
                (
                    photo,
                    np.array(bbox),
                    downsample,
                    len(config._deepzoom_pixmaps) + idx,
                    image_name,
                )
            )
            config._current_deep_zoom_downsample_level = downsample
            config.tiles_in_use.append([bbox, round(downsample)])
            # make every item z value of -49
            config._deepzoom_pixmaps = items_added + config._deepzoom_pixmaps

            # get unique values
            unique_downsample = list(set([i[2] for i in config._deepzoom_pixmaps]))
            unique_downsample.sort(reverse=True)
            # unique_downsample = sorted(unique_downsample, reverse=True)
            # create an order dict from 1 to len(unique_downsample)
            order_dict = {
                round(i, 3): idx for idx, i in enumerate(reversed(unique_downsample))
            }
        except Exception as e:
            logger.error(e)
            return
        for i, item in enumerate(config._deepzoom_pixmaps):
            try:
                item[0].setZValue(-50 + order_dict[round(item[2], 3)])
            except Exception as e:
                logger.error(e)
                pass

    def MoveLeftImage(self):
        if (
            self.MainWindow.current_imagenumber
            < len(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images
            )
            - 1
        ):
            self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
            self.MainWindow.current_imagenumber += 1
            self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
            self.MainWindow.myButtonHandler.SetCheckToTrue(
                self.MainWindow.current_imagenumber
            )
            self.MainWindow.myButtonHandler.UnparentLastCondition(Mode="MASK")
            self.MainWindow.myButtonHandler.UpdateMasks(
                self.MainWindow.RNAi_list.currentItem().text(),
                self.MainWindow.current_imagenumber,
            )

    def MoveRightImage(self):
        if self.MainWindow.current_imagenumber > 0:
            self.MainWindow.previous_imagenumber = self.MainWindow.current_imagenumber
            self.MainWindow.current_imagenumber -= 1
            self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
            self.MainWindow.myButtonHandler.SetCheckToTrue(
                self.MainWindow.current_imagenumber
            )
            self.MainWindow.myButtonHandler.UnparentLastCondition(Mode="MASK")
            self.MainWindow.myButtonHandler.UpdateMasks(
                self.MainWindow.RNAi_list.currentItem().text(),
                self.MainWindow.current_imagenumber,
            )

    def resizeEvent(self, event):
        # self.myGlobalWidthStart = self.MainWindow.dock_for_group_pg1_left.width()
        self.myGlobalWidthEnd = self.width()
        self.LeftArrowChangeButton.updatePositionViewer()
        self.RightArrowChangeButton.updatePositionViewer()
        # TODO: This hideMe function needs to be fixed as it causes a crash.
        # if self.mapToScene(self.QuickTools.myquickToolsWidget.pos()).x() < self.width():
        #     self.QuickTools.videowidget.hideME()
        return super(PhotoViewer, self).resizeEvent(event)

    # def focusOutEvent(self, event):
    #     # This ensures that when the focus goes out, it is set back.
    #     # this is a temporary messy fix for the focus issue (keystrokes not registering)
    #     self.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)

    def dragMoveEvent(self, event):
        """Event handler for various events involving drugging items, currently uses:
                - drag and drop for images to the current condition / group

        Args:
            event (QEvent):
        """
        md = event.mimeData()

        if md.hasUrls():
            import os

            event.acceptProposedAction()
            event.accept()
            path, myending = os.path.splitext(md.urls()[0].path())
            if ".plab" in myending:
                event.acceptProposedAction()
            listOfAccepted = [
                ".TIF",
                ".tif",
                ".tiff",
                ".png",
                ".PNG",
                ".jpg",
                "jpeg",
                "jpg",
                "JPEG",
                "JPG",
            ]
            if myending in listOfAccepted:
                event.acceptProposedAction()

    def update_class_scene_color(self, mask_uuid: int):
        """Updates the QGraphicsItem placed in the scene that represenets the mask with the id provided

        Args:
            mask_uuid (int): mask id to reference the original mask object
        """
        mask_obj = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[self.MainWindow.current_imagenumber]
            .get_by_uuid(mask_uuid)
        )

        for item in self.scene().items():
            if hasattr(item, "mask_uuid"):
                if item.mask_uuid == mask_obj.unique_id:
                    item = self.MainWindow.set_mask_color_from_class(
                        item, mask_obj.class_id
                    )
                    item.update()

    def add_new_images_by_drag_and_drop(self, urls: list = [], check_for_videos=False):
        allImagesDropednLoaded = []
        allFilesPaths = []

        if len(urls) != 0:
            if self.MainWindow.RNAi_list.count() == 0:
                self.MainWindow.add_new_treatment_item()
        else:
            logger.info("No images were drag-and-dropped, aborting")
            return
        self.MainWindow.myButtonHandler.SetUpButtons(
            self.MainWindow.DH.BLobj.get_current_condition(),
            self.MainWindow,
            imagesUrls=urls,
            check_for_videos=check_for_videos,
        )
        # self.MainWindow.load_main_scene(fit_in_view=True)

    def dropEvent(self, event):
        """
        url drop event for drag and drop action on the main viewer
        """
        md = event.mimeData()
        print(md)
        if md.hasUrls():
            import os

            urls = [i.toLocalFile() for i in md.urls()]
            self.load_files_by_drag_and_drop(urls)
            event.acceptProposedAction()
            event.accept()
        # return super(PhotoViewer, self).dropEvent( event)

    def combine_image_channels_and_save_to_disk_as_one_folder(
        self, image_channel_list, channel_names, multi_treatment=False, treatmetns=None
    ):
        # Combines all images into one image , saves it to disk and returns the url
        import copy

        image_channel_list_arr = []
        channel_names_arr = []
        if not multi_treatment:
            image_channel_list_arr.append(image_channel_list)
            channel_names_arr.append(channel_names)
        else:
            image_channel_list_arr = image_channel_list
            channel_names_arr = channel_names
        for i in range(len(image_channel_list_arr)):  # for each treatment
            if not len(image_channel_list_arr[i]):
                return
            if not channel_names:
                return

            if not sum([len(i) for i in image_channel_list_arr[i]]) == (
                len(image_channel_list_arr[i][0]) * len(image_channel_list_arr[i])
            ):
                logger.warning(
                    "Channel images to be combined dont have the same number, trying to import from the smallest batch"
                )
                return
                # # TODO: fix this and implement
                # # find the smallest batch
                # m = float("inf")
                # smallest_channel_list = []
                # for ii in range(len(channel_names_arr[i])):
                #     if len(image_channel_list_arr[i][ii]) < m:
                #         smallest_index = ii
                #         m = len(image_channel_list_arr[i][i])
                # image_channel_list_arr[i] = copy.copy(image_channel_list_arr[i])
                # smallest_batch = image_channel_list_arr[i][smallest_index]
                # smallest_channel = channel_names_arr[i][smallest_index]
                # for l in range(len(image_channel_list_arr[i])):
                #     for ll in range(len(image_channel_list_arr[i][l])):
                #         indx = (
                #             image_channel_list_arr[i][l][ll]
                #             .lower()
                #             .index(channel_names_arr[i][l])
                #         )
                #         image_channel_list_filtered[l][ll] = (
                #             image_channel_list_arr[i][l][ll][:indx]
                #             + image_channel_list_arr[i][l][ll][
                #                 indx + len(channel_names_arr[i][l]) :
                #             ]
                #         )
                # for sb in smallest_batch:
                #     matching_items = [
                #         idx = image_channel_list_arr[i][i].index(sb.lower().replace(smallest_channel.lower()))
                #         for i in range(len(image_channel_list))
                #     ]
                #     image_channel_list_filtered.append()
            else:
                # read each channel of the image and combine them into one
                out_urls = []
                for ii in range(
                    len(image_channel_list_arr[i])
                ):  # for every image group in the treatment
                    import cv2

                    channel_images = []

                    for j in range(
                        len(image_channel_list_arr[i][ii])
                    ):  # for every channel / sub-image
                        # TODO: adjust for pyramidal????
                        img, result_dict = readImage(image_channel_list_arr[i][ii][j])
                        chn = result_dict.get("channels", None)
                        if len(chn) != 1 or len(img.shape) != 2:
                            config.global_signal.errorSignal(
                                "The images to be combined are not grayscale, please provide grayscale images"
                            )
                            logger.warning(
                                "Images provided are not grayscale, aborting"
                            )
                            return
                        if len(img.shape) == 3:
                            img = img.squeeze()
                            if len(img.shape) == 3:
                                config.global_signal.errorSignal(
                                    "The images to be combined are not grayscale, please provide grayscale images"
                                )
                        channel_images.append(img)  # raw image

                    # Prepare ImageJ style metadata with channel names
                    # channel_names_arr[i] = list(channel_names_arr[i][j])
                    metadata = {"cs_channels": channel_names_arr[i][ii], "axes": "YXC"}

                    combined_image = np.stack(channel_images, axis=-1)
                    # save the image as a tiff with the channels included
                    import tifffile

                    # generate a uuid that does not exist in config.cache_dir
                    import uuid
                    import os

                    file_name = os.path.basename(image_channel_list_arr[i][ii][0])
                    indx_channel = file_name.lower().index(
                        channel_names_arr[i][ii][0].lower()
                    )
                    # delete channel from the original filename
                    file_name = (
                        file_name[:indx_channel]
                        + file_name[indx_channel + len(channel_names_arr[i][ii]) :]
                    )
                    output_path = os.path.join(
                        str(config.cache_dir), file_name + ".tif"
                    )
                    iii = 0
                    while os.path.exists(output_path):
                        import random

                        if iii > 1000:
                            break
                        output_path = os.path.join(
                            config.cache_dir,
                            file_name + str(random.randint(0, 1000)) + ".tif",
                        )
                        iii += 1
                    # Save the combined image as a TIFF file with metadata
                    tifffile.imsave(output_path, combined_image, metadata=metadata)
                    out_urls.append(output_path)
                if treatmetns:
                    self.MainWindow.add_new_treatment_item(treatmetns[i])
                self.load_files_by_drag_and_drop(out_urls)

    def combine_image_channels_and_save_to_disk(
        self, image_channel_list, channel_names, multi_treatment=False, treatmetns=None
    ):
        # Reads the grayscale images, combines them and saves them to disk. If images are not grayscale raise error
        import copy

        image_channel_list_arr = []
        channel_names_arr = []
        if not multi_treatment:
            image_channel_list_arr.append(image_channel_list)
            channel_names_arr.append(channel_names)
        else:
            image_channel_list_arr = image_channel_list
            channel_names_arr = channel_names
        for i in range(len(image_channel_list_arr)):
            if not len(image_channel_list_arr[i]):
                return
            if not channel_names:
                return

            if not sum([len(i) for i in image_channel_list_arr[i]]) == (
                len(image_channel_list_arr[i][0]) * len(image_channel_list_arr[i])
            ):
                logger.warning(
                    "Channel images to be combined dont have the same number, trying to import from the smallest batch"
                )
                return
                # # TODO: fix this and implement
                # # find the smallest batch
                # m = float("inf")
                # smallest_channel_list = []
                # for ii in range(len(channel_names_arr[i])):
                #     if len(image_channel_list_arr[i][ii]) < m:
                #         smallest_index = ii
                #         m = len(image_channel_list_arr[i][i])
                # image_channel_list_arr[i] = copy.copy(image_channel_list_arr[i])
                # smallest_batch = image_channel_list_arr[i][smallest_index]
                # smallest_channel = channel_names_arr[i][smallest_index]
                # for l in range(len(image_channel_list_arr[i])):
                #     for ll in range(len(image_channel_list_arr[i][l])):
                #         indx = (
                #             image_channel_list_arr[i][l][ll]
                #             .lower()
                #             .index(channel_names_arr[i][l])
                #         )
                #         image_channel_list_filtered[l][ll] = (
                #             image_channel_list_arr[i][l][ll][:indx]
                #             + image_channel_list_arr[i][l][ll][
                #                 indx + len(channel_names_arr[i][l]) :
                #             ]
                #         )
                # for sb in smallest_batch:
                #     matching_items = [
                #         idx = image_channel_list_arr[i][i].index(sb.lower().replace(smallest_channel.lower()))
                #         for i in range(len(image_channel_list))
                #     ]
                #     image_channel_list_filtered.append()
            else:
                # read each channel of the image and combine them into one
                out_urls = []
                for ii in range(len(image_channel_list_arr[i][0])):
                    import cv2

                    channel_images = []
                    for j in range(len(image_channel_list_arr[i])):
                        # TODO: adjusts for pyramidal??
                        img, result_dict = readImage(image_channel_list_arr[i][j][ii])
                        chn = result_dict.get("channels", None)
                        if len(chn) != 1 or len(img.shape) != 2:
                            config.global_signals.errorSignal.emit(
                                "The images to be combined are not grayscale, please provide grayscale images"
                            )
                            logger.warning(
                                "Images provided are not grayscale, aborting"
                            )
                            return
                        if len(img.shape) == 3:
                            img = img.squeeze()
                            if len(img.shape) == 3:
                                config.global_signal.errorSignal(
                                    "The images to be combined are not grayscale, please provide grayscale images"
                                )
                        channel_images.append(img)  # raw image

                    combined_image = np.stack(channel_images, axis=-1)
                    # save the image as a tiff with the channels included
                    import tifffile

                    # Prepare ImageJ style metadata with channel names
                    channel_names_arr[i] = list(channel_names_arr[i])
                    metadata = {"cs_channels": channel_names_arr[i], "axes": "YXC"}

                    # generate a uuid that does not exist in config.cache_dir
                    import uuid
                    import os

                    file_name = os.path.basename(image_channel_list_arr[i][0][ii])
                    indx_channel = file_name.lower().index(
                        channel_names_arr[i][0].lower()
                    )
                    # delete channel from the original filename
                    file_name = (
                        file_name[:indx_channel]
                        + file_name[indx_channel + len(channel_names_arr[i][0]) :]
                    )
                    output_path = os.path.join(
                        str(config.cache_dir), file_name + ".tif"
                    )
                    iii = 0
                    while os.path.exists(output_path):
                        import random

                        if iii > 1000:
                            break
                        output_path = os.path.join(
                            config.cache_dir,
                            file_name + str(random.randint(0, 1000)) + ".tif",
                        )
                        iii += 1
                    # Save the combined image as a TIFF file with metadata
                    tifffile.imsave(output_path, combined_image, metadata=metadata)
                    out_urls.append(output_path)
                if treatmetns:
                    self.MainWindow.add_new_treatment_item(treatmetns[i])
                self.load_files_by_drag_and_drop(out_urls)

    def get_channel_patterns_from_images(self, img_file_list):
        """
        This method is used to find patterns in the names of image files that match the channel names defined in the configuration.
        It returns a boolean indicating if channels were found as images, a list of matched channel paths, and a set of filtered patterns with the same count.

        Parameters:
        img_file_list (list): A list of image file paths.

        Returns:
        tuple: A tuple containing:
            - FOUND_CHANNELS_AS_IMAGES (bool): A flag indicating if channels were found as images.
            - matched_channel_paths (list): A list of matched channel paths.
            - filtered_patterns_with_same_count (set): A set of filtered patterns with the same count.
        """
        from collections import defaultdict
        from natsort import natsorted
        from functools import partial
        import re
        import glob

        FOUND_CHANNELS_AS_IMAGES = False
        matched_channel_paths = list()
        filtered_patterns_with_same_count = set()

        channel_names = [i.lower() for i in config.channel_colors]
        pattern_matches = defaultdict(list)
        # Finding matches for each pattern
        for pattern in channel_names:
            pattern_matches[pattern] = {
                filename
                for filename in img_file_list
                if re.search(pattern, os.path.basename(filename).lower())
            }

        # Creating a reverse map where the key is the number of matches and value is a list of patterns
        count_to_patterns = defaultdict(set)
        for pattern, matches in pattern_matches.items():
            if not matches:
                continue
            count_to_patterns[len(matches)].add(pattern)

        # Finding patterns with the same count and printing them
        for count, patterns_with_same_count in count_to_patterns.items():
            if len(patterns_with_same_count) > 1:
                filtered_patterns_with_same_count = set(patterns_with_same_count)
                patterns_list = sorted(patterns_with_same_count, key=len, reverse=True)

                for i in range(len(patterns_list)):
                    for j in range(i + 1, len(patterns_list)):
                        if patterns_list[j] in patterns_list[i]:
                            filtered_patterns_with_same_count.discard(patterns_list[j])

                if (
                    len(filtered_patterns_with_same_count) > 1
                    and len(filtered_patterns_with_same_count) < 4
                ):
                    FOUND_CHANNELS_AS_IMAGES = True
                    matched_channel_paths = [
                        natsorted(pattern_matches[i])
                        for i in filtered_patterns_with_same_count
                        if len(pattern_matches[i]) > 0
                        and len(pattern_matches[i]) <= len(img_file_list)
                    ]
                    break
                # print(f"Patterns with {count} matches:")
                # for pattern in filtered_patterns_with_same_count:
            #     print(f"{pattern}: {', '.join(pattern_matches[pattern])}")
        return (
            FOUND_CHANNELS_AS_IMAGES,
            matched_channel_paths,
            filtered_patterns_with_same_count,
        )

    def load_files_by_drag_and_drop(
        self, urls=[], channel_pattern=True, treatment_pattern=True, auto_accept=False
    ):
        """
        Determines if the list of urls is:
        1) a list of files -> open files as 1 treatment
        2) a list of folders -> open each subfolder files on a treatment with the name of the folder
        3) a single folder |
                            | -> if subfolders are folders -> open as treatments
                            | -> if subfolders are files -> open as 1 treatment
        This function also looks for patterns within images:
            ex. [img_1_gfp.png , img_1_rfp.png ] -> will open as one image unless channel_pattern == True or
                                                    the user declines pattern matching.
        auto_accept -> Does not trigger a dialog for patterns etc... instead automatically
        accept any action
        """

        from functools import partial
        import glob

        # case of urls as dict --> already determined treatments names and paths
        if isinstance(urls, dict):
            for k, v in urls.items():
                self.MainWindow.add_new_treatment_item(k)
                QtWidgets.QApplication.processEvents()  # needed to prevent errors from uuids missmatch
                self.add_new_images_by_drag_and_drop(v)
            return

        ## TODO: Not supported yet
        # # if file is video, load as video
        # if len(urls) > 0 and isinstance(urls[0], str) and is_video_file(urls[0]):
        #     self.add_new_images_by_drag_and_drop(
        #         urls, check_for_videos=True
        #     )  # forces to check on SetUpButtons methods if its a video

        # if file is a video, open as one condition with frames
        if len(urls) > 0 and isinstance(urls[0], str) and urls[0].endswith(".wmv"):
            # TODO: patch this method correctly
            # self.MainWindow.add_new_treatment_item()
            # open with opencv
            import cv2

            import_url_dict = {}
            # convert all videos to treatments with images
            all_video_urls = [i for i in urls if i.endswith(".wmv")]
            for v_urls in all_video_urls:
                all_frame_paths = []
                cap = cv2.VideoCapture(v_urls)
                try:
                    if cap.isOpened() is False:
                        config.global_signals.errorSignal.emit(
                            "Error opening video stream or file"
                        )

                    # get the url basename
                    url_basename = os.path.basename(v_urls)
                    # Read until video is completed
                    frame_counter = 1
                    skip_frames = 10  # reduce framerate by 4
                    skip_i = 0
                    while cap.isOpened():
                        # if frame_counter == 10:
                        #     break
                        # Capture frame-by-frame
                        ret, frame = cap.read()
                        if skip_i < skip_frames:
                            skip_i += 1
                            continue
                        else:
                            skip_i = 0
                        if ret is False:
                            break

                        # store in the cache dir as filename_0000.png at config.cache_dir
                        frame_path = os.path.join(
                            config.cache_dir,
                            url_basename + "_" + str(frame_counter).zfill(8) + ".png",
                        )
                        all_frame_paths.append(frame_path)

                        # if ret is True and frame_counter < 30:
                        cv2.imwrite(frame_path, frame)
                        frame_counter += 1

                except Exception as e:
                    cap.release()
                    config.global_signals.errorSignal.emit(
                        "Error opening video stream or file"
                    )
                    return
                cap.release()
                import_url_dict[url_basename] = all_frame_paths

            return self.load_files_by_drag_and_drop(import_url_dict)

        #############################################
        ############# Urls of images ################
        #############################################

        # Case of urls as list --> need to determine action
        # check if urls are folders or images, if its a mixture of both folders and images, then just keep  the folders
        # and discard the images
        try:
            urls = [i for i in urls if i]
        except:
            pass
        if (
            (len(urls) > 0) and isinstance(urls[0], str) and os.path.isfile(urls[0])
        ):  # multiple urls which means we read the images
            # TODO: change in the future to support multiple folders
            path, myending = os.path.splitext(urls[0])
            if ".plab" in myending:
                self.MainWindow.plaba_load_process(
                    plab_object=None,
                    PreGivenUrl=os.path.normpath(urls[0])[1:],
                )
            elif myending.lower() in config.ALL_ACCEPTED_FORMATS:
                QtWidgets.QApplication.processEvents()
                # get images as a list
                img_file_list = urls
                img_file_list = [
                    i
                    for i in img_file_list
                    if i.lower().endswith(tuple(config.ALL_ACCEPTED_FORMATS))
                ]
                # check if there is a channel pattern on the image urls
                # get all possible channel names
                import re

                if treatment_pattern:
                    pats = find_treatment_patterns_within_filepaths(img_file_list)
                    if len(list(pats.keys())) > 1:
                        if auto_accept:
                            self.load_files_by_drag_and_drop(urls=pats)
                        else:
                            # prompt user to add multiple treatments
                            config.global_signals.actionDialogSignal.emit(
                                "Found patterns within the imported items,\nsplit them to treatments? \nTreatments found: "
                                + " - ".join([ii for ii in list(list(pats.keys()))]),
                                {
                                    "Yes": partial(
                                        self.load_files_by_drag_and_drop,
                                        urls=pats,
                                    ),
                                    "No": partial(
                                        self.load_files_by_drag_and_drop,
                                        urls=img_file_list,
                                        treatment_pattern=False,
                                    ),
                                },
                            )
                        return

                if channel_pattern:
                    (
                        FOUND_CHANNELS_AS_IMAGES,
                        matched_channel_paths,
                        filtered_patterns_with_same_count,
                    ) = self.get_channel_patterns_from_images(img_file_list)
                    if FOUND_CHANNELS_AS_IMAGES and len(matched_channel_paths) > 1:
                        if auto_accept:
                            self.combine_image_channels_and_save_to_disk(
                                image_channel_list=matched_channel_paths,
                                channel_names=filtered_patterns_with_same_count,
                            )
                        else:
                            # prompt the user if he wants to utilize the channel pattern
                            config.global_signals.actionDialogSignal.emit(
                                "Found channel pattern in the image names,\nwould you like to merge them? \nChannels found: "
                                + " - ".join(
                                    [
                                        ii.upper()
                                        for ii in list(
                                            filtered_patterns_with_same_count
                                        )
                                    ]
                                ),
                                {
                                    "Yes, combine them": partial(
                                        self.combine_image_channels_and_save_to_disk,
                                        image_channel_list=matched_channel_paths,
                                        channel_names=filtered_patterns_with_same_count,
                                    ),
                                    "No": partial(
                                        self.load_files_by_drag_and_drop,
                                        urls=img_file_list,
                                        channel_pattern=False,
                                    ),
                                },
                            )
                        return
                print("now droping")
                self.add_new_images_by_drag_and_drop(img_file_list)
        else:
            # Case were we import folders are treatments
            # get dir base name

            # get the basename
            # get all files in dir
            all_folders = [i for i in urls if isinstance(i, list) or os.path.isdir(i)]
            all_files = [i for i in urls if isinstance(i, str) and os.path.isfile(i)]

            #############################################
            ####### Urls of Dirs (as treatments) ########
            #############################################
            # if len(all_folders) > len(all_files):
            #     # import every sub - folder as a new condition
            if len(all_folders) == 1 and len(all_files) == 0:
                # case of 1 folder, list everything in it and recurse
                if not isinstance(all_folders[0], list):
                    all_urls = glob.glob(os.path.join(all_folders[0], "*"))
                else:
                    all_urls = all_folders[0]
                all_urls.sort()
                self.load_files_by_drag_and_drop(all_urls)
                return
            folders_patterns = []
            all_folders_images = []
            treatments = []
            multiple_treatment_dict = {}

            counter = 1
            for folder in all_folders:
                if isinstance(folder, list):
                    cond_name = os.path.basename(os.path.dirname(folder[0]))
                else:
                    cond_name = os.path.basename(os.path.dirname(folder))
                treatments.append(cond_name)
                # get all images under that folder:
                if isinstance(folder, list):
                    all_files = folder
                else:
                    all_files = glob.glob(folder + "/*.*")
                all_files = [
                    i
                    for i in all_files
                    if i.lower().endswith(tuple(config.ALL_ACCEPTED_FORMATS))
                ]
                all_folders_images.append(all_files)
                if isinstance(folder, list):
                    base_name = os.path.basename(os.path.dirname(folder[0]))
                else:
                    base_name = os.path.basename(os.path.dirname(folder))
                # Ensure unique key by appending number if needed
                unique_name = base_name
                if unique_name == "":
                    # name it something random
                    unique_name = f"untitled_{counter}"
                while unique_name in multiple_treatment_dict:
                    unique_name = f"{base_name}_{counter}"
                    counter += 1

                multiple_treatment_dict[unique_name] = all_files
                current_folder_pattern = self.get_channel_patterns_from_images(
                    all_files
                )
                folders_patterns.append(current_folder_pattern)

            # case of 1 folder  = 1 image, where 1 folder contains multiple channels as 1
            # image per channel. This is true if all folder have the same amount of images
            # and every image within the folder is a single channel image.
            # this can be triggered here if the channel is on the name of the image
            # or after the images are imported if the channel is on the image metadata (TODO:Implement this)

            #### SPECIAL CASE ####
            # - Multiple folder, with only 1 image each --> open as images for one treatment
            if set([len(i) for i in all_folders_images]) == {1}:
                # flatten all_folders_images
                import itertools

                all_images = list(itertools.chain(*all_folders_images))
                if auto_accept:
                    self.add_new_images_by_drag_and_drop(all_images)
                else:

                    config.global_signals.actionDialogSignal.emit(
                        "Found multiple folders with only 1 image each, would you like to merge them to one treatment?\nImport as : ",
                        {
                            "One treatment": partial(
                                self.add_new_images_by_drag_and_drop,
                                all_images,
                            ),
                            "Multiple treatments": partial(
                                self.load_files_by_drag_and_drop,
                                urls=multiple_treatment_dict,
                            ),
                        },
                    )
                return

            # check if every folder is an image with every channel as a single image within the folder
            if (
                len(list(set([len(i[1]) for i in folders_patterns]))) == 1
                and [len(list(set(i[2]))) for i in folders_patterns]
                == [len(list(i[2])) for i in folders_patterns]
                and channel_pattern
                and [len(list(set(i[2]))) for i in folders_patterns][0]
                > 1  # at least 2 channels
                and all([i[0] for i in folders_patterns])
            ):
                # case of 1 folder  = 1 image, where 1 folder contains multiple channels as 1
                all_images = [[x[0] for x in i[1]] for i in folders_patterns]
                channels = [list(i[2]) for i in folders_patterns]
                # convert empty channels to gray
                channels = [["gray"] if not i else i for i in channels]
                # get the parent folder and use it as the treatment name
                cond_name = os.path.basename(os.path.dirname(urls[0]))
                if auto_accept:
                    try:
                        self.combine_image_channels_and_save_to_disk_as_one_folder(
                            image_channel_list=all_images,
                            channel_names=channels,
                            treatmetns=[cond_name],
                        )
                    except Exception as e:
                        config.global_signals.errorSignal.emit(
                            f"Failed to combine images: {e}"
                        )
                        logger.warning(f"Failed to combine images: {e}")
                        return
                else:
                    config.global_signals.actionDialogSignal.emit(
                        "Found channel pattern in the image names,\nwould you like to merge them? \nChannels found: "
                        + " - ".join([ii.upper() for ii in list(channels[0])]),
                        {
                            "Yes, combine them": partial(
                                self.combine_image_channels_and_save_to_disk_as_one_folder,
                                image_channel_list=all_images,
                                channel_names=channels,
                                treatmetns=[cond_name],
                            ),
                            "No": partial(
                                self.load_files_by_drag_and_drop,
                                urls=all_images,
                                channel_pattern=False,
                            ),
                        },
                    )
                return
            # if channel_pattern
            # case wher for each folder there is a channel pattern amongst all images
            if (
                channel_pattern
                and folders_patterns
                and all([p[0] for p in folders_patterns])
            ):
                if auto_accept:
                    self.combine_image_channels_and_save_to_disk(
                        image_channel_list=[c[1] for c in folders_patterns],
                        channel_names=[c[2] for c in folders_patterns],
                        multi_treatment=True,
                        treatmetns=treatments,
                    )
                else:
                    # for each folder add with pattern
                    config.global_signals.actionDialogSignal.emit(
                        "Found channel pattern in the image names,\nwould you like to merge them? \nChannels found: "
                        + " - ".join(
                            [ii.upper() for ii in list(folders_patterns[0][2])]
                        ),
                        {
                            "Yes, combine them": partial(
                                self.combine_image_channels_and_save_to_disk,
                                image_channel_list=[c[1] for c in folders_patterns],
                                channel_names=[c[2] for c in folders_patterns],
                                multi_treatment=True,
                                treatmetns=treatments,
                            ),
                            "No": partial(
                                self.load_files_by_drag_and_drop,
                                urls=all_folders,
                                force=True,
                            ),
                        },
                    )
                return
            else:
                # normal import of treatment / dirs
                for folder in all_folders:
                    if isinstance(folder, list):
                        cond_name = os.path.basename(folder[0])
                    else:
                        cond_name = os.path.basename(os.path.dirname(folder))
                    cond_name = self.MainWindow.add_new_treatment_item(cond_name)
                    # get all images under that folder:
                    if isinstance(folder, list):
                        all_files = folder
                    else:
                        all_files = glob.glob(folder + "/*.*")
                    all_files = [
                        i
                        for i in all_files
                        if i.lower().endswith(tuple(config.ALL_ACCEPTED_FORMATS))
                    ]

                    self.add_new_images_by_drag_and_drop(all_files)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # must accept the dragEnterEvent or else the dropEvent can't occur !!!
            event.acceptProposedAction()
        else:
            event.ignore()

        return super(PhotoViewer, self).dragEnterEvent(event)

    def hasPhoto(self):
        return not self._empty

    def fitImageInView(self):  # , scale=True):D

        image_object = self.MainWindow.DH.BLobj.get_current_image_object()
        if not image_object:
            return

        self._zoom = 0
        if not self.rect().isNull():
            if self.hasPhoto():
                if not image_object.SizeX or not image_object.SizeY:
                    logger.warning(f"Could not fit image in view, image size is null")
                    return
                x_padding = image_object.SizeX * 0.25
                y_padding = image_object.SizeY * 0.25
                self.scene().setSceneRect(
                    -image_object.SizeX - x_padding,
                    -image_object.SizeX - y_padding,
                    (3 * image_object.SizeX) + (2 * x_padding),
                    (3 * image_object.SizeY) + (2 * y_padding),
                )
                self.setTransformationAnchor(
                    QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
                )
                self.fitInView(
                    0,
                    0,
                    image_object.SizeX,
                    image_object.SizeY,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                )
            self._zoom = 0

    def getPainterPathCircle(self, radius, pos):
        """
        It creates a circle with a radius of <code>radius</code> and a center at <code>pos</code>.

        Args:
          radius: The radius of the circle.
          pos: The position of the circle

        Returns:
          A QPainterPath object.
        """
        self.groupPath = QtGui.QPainterPath()
        self.groupPath.moveTo(pos.x(), pos.y())
        self.groupPath.arcTo(
            pos.x() - (radius / 2), pos.y() - (radius / 2), radius, radius, 0.0, 360.0
        )
        self.groupPath.closeSubpath()
        return self.groupPath

    def setPhoto_and_mask(self, pixmap=None):
        self._zoom = 0
        self.Cpixmap = pixmap
        self._empty = False
        self._photo.setPixmap(pixmap)

    def setPhoto(self, pixmap=None, fit_in_view_state=True, rescaled_width=None):
        self._zoom = 0
        if pixmap and not pixmap == 0:
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            if (
                self._photo.sceneBoundingRect()
                and rescaled_width
                and int(rescaled_width) != int(self._photo.sceneBoundingRect().width())
            ):
                # If the photo is scaled:
                scale = rescaled_width / self._photo.sceneBoundingRect().width()
                self._photo.setScale(scale)
            elif rescaled_width and (pixmap.width() != rescaled_width):
                scale = rescaled_width / pixmap.width()
                self._photo.setScale(scale)
            else:
                self._photo.setScale(1)
            self._photo.setPixmap(pixmap)
        else:
            return
        if fit_in_view_state == True:
            pass
        else:
            pass
        if self._photo.sceneBoundingRect():
            center_x = self._photo.sceneBoundingRect().width() // 2
            center_y = self._photo.sceneBoundingRect().height() // 2
        else:
            center_x = pixmap.width() // 2
            center_y = pixmap.height() // 2
        self.centerOn(
            0 + int(center_x),
            0 + int(center_y),
        )

    def check_and_remove_deepzoom_tiles_that_dont_belong(self):
        """
        Iterate of the deep zoom tiles, if any tile is not for the current image
        remove it from the scene
        """
        current_image_object = self.MainWindow.DH.BLobj.get_current_image_object()
        if not current_image_object:
            return
        current_image_file_name = current_image_object.fileName

        tiles_to_be_removed = []
        for tile in config._deepzoom_pixmaps:
            # tile[4] is the image name
            if not tile[4] != current_image_file_name:
                try:
                    tiles_to_be_removed.append(tile)
                    self._scene.removeItem(tile[0])
                except Exception as e:
                    logger.warning(f"Error removing tile {e}")

        for tile in tiles_to_be_removed:
            config._deepzoom_pixmaps.remove(tile)

    @config.threaded
    def check_and_update_high_res_slides(self, force_update=False):
        # If the current image is ulra high res, update the tiles
        # visible within the viewport
        # if there is an image
        if self.MainWindow.current_imagenumber == None:
            return
        current_condition = self.MainWindow.DH.BLobj.get_current_condition()
        if not current_condition:
            return
        image_object = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[self.MainWindow.current_imagenumber]
        )
        if not image_object:
            return
        if image_object._is_ultra_high_res:  # and not image_object._during_scene_update
            # update config viewport bbox in config and map to scene
            bbox_rect = self.mapToScene(self.viewport().rect()).boundingRect()
            config.viewport_bounding_box = [
                bbox_rect.x(),
                bbox_rect.y(),
                bbox_rect.width(),
                bbox_rect.height(),
            ]
            scene_rect = self.mapToScene(self.viewport().rect()).boundingRect()
            center = scene_rect.center()
            zoom_level = self.transform().m11()
            if config.HIGH_RES_SCENE_LAST_UPDATED_POS and not force_update:
                # check if we are zoomed in (meaning the viewport) below threashold (average width + height  < ULTRA_HIGH_RES_THRESHOLD)
                if (
                    (
                        config.HIGH_RES_SCENE_LAST_UPDATED_POS.x()
                        * config.HIGH_RES_SCENE_POSITION_THRESHOLD
                    )
                    > abs(center.x() - config.HIGH_RES_SCENE_LAST_UPDATED_POS.x())
                    or (
                        config.HIGH_RES_SCENE_LAST_UPDATED_POS.x()
                        * config.HIGH_RES_SCENE_POSITION_THRESHOLD
                    )
                    > abs(center.y() - config.HIGH_RES_SCENE_LAST_UPDATED_POS.y())
                    or (zoom_level * config.HIGH_RES_SCENE_ZOOM_THRESHOLD)
                    > abs(config.HIGH_RES_SCENE_LAST_UPDATED_ZOOM_LEVEL - zoom_level)
                ):
                    return

            config.HIGH_RES_SCENE_LAST_UPDATED_POS = center
            config.HIGH_RES_SCENE_LAST_UPDATED_ZOOM_LEVEL = zoom_level
            # update the scene to ultra high res
            config.global_signals.update_scene_ultra_high_res_plane_signal.emit(
                {
                    "image_uuid": self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                    .unique_id,
                    # get the viewport centerpoint position in the scene
                    "image_position": center,
                    # get the size of the desired tile, it should be the visible scene size in the viewport + 1.3x
                    "image_size": [
                        scene_rect  # The above code is a Python program that is currently empty. It
                        # contains a single comment line denoted by the '#' symbol.
                        .width() * 0.99,
                        scene_rect.height() * 0.99,
                    ],
                }
            )

    def zoom_in(self, zoom_factor=None):
        if zoom_factor == None:
            zoom_factor = 1.2
        mod = 5
        self.scale(1 + (zoom_factor / mod), 1 + (zoom_factor / mod))
        config.global_signals.check_and_update_high_res_slides_signal.emit()

    def zoom_out(self, zoom_factor=None):
        if zoom_factor == None:
            zoom_factor = 1.2
        mod = 5
        self.scale(1 - (zoom_factor / mod), 1 - (zoom_factor / mod))
        # Adjust center of zoom
        # Get current transformation matrix
        matrix = self.transform()
        # Shift the origin point to the left
        matrix.translate(-400, 0)  # -50 is just an example, adjust as needed
        # Apply the new transformation matrix
        self.setTransform(matrix)
        config.global_signals.check_and_update_high_res_slides_signal.emit()

    def wheelEvent(self, event):
        main_pixmap_scale = self._photo.scale()
        scroll_step = int(
            self.base_step * (1 / self.transform().m11()) * main_pixmap_scale
        )

        # if control modifier is pressed, zoom in/out
        if event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
                event.accept()
                return
            else:
                self.zoom_out()
                event.accept()
                return

        else:
            self.translate(
                event.pixelDelta().x() * scroll_step,
                event.pixelDelta().y() * scroll_step,
            )
            return super(PhotoViewer, self).wheelEvent(event)

    def scaleBarPlaceFirstPoint(self, pos):
        if not self.scaleBarDraw_duringDraw_STATE:
            self.scaleBar_FirstPoint = [pos.x(), pos.y()]
            self.scaleBarDraw_duringDraw_STATE = True
        else:
            self.scaleBarComplete(pos)

    def scaleBarWhile(self, pos):
        if self.scaleBarWhileLine:
            self._scene.removeItem(self.scaleBarWhileLine)
        self.scaleBarWhileLine = QtWidgets.QGraphicsLineItem(
            self.scaleBar_FirstPoint[0], self.scaleBar_FirstPoint[1], pos.x(), pos.y()
        )
        pen_width = 3
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
        pen.setWidth(pen_width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)
        self.scaleBarWhileLine.setPen(pen)
        self._scene.addItem(self.scaleBarWhileLine)

    def scaleBarComplete(self, pos):
        self.scaleBarFinalDistance = self.getDistanceValue(
            self.scaleBar_FirstPoint[0], self.scaleBar_FirstPoint[1], pos.x(), pos.y()
        )
        print("--------here scale bar")
        print(self.scaleBarFinalDistance)
        print(
            self.scaleBar_FirstPoint[0], self.scaleBar_FirstPoint[1], pos.x(), pos.y()
        )
        if self.scaleBarWhileLine:
            self._scene.removeItem(self.scaleBarWhileLine)
        self.MainWindow.myScaleDialogClass.myDialog.raise_()
        self.MainWindow.myScaleDialogClass.doubleSpinBox.setValue(
            self.scaleBarFinalDistance
        )

        # scale bar tool
        self.scaleBarDraw_STATE = False
        self.scaleBarDraw_duringDraw_STATE = False
        self.scaleBar_FirstPoint = []
        self.scaleBarWhileLine = None
        self.scaleBarFinalDistance = None

    def getMagicBrushGradientMultiplier(self, image):
        """ """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return np.ones(gray.shape, dtype=np.uint8)

    def getSharpFallOff(self, value, radius, dt):
        return (-((value / radius)) + 1) * dt

    def movePointsBrushToolMagic1(self, dtx, dty, pointsList):
        """
        computes a new point based on edge maps
        compute edge map, move points based on map
        """

        pointsList = self.getPointsOnlyFromItemList(pointsList)
        for point in pointsList:
            point.setX(point.x() - (dtx - (dtx / 255)))
            point.setY(point.y() - (dty - (dty / 255)))
        return

    def getPointsOnlyFromItemList(self, ItemList):
        for myItem in ItemList:
            if type(myItem) != GripItem:
                ItemList.remove(myItem)
        return ItemList

    def disable_aa_tool(self):
        """
        This function hides the Auto cut / grab cut tool
        """
        if self.aa_review_state == True:
            self.Ui_control(lock_wdigets=False)
        self.aa_review_state = False
        self.i_am_drawing_state_bbox = False
        self.during_drawing_bbox = False
        return

    def auto_annotate_tool_while_draw(self, pos):
        """
        Starts the magic roi process, by adding the graphics elements to the scene

        Function runs in between the auto_annotate_tool_start and stop and its drawing and
        deleting a box from the first click to ther current for every iteration
        """
        if self.i_am_drawing_state_bbox == False:
            return
        if self.during_drawing_bbox == True:
            try:
                self._scene.removeItem(self.bbox_drawing)
            except Exception as e:
                print(e)
                pass

        pen_width = 2
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
        pen.setWidth(pen_width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)

        startXrect = min(self.aa_tool_bb_first_x, pos.x())
        startYrect = min(self.aa_tool_bb_first_y, pos.y())
        endXrect = max(self.aa_tool_bb_first_x, pos.x())
        endYrect = max(self.aa_tool_bb_first_y, pos.y())
        widthRectAA = endXrect - startXrect
        heightRectAA = endYrect - startYrect
        scale_x = self.transform().m11()  #  get the view scale
        w = 14 / (
            scale_x * 2
        )  # from the view scale, adjus the size of the points width to always be constant
        self.bbox_drawing = bbox_drawing_cls(
            w, startXrect, startYrect, widthRectAA, heightRectAA
        )

        self._scene.addItem(self.bbox_drawing)

        self.during_drawing_bbox = True
        self.last_bbox_x = pos.x()
        self.last_bbox_y = pos.y()

    def draw_bounding_box_stop_THREADED(self, pos):
        # Set up multiprocess
        from celer_sight_ai.core.Workers import Worker
        from celer_sight_ai import config

        # if no class exists, throw error and abort
        current_class_widget = (
            self.MainWindow.custom_class_list_widget.currentItemWidget()
        )
        if not current_class_widget:
            config.global_signals.errorSignal.emit(
                "No category added, please add a category to continue"
            )
            return
        class_id = (
            self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id
        )
        self.draw_bounding_box_stop(
            None,
            self.MainWindow.DH.BLobj.get_current_group(),  # this is the group name, it needs to change to group id
            self.MainWindow.DH.BLobj.get_current_condition_uuid(),
            self.MainWindow.DH.BLobj.get_current_image_uuid(),
            class_id,
        )
        return

    @config.q_threaded
    def threadedBoundingBoxStopWorkerResultFunction(self):
        if hasattr(self, "bbox_drawing"):
            if self.bbox_drawing:
                if self.bbox_drawing in self._scene.items():
                    self._scene.removeItemSafely(self.bbox_drawing)

    def filter_contours_for_one_ROI(self, contours, hierarchies):
        """
        The function filters contours to find the contour with the maximum area and returns it along with
        any holes that are contained within it.

        Args:
        contours: A list of masks, where each mask is represented as a numpy array of shape (N, 1,
        2), where N is the number of points in the contour.
        hierarchies: The `hierarchies` parameter is a list of hierarchies for each contour in the
        `contours` list. Each hierarchy is represented as a list of four values: [next, previous, first
        child, parent]. These values represent the relationships between contours.

        Returns:
        two values: the contour with the maximum area (contours[max_area_index]) and a list of contours
        (holes) whose parent contour is the contour with the maximum area.
        """
        # find the index of the contour with the maximum area
        # make sure all masks are 2D
        contours = [cnt.squeeze() for cnt in contours]
        max_area_index = np.argmax([cv2.contourArea(cnt) for cnt in contours])

        # filter out only the contours (holes) whose parent is the max_area_index contour
        holes = [
            contours[i]
            for i, hierarchy in enumerate(hierarchies[0])
            if hierarchy[3] == max_area_index
        ]
        out = []
        out.append(contours[max_area_index])
        out.extend(holes)
        return out

    def is_magic_mask_generator_mode(self):
        """
        Checks the MainWindow.ai_model_combobox mode
        to check the available models check on config.MagicToolModes
        """
        from celer_sight_ai.config import MagicToolModes

        suggestion_modes = [
            MagicToolModes.MAGIC_BOX_WITH_PREDICT.name,
            MagicToolModes.MAGIC_POINT_ROI_WITH_PREDICT.name,
        ]
        if self.MainWindow.ai_model_combobox.get_mode().name in suggestion_modes:
            return True
        return False

    @config.threaded
    def draw_bounding_box_stop(
        self,
        bbox,  # -> [x1, y1, x2, y2]
        current_group,
        current_condition,  # TODO: change to uuid in the future
        current_image_uuid,
        class_id,
        progress_callback=False,
    ):
        """
        runs the first time we release the mouse after the aa_draw
        """
        import numpy as np
        from celer_sight_ai import config

        logger.debug("draw_bounding_box_stop")

        # get current image
        while config.load_main_scene_read_image == True:
            import time

            time.sleep(0.001)
        current_condition_name = current_condition
        treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()

        image_uuid = current_image_uuid

        # check bounds
        # place bnounds in correct position
        if isinstance(bbox, type(None)):
            x1 = min(self.aa_tool_bb_first_x, self.last_bbox_x)
            x2 = max(self.aa_tool_bb_first_x, self.last_bbox_x)
            y1 = min(self.aa_tool_bb_first_y, self.last_bbox_y)
            y2 = max(self.aa_tool_bb_first_y, self.last_bbox_y)
        else:
            x1, y1, x2, y2 = bbox
        # Make the click tool same size/raidus:
        from celer_sight_ai.io.image_reader import (
            get_optimal_crop_bbox,
            generate_complete_spiral_tiles,
        )

        # get image object
        image_object = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[current_image_uuid]
        )
        if not image_object.SizeX or not image_object.SizeY:
            logger.warning("Image size not found, skipping")
            return
        bbox_tile = get_optimal_crop_bbox(
            image_object.SizeX,
            image_object.SizeY,
            [round(x1), round(y1), round(x2), round(y2)],
            class_id,
        )  # bbox is [x1, y1, x2, y2]
        bbox_tile = list(bbox_tile)

        # if the bounding box is out of bounds, adjust it to be within bounds
        if image_object.SizeX - bbox_tile[3] < 0:
            difference = bbox_tile[3] - image_object.SizeY
            bbox_tile[3] = int(bbox_tile[3] - difference)
            # adjust top
            bbox_tile[1] = int(max(0, bbox_tile[1] - difference))
        if image_object.SizeY - bbox_tile[2] < 0:
            difference = bbox_tile[2] - image_object.SizeX
            bbox_tile[2] = int(bbox_tile[2] - difference)
            # adjust left
            bbox_tile[0] = int(max(0, bbox_tile[0] - difference))

        # make sure that the bbox is square (use the largest dimension)
        bbox_tile[2] = bbox_tile[3] = max(bbox_tile[2], bbox_tile[3])

        # get image object for this bbox_tile
        seg_image_prior = image_object.getImage(
            to_uint8=True,
            to_rgb=True,
            fast_load_ram=True,  # load image quickly from config.ram_image, used in brightness adjustment
            for_interactive_zoom=True,  # When loading a viewport array, use tricks to load it faster
            for_thumbnail=False,
            bbox=bbox_tile,  # [bbox_tile[0], bbox_tile[1], bbox_tile[2] - bbox_tile[0], bbox_tile[3] - bbox_tile[1]], # bbox : [x,y,w,h]
            avoid_loading_ultra_high_res_arrays_normaly=True,
        )
        # if the bounding box is less than config.MAGIC_BOX_2_IDEAL_SIZE then we need to infer using tiles
        self.mgcClickWidth = max(x2 - x1, y2 - y1)

        if (y2 - y1) * (x2 - x1) < 30:
            self.threadedBoundingBoxStopWorkerResultFunction()
            return None
        logger.debug("before get mask")

        mask_uuid = str(config.get_unique_id())
        while (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[self.MainWindow.current_imagenumber]
            .get_by_uuid(mask_uuid)
            != None
        ):
            mask_uuid = str(config.get_unique_id())
        celer_sight_object = {
            "image_uuid": image_uuid,
            "condition_uuid": treatment_uuid,
            "group_uuid": current_group,  # should change to uuid when its supported
            "class_uuid": self.MainWindow.DH.BLobj.get_current_class_uuid(),
            "mask_uuid": mask_uuid,
            "SizeX": image_object.SizeX,
            "SizeY": image_object.SizeY,
        }
        bbox_object = [x1, y1, x2, y2]
        effective_resize_tile = [
            max(0, bbox_tile[0]),
            max(0, bbox_tile[1]),
            bbox_tile[2],  # min(image_object.SizeX, bbox_tile[2]),
            bbox_tile[3],  # min(image_object.SizeY, bbox_tile[3]),
        ]
        bbox_object_in_seg_image_prior = [
            (bbox_object[0] - effective_resize_tile[0]),
            (bbox_object[1] - effective_resize_tile[1]),
            (bbox_object[2] - effective_resize_tile[0]),
            (bbox_object[3] - effective_resize_tile[1]),
        ]
        try:
            (
                finalmask,
                offset_x,
                offset_y,
            ) = self.MainWindow.sdknn_tool.get_bounding_box_mask(
                seg_image_prior,
                celer_sight_object,
                bounding_box=bbox_object_in_seg_image_prior,  # [bbox_object[0] , bbox_object[1] , bbox_object[2]-bbox_object[0]  , bbox_object[3] - bbox_object[1] ],#bbox_object , #[round(x1), round(y1), round(x2) + x1, round(y2) + y1], # bbox_object,
                tile_bbox=bbox_tile,  # x , y , w , h
            )
        except Exception as e:
            logger.error(e)
            self.i_am_drawing_state_bbox = False
            self.during_drawing_bbox = False
            self.threadedBoundingBoxStopWorkerResultFunction()
            return

        if not isinstance(finalmask, (np.ndarray, np.generic)):
            return None

        logger.debug("before is isntace")
        if len(finalmask.shape) == 3:
            if finalmask.shape[2] >= 1:
                finalmask = finalmask[:, :, 0]

        bbox = [x1, y1, x2 - x1, y2 - y1]  # [x,y,w,h]

        self.aa_review_state = False
        from celer_sight_ai.core.magic_box_tools import mask_to_polygon

        resize_factor_x = seg_image_prior.shape[1] / effective_resize_tile[2]
        resize_factor_y = seg_image_prior.shape[0] / effective_resize_tile[3]
        print()

        # effective_resize_tile [290, 282.5, 1328, 1048]
        #
        # image_object.SizeX 1328
        # image_object.SizeY 1048

        try:
            all_arrays = mask_to_polygon(
                finalmask,
                image_shape=seg_image_prior.shape,
                offset_x=offset_x,
                offset_y=offset_y,
                resize_factor_x=resize_factor_x,
                resize_factor_y=resize_factor_y,
            )
        except Exception as e:
            logger.error(e)
            config.global_signals.notify_user_signal.emit("Error generating Roi")
            self.i_am_drawing_state_bbox = False
            self.during_drawing_bbox = False
            return

        self.i_am_drawing_state_bbox = False
        self.during_drawing_bbox = False
        if len(all_arrays) == 0:
            return

        config.global_signals.create_annotation_object_signal.emit(
            {
                "treatment_uuid": treatment_uuid,  # TODO: Change to uuid in the future
                "group_uuid": current_group,
                "array": all_arrays,
                "image_uuid": current_image_uuid,
                "class_id": class_id,
                "mask_type": "polygon",
            }
        )

        ##### calculate the typical mask width in pixels for that class ####
        from celer_sight_ai.inference_handler import calculate_polygon_width

        annotation_width = calculate_polygon_width(
            all_arrays[0].astype(np.uint32)
        )  # in diameter
        config.CLASS_REGISTRY_WIDTH[class_id] = annotation_width

        # recalculate the tile box for the suggestor if used
        bbox_tile = get_optimal_crop_bbox(
            image_object.SizeX,
            image_object.SizeY,
            [round(x1), round(y1), round(x2), round(y2)],
            class_id,
        )
        bbox_tile = list(bbox_tile)

        # if the bounding box is out of bounds, adjust it to be within bounds
        if image_object.SizeX - bbox_tile[3] < 0:
            difference = bbox_tile[3] - image_object.SizeY
            bbox_tile[3] = int(bbox_tile[3] - difference)
            # adjust top
            bbox_tile[1] = int(max(0, bbox_tile[1] - difference))

        if self.is_magic_mask_generator_mode():
            self.MainWindow.sdknn_tool.start_suggested_mask_generator(
                image_object,
                celer_sight_object,
                bbox_tile,  # [x,y,w,h]
                bbox,  # [x,y,w,h]
            )
        print("sending signal for auto bounding box")
        self.threadedBoundingBoxStopWorkerResultFunction()
        return

    def Ui_control(self, lock_wdigets=True):
        """
        control mechanism to block and enable widgets
        """

        for widget in self.MainWindow.children():
            if lock_wdigets == True:
                if widget != self:
                    try:
                        widget.setEnabled(False)
                    except:
                        pass
            elif lock_wdigets == False:
                if widget != self:
                    try:
                        widget.setEnabled(True)
                    except:
                        pass
        return

    def updateMaskCountLabel(self):
        if self.LabelMasksNumber:
            try:
                io = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.DH.BLobj.get_current_image_number()]
                )
                mask_len = len([i for i in io.masks if not i.mask_type == "bitmap"])
                if io._is_ultra_high_res:
                    # make sure viewer only updates whats needed
                    self.setViewportUpdateMode(
                        QtWidgets.QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate
                    )
                    io.set_disable_overlay_annotation_items(True)
                    io.set_fast_cache_mode(True)
                elif mask_len <= config.extra_mask_items_threshold:
                    # if the image is ultra high res, always disable extra graphic items (because they look bad on zoom out and slow down the app)
                    # update all mask graphic items to be disabled
                    io.set_disable_overlay_annotation_items(False)
                    self.setViewportUpdateMode(
                        QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate
                    )
                else:
                    self.setViewportUpdateMode(
                        QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate
                    )
                    io.set_disable_overlay_annotation_items(True)
                    # if its 3 times that amount, set strict cache
                    if mask_len > config.extra_mask_items_threshold * 3:
                        io.set_fast_cache_mode(True)
                self.LabelMasksNumber.setText("masks : " + str(mask_len))
            except Exception as e:  # when the condition is empty, it causes an error.
                logger.error(e)
                pass

    def update_annotations_color_emitter(self):
        config.global_signals.update_annotations_color_signal.emit()

    def auto_annotate_tool_start(self, pos):
        """
        On the first click when the mouse is clicked with the auto cut tool tgus ryns to set up variables for the auto_annotate_tool_while_draw function to work
        """
        pen_width = 3
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            return

        print("AUTO TOOL STARTED")
        self.i_am_drawing_state_bbox = True
        self.during_drawing_bbox = False
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
        pen.setWidth(pen_width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        side = 20
        self.aa_tool_bb_first_x = pos.x()
        self.aa_tool_bb_first_y = pos.y()
        self.prevx = pos.x()
        self.prevy = pos.y()

    def setCursorAsCircle(self, radious=70, hollow=False):
        """ """
        circle = self.CreateAAcircle(radious, 0, 255, 0)
        height, width, channel = circle.shape
        bytesPerLine = 3 * width
        mypixmap = QtGui.QPixmap.fromImage(
            QtGui.QImage(
                circle.data,
                circle.shape[1],
                circle.shape[0],
                circle.strides[0],
                QtGui.QImage.Format_ARGB32_Premultiplied,
            )
        )
        print("seting cursor reound")
        self.viewport().setCursor(QtGui.QCursor(mypixmap))
        return

    def update_tool(self, PreGivenOption=None):
        tool = self.ui_tool_selection.selected_button
        """
        function that updates the Ui when we select item
        TODO: update this
        """

        logger.debug(f"update tool called for {PreGivenOption}")
        if PreGivenOption == tool:
            print("prev tools is same")
            return
        if not self.hasPhoto():
            tool = "selection"
            PreGivenOption = "selection"
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        if PreGivenOption != None:
            print("prev given option is not none")
            tool = PreGivenOption
        self.makeAllGraphicItemsSelectable()
        self.MainWindow.clearViewerOnRefresh(with_masks=False)
        allTools = [
            self.add_mask_btn_state,
            self.aa_tool_draw,
            self.brushMask_STATE,
            self.rubberBandActive,
            self.SkGb_STATE,
            self.CELL_SPLIT_TOOL_STATE,
            self.CELL_SPLIT_DRAWING,
            self.SkGb_during_drawing,
            self.mgcClick_STATE,
            self.MAGIC_BRUSH_STATE,
            self.MAGIC_BRUSH_DURING_DRAWING,
            self.mgcBrushT_i_am_drawing_state,
            self.ML_brush_tool_draw_during_draw,
            self.ML_brush_tool_draw_mode_review,
            self.ML_brush_tool_object_state,
            self.ML_brush_tool_draw_is_active,
            self.rm_Masks_STATE,
            self.rm_Masks_tool_draw,
        ]
        # for tools in allTools:
        #     tools = False

        # self.brushMaskTmpGraphicsItems = [] #temprary items to delete on release for speed
        self.brushMask_STATE = False
        self.add_mask_btn_state = False
        self.aa_tool_draw = False
        self.rubberBandActive = False
        self.SkGb_STATE = False
        # self.CELL_SPLIT_TOOL_STATE = False
        # self.CELL_SPLIT_DRAWING = False
        # self.CELL_SPLIT_SPOTS = []
        # self.CELL_RM_FIRST_SPOT_PLACED = False
        self.mgcClick_STATE = False
        self.SkGb_during_drawing = False
        self.MAGIC_BRUSH_STATE = False
        self.MAGIC_BRUSH_DURING_DRAWING = False
        self.mgcBrushT_i_am_drawing_state = False
        # self.ML_brush_tool_object_state = False
        self.rm_Masks_STATE = False

        self.MainWindow.ai_model_combobox.hide()

        self.QuickTools.showToolFor(tool)
        print("tool is ", tool)
        if self.previousTool == "RF_MODE_BINARY":
            # this mode when we are inside RF mode and want to use the tool there for bitmaps only
            if tool == "auto":
                self.aa_tool_draw = True
                self.makeAllGraphicItemsNonSelectable()
                self.MainWindow.pg_2_widget_graph_visualizer_3.setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap("data/icons/cursor/MagicBoxCursor.png"), -20, -20
                    )
                )
                # ensure non particle ROI
                config.global_signals.ensure_not_particle_class_selected_signal.emit()
                return
            elif tool == "brushMask":
                self.brushMask_STATE = True
                self.makeAllGraphicItemsNonSelectable()
                self.viewport().setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                )
                return
            elif tool == "polygon":
                self.viewport().setCursor(
                    QtGui.QCursor(
                        QtGui.QPixmap("data/icons/cursor/MagicBoxCursor.png"), -20, -20
                    )
                )
                self.add_mask_btn_state = True
                # ensure non particle ROI
                config.global_signals.ensure_not_particle_class_selected_signal.emit()
                return

        if tool != "RF_MODE_BINARY" and self.previousTool == "RF_MODE_BINARY":
            if self.ML_brush_tool_object_state == False:
                self.viewport().setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                )
                self.switchToQuickTools_RF_MODE(False)

        elif tool == "None":
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        elif tool == "erraseTool":
            self.rm_Masks_STATE = True
            self.makeAllGraphicItemsNonSelectable()
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
        elif tool == "magic_brush_move":
            self.MAGIC_BRUSH_STATE = True
            currentImage = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber)
            )
            self.makeAllGraphicItemsNonSelectable(asIs=True, pointsOnly=True)
            self.QuickTools.brushSizeSliderGrubCut.setValue(self.magic_brush_radious)
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
            if self.magic_brush_cursor:
                self.magic_brush_cursor.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
                )
                self.magic_brush_cursor.myW = self.magic_brush_radious
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
            return
            # self.rubberBandActive = True
        elif tool == "selection":
            print("setting cursor to selection!")
            self.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            self.makeAllGraphicItemsSelectable()
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
            pass
        elif tool == "polygon":
            self.viewport().setCursor(
                QtGui.QCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
            )
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
            # self.MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            self.add_mask_btn_state = True

            return
        elif tool == "lasso":
            pass
        elif tool == "auto":
            # magic box tool
            self.aa_tool_draw = True
            self.MainWindow.ai_model_combobox.show()
            cursor = QtGui.QCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
            QtWidgets.QApplication.restoreOverrideCursor()
            self.makeAllGraphicItemsNonSelectable()
            self.viewport().setCursor(cursor)
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
        elif tool == "skeleton grabcut":
            gl = config.global_params
            an = self.MainWindow.new_analysis_object
            if gl.organism == an.elegans:
                self.makeAllGraphicItemsNonSelectable()
                self.SkGb_STATE = True
                self.viewport().setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                )
            else:
                # TODO: this is the magic click section
                self.viewport().setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
                )
                self.QuickTools.brushSizeSliderGrubCut.setValue(self.mgcClickWidth)
                self.makeAllGraphicItemsNonSelectable()
                self.mgcClick_STATE = True
            # ensure non particle ROI
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
        elif tool == "CELL_SPLIT_SEED":
            # print('ITSSSS CELL SPLIT SEDD')
            self.CELL_SPLIT_TOOL_STATE = True
            self.makeAllGraphicItemsNonSelectable()
            self.viewport().setCursor(
                QtGui.QCursor(
                    QtGui.QPixmap("data/icons/cursor/CelerSightCursors_CellSplit.png"),
                    -1,
                    -1,
                )
            )

        elif tool == "RF_MODE_BINARY":
            self.ML_brush_tool_object_state = True
            currentImg = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber)
            )
            self.ML_brush_tool_draw_foreground_array = np.zeros(
                (currentImg.shape[0], currentImg.shape[1]), dtype=bool
            )
            self.ML_brush_tool_draw_background_array = np.zeros(
                (currentImg.shape[0], currentImg.shape[1]), dtype=bool
            )
            # self.setUpFocusModeScene(Focus=True)
            self.switchToQuickTools_RF_MODE(True)
            self.previousTool = "RF_MODE_BINARY"
            from celer_sight_ai.core.ML_tools import ML_RF

            self.MainWindow.g1_ML_settings_groupBox.show()
            self.ML_brush_tool_object = ML_RF(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber)
                .copy(),
                self.ML_brush_tool_draw_foreground_array,
                self.ML_brush_tool_draw_background_array,
                self.MainWindow,
            )
            self.START_getFeatures_Threaded()
        return False

    def spawnModelLoadedText(self):
        self.ModelLoadedLabel = QtWidgets.QLabel(self)
        self.ModelLoadedLabel.setText("ML Model\nactive")
        self.ModelLoadedLabel.setParent(self)
        self.ModelLoadedLabel.setStyleSheet(
            """
            color:rgba(0,255,0,250);
            background-color:rgba(255,255,255,20);
            font-size:12px;
            padding-left:10px;
            padding-right:10px;
            padding-top:3px;
            padding-bottom:3px; 
            border: 2px solid rgba(0,255,0,100); 
            border-radius: 5px;
                                                                    
            """
        )
        self.ModelLoadedLabel.move(10, 150)
        self.ModelLoadedLabel.show()

    def removeModelLoadedText(self):
        self.ModelLoadedLabel.hide()
        self.ModelLoadedLabel.deleteLater()

    def clearnMasksLowerThanThresh(self):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        for item in self._scene.items():
            if type(item) == PolygonAnnotation:
                if (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                    .get_by_uuid(item.mask_uuid)
                    .visibility
                    == False
                ):
                    print("deleting...", item)
                    # self._scene.removeItem(item)
                    item.DeleteMask()
        try:
            self.updateMaskCountLabel()
        except:
            pass

    def refresh_CELL_RM_FINISHED(self, myMaskList):
        raise NotImplementedError

    def ML_brush_tool_object_getFeatures_w_CallBack(self, progress_callback):
        self.ML_brush_tool_object.getFilters()
        return

    def switchToQuickTools_RF_MODE(self, mode=True):
        if mode == True:
            from celer_sight_ai.gui.transitionAnim import labelAnimation

            # self.QuickTools.annotation_tool_frame.hide()
            self.QuickTools.toolsFrame.hide()
            self.QuickTools.RandomForestCellModeFrame.show()
            self.initQuickToolsSize = self.QuickTools.myquickToolsWidget.size()
            self.QuickTools.myquickToolsWidget.setFixedSize(QtCore.QSize(350, 400))

            # make sure forground is checked
            self.QuickTools.CellsMarkerButtonTool.setChecked(True)
            self.QuickTools.BackgroundMarkerButtonTool.setChecked(False)

            self.QuickTools.pushButtonQuickTools_BrushMask.show()
            self.MainWindow.actionBrushMask.trigger()
            self.QuickTools.myquickToolsWidget.layout().removeWidget(
                self.QuickTools.RandomForestCellModeFrame
            )

            self.QuickTools.myquickToolsWidget.layout().removeWidget(
                self.QuickTools.annotation_tool_frame
            )

            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.VideoFramePlace, 0, 1, 1, 1
            )

            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.RandomForestCellModeFrame, 2, 1, 1, 1
            )

            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.annotation_tool_frame, 1, 1, 1, 1
            )
            self.QuickTools.annotation_tool_frame.setMaximumWidth(
                self.QuickTools.RandomForestCellModeFrame.width()
            )
            self.QuickTools.annotation_tool_frame.setMaximumHeight(100)
            self.QuickTools.annotation_tool_frame.setMinimumWidth(
                self.QuickTools.RandomForestCellModeFrame.width()
            )
            self.QuickTools.annotation_tool_frame.setMinimumHeight(100)

            self.QuickTools.pushButtonQuickToolsAutoSpline.hide()
            self.QuickTools.pushButtonQuickToolsErraseTool.hide()
            self.QuickTools.pushButtonQuickToolsMoveMagicBrush.hide()
            self.QuickTools.pushButtonQuickToolsRemoveSelectionTool.hide()
            self.QuickTools.pushButtonQuickToolsSelectionTool.hide()
            self.QuickTools.pushButtonQuickToolsAutoRF_MODE.hide()

            self.makeAllGraphicItemsNonSelectable()
            self.QuickTools.videowidget.transformToNormal()
        elif mode == False:
            self.QuickTools.annotation_tool_frame.show()
            self.QuickTools.pushButtonQuickTools_BrushMask.hide()
            self.QuickTools.toolsFrame.show()
            self.QuickTools.RandomForestCellModeFrame.hide()
            self.QuickTools.myquickToolsWidget.setFixedSize(self.initQuickToolsSize)
            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.VideoFramePlace, 0, 0, 1, 1
            )

            self.QuickTools.toolsFrame.hide()
            self.MainWindow.g1_ML_settings_groupBox.hide()
            self.QuickTools.annotation_tool_frame.setMaximumWidth(185)
            self.QuickTools.annotation_tool_frame.setMaximumHeight(100)
            self.QuickTools.annotation_tool_frame.setMinimumWidth(185)
            self.QuickTools.annotation_tool_frame.setMinimumHeight(100)

            self.QuickTools.pushButtonQuickToolsAutoSpline.show()
            self.QuickTools.pushButtonQuickToolsErraseTool.show()
            self.QuickTools.pushButtonQuickToolsMoveMagicBrush.show()
            self.QuickTools.pushButtonQuickToolsRemoveSelectionTool.show()
            self.QuickTools.pushButtonQuickToolsSelectionTool.show()
            self.QuickTools.pushButtonQuickToolsAutoRF_MODE.show()

            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.RandomForestCellModeFrame, 1, 1, 1, 1
            )

            self.QuickTools.myquickToolsWidget.layout().addWidget(
                self.QuickTools.annotation_tool_frame, 1, 0, 1, 1
            )

    def setUpFocusModeScene(self, Focus=True):
        if Focus == False:
            self.setStyleSheet(
                """
            QGraphicsView{
            background-color:rgb(45,45,45);
            border-color: rbga(45,45,45,0);
            border-width: 0px;  
            border-style: solid;  
            border-radius: 0;
            }  
            """
            )
            self.MainWindow.group_pg1_left.layout().setEnabled(True)
            self.MainWindow.pg_2_widget_graph_visualizer_3.layout().setEnabled(True)
            self.MainWindow.image_preview_scrollArea_Contents.layout().setEnabled(True)
            for widget in self.sceneFocusWidgetList:
                try:
                    widget.setParent(None)
                except:
                    continue
                widget.deleteLater()

        if Focus == True:
            # create widgets
            tmpWidgetLeft = QtWidgets.QWidget(self.MainWindow.group_pg1_left)
            # tmpWidgetTop = QtWidgets.QWidget(self.MainWindow.Dock_Top_pg1_tabs)
            tmpWidgetRight = QtWidgets.QWidget(
                self.MainWindow.pg_2_widget_graph_visualizer_3
            )
            tmpWidgetBottom = QtWidgets.QWidget(
                self.MainWindow.image_preview_scrollArea_Contents
            )

            self.MainWindow.group_pg1_left.layout().addWidget(tmpWidgetLeft)
            self.MainWindow.pg_2_widget_graph_visualizer_3.layout().addWidget(
                tmpWidgetRight
            )
            self.MainWindow.image_preview_scrollArea_Contents.layout().addWidget(
                tmpWidgetBottom
            )

            # move to position and add color
            tmpWidgetLeft.setGeometry(
                0,
                0,
                self.MainWindow.group_pg1_left.width(),
                self.MainWindow.group_pg1_left.height(),
            )
            tmpWidgetLeft.setStyleSheet(
                "background-color: rgba(0,0,0,120);"
            )  # rgba(0,0,0,120);

            tmpWidgetRight.setGeometry(
                0,
                0,
                self.MainWindow.pg_2_widget_graph_visualizer_3.width(),
                self.MainWindow.pg_2_widget_graph_visualizer_3.height(),
            )
            tmpWidgetRight.setStyleSheet("background-color: rgba(0,0,0,120);")
            tmpWidgetBottom.setGeometry(
                0,
                0,
                self.MainWindow.image_preview_scrollArea_Contents.width(),
                self.MainWindow.image_preview_scrollArea_Contents.height(),
            )
            tmpWidgetBottom.setStyleSheet("background-color: rgba(0,0,0,120);")
            print("this runs")

            self.MainWindow.group_pg1_left.layout().setEnabled(False)
            self.MainWindow.pg_2_widget_graph_visualizer_3.layout().setEnabled(False)
            self.MainWindow.image_preview_scrollArea_Contents.layout().setEnabled(False)
            self.setStyleSheet(
                """
                                QGraphicsView{
                                border-color: rbga(0,255,0,255);
                                border-width: 8px;  
                                border-style: solid;  
                                border-radius: 10;
                                }  
                                """
            )

            # add to my scene list
            self.sceneFocusWidgetList.append(tmpWidgetLeft)
            self.sceneFocusWidgetList.append(tmpWidgetRight)
            self.sceneFocusWidgetList.append(tmpWidgetBottom)

    def setDragMode_mc(self, mode):
        if mode == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        elif mode == QtWidgets.QGraphicsView.DragMode.NoDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    # def boundingRect(self):
    #     return self.scene_rect

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.scene_rect, self._brush)

    def toggleDragMode(self):
        if not self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.NoDrag)
        else:
            self.setDragMode_mc(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def mouseDoubleClickEvent(self, event):
        print("double click!")
        if self.SkGb_during_drawing == True:
            self.placeSkGbFinish(self.mapToScene(event.position().toPoint()))
        logger.info("im drawing state is {0}".format(self.i_am_drawing_state))
        logger.info("im drawing state is {0}".format(self.MainWindow.counter_tmp))
        if self.i_am_drawing_state == True:
            if self.MainWindow.counter_tmp >= 3:
                self.completeDrawingPolygon("complete")

        if self.CELL_SPLIT_TOOL_STATE == True:
            if self.CELL_SPLIT_DRAWING == True:
                try:
                    self.end_CELL_SPLIT_SEED(
                        self.mapToScene(event.position().toPoint())
                    )
                except:
                    pass
                self.CELL_SPLIT_DRAWING = False
                self.CELL_SPLIT_SPOTS = []
        return super(PhotoViewer, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        # mouse reslease event for photo viewer
        logger.info("mouseReleaseEvent")
        self.rm_Masks_tool_draw = False
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            self.leftMouseBtn_autoRepeat = False
        if self.MAGIC_BRUSH_DURING_DRAWING is True:
            # self.makeAllGraphicItemsNonSelectable()
            self.MAGIC_BRUSH_DURING_DRAWING = False
            # Release event here signals that the move action is done,
            # We add a redo undo from the start of the action to the end
            # for all selected items.
            from celer_sight_ai.historyStack import GripItemMoveCommand

            selected_items = self._scene.selectedItems()
            # get only grip items
            selected_items = [i for i in selected_items if type(i) == GripItem]
            if len(selected_items):
                self.MainWindow.undoStack.push(
                    GripItemMoveCommand(
                        polygon_item=selected_items[
                            0
                        ].m_annotation_item,  #  has to be the same item
                        grip_items_indexes=[i.m_index for i in selected_items],
                        grip_old_items_pos=[
                            [i.pos().x(), i.pos().y()]
                            for i in self.magic_brush_points_set_A
                        ],  # previous selected items
                        grip_new_items_pos=[
                            [i.pos().x(), i.pos().y()] for i in selected_items
                        ],
                        mask_uuid=selected_items[0].m_annotation_item.unique_id,
                        condition_uuid=self.MainWindow.DH.BLobj.get_current_condition_object().unique_id,
                        MainWindow=self.MainWindow,
                    )
                )
            # if self.hasPhoto():
            if self.MAGIC_BRUSH_STATE is True:
                self.MAGIC_BRUSH_DURING_DRAWING = False

        print(
            "On release function states are {} and {}".format(
                self.ML_brush_tool_object_state, self.ML_brush_tool_draw_is_active
            )
        )
        if (
            self.ML_brush_tool_object_state == True
            and self.ML_brush_tool_draw_is_active == True
        ):
            self.ML_brush_tool_draw_is_active = False
            for item in self.ML_brush_tool_draw_scene_items:
                self._scene.removeItem(item)
            self.ML_brush_tool_draw_scene_items = []
            config.global_signals.update_ML_BitMapScene.emit()
        self.buttonPress = False
        # self.ui_tool_selection.MyDialog.mouseReleaseEvent(event) # hides the pop up menu for tools
        # if (
        #     self.hasPhoto()
        #     and self.during_drawing_bbox == True
        #     and self.ui_tool_selection.selected_button == "auto"
        # ):
        #     if (
        #         event.type() == QtCore.QEvent.Type.MouseButtonPress
        #         or event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress
        #     ):
        #         # print("draw_# The above code is not a valid Python code. It seems to be a typo or
        # incomplete code snippet.
        # The above code is not a valid Python code. It seems to be a typo or
        # incomplete code snippet.
        # bounding_box_stop")
        #         if len(self._scene.selectedItems()) == 0:
        #             self.draw_bounding_box_stop_THREADED(
        #                 self.mapToScene(event.position().toPoint()).toPoint()
        #             )
        #             return super(PhotoViewer, self).mousePressEvent(event)

        if self.pop_up_tool_choosing_state == True:
            # self.ui_tool_selection.MyDialog.hide()
            self.pop_up_tool_choosing_state = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self.update_tool()
            return super(PhotoViewer, self).mouseReleaseEvent(event)

        return super(PhotoViewer, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.leftMouseBtn_autoRepeat = True
                if self.mgcClick_STATE:
                    cPos = self.mapToScene(event.position().toPoint())
                    # patch it
                    self.aa_tool_bb_first_x = int(cPos.x() - self.mgcClickWidth / 2)
                    self.aa_tool_bb_first_y = int(cPos.y() - self.mgcClickWidth / 2)
                    self.last_bbox_x = int(cPos.x() + self.mgcClickWidth / 2)
                    self.last_bbox_y = int(cPos.y() + self.mgcClickWidth / 2)
                    self.draw_bounding_box_stop_THREADED(
                        self.mapToScene(event.position().toPoint()).toPoint()
                    )

            self.photoClicked.emit(
                self.mapToScene(event.position().toPoint()).toPoint()
            )
            self.buttonPress = True
        return super(PhotoViewer, self).mousePressEvent(event)

    def keyReleaseEvent(self, ev):
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Shift or key == QtCore.Qt.Key.Key_Alt:
            self.POLYGON_MODIFY_MODE = None
        return super(PhotoViewer, self).keyReleaseEvent(ev)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key.Key_Escape:
            if self.i_am_drawing_state == True:
                self.completeDrawingPolygon()
            if self.SkGb_during_drawing == True:
                self.placeSkGbFinish(pos=None, COMPLETE=False)
            if self.aa_tool_draw and self.during_drawing_bbox:
                self.completeDrawing_Bounding_Box()
            return super(PhotoViewer, self).keyPressEvent(event)
        if key == QtCore.Qt.Key.Key_Enter or key == QtCore.Qt.Key.Key_Return:
            if self.i_am_drawing_state == True:
                self.completeDrawingPolygon(MODE="complete")
            if self.aa_tool_draw:
                # when the mask suggestor is on with magic box, complete the process
                # if accept all mask suggestions
                self.MainWindow.sdknn_tool.magic_box_2.accept_current_suggested_annotations()
        if key == QtCore.Qt.Key.Key_Alt:
            self.POLYGON_MODIFY_MODE = self.POLYGON_MODIFY_REMOVE
        if key == QtCore.Qt.Key.Key_Shift:
            self.POLYGON_MODIFY_MODE = self.POLYGON_MODIFY_ADD
        if (
            key == QtCore.Qt.Key.Key_Return
            and event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier
        ):
            self.MainWindow.spawn_add_class_dialog()

        return super(PhotoViewer, self).keyPressEvent(event)

    def mouseMoveEvent(self, event):
        pos_point = self.mapToScene(event.position().toPoint())
        self.MainWindow.under_window_comments.setText(
            f"Scene pos: {int(pos_point.x())} {int(pos_point.y())} viewport pos: {event.position().toPoint().x()} {event.position().toPoint().y()} "
        )
        # rubber band mode:
        if self.scaleBarDraw_duringDraw_STATE == True:
            self.scaleBarWhile(self.mapToScene(event.position().toPoint()))

        if self.ui_tool_selection.selected_button == "skeleton grabcut":
            if self.SkGb_during_drawing == True:
                self.SkGbWhileDrawing(self.mapToScene(event.position().toPoint()))

        if self.MAGIC_BRUSH_DURING_DRAWING == True:
            currentPos = self.mapToScene(event.position().toPoint())
            self.movePointsBrushToolMagic1(
                self.magic_brush_pos_a.x() - currentPos.x(),
                self.magic_brush_pos_a.y() - currentPos.y(),
                self.magic_brush_points_set_A,
            )
            self.magic_brush_pos_a = self.mapToScene(event.position().toPoint())
            # circlPainter = self.getPainterPathCircle(
            #     self.QuickTools.brushSizeSpinBoxGrabCut.value(), self.magic_brush_pos_a
            # )
            # self._scene.setSelectionArea(circlPainter)
            # self.magic_brush_points_set_A = [i for i in self._scene.selectedItems() if type(i) == GripItem]
        # FIX RUBBER BAND HERE
        """
        Draw FG or BG at CELL Random Forrest
        """
        if self.rm_Masks_tool_draw == True:
            self.DeleteAllMasksUnderMouse(event.position())
            return super(PhotoViewer, self).mouseMoveEvent(event)
        if self.i_am_drawing_state == True:
            self.CurrentPosOnScene = self.mapToScene(
                event.position().toPoint()
            ).toPoint()
        if self.aa_review_state == True:
            return super(PhotoViewer, self).mouseMoveEvent(event)
        if self.aa_tool_draw == True:
            if self.i_am_drawing_state_bbox == True:
                # starts the drawing process
                self.auto_annotate_tool_while_draw(
                    self.mapToScene(event.position().toPoint()).toPoint()
                )
            self.global_pos = self.mapToGlobal(
                QtCore.QPoint(int(event.position().x()), int(event.position().y()))
            )
            # if magic tool is active

            # update the position of the guides
            pos = self.mapToScene(event.position().toPoint())
            topLeft = self.mapToScene(0, 0)
            bottomRight = self.mapToScene(
                self.viewport().width(), self.viewport().height()
            )
            if not self.h_guide_magic_tool in self.scene().items():
                self.scene().addItem(self.h_guide_magic_tool)
                self.scene().addItem(self.v_guide_magic_tool)
            self.h_guide_magic_tool.setLine(
                topLeft.x(), pos.y(), bottomRight.x(), pos.y()
            )
            self.v_guide_magic_tool.setLine(
                pos.x(), topLeft.y(), pos.x(), bottomRight.y()
            )
            # bring it to the top
            self.h_guide_magic_tool.setZValue(9999)
            self.h_guide_magic_tool.show()
            self.v_guide_magic_tool.setZValue(9999)
            self.v_guide_magic_tool.show()

        if (
            self.ui_tool_selection.selected_button == "polygon"
            and self.hasPhoto()
            and self.pop_up_tool_choosing_state != True
        ):
            # if gui_main.DH.masks_state[gui_main.current_imagenumber] == True or gui_main.DH.masks_state_usr[gui_main.current_imagenumber] == True :

            if self._photo.isUnderMouse() and self.add_mask_btn_state == True:
                if self.MainWindow.counter_tmp > 0 and self.i_am_drawing_state == True:
                    self.draw_while_mouse_move(
                        self.mapToScene(event.position().toPoint()).toPoint()
                    )
                    return super(PhotoViewer, self).mouseMoveEvent(event)

        if self.ML_brush_tool_draw_is_active == True and self.brushMask_STATE == True:
            if self.ML_brush_tool_draw_foreground_add == True:
                # get pos on scene
                evPos = self.mapToScene(event.position().toPoint())

                currentImg = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .getImage(self.MainWindow.current_imagenumber)
                )

                rr, cc = circle(
                    evPos.x(),
                    evPos.y(),
                    self.getML_brush_tool_draw_brush_size(),
                    shape=(currentImg.shape[0], currentImg.shape[1]),
                )
                # Draw on machine learning frame
                self.ML_brush_tool_draw_foreground_array[cc, rr] = True
                # Draw on viewer
                self.CELL_RM_point_drawing = QtWidgets.QGraphicsEllipseItem(
                    evPos.x() - self.getML_brush_tool_draw_brush_size(),
                    evPos.y() - self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size(),
                )
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
                pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                self.CELL_RM_point_drawing.setBrush(
                    QtGui.QBrush(
                        QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern
                    )
                )
                self.CELL_RM_point_drawing.setPen(pen)
                self._scene.addItem(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_scene_items.append(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_background_added = True
                self.ML_brush_tool_draw_refreshed = False
                return super(PhotoViewer, self).mouseMoveEvent(event)

            elif self.ML_brush_tool_draw_background_add == True:
                evPos = self.mapToScene(event.position().toPoint())
                currentImg = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .getImage(self.MainWindow.current_imagenumber)
                )
                rr, cc = circle(
                    evPos.x(),
                    evPos.y(),
                    self.getML_brush_tool_draw_brush_size(),
                    shape=(currentImg.shape[0], currentImg.shape[1]),
                )
                # Draw on machine learning frame
                self.ML_brush_tool_draw_background_array[cc, rr] = True
                # Draw on viewer
                self.CELL_RM_point_drawing = QtWidgets.QGraphicsEllipseItem(
                    evPos.x() - self.getML_brush_tool_draw_brush_size(),
                    evPos.y() - self.getML_brush_tool_draw_brush_size(),
                    self.getML_brush_tool_draw_brush_size() * 2.0,
                    self.getML_brush_tool_draw_brush_size() * 2.0,
                )
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
                pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                self.CELL_RM_point_drawing.setBrush(
                    QtGui.QBrush(
                        QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.SolidPattern
                    )
                )
                self.CELL_RM_point_drawing.setPen(pen)
                self._scene.addItem(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_foreground_added = True
                self.ML_brush_tool_draw_scene_items.append(self.CELL_RM_point_drawing)
                self.ML_brush_tool_draw_refreshed = False
                return super(PhotoViewer, self).mouseMoveEvent(event)

        if self.pop_up_tool_choosing_state == True:
            if event.type() == QtCore.QEvent.Type.MouseMove:
                self.ui_tool_selection.MyDialog.mouseMoveEvent(event)
                # return True
        return super(PhotoViewer, self).mouseMoveEvent(event)

    def eventFilter(self, source, event):
        """
        mouse move event
        """
        if isinstance(event, QtGui.QNativeGestureEvent):
            # This is mainly for macs and zooming in using the trackpad
            typ = event.gestureType()
            if typ == QtCore.Qt.NativeGestureType.BeginNativeGesture:
                # start of event.
                self.zoomValue = 0.0
                self.target_zoom_pos = self.mapToScene(
                    event.position().toPoint()
                )  # * scale  # * scale
            elif typ == QtCore.Qt.NativeGestureType.ZoomNativeGesture:
                # During that event we are adjusting the factor of zoom
                if self.transform().m11() < 0:
                    self.scale(-1, 1)
                    return True
                if self.transform().m22() < 0:
                    self.scale(1, -1)
                    return True

                zoom_scale = 2
                self.scale(
                    np.clip(event.value(), -zoom_scale, zoom_scale) + 1.0,
                    np.clip(event.value(), -zoom_scale, zoom_scale) + 1.0,
                )

                config.global_signals.check_and_update_high_res_slides_signal.emit()
            elif typ == QtCore.Qt.NativeGestureType.SwipeNativeGesture:
                print(f"other gesture type: {typ}")
            if typ == QtCore.Qt.NativeGestureType.EndNativeGesture:
                print(f"ending gesture {-1 if self.zoomValue < 0 else 1}")
            return True

        if type(event) == QtWidgets.QWidgetItem:
            # need to skip this event it will cause errors.
            return True

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            # to draw the scale bar
            logger.info("press event at PhotoViewer")
            if self.scaleBarDraw_STATE == True:
                self.scaleBarPlaceFirstPoint(
                    self.mapToScene(event.position().toPoint())
                )
            # if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if self.rm_Masks_STATE == True:
                logger.info("masks state true")
                # remote masks tool
                self.rm_Masks_tool_draw = True
                self.DeleteAllMasksUnderMouse(event.position())
                return super(PhotoViewer, self).eventFilter(source, event)
            if self.add_mask_btn_state == True:
                logger.info("add_mask_btn_state true")
                if self.during_drawing == False:
                    if self.POLYGON_MODIFY_MODE == None:
                        if len(self.polyPreviousSelectedItems) != 0:
                            circlPainter = self.getPainterPathCircle(
                                0, QtCore.QPoint(0, 0)
                            )
                            self._scene.setSelectionArea(circlPainter)
                            self.polyPreviousSelectedItems = []
                            return super(PhotoViewer, self).eventFilter(source, event)
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if self.ML_brush_tool_object_state == True:
                    if self.brushMask_STATE:
                        logger.info(
                            "ML_brush_tool_object_state true and brushMask_STATE"
                        )
                        self.ML_brush_tool_draw_is_active = True
                        self.brushMask_DuringDrawing = True

        if event.type() == QtCore.QEvent.Type.HoverEnter:
            if self.aa_tool_draw:
                if self.h_guide_magic_tool not in self._scene.items():
                    self._scene.addItem(self.h_guide_magic_tool)
                    self._scene.addItem(self.v_guide_magic_tool)
            if self.mgcClick_STATE == True:
                logger.info("magic click state truwe!")
                self.postoscene = self.mapToScene(event.position().toPoint()).toPoint()
                if self.magic_brush_cursor:
                    if self.magic_brush_cursor in self._scene.items():
                        self.magic_brush_cursor.show()

                    else:
                        posNow = self.mapToScene(event.position().toPoint()).toPoint()
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(), posNow.y(), self.mgcClickWidth
                        )
                        self._scene.addItem(self.magic_brush_cursor)
                else:
                    posNow = self.mapToScene(event.position().toPoint()).toPoint()
                    self.magic_brush_cursor = mgcClick_cursor_cls(
                        posNow.x(), posNow.y(), self.mgcClickWidth
                    )
                    self.magic_brush_cursor.show()
                    self._scene.addItem(self.magic_brush_cursor)

        if event.type() == QtCore.QEvent.Type.HoverLeave:
            if self.mgcClick_STATE == True or self.mgcBrushT == True:
                if self.magic_brush_cursor:
                    self._scene.removeItem(self.magic_brush_cursor)
            if self.aa_tool_draw:
                if self.h_guide_magic_tool in self._scene.items():
                    self._scene.removeItem(self.h_guide_magic_tool)
                    self._scene.removeItem(self.v_guide_magic_tool)
        if event.type() == QtCore.QEvent.Type.HoverMove:
            if self.mgcClick_STATE or self.MAGIC_BRUSH_STATE:
                posNow = self.mapToScene(event.position().toPoint())
                if not self.magic_brush_cursor:
                    # self.postoscene = self.mapToScene(event.position().toPoint() ).toPoint()
                    if self.MAGIC_BRUSH_STATE:
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(),
                            posNow.y(),
                            self.magic_brush_radious,
                            mode="circle",
                        )
                    elif self.mgcClick_STATE:
                        self.magic_brush_cursor = mgcClick_cursor_cls(
                            posNow.x(), posNow.y(), self.mgcClickWidth, mode="box"
                        )
                    # self._scene.addItem(self.magic_brush_cursor)
                if not self.magic_brush_cursor in self._scene.items():
                    self._scene.addItem(self.magic_brush_cursor)

                self.magic_brush_cursor.moveToC(posNow.x(), posNow.y())
                # self.magic_brush_cursor.updateSize(self.QuickTools.brushSizeSpinBoxGrabCut.value())
            if self.aa_tool_draw == True:
                if self.buttonPress == True:
                    if (
                        self.i_am_drawing_state_bbox == False
                        and self.during_drawing == False
                        and self.aa_review_state == True
                    ):
                        logger.debug("aa_tool_draw final is true")

                        """
                        Here I need to activate:
                        if on click inside, add to mask and recompute
                        if outside then exit aa_review_state
                        if normal pos is inside the normal pos of the box then draw
                        """
                        # if self.i_am_drawing_state_bbox == False and self.during_drawing == False and self.aa_review_state == True:
                        self.aa_review_state_decider(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        return super(PhotoViewer, self).eventFilter(source, event)

        # if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
        #     self.ui_tool_selection.MyDialog.eventFilter( source, event)
        # if self.hasPhoto() and self.during_drawing_bbox==True:
        #     if event.type() == QtCore.QEvent.Type.MouseButtonRelease or event.type() == QtCore.QEvent.Type.GraphicsSceneMouseRelease:
        #         print("draw_bounding_box_stop")
        #         self.draw_bounding_box_stop_THREADED(self.mapToScene(event.position().toPoint() ).toPoint())
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.postoscene = self.mapToScene(event.position().toPoint()).toPoint()
            if self.aa_review_state == True:
                self.global_pos_x = self.postoscene.position().x()
                self.global_pos_y = self.postoscene.position().y()

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.dragPos = event.globalPosition()
                if self.SelectionStateRegions == True:
                    self.SelectionStateRegions = False
                    self.MainWindow.SelectedMaskDialog.hide()

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
            and self._photo.isUnderMouse()
        ):
            if self.MAGIC_BRUSH_STATE == True:
                if self.MAGIC_BRUSH_DURING_DRAWING == False:
                    self.magic_brush_pos_a = self.mapToScene(event.position().toPoint())
                    print("at press with radius at ", self.magic_brush_radious)
                    circlPainter = self.getPainterPathCircle(
                        self.magic_brush_radious, self.magic_brush_pos_a
                    )
                    self._scene.setSelectionArea(circlPainter)
                    self.magic_brush_points_set_A = self._scene.selectedItems()
                    self.MAGIC_BRUSH_DURING_DRAWING = True
                    self.mgcBrushT_fallOff = []

                    return super(PhotoViewer, self).eventFilter(source, event)

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
            and self._photo.isUnderMouse()
        ):
            self.leftMouseBtn_autoRepeat = True
            if self.ui_tool_selection.selected_button == "CELL_SPLIT_SEED":
                self.placeCELL_SPLIT_SEED_point(
                    self.mapToScene(event.position().toPoint())
                )
                self.CELL_SPLIT_DRAWING = True
                logger.info("button press!! CELL SPLIT")

            if self.ui_tool_selection.selected_button == "skeleton grabcut":
                if self.SkGb_STATE == True:
                    logger.info("self.SkGb_STATE is True")
                    self.placeSkGbAddPoint(self.mapToScene(event.position().toPoint()))
            # and self.MainWindow.DH.masks_state[self.MainWindow.current_imagenumber] == True :
            if self.ui_tool_selection.selected_button == "selection":
                self.global_pos_x = self.MainWindow.pos().x() + 0
                self.global_pos_y = self.MainWindow.pos().y()
                # self.selected_mask_under_mouse(self.mapToScene(event.position().toPoint() ).toPoint(), self.DH.master_mask_list)
            elif self.ui_tool_selection.selected_button == "selection":
                self.selected_mask = -1
                self.final_mask_number = -1

            if self.pop_up_tool_choosing_state == True:
                self.pop_up_tool_choosing_state = False
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                self.update_tool()
                print("stops")

        """
        Draw tool auto
        """

        if self.aa_tool_draw == True:
            if (
                event.type() == QtCore.QEvent.Type.MouseButtonPress
                or event.type() == QtCore.QEvent.Type.MouseMove
            ) and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if (
                    self.i_am_drawing_state_bbox == False
                    and self.during_drawing == False
                    and self.aa_review_state == True
                ):
                    """
                    Here I need to activate:
                    if on click inside, add to mask and recompute
                    if outside then exit aa_review_state
                    if normal pos is inside the normal pos of the box then draw
                    """
                    # if self.i_am_drawing_state_bbox == False and self.during_drawing == False and self.aa_review_state == True:
                    return True

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and self.ui_tool_selection.selected_button == "polygon"
            and self.hasPhoto() == True
            and self.dragMode() != QtWidgets.QGraphicsView.DragMode.ScrollHandDrag
        ):
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                print("its left buttons!")
                self.draw_polygon(self.mapToScene(event.position().toPoint()).toPoint())
                return super(PhotoViewer, self).eventFilter(source, event)

        if (
            event.type() == QtCore.QEvent.Type.MouseButtonPress
            and self.ui_tool_selection.selected_button == "lasso"
            and self.hasPhoto()
            and self.pop_up_tool_choosing_state != True
        ):
            # delete mask
            if (
                self.MainWindow.DH.masks_state[self.MainWindow.current_imagenumber]
                == True
                or self.MainWindow.DH.masks_state_usr[
                    self.MainWindow.current_imagenumber
                ]
                == True
            ):
                if self._photo.isUnderMouse():
                    if (
                        self.mask_under_mouse(
                            self.mapToScene(event.position().toPoint()).toPoint(),
                            self.MainWindow.DH.master_mask_list,
                        )
                        == True
                        and self.MainWindow.selection_state == False
                    ):
                        pass
                    else:
                        self.MainWindow.selected_mask = -1

                        self.MainWindow.final_mask_number = -1
            return False

        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if (
                event.button() == QtCore.Qt.MouseButton.LeftButton
                and self.ui_tool_selection.selected_button == "auto"
            ):
                if self.hasPhoto():
                    if self.during_drawing_bbox == True:
                        if len(self._scene.selectedItems()) == 0:
                            self.draw_bounding_box_stop_THREADED(
                                self.mapToScene(event.position().toPoint()).toPoint()
                            )
                            self.completeDrawing_Bounding_Box()
                    elif len(self._scene.selectedItems()) == 0:
                        # bounding box beggins process by setting init points x,y and allows for while to start
                        self.auto_annotate_tool_start(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        self.MainWindow.selected_mask -= 1

        # else:
        #     logger.warning("Not a QEvent passed to the eventFilder.")

        return super(PhotoViewer, self).eventFilter(source, event)

    def combinePolygons(self, pol1, pol2):
        myImageShape = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .getImage(self.MainWindow.current_imagenumber)
            .shape
        )
        # create empty images
        pol1Image = np.zeros(
            (myImageShape.shape[0], myImageShape.shape[1]), dtype=np.uint8
        )
        pol2Image = pol1Image.copy()

        pol1mask = skimage.draw.polygon2mask(
            (pol1Image.shape[0], pol1Image.shape[1]), np.asarray(pol1, dtype=np.uint16)
        )
        pol2mask = skimage.draw.polygon2mask(
            (pol2Image.shape[0], pol2Image.shape[1]), np.asarray(pol2, dtype=np.uint16)
        )
        FinalMask = pol1mask + pol2mask
        listAllMasks = []
        contours = skimage.measure.find_contours(FinalMask, 0.85)
        for i in range(len(contours)):
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[i]), tolerance=0.4
            ).astype(np.uint16)
            listAllMasks.append(
                QtGui.QPolygonF([QtCore.QPointF(p[1], p[0]) for p in appr_hand])
            )

        return listAllMasks

    def placeCELL_SPLIT_SEED_point(self, pos):
        """
        we place the first point of the CELL_SPLIT_STATE
        """
        self.CELL_SPLIT_SPOTS.append((pos.x(), pos.y()))

        itemDotSplitW = QtWidgets.QGraphicsEllipseItem(
            pos.x() - self.getML_brush_tool_draw_brush_size(),
            pos.y() - self.getML_brush_tool_draw_brush_size(),
            self.getML_brush_tool_draw_brush_size() * 3.0,
            self.getML_brush_tool_draw_brush_size() * 3.0,
        )
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        itemDotSplitW.setBrush(
            QtGui.QBrush(QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern)
        )
        itemDotSplitW.setPen(pen)
        self._scene.addItem(itemDotSplitW)
        itemDotSplitR = QtWidgets.QGraphicsEllipseItem(
            pos.x() - self.getML_brush_tool_draw_brush_size(),
            pos.y() - self.getML_brush_tool_draw_brush_size(),
            self.getML_brush_tool_draw_brush_size() * 2.0,
            self.getML_brush_tool_draw_brush_size() * 2.0,
        )
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        itemDotSplitR.setBrush(
            QtGui.QBrush(QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern)
        )
        itemDotSplitR.setPen(pen)
        self._scene.addItem(itemDotSplitR)
        self.sceneCELL_SPLIT_ITEMS.append(itemDotSplitR)

    def end_CELL_SPLIT_SEED(self, pos):
        raise NotImplementedError

    def placeSkGbAddPoint(self, pos):
        """
        we place the first point of the poly line
        """
        print("def placeSkGbAddPoint")

        if len(self.SkGb_points) != 0:
            pen_width = 3
            # self.QuickTools.spinBoxOpacitySkeletonGB.value(),
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.red, 0.3)
            pen.setWidth(pen_width)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            pen.setStyle(QtCore.Qt.PenStyle.DashLine)
            # add the line between two points
            line = QtWidgets.QGraphicsLineItem(
                QtCore.QLineF(
                    self.SkGb_points[-1][0], self.SkGb_points[-1][1], pos.x(), pos.y()
                )
            )
            # myPen = self.MainWindow.ColorPrefsViewer.getColorSkGc()

            # myPen.setWidth(self.QuickTools.spinBoxradiusSkeletonGB.value())
            line.setPen(pen)
            # self.SkBG_allLineScene.append(line)
            # self._scene.addItem(line)

        self.SkGb_points.append([pos.x(), pos.y()])
        self.SkGb_during_drawing = True

    def SkGbWhileDrawing(self, pos):
        """
        this runs continiusly connected the last pressed point to current position
        """
        myPen = self.MainWindow.ColorPrefsViewer.getColorSkGc()
        myPen.setWidth(self.QuickTools.spinBoxradiusSkeletonGB.value())
        try:
            self._scene.removeItem(self.SkGb_whileLine)
        except:
            print("error")
            pass

        qpp = QtGui.QPainterPath()
        points = self.SkGb_points.copy()
        points.append([pos.x(), pos.y()])

        qpp.addPolygon(QtGui.QPolygonF([QtCore.QPointF(p[0], p[1]) for p in points]))
        self.SkGb_whileLine = QtWidgets.QGraphicsPathItem(qpp)
        self.SkGb_whileLine.setPen(myPen)
        self._scene.addItem(self.SkGb_whileLine)
        # self.SkGb_whileLine = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.SkGb_points[-1][0],\
        #     self.SkGb_points[-1][1] , pos.x(),pos.y() ))
        # self.SkGb_whileLine.setPen(myPen)
        # self._scene.addItem(self.SkGb_whileLine)

    def placeSkGbFinish(self, pos, COMPLETE=True):
        """
        we end the polyline, either by completing it or deleting it
        """
        from celer_sight_ai import config

        raise NotImplementedError
        import skimage
        import cv2

        print("def placeSkGbFinish")
        from celer_sight_ai.gui.Utilities.QitemTools import (
            drawThickLine,
            skeletonGrabCut,
        )

        if COMPLETE == True:
            self.SkGb_points.append([pos.x(), pos.y()])
            self.SkGb_during_drawing = False
            imageDrawn = drawThickLine(
                self.SkGb_points,
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                int(self.QuickTools.spinBoxradiusSkeletonGB.value() * 0.66),
            )
            imageDrawnSkeleton = drawThickLine(
                self.SkGb_points,
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                int(self.QuickTools.spinBoxradiusSkeletonGB.value() * 0.07),
            )
            finalMask = skeletonGrabCut(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .getImage(self.MainWindow.current_imagenumber),
                imageDrawn,
                imageDrawnSkeleton,
            )
            finalMask = finalMask.astype(bool)
            if np.count_nonzero(finalMask) <= 4:
                return
            contours = skimage.measure.find_contours(
                finalMask.astype(np.uint8).copy(), 0.8
            )
            appr_hand = skimage.measure.approximate_polygon(
                np.asarray(contours[0]), tolerance=2
            )
            QpointPolygonMC = QtGui.QPolygonF(
                [QtCore.QPointF(p[1], p[0]) for p in appr_hand]
            )

            from celer_sight_ai import config

            config.global_signals.create_annotation_object_signal.emit(
                [
                    self.MainWindow.current_imagenumber,
                    self.MainWindow.DH.BLobj.get_current_condition(),
                    QpointPolygonMC,
                ]
            )
            self.MainWindow.selected_mask = (
                len(
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                    .masks
                )
                - 1
            )  # last added mask
            self.SkGb_points = []

            try:
                self._scene.removeItem(self.SkGb_whileLine)
            except:
                print("error")
                pass
            # self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
        else:
            self.SkGb_points = []
            self.SkGb_during_drawing = False

            try:
                self._scene.removeItem(self.SkGb_whileLine)
            except:
                print("error")
                pass

    def DeleteAllMasksUnderMouse(self, pos):
        for item in self._scene.items():
            if type(item) == PolygonAnnotation:
                if item.isUnderMouse():
                    item.DeleteMask()
                return

    def clearAllMasksUnderMouse(self, pos):
        # clear masks in current image in the self._scene
        for item in self._scene.items():
            if type(item) == PolygonAnnotation:
                # if item.isUnderMouse():
                item.DeleteMask()
                return

    def auto_annotate_pos(
        self,
        auto_tool_1,
        auto_aa_tool_gui,
        threshed_image,
        xstart,
        ystart,
        xfinish,
        yfinish,
        supplied_mask_bool=False,
    ):
        """
        auto annotation tool
        TODO: needs to become a class with widgets etc
        TODO: add the markers for removing and adding background and forgrdound
        TODO: add the appropriend GUI elements
        TODO: create a lock mechanism, while its active cant press anything else
        TODO: esc removes tool and selection
        """
        mask_pred_tmp = []
        import numpy as np

        try:
            if supplied_mask_bool == False:
                mask_result = auto_tool_1.grab_cut_v2(
                    threshed_image,
                    self.MainWindow.auto_aa_tool_gui,
                    xstart,
                    ystart,
                    xfinish,
                    yfinish,
                )
            else:
                mask_result = auto_tool_1.grab_cut_v2(
                    threshed_image,
                    self.MainWindow.auto_aa_tool_gui,
                    xstart,
                    ystart,
                    xfinish,
                    yfinish,
                    self.mask_aa_base.copy(),
                    supplied_mask__bool=True,
                )

            mask_pred_tmp = mask_result.astype(bool)
        except Exception as e:
            print(e)
            return

        if np.count_nonzero(mask_pred_tmp) <= 4:
            return 0, 0, False
        import skimage

        contours = skimage.measure.find_contours(
            mask_pred_tmp.astype(np.uint8).copy(), 0.8
        )
        appr_hand = skimage.measure.approximate_polygon(
            np.asarray(contours[0]), tolerance=2
        )

        QpointPolygonMC = QtGui.QPolygonF(
            [QtCore.QPointF(p[1], p[0]) for p in appr_hand]
        )
        self.AA_added_Polygon = QpointPolygonMC

        config.global_signals.create_annotation_object_signal.emit(
            [
                self.MainWindowRef.current_imagenumber,
                self.MainWindowRef.DH.BLobj.get_current_condition(),
                QpointPolygonMC,
                "polygon",  # by default its polygon annotation
            ]
        )

        self.MainWindow.selected_mask = (
            len(
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images[self.MainWindow.current_imagenumber]
                .masks
            )
            - 1
        )  # last added mask

        # self.load_main_scene(self.current_imagenumber)
        if auto_tool_1.y1 > auto_tool_1.y2 and auto_tool_1.x1 > auto_tool_1.x2:
            # auto_tool_1.x2, auto_tool_1.y1
            return self.aa_tool_bb_first_x, self.global_pos.y(), True
        elif auto_tool_1.y2 > auto_tool_1.y1 and auto_tool_1.x1 > auto_tool_1.x2:
            # auto_tool_1.x2, auto_tool_1.y2
            return self.aa_tool_bb_first_x, self.aa_tool_bb_first_y, True
        elif auto_tool_1.y1 > auto_tool_1.y2 and auto_tool_1.x2 > auto_tool_1.x1:
            # auto_tool_1.x1, auto_tool_1.y1
            return self.global_pos.x(), self.global_pos.y(), True
        elif auto_tool_1.y2 > auto_tool_1.y1 and auto_tool_1.x2 > auto_tool_1.x1:
            # auto_tool_1.x1, auto_tool_1.y2
            return self.global_pos.x(), self.aa_tool_bb_first_y, True
        return 0, 0, True

    def aa_signal_handler(self, add_fg=True, add_bg=False):
        if add_fg == True:
            self.FG_add = True
            self.BG_add = False
            rad = self.QuickTools.brushSizeSpinBoxGrabCut.value()
            if rad == 0:
                rad = 1
            circle = self.CreateAADisk(rad, 0, 255, 0)
            height, width, channel = circle.shape
            bytesPerLine = 3 * width
            mypixmap = QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    circle.data,
                    circle.shape[1],
                    circle.shape[0],
                    circle.strides[0],
                    QtGui.QImage.Format_ARGB32_Premultiplied,
                )
            )
        elif add_bg == True:
            self.BG_add = True
            self.FG_add = False
            rad = self.QuickTools.brushSizeSpinBoxGrabCut.value()
            if rad == 0:
                rad = 1
            circle = self.CreateAADisk(rad, 0, 0, 255)
            height, width, channel = circle.shape
            bytesPerLine = 3 * width
            mypixmap = QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    circle.data,
                    circle.shape[1],
                    circle.shape[0],
                    circle.strides[0],
                    QtGui.QImage.Format_ARGB32_Premultiplied,
                )
            )
        else:
            return

    def CreateAADisk(self, rad, r, g, b, genOpacity=255):
        import skimage.draw

        img = np.zeros((rad * 2, rad * 2, 4), dtype=np.uint8)
        rr, cc = skimage.draw.disk((rad, rad), rad)
        img[rr, cc, 0] = r
        img[rr, cc, 1] = g
        img[rr, cc, 2] = b
        img[rr, cc, 3] = 255 * (genOpacity / 255)
        return img

    def CreateAAcircle(self, rad, r, g, b, genOpacity=255):
        import skimage.draw

        img = np.zeros((rad * 2, rad * 2, 4), dtype=np.uint8)
        rr, cc = skimage.draw.circle_perimeter(rad, rad, rad - 1)
        img[rr, cc, 0] = r
        img[rr, cc, 1] = g
        img[rr, cc, 2] = b
        img[rr, cc, 3] = 255 * (genOpacity / 255)
        return img

    def draw_on_aa_mask(self, pos):
        """
        After the review state , we draw based on the mode (Forground or Bakcground)
        """
        import cv2
        import skimage

        # rad = 4
        rad = self.QuickTools.brushSizeSpinBoxGrabCut.value()
        self.aa_point_drawing = QtWidgets.QGraphicsEllipseItem(
            pos.x() - rad, pos.y() - rad, rad * 2.0, rad * 2.0
        )

        # Decide wether we are adding or removing mask
        # id add then add red spot if not then green spot
        if self.FG_add == True:
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            self.aa_point_drawing.setBrush(
                QtGui.QBrush(
                    QtCore.Qt.GlobalColor.green, QtCore.Qt.BrushStyle.SolidPattern
                )
            )
            self.aa_point_drawing.setPen(pen)
            self._scene.addItem(self.aa_point_drawing)
        else:
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            self.aa_point_drawing.setBrush(
                QtGui.QBrush(
                    QtCore.Qt.GlobalColor.red, QtCore.Qt.BrushStyle.SolidPattern
                )
            )

            # pen.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            self.aa_point_drawing.setPen(pen)
            self._scene.addItem(self.aa_point_drawing)

        rr, cc = circle(pos.y(), pos.x(), rad, shape=self.mask_aa_base.shape)
        if self.FG_add == True:
            self.mask_aa_base[rr, cc] = cv2.GC_FGD
        else:
            self.mask_aa_base[rr, cc] = cv2.GC_BGD
        return

    def aa_review_state_decider(self, pos):
        """
        This is used when we click with True for aa_tools to see if we improve the aa_annotation or we accept it

        """
        tmp_x = pos.x()
        tmp_y = pos.y()

        if (
            self.aa_tool_bb_first_x > self.last_bbox_x
            and self.aa_tool_bb_first_y > self.last_bbox_y
        ):
            # if point is in bounds in x and y
            if (
                self.aa_tool_bb_first_x > tmp_x > self.last_bbox_x
                and self.aa_tool_bb_first_y > tmp_y > self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                self.draw_on_aa_mask(pos)
            else:
                # we are not within bounds
                self.MainWindow.setCursor(
                    QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor)
                )

                self.aa_review_state = False
                # self.MainWindow.auto_annotate_tool.hide()
                self.Ui_control(lock_wdigets=False)
                self._scene.removeItem(self.bbox_drawing)
                self._scene.removeItem(self.previousAAsceneItem)
                self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)

        elif (
            self.aa_tool_bb_first_x > self.last_bbox_x
            and self.aa_tool_bb_first_y < self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x > tmp_x > self.last_bbox_x
                and self.aa_tool_bb_first_y < tmp_y < self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                self.draw_on_aa_mask(pos)
            else:
                # we are not within bounds
                self.aa_review_state = False
                self.Ui_control(lock_wdigets=False)
                # self.MainWindow.auto_annotate_tool.hide()
                self._scene.removeItem(self.bbox_drawing)
                self._scene.removeItem(self.previousAAsceneItem)
                print("aa out of bounds")
                self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)

        elif (
            self.aa_tool_bb_first_x < self.last_bbox_x
            and self.aa_tool_bb_first_y > self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x < tmp_x < self.last_bbox_x
                and self.aa_tool_bb_first_y > tmp_y > self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                self.draw_on_aa_mask(pos)
            else:
                print("aa out of bounds")

                # we are not within bounds
                self.aa_review_state = False
                self.Ui_control(lock_wdigets=False)
                # self.MainWindow.auto_annotate_tool.hide()

                self._scene.removeItem(self.bbox_drawing)
                self._scene.removeItem(self.previousAAsceneItem)
                self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)

        elif (
            self.aa_tool_bb_first_x < self.last_bbox_x
            and self.aa_tool_bb_first_y < self.last_bbox_y
        ):
            if (
                self.aa_tool_bb_first_x < tmp_x < self.last_bbox_x
                and self.aa_tool_bb_first_y < tmp_y < self.last_bbox_y
            ):
                # this means we are within bounds so we draw
                self.draw_on_aa_mask(pos)
            else:
                # we are not within bounds
                print("aa out of bounds")
                self.aa_review_state = False
                self.MainWindow.Ui_control(lock_wdigets=False)
                # self.MainWindow.auto_annotate_tool.hide()
                if hasattr(self, "bbox_drawing"):
                    if self.bbox_drawing:
                        self._scene.removeItem(self.bbox_drawing)
                        self._scene.removeItem(self.previousAAsceneItem)
                self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)

    def completeDrawing_Bounding_Box(self, MODE="clean"):
        if MODE == "clean":
            self.aa_review_state = False
            self.i_am_drawing_state_bbox = False
            self.during_drawing_bbox = False

            try:
                self._scene.removeItem(self.bbox_drawing)
            except:
                pass

    def completeDrawingPolygon(self, MODE="clean"):
        """
        If mode is clean then we delete all of the points,
        if mode is "complete" then we complete the drwaing by
        adding a last poing
        """
        import skimage

        self.i_am_drawing_state = False
        self.during_drawing = False
        self.makeAllGraphicItemsSelectable()
        for gitem in self.polygon_graphic_grip_items:
            # remove from scene
            self._scene.removeItem(gitem)
            # delete item
            del gitem
        if MODE == "clean":
            self.MainWindow.counter_tmp = 0
            self.MainWindow.temp_mask_to_use_Test_x = []
            self.MainWindow.temp_mask_to_use_Test_y = []
            self.MainWindow.first_x = -1
            self.MainWindow.first_y = -1
            # self.MainWindow.DH.masks_state_usr[self.MainWindow.current_imagenumber] =True
            self.MainWindow.worm_mask_points_x = []
            self.MainWindow.worm_mask_points_y = []
            self.MainWindow.i_am_drawing_state = False
            self.MainWindow.list_px = []
            self.MainWindow.list_py = []
            self._scene.removeItem(self.moving_line)
            for item in self.polyTmpItems:
                if item in self._scene.items():
                    self._scene.removeItem(item)
            self._scene.removeItem(self.startPointDrawingS)
            self._scene.removeItem(self.startPointDrawingL)
        elif MODE == "complete":
            self.MainWindow.temp_mask_to_use_Test_x = (
                self.MainWindow.temp_mask_to_use_Test_x[:-1]
            )
            self.MainWindow.temp_mask_to_use_Test_y = (
                self.MainWindow.temp_mask_to_use_Test_y[:-1]
            )
            self.MainWindow.worm_mask_points_x = self.MainWindow.temp_mask_to_use_Test_x
            self.MainWindow.worm_mask_points_y = self.MainWindow.temp_mask_to_use_Test_y
            # Add last element and point we are on now:

            self.MainWindow.worm_mask_points_x.append(self.MainWindow.prevx)
            self.MainWindow.worm_mask_points_y.append(self.MainWindow.prevy)

            if len(self.MainWindow.worm_mask_points_x) <= 3:
                self.completeDrawingPolygon()
                return

            self.QpolygonsSaved_Y = []
            self.QpolygonsSaved_X = []

            self.MainWindow.selected_mask_origin = "POLYGON"

            # Here we add the points to the global varible
            self.QpolygonsSaved_X = self.MainWindow.worm_mask_points_x.copy()
            self.QpolygonsSaved_Y = self.MainWindow.worm_mask_points_y.copy()

            tmpList1 = []
            outArrayBitMask = []
            tmpList1 = np.array(
                [
                    np.array(self.MainWindow.worm_mask_points_x),
                    np.array(self.MainWindow.worm_mask_points_y),
                ]
            ).T
            outArrayBitMask = tmpList1

            self.RemoveStartPolygonPoint()
            QtWidgets.QApplication.processEvents()
            if self.moving_line:
                self._scene.removeItem(self.moving_line)
            for item in self.polyTmpItems:
                if item in self._scene.items():
                    self._scene.removeItem(item)

            if self.ML_brush_tool_object_state == True:
                import skimage
                from celer_sight_ai import config

                image_object = (
                    self.MainWindow.DH.BLobj.groups["default"]
                    .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                    .images[self.MainWindow.current_imagenumber]
                )
                # create bitmap mask
                image_shape = [image_object.SizeX, image_object.SizeY]

                outMask = skimage.draw.polygon2mask(
                    image_shape, outArrayBitMask
                ).astype(bool)
                if self.ML_brush_tool_draw_foreground_add == True:
                    config.global_signals.addToML_Canvas_FG.emit(
                        [
                            self.MainWindow.current_imagenumber,
                            self.MainWindow.DH.BLobj.get_current_condition(),
                            outMask,
                        ]
                    )
                if self.ML_brush_tool_draw_background_add == True:
                    config.global_signals.addToML_Canvas_BG.emit(
                        [
                            self.MainWindow.current_imagenumber,
                            self.MainWindow.DH.BLobj.get_current_condition(),
                            outMask,
                        ]
                    )
                config.global_signals.update_ML_BitMapScene.emit()

            else:
                from celer_sight_ai import config

                config.global_signals.create_annotation_object_signal.emit(
                    {
                        "array": [tmpList1],
                        "image_uuid": self.MainWindow.DH.BLobj.get_current_image_uuid(),
                        "class_id": self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id,
                        "mask_type": "polygon",  # polygon by default
                    }
                )
                self.updateMaskCountLabel()

            self.MainWindow.counter_tmp = 0
            self.MainWindow.temp_mask_to_use_Test_x = []
            self.MainWindow.temp_mask_to_use_Test_y = []
            self.MainWindow.first_x = -1
            self.MainWindow.first_y = -1
            # self.MainWindow.DH.masks_state_usr[self.MainWindow.current_imagenumber] =True
            self.MainWindow.worm_mask_points_x = []
            self.MainWindow.worm_mask_points_y = []
            self.MainWindow.i_am_drawing_state = False

    def makeAllGraphicItemsNonSelectable(
        self, asIs=False, pointsOnly=False, cursor=None
    ):
        """
        iterate overa ll graphic items and make them non selectable
        """
        print(
            f"Making all graphic items non selectable with asIs={asIs} and pointsOnly={pointsOnly}"
        )
        print("---------")
        if not asIs:
            for item in self._scene.items():
                if type(item) == QtWidgets.QGraphicsPixmapItem:
                    if cursor != None:
                        item.setCursor(cursor)
                    continue
                if type(item) == PolygonAnnotation:
                    item.removeAllPoints()
                    item.canDetectChange = False
                item.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
                )
        else:
            for item in self._scene.items():
                if type(item) == QtWidgets.QGraphicsPixmapItem:
                    continue
                if type(item) == PolygonAnnotation:
                    if not item.pointsInited:
                        item.canDetectChange = False
                        item.setFlag(
                            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
                            False,
                        )
                    elif pointsOnly == True:
                        # item.canDetectChange = False
                        item.setFlag(
                            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
                            False,
                        )
                        item.setFlag(
                            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
                            False,
                        )
                        item.showInitedPoints()

    def makeAllGraphicItemsSelectable(self):
        """
        iterate overa ll graphic items and make them non selectable
        """
        for item in self._scene.items():
            if type(item) == QtWidgets.QGraphicsPixmapItem:
                continue
            if type(item) == PolygonAnnotation or type(item) == GripItem:
                item.canDetectChange = True
                item.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True
                )

    def onDeleteUpdateModifierPolygonAnnotation(self, PosDeleted):
        """
        when we deletea polygon annotation we update all the polygons above, their modfier -1
        """
        pass
        # for item in self._scene.items():
        #     if type(item) == PolygonAnnotation:
        #         if item.MaskPosition > PosDeleted:
        #             item.MaskPosition -= 1

    def RemoveStartPolygonPoint(self):
        self._scene.removeItem(self.startPointDrawingS)
        self._scene.removeItem(self.startPointDrawingL)

    def getDistanceValue(self, startX, startY, endX, endY):
        return np.linalg.norm(np.array([endX, endY]) - np.array([startX, startY]))

    def getDistance(self, startX, startY, endX, endY):
        """
        computes the manhatan distance between two points
        """

        distanceActual = np.linalg.norm(
            np.array([endX, endY]) - np.array([startX, startY])
        )
        if ((distanceActual * ((self._zoom / 10 + 1)))) <= (
            self.QuickTools.spinBoxPolygonTool.value() / 10
        ) + 10:
            return True
        else:
            return False

    def draw_polygon(self, pos, MODE=None):
        """
        This is the Polygon tool, it runs until the mask has been completed through the event filter
        its a faster version of the draw polygon tool and the one currently used
        """
        import time

        start = time.time()
        import cv2
        import numpy as np
        import skimage

        pen_width = 3
        if self.add_mask_btn_state == False:
            return
        # if self.selection_state == True:
        #     return
        if self.underMouse == False:
            return
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            return

        self.i_am_drawing_state = True
        self.during_drawing = False

        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.NoDrag:
            self.MainWindow.counter_tmp += 1
            self.MainWindow.temp_mask_to_use_Test_x.append(pos.x())
            self.MainWindow.temp_mask_to_use_Test_y.append(pos.y())

            c = self.MainWindow.custom_class_list_widget.classes[
                self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id
            ].color
            # self.MainWindow.custom_class_list_widget.currentItemWidget.

            # add a grip item at position
            self.gripItem = GripItem(None, None, c)
            self.gripItem.setPos(pos.x(), pos.y())
            self.gripItem.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
            )
            self.gripItem.update_annotations_color()
            self._scene.addItem(self.gripItem)
            self.polygon_graphic_grip_items.append(self.gripItem)

            # This is initiated right on the first click
            if self.MainWindow.counter_tmp == 1:
                self.makeAllGraphicItemsNonSelectable()
                if (
                    self.POLYGON_MODIFY_MODE != None
                    and len(self.polyPreviousSelectedItems) != 0
                ):
                    # for item self.polyPreviousSelectedItems
                    for item in self.polyPreviousSelectedItems:
                        if type(item) == PolygonAnnotation:
                            item.PassThroughClicks = True
                            item.setFlag(
                                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
                                False,
                            )
                            self.myPreviousPolygonAnnotationForEdit = item
                self.polyTmpItems = []

                self.MainWindow.list_py = []
                self.MainWindow.list_px = []
                self.MainWindow.first_x = pos.x()
                self.MainWindow.first_y = pos.y()
                self.MainWindow.prevx_first = pos.x()
                self.MainWindow.prevy_first = pos.y()

            if self.MainWindow.counter_tmp != 1:
                print("before np max")
                try:
                    if self.moving_line and self.moving_line in self._scene.items():
                        self._scene.removeItem(self.moving_line)
                except Exception as e:
                    logger.error(e)
                # self.MainWindow.line_drawing_1 = QtCore.QLineF(self.MainWindow.prevx,self.MainWindow.prevy, pos.x(), pos.y())
                self.PlacedLine = QtWidgets.QGraphicsLineItem(
                    self.MainWindow.prevx, self.MainWindow.prevy, pos.x(), pos.y()
                )
                pen = self.MainWindow.ColorPrefsViewer.getPen()
                pen.setCosmetic(True)
                self.PlacedLine.setPen(pen)
                self._scene.addItem(self.PlacedLine)
                self.polyTmpItems.append(self.PlacedLine)
                # self._scene.addLine(self.MainWindow.line_drawing_1, pen= self.MainWindow.ColorPrefsViewer.getPen())
                # self.MainWindow.img_for_mask_tmp = np.maximum(
                #     self.MainWindow.img_for_mask_tmp,
                #     self.MainWindow.img_for_mask_tmp_prev,
                # )
                print("after np max")

            if self.MainWindow.counter_tmp > 3:
                # counter more than 3
                print("before draw circle")
                # image_circle = np.zeros(
                #     (self.MainWindow.DH.BLobj.groups['default'].conds[self.MainWindow.DH.BLobj.get_current_condition()].getImage(self.MainWindow.current_imagenumber).shape[0]+30,
                #     self.MainWindow.DH.BLobj.groups['default'].conds[self.MainWindow.DH.BLobj.get_current_condition()].getImage(self.MainWindow.current_imagenumber).shape[1]+30),
                #     dtype= bool)
                # print("after draw circle")

                # rr_circle, cc_circle = circle(self.MainWindow.first_y,self.MainWindow.first_x,\
                #      10, shape = image_circle.shape)
                # image_circle[rr_circle, cc_circle] = True
                # image_circle2 = image_circle.astype(bool)
                # self.image_circle2 = image_circle2

                if (
                    self.getDistance(
                        self.MainWindow.first_x,
                        self.MainWindow.first_y,
                        pos.x(),
                        pos.y(),
                    )
                    == True
                ):
                    # remove last element
                    self._scene.removeItem(self.PlacedLine)
                    self.polyTmpItems.append(self.PlacedLine)
                    self.MainWindow.temp_mask_to_use_Test_x = (
                        self.MainWindow.temp_mask_to_use_Test_x[:-1]
                    )
                    self.MainWindow.temp_mask_to_use_Test_y = (
                        self.MainWindow.temp_mask_to_use_Test_y[:-1]
                    )
                    # rr, cc = skimage.draw.polygon(self.MainWindow.temp_mask_to_use_Test_y,self.MainWindow.temp_mask_to_use_Test_x, shape=image_circle.shape )
                    # self.MainWindow.img_for_mask_tmp[rr,cc] = True
                    self.MainWindow.worm_mask_points_x = (
                        self.MainWindow.temp_mask_to_use_Test_x
                    )
                    self.MainWindow.worm_mask_points_y = (
                        self.MainWindow.temp_mask_to_use_Test_y
                    )
                    self.myScene_worm_mask_points_x_slot = []
                    self.myScene_worm_mask_points_y_slot = []
                    # Add mask to Overview tab adn the AssetButtonListPolygon list

                    self.MainWindow.selected_mask_origin = "POLYGON"
                    if self.POLYGON_MODIFY_MODE == None:
                        # Here we add the points to the global varible
                        self.myScene_worm_mask_points_x_slot.append(
                            self.MainWindow.worm_mask_points_x.copy()
                        )
                        self.myScene_worm_mask_points_y_slot.append(
                            self.MainWindow.worm_mask_points_y.copy()
                        )

                        currentMaskPos = len(self.myScene_worm_mask_points_x_slot) - 1

                        tmpList1 = np.array(
                            [
                                np.array(
                                    self.myScene_worm_mask_points_x_slot[currentMaskPos]
                                ),
                                np.array(
                                    self.myScene_worm_mask_points_y_slot[currentMaskPos]
                                ),
                            ]
                        ).T

                        from celer_sight_ai import config

                        if self.ML_brush_tool_object_state == True:
                            outArrayBitMask = []
                            for p in range(len(self.MainWindow.worm_mask_points_y)):
                                outArrayBitMask.append(
                                    [
                                        self.MainWindow.worm_mask_points_y[p],
                                        self.MainWindow.worm_mask_points_x[p],
                                    ]
                                )
                            import skimage
                            from celer_sight_ai import config

                            # create bitmap mask
                            image_shape = (
                                self.MainWindow.DH.BLobj.groups["default"]
                                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                                .getImage(self.MainWindow.current_imagenumber)
                                .shape[0:2]
                            )

                            outMask = skimage.draw.polygon2mask(
                                image_shape, outArrayBitMask
                            ).astype(bool)

                            if self.ML_brush_tool_draw_foreground_add == True:
                                config.global_signals.addToML_Canvas_FG.emit(
                                    [
                                        self.MainWindow.current_imagenumber,
                                        self.MainWindow.DH.BLobj.get_current_condition(),
                                        outMask,
                                    ]
                                )
                            if self.ML_brush_tool_draw_background_add == True:
                                config.global_signals.addToML_Canvas_BG.emit(
                                    [
                                        self.MainWindow.current_imagenumber,
                                        self.MainWindow.DH.BLobj.get_current_condition(),
                                        outMask,
                                    ]
                                )
                            config.global_signals.update_ML_BitMapScene.emit()

                        else:
                            config.global_signals.create_annotation_object_signal.emit(
                                {
                                    "image_uuid": self.MainWindow.DH.BLobj.get_current_image_uuid(),
                                    "array": [tmpList1],
                                    "class_id": self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id,
                                    "mask_type": "polygon",  # polygon by default
                                }
                            )

                        self.RemoveStartPolygonPoint()
                        QtWidgets.QApplication.processEvents()

                        self.MainWindow.counter_tmp = 0
                        self.MainWindow.temp_mask_to_use_Test_x = []
                        self.MainWindow.temp_mask_to_use_Test_y = []
                        self.MainWindow.first_x = -1
                        self.MainWindow.first_y = -1
                        self.MainWindow.worm_mask_points_x = []
                        self.MainWindow.worm_mask_points_y = []
                        self.MainWindow.i_am_drawing_state = False

                        self._scene.removeItem(self.moving_line)
                        for item in self.polyTmpItems:
                            if item in self._scene.items():
                                self._scene.removeItem(item)
                        self.updateMaskCountLabel()
                        from celer_sight_ai import config

                    else:
                        itemSelected = self.myPreviousPolygonAnnotationForEdit
                        myPrevSelectedItem = itemSelected
                        myPolygon = itemSelected.PolRef

                        from celer_sight_ai.core.ML_tools import GetPointsFromQPolygonF

                        myPolygon2, boundingBox = GetPointsFromQPolygonF(myPolygon)
                        CImageRef = (
                            self.MainWindow.DH.BLobj.groups["default"]
                            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                            .getImage(self.MainWindow.current_imagenumber)
                        )

                        OutMask1 = skimage.draw.polygon2mask(
                            (CImageRef.shape[0], CImageRef.shape[1]), myPolygon2
                        )

                        # Here we add the points to the global varible
                        self.myScene_worm_mask_points_x_slot.append(
                            self.MainWindow.worm_mask_points_x.copy()
                        )
                        self.myScene_worm_mask_points_y_slot.append(
                            self.MainWindow.worm_mask_points_y.copy()
                        )

                        currentMaskPos = (
                            len(
                                self.MainWindow.DH.BLobj.groups["default"]
                                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                                .images[self.MainWindow.current_imagenumber]
                                .masks
                            )
                            - 1
                        )
                        tmpList1 = []
                        for p in range(
                            len(self.myScene_worm_mask_points_x_slot[currentMaskPos])
                        ):
                            tmpList1.append(
                                QtCore.QPointF(
                                    self.myScene_worm_mask_points_x_slot[
                                        currentMaskPos
                                    ][p],
                                    self.myScene_worm_mask_points_y_slot[
                                        currentMaskPos
                                    ][p],
                                )
                            )

                        tmpPolygon = QtGui.QPolygonF(tmpList1)

                        tmpPolygon2, boundingBox = GetPointsFromQPolygonF(tmpPolygon)

                        OutMask2 = skimage.draw.polygon2mask(
                            (CImageRef.shape[0], CImageRef.shape[1]), tmpPolygon2
                        )

                        if self.POLYGON_MODIFY_MODE == self.POLYGON_MODIFY_ADD:
                            finalMask = OutMask2 + OutMask1
                        else:
                            finalMaskTmp = np.bitwise_and(OutMask1, OutMask2)
                            finalMask = np.bitwise_xor(OutMask1, finalMaskTmp)
                        contours = skimage.measure.find_contours(finalMask, 0.8)
                        for i in range(len(contours)):
                            appr_hand = skimage.measure.approximate_polygon(
                                np.asarray(contours[i]), tolerance=2.2
                            ).astype(np.uint16)
                            listAllMasks = QtGui.QPolygonF(
                                [QtCore.QPointF(p[1], p[0]) for p in appr_hand]
                            )
                        from celer_sight_ai import config

                        config.global_signals.create_annotation_object_signal.emit(
                            {
                                "image_uuid": self.MainWindow.DH.BLobj.get_current_image_uuid(),
                                "array": [listAllMasks],
                                "class_id": self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id,
                                "mask_type": "polygon",  # polygon by default
                            }
                        )
                        # get condition uuid
                        treatment_uuid = (
                            self.MainWindow.DH.BLobj.get_current_condition().unique_id
                        )
                        image_uuid = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
                            self.MainWindow.current_imagenumber
                        ).unique_id
                        config.global_signals.MaskToSceneSignal.emit(
                            {
                                "image_uuid": self.MainWindow.current_imagenumber,
                                "mask_uuid": image_uuid.masks[-1].unique_id,
                                "mask_type": "polygon",
                            }
                        )

                        # self.MainWindow.load_main_scene(self.MainWindow.current_imagenumber)
                        # add Undo Stack
                        self.MainWindow.load_main_scene(
                            self.MainWindow.current_imagenumber
                        )

            self.MainWindow.prevx = pos.x()
            self.MainWindow.prevy = pos.y()
            self.MainWindow.list_px.append(pos.x())
            self.MainWindow.list_py.append(pos.y())

            return

    def draw_while_mouse_move(self, pos):
        # print("to hereo ok")
        # print(self.add_mask_btn_state , " " , self.i_am_drawing_state)
        if self.add_mask_btn_state == False:
            return
        if self.i_am_drawing_state == False:
            return

        if self.during_drawing == True:
            try:
                self._scene.removeItem(self.moving_line)
            except:
                return

        if self.MainWindow.counter_tmp > 2:
            if (
                self.getDistance(
                    self.MainWindow.first_x, self.MainWindow.first_y, pos.x(), pos.y()
                )
                == True
            ):
                self.moving_line = QtWidgets.QGraphicsLineItem(
                    self.MainWindow.first_x,
                    self.MainWindow.first_y,
                    self.MainWindow.prevx,
                    self.MainWindow.prevy,
                )
            else:
                self.moving_line = QtWidgets.QGraphicsLineItem(
                    self.MainWindow.prevx, self.MainWindow.prevy, pos.x(), pos.y()
                )
        else:
            self.moving_line = QtWidgets.QGraphicsLineItem(
                self.MainWindow.prevx, self.MainWindow.prevy, pos.x(), pos.y()
            )
        pen = self.MainWindow.ColorPrefsViewer.getPen()
        pen.setCosmetic(True)
        self.moving_line.setPen(pen)
        self._scene.addItem(self.moving_line)

        # self.viewer.update()
        self.during_drawing = True
        return


class SceneViewer(QtWidgets.QGraphicsScene):
    def __init__(self, viewer=None):
        super(SceneViewer, self).__init__()
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


class BitMapAnnotation(QtWidgets.QGraphicsPixmapItem):
    def __init__(
        self,
        MyParent=None,
        mask_object=None,
        bitmap_array=None,  # np.array
        class_id=None,
        unique_id=None,
    ):
        super(BitMapAnnotation, self).__init__()

        self.non_hover_opacity = 50
        self.hover_opacity = 120
        self.MyParent = MyParent
        self.mask_object = mask_object
        self.class_id = class_id
        self.is_particle = mask_object.is_particle
        if class_id:
            self.class_id = class_id

        self.class_name = self.MyParent.custom_class_list_widget.classes[
            class_id
        ].text()
        self.setZValue(14)  # above masks, below class label (15)
        self.colorToUseNow = self.get_mask_color()
        self.setAcceptHoverEvents(True)
        self.unique_id = unique_id  # unique id is the same as the unique mask id

        self.bitmap_array = bitmap_array
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, False)
        self.center_point_graphics_item = None
        self.class_graphics_item = None

        # ID of the mask
        self.Condition = self.MyParent.DH.BLobj.get_current_condition()
        self.imagenumber = self.MyParent.current_imagenumber

        # crete the polygon item
        self.set_bitmap()
        self.set_clip_elements()

    def check_if_class_is_visible(self):
        return self.MyParent.custom_class_list_widget.classes[
            self.class_id
        ]._is_class_visible

    def _apply_color_map(self, mask_array, color, max_opacity=0.8):
        rgba = np.zeros((mask_array.shape[0], mask_array.shape[1], 4), dtype=np.uint8)
        mask_array = mask_array
        rgba[:, :, 0] = color[0]  # * mask_array * max_opacity
        rgba[:, :, 1] = color[1]  # * mask_array * max_opacity
        rgba[:, :, 2] = color[2]  # * mask_array * max_opacity
        rgba[:, :, 3] = (mask_array * (color[3] / 100)).astype(np.uint8)
        # Alpha channel set by mask values
        # color[3] max is 100

        return rgba

    def update_annotations_color(self):
        self.set_bitmap()

    def is_particle(self):
        # Trace the class object and determine if current class
        # is a particles class
        return self.MyParent.custom_class_list_widget.classes[self.class_id].is_particle

    def get_mask_color(self):
        """
        If the class_name is in the dictionary of classes, then use the color from the dictionary, otherwise
        use the color from the button

        Args:
          class_name: the class id of the object you want to get the color for.

        Returns:
          The color of the mask.
        """
        colorToUseNow = self.MyParent.custom_class_list_widget.classes[
            self.class_id
        ].color
        return colorToUseNow

    def get_parent_class(self):
        self.parent_class_name = (
            self.MainWindow.CustomClassListWidget.get_parent_class_name_by_class_name(
                self.class_id
            )
        )

    def set_bitmap(self):
        # convert array to qimage to be used for the graphicsview pixmap

        height, width = self.bitmap_array.shape
        self.rect = QtCore.QRectF(0, 0, width, height)
        self.qimage_bitmap = QtGui.QImage(
            self._apply_color_map(self.bitmap_array.copy(), self.get_mask_color()).data,
            width,
            height,
            QtGui.QImage.Format.Format_RGBA8888,
        )

        self.pixmap_bitmap = QtGui.QPixmap.fromImage(self.qimage_bitmap)

        self.qimage_bitmap = self.pixmap_bitmap.toImage()

    # Need to reiplement this method for the overriden paint method
    def boundingRect(self):
        return self.rect

    def set_clip_elements(self):
        path_items = [
            item
            for item in self.MyParent.viewer.scene().items()
            if isinstance(item, PolygonAnnotation)
        ]
        # Combine all the paths
        self.combined_path = QtGui.QPainterPath()
        for item in path_items:
            self.combined_path = self.combined_path.united(item.path())

    def paint(self, painter: QtGui.QPainter, option, widget):
        # Mask the QImage using the combined path
        self.set_clip_elements()
        painter.setClipPath(self.combined_path)
        painter.drawImage(self.rect, self.qimage_bitmap, self.rect)
        return super(BitMapAnnotation, self).paint(painter, option, widget)


class PolygonAnnotation(QtWidgets.QGraphicsPathItem):
    canDetectChange = False

    def __init__(
        self,
        MyParent=None,
        image_uuid=None,
        polygon_array=None,
        class_id=None,
        unique_id=None,
        track_unique_id=None,  # this is the unique id of the track annotation
        is_suggested=False,
        score=1.0,
        _disable_spawn_extra_items=False,
    ):
        self.canDetectChange = False
        super(PolygonAnnotation, self).__init__()
        import uuid

        assert polygon_array is not None
        assert unique_id is not None

        ######################
        ##### PROPERTIES #####
        ######################
        self.image_uuid = image_uuid
        # Z values
        z_adjustment = MyParent.custom_class_list_widget.classes[
            class_id
        ].indentation  # indentetion of the mask
        self.on_click_zvalue = 3 + (z_adjustment * 4)
        self.point_zvalue = 18 + (z_adjustment * 4)
        self.non_selected_zvalue = 1 + (
            z_adjustment * 4
        )  # when the mask is not selected
        self.setZValue(self.non_selected_zvalue)
        self.hover_enter_zvalue = 2 + (
            z_adjustment * 4
        )  # when the mouse enters the mask
        self.canDetectChange = False

        # bbox in [x1, y1, x2, y2]
        self.bbox = None  # set when setting the array, used by boundingRect for faster rendering

        # opacities
        self.polygon_edge_multiplier = 6.5
        self.non_hover_opacity = 30
        self.hover_opacity = 80

        # points
        self.m_points = []
        self.hasPoints = False
        self.pointsInited = False
        self.pointsCreated = False
        self.polygon_array = []
        for i in range(len(polygon_array)):
            if isinstance(polygon_array[i], list):
                polygon_array[i] = np.asarray(polygon_array[i])
            self.polygon_array.append(polygon_array[i].squeeze())

        self.polygon_array = [
            i.squeeze() for i in polygon_array
        ]  # reference to DH Qpoints polygon

        # For suggested annotations
        self.set_is_suggested(is_suggested)
        self.score = score
        self._disable_spawn_extra_items = _disable_spawn_extra_items
        self.MyParent = MyParent
        self.myCPen = self.MyParent.ColorPrefsViewer.getPen(
            ForMask=True, class_id=class_id
        )
        self.setAcceptHoverEvents(True)
        self.unique_id = unique_id  # same as mask
        self.setPen(self.myCPen)  # , self.MyParent.ColorPrefsViewer.MaskWidth)
        self.class_name = self.MyParent.custom_class_list_widget.classes[
            class_id
        ].text()
        self.class_id = class_id

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        config.global_signals.update_annotations_color_signal.connect(
            self.update_annotations_color
        )

        # extra graphic items
        self.poly_hole_scene_items = []
        self.center_point_graphics_item = None
        self.class_graphics_text_item = None

        # ID of the mask
        self.Condition = self.MyParent.DH.BLobj.get_current_condition()
        self.imagenumber = self.MyParent.current_imagenumber
        self.unique_id = unique_id

        # Track attributes
        self.track_unique_id = track_unique_id

        # create the polygon item and delete if no parent class annotation
        # with overlapping iou
        self.update_with_hierarchical_annotation()

        # holder for GripItem objects
        self.m_items = []

        self.PosModifier = 0  # for when we had deleted masks above the current position
        # we can see the points either way with passthroughclicks
        self.PassThroughClicks = False

        self.setCacheMode(
            QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache
        )  # DeviceCoordinateCache) ItemCoordinateCache
        self.fast_cache_mode = False
        if not self.check_if_class_is_visible():
            self.set_visible_all(False)

    def set_fast_cache_mode(self, mode=True):
        """
        Sets the cache mode for the polygon annotation item
        If there are a lot of annotation items, high caching is prefered.
        """
        if mode == self.fast_cache_mode:
            return
        elif mode == True:

            self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache)
            self.fast_cache_mode = True
        else:
            self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache)
            self.fast_cache_mode = False

    def set_is_suggested(self, is_suggested):
        self.is_suggested = is_suggested
        if not self.is_suggested:
            self.score = 1.0
            self.canDetectChange = True
        else:
            self.canDetectChange = False

    def set_visible_all(self, mode=True):
        self.setVisible(mode)
        if self.class_graphics_text_item:
            self.class_graphics_text_item.setVisible(mode)
        if self.center_point_graphics_item:
            self.center_point_graphics_item.setVisible(mode)
        for item in self.poly_hole_scene_items:
            item.setVisible(mode)

    def check_if_class_is_visible(self):
        return self.MyParent.custom_class_list_widget.classes[
            self.class_id
        ]._is_class_visible

    def set_disable_spawn_extra_items_variable(self, value):
        # Updates the polygon graphics item to remove or add the extra annotation items
        # These items are text and a circle in the cetner of the annotaiton region
        # On large image with multiple annotations, these are ommited as its expensive to rerender
        # And keep their transformations constant to zoom (custom cosmetics)
        if value == self._disable_spawn_extra_items:
            return
        self._disable_spawn_extra_items = value
        # update the polygon annotation
        self.update_annotation()

    def update_annotations_color(self):
        # updates the annotation color and opacity from the class properties

        opacity_value = self.MyParent.pg1_settings_mask_opasity_slider.value() / 100
        opacity_value = int(self.non_hover_opacity * opacity_value)

        ### Set the opacity of the polygon annotation

        # get current pen
        color = self.get_mask_color()
        pen = self.pen()
        # set opacity
        pen.setColor(
            QtGui.QColor(
                color[0],
                color[1],
                color[2],
                int(min(opacity_value * self.polygon_edge_multiplier, 255)),
            )
        )
        # set pen
        self.setPen(pen)
        # get current brush
        brush = self.brush()
        # set opacity
        brush.setColor(
            QtGui.QColor(
                color[0],
                color[1],
                color[2],
                opacity_value,
            )
        )
        # set brush
        self.setBrush(brush)

        ### set the opacity of the center point

        if self.center_point_graphics_item:
            self.center_point_graphics_item.setOpacity(opacity_value)
        for p in self.m_items:
            p.update_annotations_color(color)
        for h in self.poly_hole_scene_items:
            h.update_annotations_color(color)
        if self.center_point_graphics_item:
            self.center_point_graphics_item.update_annotations_color(color)
        if self.class_graphics_text_item:
            self.class_graphics_text_item.update_annotations_color(color)

    @staticmethod
    def array2d_to_qpolygonf(np_array=None):
        """
        Utility function to convert two 1D-NumPy arrays representing curve data
        (X-axis, Y-axis data) into a single polyline (QtGui.PolygonF object).
        This feature is compatible with PyQt4, PyQt5 and PySide2 (requires QtPy).

        License/copyright: MIT License © Pierre Raybaut 2020-2021.

        :param numpy.ndarray xdata: 1D-NumPy array
        :param numpy.ndarray ydata: 1D-NumPy array
        :return: Polyline
        :rtype: QtGui.QPolygonF
        """
        if isinstance(np_array, list):
            np_array = np.array(np_array)
        xdata, ydata = np_array.T
        if not (xdata.size == ydata.size == xdata.shape[0] == ydata.shape[0]):
            xdata = xdata.squeeze()
            ydata = ydata.squeeze()
        if not (xdata.size == ydata.size == xdata.shape[0] == ydata.shape[0]):
            raise ValueError("Arguments must be 1D NumPy arrays with same size")
        size = xdata.size
        item_size = 8
        polyline = QtGui.QPolygonF([QtCore.QPointF(0, 0)] * size)

        buffer = polyline.data()
        buffer.setsize(
            (item_size * 2) * size
        )  # 16 bytes per point: 8 bytes per X,Y value (float64)
        memory = np.frombuffer(buffer, np.float64)
        memory[: (size - 1) * 2 + 1 : 2] = np.array(xdata, dtype=np.float64, copy=False)
        memory[1 : (size - 1) * 2 + 2 : 2] = np.array(
            ydata, dtype=np.float64, copy=False
        )
        return polyline

    def update_annotation(self):
        self.setPolygon(self.polygon_array)

    def update_with_hierarchical_annotation(self):
        """
        Update the polygon annotation with hierarchical mask data.

        This method retrieves the hierarchical mask for the current annotation
        and updates the polygon accordingly. If the hierarchical mask cannot be
        retrieved or is empty, the annotation is deleted.
        """
        # Get current image object
        img_obj = self.MyParent.DH.BLobj.get_image_object_by_uuid(self.image_uuid)

        try:
            hierarchical_polygon = img_obj.get_hierarchical_mask(
                mask_uuid=self.unique_id
            )
        except Exception as e:
            logger.error(f"Error retrieving hierarchical mask: {e}")
            config.global_signals.notificationSignal.emit(
                "Error retrieving ROI's hierachy, deleting ROI."
            )
            self._delete_current_mask()
            return

        if hierarchical_polygon:
            self.setPolygon(hierarchical_polygon)
        else:
            config.global_signals.notificationSignal.emit(
                "No parent ROI found, deleting ROI."
            )
            self._delete_current_mask()

    def _delete_current_mask(self):
        """
        Helper method to delete the current mask annotation.
        """
        config.global_signals.deleteMaskFromMainWindow.emit(
            {
                "image_uuid": self.image_uuid,
                "mask_uuid": self.unique_id,
                "class_id": self.class_id,
            }
        )

    def get_mask_color(self):
        """
        If the class_id is in the dictionary of classes, then use the color from the dictionary, otherwise
        use the color from the button

        Args:
          class_id: the class id of the object you want to get the color for.

        Returns:
          The color of the mask.
        """
        colorToUseNow = self.MyParent.custom_class_list_widget.classes[
            self.class_id
        ].color

        return colorToUseNow

    def boundingRect(self):
        if self.bbox is None:
            return QtCore.QRectF(0, 0, 0, 0)
        return QtCore.QRectF(
            self.bbox[0],
            self.bbox[1],
            self.bbox[2] - self.bbox[0],
            self.bbox[3] - self.bbox[1],
        )

    def setPolygon(self, polygon):
        path = QtGui.QPainterPath()
        np_polygon_0 = np.array(polygon[0])
        self.bbox = [
            int(np.min(np_polygon_0[:, 0])),
            int(np.min(np_polygon_0[:, 1])),
            int(np.max(np_polygon_0[:, 0])),
            int(np.max(np_polygon_0[:, 1])),
        ]
        if len(polygon) > 0:
            p_arr = self.array2d_to_qpolygonf(np_polygon_0)
            if p_arr:
                path.addPolygon(p_arr)
                path.closeSubpath()
            else:
                return
        if len(polygon) > 1:
            # Subtract the hole polygons from the main path
            for h in range(1, len(polygon)):
                p_arr = self.array2d_to_qpolygonf(polygon[h])
                if p_arr:
                    sub_path = QtGui.QPainterPath()
                    sub_path.addPolygon(p_arr)
                    sub_path.closeSubpath()
                    path = path.subtracted(sub_path)

        self.setPath(path)
        colorToUseNow = self.get_mask_color()
        somepen = QtGui.QPen(
            QtGui.QColor(
                colorToUseNow[0],
                colorToUseNow[1],
                colorToUseNow[2],
                int(
                    self.non_hover_opacity
                    * self.polygon_edge_multiplier
                    * (self.MyParent.pg1_settings_mask_opasity_slider.value() / 100),
                ),
            )
        )
        somepen.setWidth(
            self.MyParent.viewer.QuickTools.lineWidthSpinBoxPolygonTool.value()
        )
        somepen.setCapStyle(
            self.MyParent.ColorPrefsViewer.MyStyles[
                self.MyParent.ColorPrefsViewer.CurrentPenCapStyle
            ]
        )
        somepen.setStyle(
            self.MyParent.ColorPrefsViewer.MyStyles[
                self.MyParent.ColorPrefsViewer.CurrentPenStyle
            ]
        )
        somepen.setCosmetic(True)  # so that stroke is always constant
        self.setPen(somepen)
        brush = QtGui.QBrush(
            QtGui.QColor(
                colorToUseNow[0],
                colorToUseNow[1],
                colorToUseNow[2],
                int(
                    self.non_hover_opacity
                    * (self.MyParent.pg1_settings_mask_opasity_slider.value() / 100)
                ),
            )
        )
        self.setBrush(brush)
        if (not self.is_suggested) and not self._disable_spawn_extra_items:
            p = self.get_point_inside_polygon(np_polygon_0)
            self.center_point = self.mapToScene(QtCore.QPointF(p.x, p.y))
            # Create a circle item and add it to the scene
            self.center_point_graphics_item = CenterCircleGraphicsItem(
                5.7, self.center_point.x(), self.center_point.y(), colorToUseNow
            )  # Change the rectangle to position and size your circle
            # Create a text item and add it to the scene
            if self.track_unique_id:
                text = (
                    self.class_name
                    + " "
                    + str(config.track_annotation_map.get(self.track_unique_id))
                )
            else:
                text = self.class_name
            # Name of the class on the scene
            self.class_graphics_text_item = ClassGraphicsTextItem(
                text,
                self.center_point.x(),
                self.center_point.y(),
                colorToUseNow,
            )  # Change "Sample text" to your desired text
        else:
            # For suggested annotations, make them non-hover non-selectable and non clickable
            self.setAcceptHoverEvents(False)
            self.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
            )
            self.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False
            )

    def get_graphic_scene_items(self):
        """adds all graphic items related to this single annotation
        In this case they are:
        1. the polygon
        2. the center point
        3. the class text
        """
        return [
            i
            for i in [
                self,
                self.center_point_graphics_item,
                self.class_graphics_text_item,
            ]
            if i
        ]

    def get_point_inside_polygon(self, coordinates):
        # this function gets a cutout of the array, and creates a mask that is then skeletonized
        # to find the center point of the skeleton
        if isinstance(coordinates, np.ndarray):
            if len(coordinates.shape):
                coordinates = coordinates.squeeze()
        polygon = Polygon(coordinates)
        return polygon.representative_point()

    def paint(self, painter, option, widget):
        option.state &= ~QtWidgets.QStyle.StateFlag.State_Selected
        super(PolygonAnnotation, self).paint(painter, option, widget)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            event.ignore()
        return super(PolygonAnnotation, self).eventFilter(source, event)

    def FindPosAtList(self, ListToIndex):
        """
        Required for custom index operation
        """
        for i in range(len(ListToIndex)):
            if self == ListToIndex[i]:
                return i
        return -1

    def DeleteMask(self, action=None):
        """
        From Context menu deletes Self and all_worm_mask_points_x_slot, mask_RNAi_slots, all_masks,mask_RNAi_slots_QPoints
        """

        masks = (
            self.MyParent.DH.BLobj.groups["default"]
            .conds[self.MyParent.DH.BLobj.get_current_condition()]
            .images[self.MyParent.current_imagenumber]
            .get_by_uuid(self.unique_id)
        )
        if masks:

            config.global_signals.deleteMaskFromMainWindow.emit(
                {
                    "mask_uuid": self.unique_id,
                }
            )

        if self in self.MyParent.viewer.sceneItemsListUndo:
            self.MyParent.viewer.sceneItemsListUndo.remove(self)
        self.MyParent.viewer._scene.removeItem(self)
        self.MyParent.viewer.updateMaskCountLabel()
        self.removeAllPoints()
        # remove text and bounding box
        if self.center_point_graphics_item:
            self.MyParent.viewer._scene.removeItem(self.center_point_graphics_item)
        if self.class_graphics_text_item:
            self.MyParent.viewer._scene.removeItem(self.class_graphics_text_item)

    def DeleteTrack(self):
        # delete tracks  from all images
        config.global_signals.deleteTrackFromMainWindow.emit(
            {
                "treatment_uuid": self.MyParent.DH.BLobj.get_current_condition_uuid(),
                "track_unique_id": self.track_unique_id,
                "class_id": self.class_id,
            }
        )
        self.cleanup_scene_items()

    def cleanup_scene_items(self):
        """
        Clean up all scene items associated with this polygon annotation.
        """
        # Remove the polygon itself from the scene
        if self in self.MyParent.viewer.sceneItemsListUndo:
            self.MyParent.viewer.sceneItemsListUndo.remove(self)
        self.MyParent.viewer._scene.removeItem(self)

        # Remove all grip points
        self.removeAllPoints()

        # Remove center point if it exists
        if (
            hasattr(self, "center_point_graphics_item")
            and self.center_point_graphics_item
        ):
            self.MyParent.viewer._scene.removeItem(self.center_point_graphics_item)
            self.center_point_graphics_item = None

        # Remove class text if it exists
        if hasattr(self, "class_graphics_text_item") and self.class_graphics_text_item:
            self.MyParent.viewer._scene.removeItem(self.class_graphics_text_item)
            self.class_graphics_text_item = None

        # Update the mask count label
        self.MyParent.viewer.updateMaskCountLabel()

    def initPoints(self):
        """
        Initiates all points at the begining
        """
        logger.debug("init all points start")
        iterator = 0
        self.m_items = []
        self.MyParent.blockSignals(True)
        self.setZValue(self.on_click_zvalue)
        # get color
        c = self.get_mask_color()
        # make sure there are no other polygon objects selected in the scene other than self
        for item in self.MyParent.viewer.scene().selectedItems():
            if isinstance(item, PolygonAnnotation):
                if item != self:
                    item.setSelected(False)
                    # remove points
                    item.removeAllPoints()

        for m in range(len(self.polygon_array)):
            # for every mask -> [main polygon , hole1, hole2, ...]
            for point in self.polygon_array[m]:
                item = GripItem(self, iterator, c)  # set color
                item.setZValue(self.point_zvalue)

                self.m_items.append(item)
                item.setPos(QtCore.QPointF(point[0], point[1]))
                item.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
                    True,
                )
                item.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations,
                    True,
                )
                iterator += 1

        # poly_items = [i for i in self.polygon()]
        # self.update_annotation()

        # print("init all points end")
        # self.removeAllPoints()

        # Needs to be here to not invoke selection when we create points

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True
        )
        self.MyParent.blockSignals(False)
        return

    def showInitedPoints(self):
        """
        shows all of the points that have been created
        """
        if self.pointsInited is False:
            for itemPoint in self.m_items:
                self.scene().addItem(itemPoint)
                if self.canDetectChange is False:
                    itemPoint.canDetectChange = True
        self.pointsInited = True

    def number_of_points(self):
        return len(self.m_items)

    def removeAllPoints(self):
        # try:
        if hasattr(self, "pointsInited") and self.pointsInited is True:
            for itemPoint in self.m_items:
                if itemPoint in self.MyParent.viewer._scene.items():
                    self.MyParent.viewer._scene.removeItem(itemPoint)
        self.pointsInited = False
        return

    def get_modified_index(self, point_pos):
        cumulative_len = 0
        for i, arr in enumerate(self.polygon_array):
            if cumulative_len <= point_pos < cumulative_len + len(arr):
                return i, point_pos - cumulative_len
            cumulative_len += len(arr)
        raise ValueError("Point position out of range")

    def movePoint(self, i, p):
        # i -> index of self.m_items, which should be the same as self.polygon_array
        arr_id, new_idx = self.get_modified_index(i)
        p_map = self.mapFromScene(p)
        # Update the array holding polygon points
        self.MyParent.DH.BLobj.groups["default"].conds[self.Condition].images[
            self.imagenumber
        ].masks[self.unique_id].update_point(
            point_pos=new_idx,
            new_value=np.array([p_map.x(), p_map.y()]),
            array_pos=arr_id,
        )  # point_pos=None, new_value=None, array_pos=None

    def move_item(self, index, pos):
        print("move item Polygon")
        if 0 <= index < len(self.m_items):
            item = self.m_items[index]
            item.setEnabled(False)
            item.setPos(pos)
            item.setEnabled(True)

    def spawn_polygon_holes(self):
        if len(self.polygon_array) > 0:
            color = self.get_mask_color()
            for h in range(1, len(self.polygon_array)):
                self.poly_hole_scene_items.append(
                    HoleAnnotationItem(self, self.polygon_array[h], h, color)
                )
                # add it to the viewer scene
                self.MyParent.viewer.scene().addItem(self.poly_hole_scene_items[-1])

    def despawn_polygon_holes(self):
        for item in self.poly_hole_scene_items:
            self.MyParent.viewer.scene().removeItem(item)
        self.poly_hole_scene_items = []
        self.setZValue(self.non_selected_zvalue)

    def itemChange(self, change, value):
        try:
            if self.canDetectChange is True:
                # print("selected items are", self.MyParent.viewer._scene.selectedItems())
                if (
                    change
                    == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemSelectedChange
                ):
                    if self.pointsCreated is False:
                        self.initPoints()
                        self.removeAllPoints()
                        self.pointsCreated = True
                    # we can see the points either way with passthroughclicks
                    if not self.isSelected() or self.PassThroughClicks is True:
                        self.showInitedPoints()
                        # spawn all polygon holes
                        self.spawn_polygon_holes()
                        self.setPolygon(self.polygon_array)

                    elif (
                        self.isSelected()
                        and self.MyParent.viewer.MAGIC_BRUSH_STATE is False
                    ):
                        self.removeAllPoints()
                        self.despawn_polygon_holes()
                        self.update_with_hierarchical_annotation()
                        # make sure this annotation is cropped through hierarchy

            else:
                self.removeAllPoints()
        except Exception as e:
            logger.error("PolygonAnnotation itemChange error: {}".format(e))
            # log traceback
            import traceback

            logger.error(traceback.format_exc())
        return super(PolygonAnnotation, self).itemChange(change, value)

    def contextMenuEvent(self, event):
        """
        Conetext menu for masks that runs on right click
        """
        menu = QtWidgets.QMenu()

        self.DeleteAction = QtGui.QAction("Delete", None)
        self.DeleteAction.triggered.connect(self.DeleteMask)
        # if annotation is track add delete track option
        if hasattr(self, "track_unique_id") and self.track_unique_id:
            self.DeleteTrackAction = QtGui.QAction("Delete Track", None)
            self.DeleteTrackAction.triggered.connect(self.DeleteTrack)
            menu.addAction(self.DeleteTrackAction)
        menu2 = QtWidgets.QMenu("Assign Class")
        ActionList = []
        ii = 0
        for i in range(self.MyParent.custom_class_list_widget.count()):
            if self.MyParent.custom_class_list_widget.item(i).isHidden() == True:
                continue
            class_name = self.MyParent.custom_class_list_widget.getItemWidget(i).text()
            class_id = self.MyParent.custom_class_list_widget.getItemWidget(i).unique_id
            ActionList.append(QtGui.QAction(class_name, None))

            ActionList[ii].triggered.connect(
                lambda _, b=(class_id): self.MyParent.DH.BLobj.groups["default"]
                .conds[self.MyParent.DH.BLobj.get_current_condition()]
                .images[self.MyParent.current_imagenumber]
                .change_class(self.unique_id, b)
            )
            ActionList[ii].triggered.connect(
                lambda: config.global_signals.load_main_scene_signal.emit()
            )

            menu2.addAction(ActionList[ii])
            ii += 1

        menu.addMenu(menu2)
        menu.addAction(self.DeleteAction)
        menu.exec(event.screenPos())

    def AssignTextToAssetMask(self, Mask=None, text=None):
        try:
            self.MyParent.DH.AssetMaskDictionary[
                self.MyParent.DH.BLobj.get_current_condition()
            ][self.MyParent.current_imagenumber][Mask].RegionAttribute = text
            self.MyParent.DH.AssetMaskDictionary[
                self.MyParent.DH.BLobj.get_current_condition()
            ][self.MyParent.current_imagenumber][
                Mask
            ].BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                text
            )
            self.MyParent.load_main_scene(self.MyParent.current_imagenumber)
        except:
            del self.MyParent.DH.mask_RNAi_slots_QPoints[
                self.MyParent.DH.BLobj.get_current_condition()
            ][self.MyParent.current_imagenumber][Mask]
            self.MyParent.load_main_scene(self.MyParent.current_imagenumber)

    def mousePressEvent(self, event):
        self.startingPosX = self.pos().x()
        self.startingPosY = self.pos().y()
        self.MyParent.viewer.polyPreviousSelectedItems.append(self)
        return super(PolygonAnnotation, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.endingPosX = self.pos().x()
        self.endingPosY = self.pos().y()
        return super(PolygonAnnotation, self).mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        # make sure current class exists (sometimes due to asyncronus deletion
        # it might no exist anymore)
        if (
            self.MyParent.DH.BLobj.get_current_condition()
            in self.MyParent.DH.BLobj.groups["default"].conds.keys()
        ):
            color = self.get_mask_color()
            # get brush
            brush = self.brush()
            brush.setColor(
                QtGui.QColor(
                    color[0],
                    color[1],
                    color[2],
                    min(
                        int(self.hover_opacity * (color[3] / 100)),
                        255,
                    ),
                )
            )
            self.setBrush(brush)
            # set pen brighter
            pen = self.pen()
            pen.setColor(
                QtGui.QColor(
                    pen.color().red(),
                    pen.color().green(),
                    pen.color().blue(),
                    int(
                        min(
                            self.hover_opacity
                            * self.polygon_edge_multiplier
                            * (color[3] / 100),
                            255,
                        ),
                    ),
                )
            )
            self.setPen(pen)
            self.setZValue(self.hover_enter_zvalue)
            self.setFocus()

        return super(PolygonAnnotation, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        color = self.get_mask_color()
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(
                    color[0],
                    color[1],
                    color[2],
                    int(self.non_hover_opacity * (color[3] / 100)),
                )
            )
        )
        # restore pen color
        pen = self.pen()
        pen.setColor(
            QtGui.QColor(
                color[0],
                color[1],
                color[2],
                int(
                    min(
                        self.non_hover_opacity
                        * self.polygon_edge_multiplier
                        * (color[3] / 100),
                        255,
                    ),
                ),
            )
        )
        self.setPen(pen)

        # if self is selected
        if self.isSelected():
            self.setZValue(self.on_click_zvalue)
        else:
            self.setZValue(self.non_selected_zvalue)
        return super(PolygonAnnotation, self).hoverLeaveEvent(event)


class HoleAnnotationItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, annotation_item, hole_array, array_index=None, color=None):
        super().__init__()
        self.array_index = array_index
        self.hole_array = hole_array
        self.annotation_item = annotation_item
        # set brush to dark gray
        self.setAcceptHoverEvents(True)
        # class_name = (
        #     self.annotation_item.MyParent.DH.BLobj.groups["default"]
        #     .conds[self.annotation_item.MyParent.DH.BLobj.get_current_condition()]
        #     .images[self.annotation_item.MyParent.current_imagenumber]
        #     .get_by_uuid(self.annotation_item.unique_id)
        #     # The above code is setting the alpha value of a brush color to 255, which means the color is
        #     # fully opaque. The brush color is defined as white with RGB values of 255, 255, 255.
        #     .class_id
        # )
        self.my_brush = self.brush()
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.color.setAlpha(125)
        self.my_brush.setColor(self.color)
        self.my_brush.setStyle(QtCore.Qt.BrushStyle.BDiagPattern)
        # self.brush.setAlpha(QtGui.QColor(255, 255, 255, 255))
        self.setBrush(self.my_brush)
        # set an empty pen
        self.setPen(QtGui.QPen(QtCore.Qt.PenStyle.NoPen))
        path = QtGui.QPainterPath()
        path.addPolygon(self.annotation_item.array2d_to_qpolygonf(self.hole_array))
        path.closeSubpath()
        self.setPath(path)
        self.setZValue(1)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def update_annotations_color(self, color):
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.my_brush.setColor(color)
        self.setBrush(self.my_brush)

    def hoverEnterEvent(self, event):
        # make sure current class exists (sometimes due to asyncronus deletion
        # it might no exist anymore)
        if self.my_brush:
            self.color = self.my_brush.color()
            self.color.setAlpha(125)
            self.my_brush.setColor(self.color)
            self.setFocus()
        return super(HoleAnnotationItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.color = self.my_brush.color()
        self.color.setAlpha(255)
        self.my_brush.setColor(self.color)
        return super(HoleAnnotationItem, self).hoverLeaveEvent(event)

    def delete_hole(self):
        config.global_signals.delete_hole_from_mask_signal.emit(
            [
                self.array_index,
                self,
                self.annotation_item.MyParent.current_imagenumber,  #  image id
                self.annotation_item.MyParent.DH.BLobj.get_current_condition(),  #  condition id
                self.annotation_item.unique_id,  #  annotation id (same as mask object)
                self.annotation_item.MyParent.DH.BLobj.groups["default"]
                .conds[self.annotation_item.MyParent.DH.BLobj.get_current_condition()]
                .images[self.annotation_item.MyParent.current_imagenumber]  # class id
                .get_by_uuid(self.annotation_item.unique_id)
                .class_id,
            ]
        )

    def contextMenuEvent(self, event):
        """
        Conetext menu for masks that runs on right click
        """
        menu = QtWidgets.QMenu()

        self.DeleteAction = QtGui.QAction("Delete hole", None)
        self.DeleteAction.triggered.connect(self.delete_hole)
        menu.addAction(self.DeleteAction)
        menu.exec(event.screenPos())


class ClassGraphicsTextItem(QtWidgets.QGraphicsItem):
    def __init__(self, text, x, y, box_color):
        super().__init__()
        self.text = text
        self.color = QtGui.QColor(
            int(box_color[0] * 0.75), int(box_color[1] * 0.75), int(box_color[2] * 0.75)
        )
        self.x = x
        self.y = y
        self.setZValue(15)
        self.my_pen = QtGui.QPen(self.color)
        self.my_brush = QtGui.QBrush(self.color)
        self.font = QtGui.QFont()

    def boundingRect(self):
        scale = self.scene().views()[0].transform().m11()
        self.font.setPixelSize(int(13.5 / scale))
        fm = QtGui.QFontMetricsF(self.font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()

        return QtCore.QRectF(
            0,
            0,
            text_width * 1.3,
            text_height * 1.3,
        )

    def update_annotations_color(self, color):
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.my_pen.setColor(self.color)
        self.my_brush.setColor(self.color)
        self.update()

    def paint(self, painter, option, widget=None):
        scale = self.scene().views()[0].transform().m11()
        self.setPos(QtCore.QPointF(self.x + (16 / scale), self.y - (9 / scale)))

        self.my_pen.setWidthF(1 / scale)
        painter.setPen(self.my_pen)
        # get brush

        painter.setBrush(self.my_brush)

        self.font = painter.font()
        self.font.setPixelSize(int(13.5 / scale))
        painter.setFont(self.font)

        fm = QtGui.QFontMetricsF(self.font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()
        # Draw the bounding rectangle with rounded corners
        rect = QtCore.QRectF(
            0,
            0,
            (text_width * 1.3),
            (text_height * 1.3),
        )

        painter.drawRoundedRect(rect, 5 / scale, 5 / scale)

        painter.setPen(QtGui.QColor("white"))  # Set text color
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.text)


class CenterCircleGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, radius, x, y, color):
        super().__init__()
        self.radius = radius
        self.setPos(QtCore.QPointF(x, y))
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.setZValue(15)
        self.my_pen = QtGui.QPen(self.color)
        self.my_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))

    def boundingRect(self):
        scale = self.scene().views()[0].transform().m11()
        # The bounding rectangle will be a square with sides of length 2*radius
        return QtCore.QRectF(
            -self.radius / scale,  # x
            -self.radius / scale,  # y
            2 * self.radius / scale,  # width
            2 * self.radius / scale,  # height
        )

    def paint(self, painter, option, widget=None):
        scale = self.scene().views()[0].transform().m11()

        self.my_pen.setWidthF(1.6 / scale)

        # set brush
        painter.setBrush(self.my_brush)
        painter.setPen(self.my_pen)
        painter.drawEllipse(
            QtCore.QPointF(0, 0), self.radius / scale, self.radius / scale
        )

    def update_annotations_color(self, color):
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.my_pen = QtGui.QPen(self.color)
        self.update()


class GripItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, annotation_item=None, index=None, color=None):
        super(GripItem, self).__init__()
        self.is_being_created = True
        self.circle = QtGui.QPainterPath()
        self.circle.addEllipse(QtCore.QRectF(-3, -3, 7, 7))
        self.square = QtGui.QPainterPath()
        self.square.addEllipse(QtCore.QRectF(-4, -4, 9, 9))
        self.m_annotation_item = annotation_item
        self.m_index = index
        if annotation_item:
            self.setParentItem(annotation_item)
        self.setPath(self.circle)
        my_color = QtGui.QColor(color[0], color[1], color[2], 255)

        self.my_brush = QtGui.QBrush(QtGui.QColor(my_color.lighter(150)))

        self.setBrush(self.my_brush)
        self.my_pen = QtGui.QPen(QtGui.QColor(my_color.lighter(250)), 1)
        self.my_pen.setCosmetic(True)

        self.setPen(self.my_pen)
        self.setAcceptHoverEvents(True)
        self.setZValue(11)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # if self.m_annotation_item.MyParent.viewer.ui_tool_selection.selected_button == "magic_brush_move":
        #     self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False)
        self.magicMove = False  # indicates if its moved by magic brush
        self.is_being_created = False

    def mousePressEvent(self, event):
        if self.m_annotation_item:
            if self.m_annotation_item.MyParent.viewer.MAGIC_BRUSH_STATE:
                # propagate event to parent
                if self.m_annotation_item:
                    return self.m_annotation_item.mousePressEvent(event)
                # self.m_annotation_item.MyParent.viewer.mousePressEvent(event)

    def update_annotations_color(self, color=None):
        if not color:
            return
        my_color = QtGui.QColor(color[0], color[1], color[2], 255)
        self.my_brush = QtGui.QBrush(QtGui.QColor(my_color.lighter(150)))
        self.setBrush(self.my_brush)
        self.my_pen = QtGui.QPen(QtGui.QColor(my_color.lighter(250)), 1)
        self.my_pen.setCosmetic(True)
        self.setPen(self.my_pen)

    def itemChange(self, change, value):
        if self.m_annotation_item:
            if self.m_annotation_item.canDetectChange is True:
                if (
                    change
                    == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemSelectedChange
                ):
                    pass
                elif (
                    change
                    == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
                    and self.isEnabled()
                ):
                    if (
                        self.m_annotation_item.MyParent.viewer.sceneRubberband.isVisible()
                        == True
                    ):
                        self.m_annotation_item.MyParent.viewer.sceneRubberband.hide()
                        self.m_annotation_item.MyParent.viewer.firstRubberBandDrag = (
                            False
                        )
                    if value.isNull():
                        return super(GripItem, self).itemChange(change, value)
                    self.m_annotation_item.movePoint(self.m_index, value)
                    self.m_annotation_item.update_annotation()
        return super(GripItem, self).itemChange(change, value)


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
        print("setting radius to {}".format(radius))
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
