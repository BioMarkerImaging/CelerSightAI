import typing
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QButtonGroup,
    QLabel,
)
from celer_sight_ai.QtAssets.stylized_widget import StylableWidget
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from celer_sight_ai import config
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def read_all_experiment_cfgs(p=None):
    import json

    """
    Reads the contentds of the config file (json)
    """
    with open(p, "r") as f:
        cfg = json.load(f)
    return cfg


def validate_cfg(d: dict = {}) -> bool:
    """
    A valid class needs a classes key with a list of classes (dicts). Classes value is a list of classes.
    If any class contains children these need to be verified as well. Every class needs a class name.
    All classes need to be unqiue
    """
    classes = d.get("classes")
    if not classes:
        print("Did not find any classes")
        return False
    # make sure all classes are unqiue
    if len(classes) != len(set([c.get("class_name") for c in classes])):
        print("Some classes have the same name (not allowed)")
        return False

    if not "supercategory" in d:
        print("No supercategory found")
        return False
    for c in classes:
        if not validate_class_cfg(c):
            print("Could not validade child class")
            return False
    return True


def validate_class_cfg(d: dict = {}) -> bool:
    if not d.get("class_name"):
        print("No class name found")
        return False
    if not d.get("uuid"):
        print("No uuid found")
        return False
    if d.get("children_classes"):
        for item in d.get("children_classes"):
            if not validate_class_cfg(item):
                return False
    return True


def process_cfg_for_grid_button_image_selector(cfg) -> str:
    keywords = []
    if not cfg:
        return ""

    # get the key words if they exists
    # get all class values and their children values
    def get_all_keywords(d={}, keywords=[]):
        if isinstance(d, list):
            for item in d:
                get_all_keywords(item, keywords)
            return keywords
        elif not isinstance(d, dict):
            cn = d.get("class_name")
            if cn:
                keywords.append(d.get("class_name"))
            spc = d.get("supercategory")
            if spc:
                keywords.append(spc)
            kw = d.get("keywords")
            if kw:
                keywords.extend(kw)
            if d.get("children_classes"):
                return get_all_keywords(d.get("children_classes"), keywords)
            else:
                return keywords

    spc = cfg.get("supercategory")
    if spc:
        keywords.append(spc)
    txt = cfg.get("text")
    if txt:
        keywords.append(txt)

    keywords.extend(get_all_keywords(cfg["classes"]))
    return " ".join(keywords)


def gather_cfgs(supercategory: str | None = None) -> list:
    """
    Gets all configs on experiment_configs folder
    """
    import glob
    import os
    from celer_sight_ai import configHandle

    # get current parent / parent dir
    p = configHandle.getLocal()
    all_experiement_configs = []
    # configs are in two folders, one for local classes and one for cloud classes
    # local
    cloud_categories_path = os.path.join(p, config.CLOUD_CATEGORIES_FILE)

    if os.path.exists(cloud_categories_path):
        with open(cloud_categories_path, "r") as f:
            cloud_categories = json.load(f)
    else:
        cloud_categories = []
    # extend with classes
    all_experiement_configs.extend(cloud_categories)
    # get local experiement configs
    if os.path.exists(os.path.join(p, config.LOCAL_CATEGORIES_FILE)):
        with open(os.path.join(p, config.LOCAL_CATEGORIES_FILE), "r") as f:
            local_categories = json.load(f)
    else:
        local_categories = []
    # extend with local categories
    all_experiement_configs.extend(local_categories)
    # only keep valid configs
    all_cfg = [i for i in all_experiement_configs if validate_cfg(i)]

    # filter by supercategroy if provided
    if supercategory:
        all_cfg = [i for i in all_cfg if i.get("supercategory") == supercategory]
    return all_cfg


class SquareButton(QPushButton):
    # with_model_type_selection -> Pro or Lite

    def __init__(
        self,
        parent_main_button,
        cfg,
        size=250,
        parent=None,
        with_model_type_selection=True,
        display_text=True,  # New parameter to control text display
    ):
        super(SquareButton, self).__init__(parent)
        self.original_size = size  # Initialize original_size
        self.color = (255, 214, 0)
        from celer_sight_ai.QtAssets.pro_lite_model_toggle_component import (
            AnimatedToggleButton,
        )

        self.parent_main_button = parent_main_button
        self.radius_of_icon = 10
        self.is_valid = False
        self.display_text = display_text  # Store the display_text parameter
        try:

            self.text_item = cfg["text"]
            self.supercategory = cfg.get("supercategory")
            self.classes = [i["class_name"] for i in cfg.get("classes")]
            if not validate_cfg(cfg):
                self.is_valid = False
                return
        except Exception as e:
            logger.error(f"Could not read config {cfg} {e}")
            self.is_valid = False  # mark it so that its not added to the grid table

        self.is_valid = True
        self.ratio = self.screen().devicePixelRatio()  # * 2
        self.with_model_type_selection = with_model_type_selection

        self.cfg = cfg
        self.cfg_uuid = cfg.get("uuid")
        if not self.cfg_uuid:
            # use the first class uuid
            self.cfg_uuid = cfg["classes"][0]["uuid"]
        self.update_icon()

        self.size = int(size * self.ratio)
        self.setCheckable(True)
        self.toggled.connect(self.onToggleButton)

        # reise for the smallest side to be == size
        height, width = self.numpy_image.shape[:2]
        if height > width:
            scale = self.size / width
        else:
            scale = self.size / height
        self.setAutoExclusive(True)
        self.numpy_image = cv2.resize(self.numpy_image, None, fx=scale, fy=scale)
        # crop from the largest side to square
        self.numpy_image = self.numpy_image[: self.size, : self.size]
        if not isinstance(self.numpy_image, type(None)):
            self.numpy_image = cv2.resize(self.numpy_image, (self.size, self.size))
        # Set fixed size to the button
        self.setFixedSize(self.original_size, self.original_size)
        self.setStyleSheet(
            """
            border: 0px;
            background-color: transparent;
            """
        )
        if self.with_model_type_selection:
            self.model_button = AnimatedToggleButton(
                self, available_modes=["Pro", "Lite"]
            )

        self.setChecked(False)
        # self.button_pressed.connect(self.on_button_press)
        # self.button_pressed.connect(self.toggle)
        if not self.isChecked():
            self.set_normal_background()
        else:
            self.set_checked_background()
        self.uncheck_color = tuple([i // 2 for i in self.color])
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self.keywords = process_cfg_for_grid_button_image_selector(
            cfg
        )  # get all keywords for filtering

    def focusInEvent(self, event):
        # When this widget receives focus, set focus to the parent widget
        self.parent_main_button.setFocus()

    def focusOutEvent(self, event):
        # When this widget loses focus, ensure the parent widget has focus
        self.parent_main_button.setFocus()

    def mousePressEvent(self, event):
        # Prevent the button from being clicked, but focus the parent
        self.parent_main_button.setFocus()
        # When the mouse is pressed, set focus to the parent widget
        self.parent_main_button.setChecked(True)
        event.ignore()

    def update_icon(self):
        from celer_sight_ai import configHandle

        # open config
        if isinstance(self.cfg, str):  # can be a path or a str
            with open(self.cfg, "r") as f:
                # read json
                cfg = json.load(f)
        else:
            cfg = self.cfg
        image_data_folder = os.path.join(
            configHandle.getLocal(), "experiment_configs/category_image_cache"
        )
        # if "image" exists in the dict, its a user path to the image
        if cfg.get("image"):
            self.numpy_image = cv2.imread(cfg["image"])
            if isinstance(self.numpy_image, type(None)):
                return
            # bgr to rgb
            self.numpy_image = cv2.cvtColor(self.numpy_image, cv2.COLOR_BGR2RGB)
            return
        elif cfg.get("type") == "local" and not os.path.exists(
            os.path.join(image_data_folder, f"{self.cfg_uuid}.jpg")
        ):
            # needs local image to be generated locally
            config.categories_that_need_thumbnail.append(cfg)
            # case were image doesnt exists, so just create a blank image
            self.numpy_image = np.zeros((250, 250, 3), dtype=np.uint8)
        # if image doesnt exists, add the default image
        elif not os.path.exists(
            os.path.join(image_data_folder, f"{self.cfg_uuid}.jpg")
        ):
            self.numpy_image = np.zeros(
                [540, 540, 3], dtype=np.uint8
            )  # cv2.imread("data/icons/downloading_tmp_icon.png")
            # needs thumbnail to be generated for this class and sent to server
            config.categories_that_need_thumbnail.append(cfg)
        else:
            self.numpy_image = cv2.imread(
                os.path.join(image_data_folder, f"{self.cfg_uuid}.jpg")
            )
            if isinstance(self.numpy_image, type(None)):
                return
            # bgr to rgb
            if not isinstance(self.numpy_image, type(None)):
                self.numpy_image = cv2.cvtColor(self.numpy_image, cv2.COLOR_BGR2RGB)
        if isinstance(self.numpy_image, type(None)):
            # it means the image is not valid, delete it so that it gets redownloaded later
            os.remove(os.path.join(image_data_folder, f"{self.cfg_uuid}.jpg"))
            self.numpy_image = np.zeros(
                [540, 540, 3], dtype=np.uint8
            )  # cv2.imread("data/icons/downloading_tmp_icon.png")

    def onToggleButton(self, checked: bool):
        # check if any other button is checked
        if not self.isChecked():
            self.set_normal_background()
        else:
            self.set_checked_background()

    def set_checked_background(self):
        img = self.numpy_image.copy()
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=0.5)
        # the text is embeded in the background image
        if self.display_text:  # Check if text should be displayed
            img = self.add_text_to_image(img, self.text_item, divizor=1)
        # read icon with transparency
        import random

        if self.with_model_type_selection:
            self.model_button.show()
        texture = cv2.imread(
            f"data/icons/model_class_background_3.png",
            -1,
        )
        if isinstance(texture, type(None)):
            logger.error(f"Could not read texture {texture}")
            logger.error(f"Current working directory {os.getcwd()}")
            logger.error(f"Config {self.cfg}")
            return
        # # convert to RGBA always
        texture = cv2.cvtColor(texture, cv2.COLOR_BGRA2RGBA)
        texture = cv2.resize(texture, (self.size, self.size))

        # Separate the alpha channel from the overlay image
        alpha_channel = texture[:, :, 3]
        overlay_rgb = texture[:, :, :3]
        # if image is not square, crop to square from the smallest side
        if img.shape[0] > img.shape[1]:
            img = img[: img.shape[1], :, ...]
        else:
            img = img[:, : img.shape[0], ...]

        # if the image is not the same shape as the texture, resize it
        if img.shape[0] != texture.shape[0]:
            img = cv2.resize(img, (self.size + 10, self.size + 10))
        # Blend the images based on the alpha channel
        img = (
            overlay_rgb * (alpha_channel[:, :, None] / 255.0)
            + img * (1 - alpha_channel[:, :, None] / 255.0)
        ).astype(np.uint8)

        q_image = QtGui.QImage(
            img.copy(),
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmap = QtGui.QPixmap(q_image)
        self.pixmap.setDevicePixelRatio(self.ratio)

        self.update()

    def add_text_to_image(self, img, text, divizor=4):
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font_size = 42
        if self.original_size < 250:
            font_size = 22
        font = ImageFont.truetype(
            "data/fonts/Montserrat/static/Montserrat-Regular.ttf",
            font_size * self.ratio,
        )
        text_color = self.color  # white
        import textwrap

        if len(text) >= 10:
            lines = textwrap.wrap(text, width=5)
        else:
            lines = textwrap.wrap(text, width=10)
        max_width = 0
        total_height = 0
        for line in lines:
            x1, y1, x2, y2 = draw.textbbox((0, 0), line, font=font)
            width = x2 - x1
            height = y2 - y1
            max_width = max(max_width, width)
            total_height += height

        x = (img_pil.width - max_width) // 2
        y = (img_pil.height - total_height) // 2

        line_heights = []
        for line in lines:
            x1, y1, x2, y2 = draw.textbbox((0, 0), line, font=font)
            width = x2 - x1
            height = y2 - y1
            line_heights.append(height)

        line_y = y
        for i in range(len(lines)):
            x1, y1, x2, y2 = draw.textbbox((0, 0), lines[i], font=font)
            width = x2 - x1
            height = y2 - y1
            line_x = x + (max_width - width) // 2
            draw.text(
                (line_x, line_y - (15 * self.ratio)),
                lines[i],
                fill=tuple([x // divizor for x in text_color]),
                font=font,
            )
            line_y += line_heights[i]
        # to numpy
        img = np.array(img_pil)
        return img

    def set_normal_background(self):
        if self.with_model_type_selection:
            self.model_button.hide()
        # make image black and white with 3 channels
        img = cv2.cvtColor(self.numpy_image, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # convert to RGB always
        # create an empty image for the text, black background
        if self.display_text:  # Check if text should be displayed
            img = self.add_text_to_image(img, self.text_item, divizor=3)
        numpy_image_with_text = self.apply_motion_blur(img, 2)
        # Convert numpy image to QPixmap
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(
            numpy_image_with_text.copy(),
            numpy_image_with_text.shape[1],
            numpy_image_with_text.shape[0],
            numpy_image_with_text.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmap = QtGui.QPixmap(q_image)
        self.pixmap.setDevicePixelRatio(self.ratio)
        self.update()

    def apply_motion_blur(self, image, size):
        """
        Apply horizontal motion blur to an image.

        Parameters:
            - image_path (str): Path to the input image.
            - output_path (str): Path to save the blurred image.
            - size (int): Size of the blur kernel. Larger values produce more blur.
        """

        # Generate the motion blur kernel
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
        kernel_motion_blur /= size

        # Apply the kernel to the input image
        output = cv2.filter2D(image, -1, kernel_motion_blur)
        return output

    def set_as_hover(self):
        if self.display_text:  # Check if text should be displayed
            img = self.add_text_to_image(self.numpy_image, self.text_item, divizor=2)
        else:
            img = self.numpy_image.copy()

        # Convert numpy image to QPixmap
        q_image = QtGui.QImage(
            img.copy(),
            img.shape[1],
            img.shape[0],
            img.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmap = QtGui.QPixmap(q_image)
        self.pixmap.setDevicePixelRatio(self.ratio)

    def resizeEvent(self, event):
        # Override resizeEvent to always maintain square shape and icon size
        size = min(self.width(), self.height())
        self.setIconSize(QtCore.QSize(size, size))
        super(SquareButton, self).resizeEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Create a rounded rectangle path
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(0, 0, self.original_size, self.original_size)
        radius = self.radius_of_icon  # Set the radius for rounded corners
        path.addRoundedRect(rect, radius, radius)

        # Set the rounded rectangle path as a clipping path
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.pixmap)

        self.round_rect_path = QtGui.QPainterPath()
        self.round_rect_path.addRoundedRect(rect, radius, radius)
        if self.isChecked():
            c = self.color
        else:
            c = self.uncheck_color

        # uncomment to draw a border
        # pen = QtGui.QPen(QtGui.QColor(c[0], c[1], c[2]))
        # pen.setWidth(4)
        # painter.setPen(pen)
        # painter.drawPath(self.round_rect_path)

        # Call the paintEvent of the super class to draw the button

        super(SquareButton, self).paintEvent(event)


class RegionWideButton(StylableWidget):
    clicked = QtCore.pyqtSignal()  # Define a new signal

    def __init__(
        self,
        filterable_icon_table,
        cfg,
        size: int = 125,
        with_model_type_selection=False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.filterable_icon_table = filterable_icon_table
        self.cfg = cfg
        self.bbox_width = 350
        self.bbox_height = int(size * 1.40)
        self.setFixedHeight(self.bbox_height)
        self.setFixedWidth(self.bbox_width)
        self.outer_layout = QVBoxLayout(self)
        self.background_widget = QWidget(self)
        self.outer_layout.addWidget(self.background_widget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no extra margins
        self.outer_layout.setSpacing(0)  # Ensure no extra spacing
        self.background_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.button_group = None  # Initialize button_group attribute

        self.setStyleSheet(
            """
                           background-color: rgb(27,27,27);
                           border-radius: 5px;
                           padding: 0 px;
                           margin: 0 px;
                           """
        )

        self.border_width = 0.8

        self._is_hovering = False

        # Add drop shadow effect to the widget
        widget_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        widget_shadow.setBlurRadius(20)
        widget_shadow.setXOffset(0)
        widget_shadow.setYOffset(2)
        widget_shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.setGraphicsEffect(widget_shadow)

        # Add drop shadow effect to the background widget
        background_shadow = QtWidgets.QGraphicsDropShadowEffect(self.background_widget)
        background_shadow.setBlurRadius(10)
        background_shadow.setXOffset(0)
        background_shadow.setYOffset(2)
        background_shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        # Create a horizontal layout to hold the SquareButton and the grid widget
        self.inner_layout = QtWidgets.QHBoxLayout(self.background_widget)
        self.inner_layout.setContentsMargins(10, 0, 0, 0)  # Ensure no extra margins

        # Create the SquareButton with the cfg parameter
        self.square_button = SquareButton(
            self,
            cfg=cfg,
            size=size,
            with_model_type_selection=with_model_type_selection,
            display_text=False,
        )
        self.square_button.setFixedSize(size, size)  # Set a fixed size for the button
        self.inner_layout.addWidget(
            self.square_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        # self.square_button.setGraphicsEffect(background_shadow)

        spacing = 0
        self.margin_amount = 2
        self.setContentsMargins(
            self.margin_amount,
            self.margin_amount,
            self.margin_amount,
            self.margin_amount,
        )
        self.inner_layout.setSpacing(spacing)

        # Create the grid widget
        self.grid_widget = QWidget(self)
        self.setMinimumHeight(self.bbox_height)
        self.grid_layout = QGridLayout(self.grid_widget)
        self.inner_layout.addWidget(self.grid_widget)

        # Add large white text in the first column, first row
        large_text = QLabel(cfg["text"])
        large_text.setStyleSheet(
            "color: rgb(205,205,205); font-size: 15px; font-weight: 300;"
        )
        large_text.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )  # Center text vertically

        large_text.setFixedHeight(27)
        self.grid_layout.addWidget(
            large_text, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        # Parse the date string
        updated_date_str = cfg.get("updated_at", "")
        try:
            if updated_date_str:
                updated_date = datetime.strptime(
                    updated_date_str, "%a, %d %b %Y %H:%M:%S GMT"
                )
            else:
                updated_date = datetime.now()
        except ValueError:
            updated_date = datetime.now()  # Fallback to current time if parsing fails

        time_diff = datetime.now() - updated_date

        def plural(n):
            return "s" if n != 1 else ""

        if time_diff.days >= 365:
            years = time_diff.days // 365
            time_str = f"{years} year{plural(years)} ago"
        elif time_diff.days >= 30:
            months = time_diff.days // 30
            time_str = f"{months} month{plural(months)} ago"
        elif time_diff.days >= 7:
            weeks = time_diff.days // 7
            time_str = f"{weeks} week{plural(weeks)} ago"
        else:
            time_str = f"{time_diff.days} day{plural(time_diff.days)} ago"

        small_text_value = f"Owner: {cfg.get('classes',[{}])[0].get('lab', 'Community')} • Updated {time_str}"
        small_text = QLabel(small_text_value)
        small_text.setStyleSheet(
            "color: rgb(132,132,132); font-size: 12px; font-weight: 300;"
        )
        small_text.setFixedHeight(27)
        small_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(
            small_text, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        # Add icon in the second column, first and second row
        icon_label = QLabel()
        icon_pixmap = QtGui.QPixmap("path/to/icon.png")  # Replace with your icon path
        icon_label.setPixmap(icon_pixmap)
        self.grid_layout.addWidget(icon_label, 0, 1, 2, 1)  # Span two rows

        # Set the grid layout to expand horizontally
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 0)
        # Ensure the grid widget is visible
        self.grid_widget.show()

        # Connect signals for pressed and clicked
        self.square_button.pressed.connect(lambda: self.on_square_button_pressed())
        self.square_button.clicked.connect(lambda: self.on_square_button_clicked())
        self.square_button.clicked.connect(
            lambda: self.clicked.emit()
        )  # Emit the new signal

        # Enable context menu
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def click(self):
        self.square_button.click()

    @property
    def supercategory(self):
        return self.square_button.supercategory

    @property
    def classes(self):
        return self.square_button.classes

    @property
    def text(self):
        return self.square_button.text

    def isChecked(self):
        return self.square_button.isChecked()

    def setChecked(self, checked):
        if checked and self.filterable_icon_table.button_group_regions:
            for btn in self.filterable_icon_table.button_group_regions:
                if isinstance(btn, RegionWideButton) and btn != self:
                    btn.setChecked(False)
        # update all buttons
        [i.update() for i in self.filterable_icon_table.button_group_regions]
        self.square_button.setChecked(checked)
        self.update()

    @property
    def keywords(self):
        return self.square_button.keywords

    @property
    def is_valid(self):
        return self.square_button.is_valid

    @property
    def isPressed(self):
        return self.square_button.isPressed()

    def on_square_button_pressed(self):
        print("SquareButton pressed")

    def on_square_button_clicked(self):
        print("SquareButton clicked")

    def event(self, event: QEvent) -> bool:
        # Override event to prevent propagation of hover and click events
        if event.type() in (QEvent.Type.HoverEnter, QEvent.Type.MouseButtonPress):
            return True  # Stop event propagation
        return super().event(event)

    def show_context_menu(self, position):
        # only allow context menu for local items for now

        if not self.cfg.get("type", None) or not config.is_admin():  # cloud
            if self.cfg.get("private", True) and not config.is_admin():
                logger.info(
                    f"User {config.user_attributes.username} cabt modify a private model without admin rights"
                )
                return
            else:
                # if the model is not private, but the user does not have
                # rights to it , cant delete it
                if self.cfg.get("lab", None) != config.user_attributes.lab_uuid:
                    logger.info(
                        f"User {config.user_attributes.username} does not have rights to modify this model"
                    )
                    return

        context_menu = QtWidgets.QMenu(self)
        # Add actions to the context menu
        action_delete = context_menu.addAction("Delete")

        # # Connect actions to slots
        action_delete.triggered.connect(self.delete_item)

        # Show the context menu
        context_menu.exec(self.mapToGlobal(position))

    def delete_item(self):
        from celer_sight_ai import config
        from celer_sight_ai import configHandle

        # if its a local item just the delete the class from the file
        if self.cfg.get("type", None) == "local":
            if os.path.exists(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE):
                with open(
                    os.path.join(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE),
                    "r",
                ) as f:
                    data = json.load(f)
                for cfg_item in data:
                    if cfg_item == self.cfg:
                        logger.info(f"Deleting item: {cfg_item}")
                        data.remove(cfg_item)
                        break
                with open(
                    os.path.join(configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE),
                    "w",
                ) as f:
                    json.dump(data, f, indent=4)
        # otherwise delete from the server
        else:
            # on cloud categories , there is always 1 class and
            # that is the class we will use for deletion
            category = self.cfg["classes"][0].get("uuid", None)
            data = {
                "supercategory": self.cfg["supercategory"],
                "category": category,
                "username": config.user_attributes.username,
            }
            config.client.remove_category_cloud(data)
        # refresh the grid
        config.global_signals.refresh_categories_signal.emit()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # Emit the clicked signal when the widget is pressed
        self.clicked.emit()

        super().mousePressEvent(event)

    def event(self, event: QEvent) -> bool:
        if event.type() in (
            QEvent.Type.HoverEnter,
            QEvent.Type.HoverLeave,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.MouseButtonRelease,
        ):
            # Handle the event in this class
            if event.type() == QEvent.Type.HoverEnter:
                if not self.isChecked():
                    self.square_button.set_as_hover()
                self.update()
            elif event.type() == QEvent.Type.HoverLeave:
                if not self.isChecked():
                    self.square_button.set_normal_background()
                self.update()
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.setChecked(True)

        return super().event(event)

        # # For all other events, use the default handling
        # return super().event(event)

        # def event(self, event: QEvent) -> bool:
        #     # Override event to prevent propagation of hover and click events
        #     if event.type() == QEvent.Type.HoverEnter:
        #         # if its checked, do not change the hover state
        #         if not self.isChecked():
        #             self.square_button.set_as_hover()
        #         self.square_button.update()
        #         self.update()
        #     elif event.type() == QEvent.Type.MouseButtonPress:
        #         self.setChecked(True)
        #         self.update()
        #         return True # stop event propagation
        #     elif event.type() == QEvent.Type.HoverLeave:
        #         # if its checked, do not change the hover state
        #         if not self.isChecked():
        #             self.square_button.set_normal_background()
        #         self.square_button.update()
        #         # self._is_hovering = False
        #         self.update()

        #     return super().event(event)

        # def non_hovering_border_for_painter(self, painter: QtGui.QPainter , path , rect):

        #     # Create a gradient for the specular highlight border
        #     gradient = QtGui.QLinearGradient(rect.topLeft() + QtCore.QPointF(160, 0), rect.bottomRight()- QtCore.QPointF(160, 0))
        #     gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 60))    # Fade to transparent
        #     gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 20))    # Fade to transparent
        #     gradient.setColorAt(1, QtGui.QColor(255, 255, 255, 0))    # Fade to transparent

        #     # Set the pen with the gradient
        #     pen = QtGui.QPen(QtGui.QBrush(gradient), self.border_width)
        #     painter.setPen(pen)
        #     painter.drawPath(path)

        # def hovering_border_for_painter(self, painter: QtGui.QPainter , path , rect):
        #     # Create a brighter all-around border for hovering state

        #     # Create a gradient for the specular highlight border
        #     gradient = QtGui.QLinearGradient(rect.topLeft() + QtCore.QPointF(160, 0), rect.bottomRight()- QtCore.QPointF(160, 0))
        #     gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 70))  # Start with a light color
        #     gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 20))    # Fade to transparent
        #     gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 0))    # Fade to transparent

        #     pen = QtGui.QPen(QtGui.QBrush(gradient), 1.5)  # Slightly thicker pen for visibility
        #     painter.setPen(pen)
        #     painter.drawPath(path)

        #     # Add a subtle inner glow effect
        #     glow_color = QtGui.QColor(255, 255, 255, 40)  # Very subtle white glow
        #     glow_pen = QtGui.QPen(glow_color, 0.9)
        #     painter.setPen(glow_pen)
        #     painter.drawPath(path.translated(0, 1))  # Draw slightly offset path for glow effect

        # def checked_border_for_painter(self, painter: QtGui.QPainter, path, rect):
        #     # Create a more prominent border for the checked state

        #     # Create a gradient for the border
        #     gradient = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        #     gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 120))  # Brighter start
        #     gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 80))  # Mid-point
        #     gradient.setColorAt(1, QtGui.QColor(255, 255, 255, 120))  # Brighter end

        #     # Set the pen with the gradient
        #     pen = QtGui.QPen(QtGui.QBrush(gradient), 2.0)  # Thicker pen for visibility
        #     painter.setPen(pen)
        #     painter.drawPath(path)

        #     # Add a more pronounced inner glow effect
        #     glow_color = QtGui.QColor(255, 255, 255, 60)  # Brighter white glow
        #     glow_pen = QtGui.QPen(glow_color, 1.2)
        #     painter.setPen(glow_pen)
        #     painter.drawPath(path.translated(0, 1))  # Draw slightly offset path for glow effect

        #     # Add a second, outer glow for more emphasis
        #     outer_glow_color = QtGui.QColor(255, 255, 255, 30)  # Subtle outer glow
        #     outer_glow_pen = QtGui.QPen(outer_glow_color, 0.8)
        #     painter.setPen(outer_glow_pen)
        #     painter.drawPath(path.translated(0, 2))  # Draw another offset path for outer glow

        # def paintEvent(self, event):
        #     painter = QtGui.QPainter(self)
        #     painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        #     # Create a rounded rectangle path
        #     path = QtGui.QPainterPath()
        #     # rect = QtCore.QRectF(0, 0, self.width(), self.height())
        #     margin =  self.margin_amount  # Adjust this value based on your layout's margins
        #     padding = 0
        #     rect = QtCore.QRectF(
        #         margin + padding,
        #         margin + padding,
        #         self.bbox_width - (2*margin) - (2 * padding),
        #         self.bbox_height - (2*margin)- (2 * padding)
        #     )
        #     radius = 5  # Set the radius for rounded corners
        #     path.addRoundedRect(rect, radius, radius)
        #     # if its checked, draw the checked border
        #     if self.isChecked():
        #         self.checked_border_for_painter(painter, path, rect)
        #     # check if the mouse is hovering over the button
        #     elif self._is_hovering:
        #         self.hovering_border_for_painter(painter, path, rect)
        #     else:
        #         self.non_hovering_border_for_painter(painter, path, rect)
        #     # Call the paintEvent of the super class to draw the button
        #     super(RegionWideButton, self).paintEvent(event)


class FilterableIconTable(QWidget):
    def __init__(
        self,
        category_map,
        icon_size=40,
        supercategory=None,
        collumns=2,
        with_model_type_selection=False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        from celer_sight_ai import config

        self.setStyleSheet(
            """
                           background-color: rgb(43,43,43);
                           border: 0px solid rgba(200,200,200,0);
                           border-radius: 7px;
                           padding: 0 px;
                           margin: 0 px;
                           """
        )
        self.outer_layout = QVBoxLayout(self)
        self.background_widget = QWidget(self)
        self.outer_layout.addWidget(self.background_widget)

        self.background_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.with_model_type_selection = with_model_type_selection
        config.global_signals.update_category_icons_signal.connect(
            self.update_all_button_icons
        )
        # add a layout within the background widget
        self.MainWindow = self.parent()
        self.vblayout = QVBoxLayout(self.background_widget)
        self.cols = collumns
        self.search_line_edit = QLineEdit()
        self.search_line_edit.textChanged.connect(self.filter_items)
        self.vblayout.addWidget(self.search_line_edit)

        self.grid_widget = QtWidgets.QWidget(self.background_widget)
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_widget.setLayout(self.grid_layout)
        # add grid widget on a scrollable area
        self.scroll_area = QtWidgets.QScrollArea(self.background_widget)
        # set scrollbar as needed
        self.scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        # no horizontal scrollbar
        self.scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.grid_widget)
        self.vblayout.addWidget(self.scroll_area)
        self.setLayout(self.vblayout)

        self.button_group_regions = []  # just a list
        self.button_group = None
        self.icon_size = icon_size
        self.items = {}
        self.ignore_configs = ["default.json"]
        self.updating = False

        self.spawn_buttons()

        config.global_signals.refresh_categories_signal.connect(
            self.fetch_all_categories_and_update_grid
        )

    def spawn_buttons(self):
        self.updating = True
        if not config.supercategory:
            # Wait and spawn until the supercategory is set
            self.updating = False
            return
        # Clear previous buttons without deleting them
        for i in self.button_group_regions:
            i.hide()  # Hide the button instead of deleting
        self.button_group_regions.clear()
        self.items.clear()

        # Create new buttons
        category_map = gather_cfgs(config.supercategory)
        for c in category_map:
            btn = RegionWideButton(
                self,
                c,
                size=self.icon_size,
                with_model_type_selection=self.with_model_type_selection,
            )
            if not btn.is_valid:
                btn.hide()
                continue
            btn.setParent(self.grid_widget)

            btn.clicked.connect(lambda: self.handle_button_clicked())
            # self.button_group.addButton(btn.square_button)
            self.button_group_regions.append(btn)
            # btn.button_group = self.button_group
            self.items[btn] = btn.keywords
            btn.show()

        self.grid_widget.setVisible(True)
        self.updating = False
        self.update_grid()

    def update_all_button_icons(self):
        for btn in self.items:
            if hasattr(btn, "update_icon"):
                btn.update_icon()

    def fetch_all_categories_and_update_grid(self):
        # if we are in offline mode, dont refetch cloud categories
        from celer_sight_ai import config

        if not config.user_cfg["OFFLINE_MODE"]:
            # fetch all categories from cloud
            response_json = config.client.get_cloud_classes()
            config.client._update_cloud_categories(
                {"organism_map": response_json}, config.settings
            )

        # Refresh local categories by re-reading from disk
        from celer_sight_ai import configHandle
        import os

        local_categories_path = os.path.join(
            configHandle.getLocal(), config.LOCAL_CATEGORIES_FILE
        )
        if os.path.exists(local_categories_path):
            with open(local_categories_path, "r") as f:
                config.local_categories = json.load(f)

        self.spawn_buttons()

    def update_grid(self):
        import time

        wait_iters = 0
        while self.updating:
            time.sleep(0.1)
            wait_iters += 1
            if wait_iters > 10:
                logger.warning("Grid update is taking too long, skipping")
                return
            continue

        # Clear the existing layout
        self.clear_layout(self.grid_layout)

        # Filter items
        all_class_names = [
            i.text() for i in self.MainWindow.custom_class_list_widget.classes.values()
        ]
        # hide all items, as some wont be filtered
        for btn in self.button_group_regions:
            btn.hide()
        filtered_items = [
            btn
            for btn, text in self.items.items()
            if (
                self.search_line_edit.text().lower() in text.lower()
                and (btn.supercategory == config.supercategory)
                and not (any([c in btn.classes for c in all_class_names]))
            )
        ]

        # Add filtered buttons to the grid
        row, col = 0, 0
        for btn in filtered_items:
            self.grid_layout.addWidget(btn, row, col)
            btn.show()  # Ensure the button is visible
            col += 1
            if col >= self.cols:
                col = 0
                row += 1

        # Add a vertical spacer at the bottom
        self.grid_layout.addItem(
            QtWidgets.QSpacerItem(
                0,
                0,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Expanding,
            ),
            row + 1,
            0,
            1,
            -1,  # Span all columns
        )

        self.grid_layout.setSpacing(10)

        # Set the first visible button as checked
        if filtered_items:
            filtered_items[0].setChecked(True)

        # Force layout update
        self.grid_widget.updateGeometry()
        self.scroll_area.updateGeometry()
        self.grid_widget.setVisible(True)

        self.update()

        def is_widget_in_layout(self, layout, widget_to_check):
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget == widget_to_check:
                    return True
            return False

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                layout.removeWidget(widget)
                widget.hide()  # Hide the widget instead of setting parent to None
            elif item.spacerItem():
                layout.removeItem(item)
            elif item.layout():
                self.clear_layout(item.layout())

    def filter_items(self, text):
        if self.updating:
            return
        self.update_grid()

    def handle_button_clicked(self):
        btn = self.sender()
        if btn.isChecked():
            print(f"Button {btn.text()} is checked")
        else:
            print(f"Button {btn.text()} is unchecked")


class FilterableClassList(FilterableIconTable):
    # This widget only apears on the project page when the user clicks on "add" class
    # When you lose focus on this widget it will be deleted
    def __init__(self, items, icon_size=40, *args, **kwargs) -> None:

        super().__init__(items, icon_size=icon_size, collumns=1, *args, **kwargs)
        from celer_sight_ai.QtAssets.stylized_widget import StylableButton

        # self.setWindowFlags(Qt.WindowType.Popup)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enables focus for the widget
        self.setFocus()  # Set initial focus
        # set as application modal
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # calculate minimum width to fit all the buttons
        gap = 21

        # add a "Add class" an cancel button
        self.add_class_btn = QPushButton("Add")
        self.add_class_btn.clicked.connect(lambda: self.add_class())
        self.add_class_btn.setStyleSheet(
            """
            QPushButton{
                    background-color: rgba(0,0,0,0);
                    color: rgb(105,215,105);
                    border-radius: 5px;
                    }
            QPushButton:hover{
                    background-color: rgba(105,215,105, 30);
                    color: rgb(155,255,155);
                    }
            """
        )
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.cancel_btn.setStyleSheet(
            """
            QPushButton{
                    background-color: rgba(0,0,0,0);
                    color: rgb(215 ,105,105);
                    border: 0px solid rgb(165,255,165);
                    border-radius: 5px;
                    }
            QPushButton:hover{
                    background-color: rgba(215,105,105, 30);
                    color: rgb(255,155,155);
                    }
            """
        )
        self.button_group_actions = QButtonGroup(self.background_widget)
        self.button_group_actions.addButton(self.add_class_btn)
        self.button_group_actions.addButton(self.cancel_btn)
        self.hblayout = QtWidgets.QHBoxLayout(self)
        # add title -> Add class:
        self.vblayout.removeWidget(self.search_line_edit)
        self.vblayout.removeWidget(self.scroll_area)

        self.vblayout.addWidget(self.search_line_edit)
        self.vblayout.addWidget(self.scroll_area)

        # Add the ok cancel buttons
        self.vblayout.addLayout(self.hblayout)
        self.hblayout.addWidget(self.cancel_btn)
        self.hblayout.addWidget(self.add_class_btn)
        self.button_group_actions.setExclusive(True)
        self.add_class_btn.setCheckable(False)
        # set background color
        self.setStyleSheet(
            """
            QWidget{
                background-color: rgba(25,25,25,150);
                border-radius:10px;
                }
            QScrollArea{
                border-radius:10px;
            }
            QScrollArea QWidget#Viewport {
                border-radius: 10px;
            }
            """
        )
        self.scroll_area.viewport().setStyleSheet(
            """
                border-radius: 10px;
            """
        )
        self.scroll_area.viewport().setAutoFillBackground(False)
        from celer_sight_ai.QtAssets.category_and_contribution_widgets import (
            DialogWidgetTitleHat,
        )

        # add hat
        self.title_hat = DialogWidgetTitleHat("Add Class dsfsd", self)
        self.title_hat.setObjectName("title_hat")
        self.title_hat.show()

        # bbox_width
        title_width = 400
        if len(self.button_group_regions):
            title_width = max([i.bbox_width for i in self.button_group_regions]) + 100
        # set minimum dimentions
        self.setMinimumWidth(title_width)
        self.setMinimumHeight(300)
        self.title_hat.setMinimumWidth(title_width)
        self.title_hat.setMinimumHeight(400)
        self.title_hat.setFixedSize(title_width, title_width)
        self.title_hat.setMaximumSize(title_width, 400)
        self.title_hat.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.installEventFilter(self)
        self.current_index = 0 if self.button_group_regions else -1
        self.spawn_buttons()

        # add new button

        # Add a tool button to create new categories on the region selection frame
        self.new_category_button = QtWidgets.QToolButton(self.background_widget)
        self.new_category_button.move(
            title_width - self.new_category_button.width() + 5, 10
        )
        self.new_category_button.setFixedSize(63, 23)

        # Center the text and icon on the button

        # Set the plus icon directly on the QToolButton
        plus_icon = QtGui.QIcon(
            "data/icons/plus_icon.png"
        )  # Make sure this icon exists
        self.new_category_button.setIcon(plus_icon)
        self.new_category_button.setIconSize(QtCore.QSize(9, 9))

        # Set the tool button style to display the icon next to the text
        self.new_category_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        # Add the "New" text
        self.new_category_button.setText("New")
        self.new_category_button.setStyleSheet("color: white;")

        # Set the button style
        self.new_category_button.setStyleSheet(
            """
            QToolButton {
                background-color: rgb(45,45,45);
                border-radius: 9px;
                padding: 3px;
                text-align: center;
                font-size: 12px;  /* Increased font size */
                padding-left: 10px;
                padding-right: 6px;
            }
            QToolButton:hover {
                background-color: rgb(65,65,65);
            }
        """
        )
        self.new_category_button.clicked.connect(
            lambda: self.MainWindow.spawn_create_new_category_dialog_on_main_scene()
        )

    def add_class(self):
        # get the selected button
        btns = [i for i in self.button_group_regions if i.isChecked()]
        if not len(btns):
            return

        if self.MainWindow.new_category_pop_up_widget:
            self.MainWindow.new_category_pop_up_widget.close()

        supercategory_relevant_buttons = [
            i for i in btns if i.supercategory == config.supercategory
        ]
        for btn in supercategory_relevant_buttons:
            if btn.isChecked():
                self.add_class_to_list(btn)
        self.close()

    def add_class_to_list(self, btn):
        # add the class to the list
        self.MainWindow.new_analysis_object.scan_class_items(btn.cfg["classes"])

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # get the parent and resize to be in the middle of the screen
        parent = self.parent()
        # get the parent size
        if not parent:
            return
        parent_size = parent.size()
        # get the parent position
        parent_pos = parent.pos()
        # get the size of the widget
        size = self.size()
        # get the new position
        new_pos = QtCore.QPoint(
            parent_pos.x() + (parent_size.width() - size.width()) // 2,
            parent_pos.y() + (parent_size.height() - size.height()) // 2,
        )
        self.move(new_pos)

    def keyPressEvent(self, event):

        event.accept()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Up:
                self.select_previous_button()
                return True
            elif key == Qt.Key.Key_Down:
                self.select_next_button()
                return True
            elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self.add_class()
                return True
        return super().eventFilter(obj, event)

    def select_previous_button(self):
        if self.button_group_regions:
            self.current_index = (self.current_index - 1) % len(
                self.button_group_regions
            )
            self.button_group_regions[self.current_index].setChecked(True)
            self.scroll_to_button(self.button_group_regions[self.current_index])

    def select_next_button(self):
        if self.button_group_regions:
            self.current_index = (self.current_index + 1) % len(
                self.button_group_regions
            )
            self.button_group_regions[self.current_index].setChecked(True)
            self.scroll_to_button(self.button_group_regions[self.current_index])

    def scroll_to_button(self, button):
        self.scroll_area.ensureWidgetVisible(button)


class FilterableClassListItem(QPushButton):
    def __init__(self, cfg, size=250, parent=None):
        # open config
        with open(cfg, "r") as f:
            # read json
            cfg = json.load(f)
        self.text_item = cfg["text"]


def main():
    app = QApplication([])
    window = FilterableIconTable(
        [
            ("celer_sight_ai/data/icons/elegans_whole_body_off.png", "Body"),
            ("celer_sight_ai/data/icons/elegans_head_off.png", "Head"),
            ("celer_sight_ai/data/icons/elegans_embryo_off.png", "Locomotion"),
            ("celer_sight_ai/data/icons/elegans_intentitne_off.png", "Intestine"),
        ]
    )
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
