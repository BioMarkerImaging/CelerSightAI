from PyQt6 import QtCore, QtGui, QtWidgets
import os
import sys
import logging
import numpy as np
import cv2
from celer_sight_ai.io.image_reader import (
    post_proccess_image,
    combine_channels,
    channel_to_color,
)
from celer_sight_ai.io.data_handler import colorize_gray_image
from celer_sight_ai import config
logger = logging.getLogger(__name__)


# class ParticleAnalysisSettingsWidget(QtWidgets.QWidget):


class ParticleAnalysisSettingsWidgetUi(QtWidgets.QWidget):

    apply_threshold_to_MainWindow_part_2_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, MainWindow=None):
        super(ParticleAnalysisSettingsWidgetUi, self).__init__(parent)

        self.parent = parent
        self.MainWindow = MainWindow
        # self.setWindowOpacity(0.0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # record current class
        self.current_class_uuid = None

        # interactive attributes
        self.threshold_value_interactive = 0  # 0-255 or 0 - max float
        self.remove_background_value_interactive = (
            0  # rollnig ball value, based on image
        )
        # saved attributes for analysis
        self.threshold_value_saved = 0  # 0-255 or 0 - max float
        self.remove_background_value_saved = 0  # rollnig ball value, based on image
        self._is_ui_spawned = False

        self.current_substract_image = None
        self.current_threshold_image = None
        self.particles_generated_list = (
            []
        )  # list all classes particles have been generated for
        self.current_class_uuid = None
        self.apply_threshold_to_MainWindow_part_2_signal.connect(self.apply_threshold_to_MainWindow_part_2)


    def despawn(self):
        # select non particle class
        config.global_signals.ensure_not_particle_class_selected_signal.emit()
        QtWidgets.QApplication.processEvents()
        # reload main scene
        config.global_signals.load_main_scene_signal.emit()
        config.global_signals.unlock_ui_signal.emit()
        self.close()

    def spawn(self, channel_list=[]):
        from celer_sight_ai import config
        # spawn the ui and initiate everything, if already spawn, just show and load saved values
        # if channel_list is empty, show message ==> To measure particles, please load an image first.

        # check if previous particles have been generated for this class
        # if so, ask if they want to proceed by deleting the old particle config
        # ^^^^^^^ this is a TODO
        # THIS PART DOES NOT ALLOW FOR MULTIPLE PARTICLE CLASSES.
        if len(channel_list) == 0:
            # select non particle class
            config.global_signals.ensure_not_particle_class_selected_signal.emit()
            QtWidgets.QApplication.processEvents()
            # warn user to load images
            config.global_signals.errorSignal.emit("Please load an image first")
            self.current_class_uuid = None
            return
        # make sure selection button is pressed
        self.MainWindow.viewer.QuickTools.pushButtonQuickToolsSelectionTool.click()
        # record current class
        self.current_class_uuid = (
            self.MainWindow.custom_class_list_widget.currentItemWidget().unique_id
        )
        # check if the class has particles generated
        # if self.MainWindow.custom_class_list_widget.currentItemWidget().
        # # record current class
        # self.current_class_uuid = (
        #     self.MainWindow.custom_class_list_widget.get_current_row_class_id()
        # )
        QtWidgets.QApplication.processEvents()
        if not self._is_ui_spawned:
            self.setupUi(self)
            self.background_slider.valueChanged.connect(
                self.set_background_value
            )  # background slider
            self.threshold_slider.valueChanged.connect(self.set_threshold_value)
            self._is_ui_spawned = True
        QtWidgets.QApplication.processEvents()

        # read settings from class if the particle analysis settings have been
        # previously set for this class
        if self.read_particle_settings_from_class_object(self.current_class_uuid):
            # remove the bitmap from all images with that mask / class
            self.MainWindow.DH.BLobj.delete_all_masks_with_class(
                self.current_class_uuid
            )
        self.show()
        # clear the channel list
        self.channel_combobox.clear()
        # add all channels

        current_image_object = (
            self.MainWindow.DH.BLobj.groups["default"]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[self.MainWindow.current_imagenumber]
        )
        for ch_key in channel_list:
            # colorize every channel
            if isinstance(ch_key, list):
                ch_name = "#{:02x}{:02x}{:02x}".format(ch_key)
            else:
                if not ch_key.startswith("#"):
                    # case of a channel name from a microscope
                    ch_name = "#{:02x}{:02x}{:02x}".format(*channel_to_color(ch_key))
            channel_name = f"<font color={ch_name}>{ch_key}</font>"

            self.channel_combobox.addItem(channel_name)
        self.resize_to_position()
        for i in range(self.channel_combobox.count()):
            self.update_channel_combobox_label(i)
        # set the first combox item as the selected one
        self.channel_combobox.setCurrentIndex(0)
        self.update_channel_combobox_label(0)
        QtWidgets.QApplication.processEvents()
        initial_background_value = 2
        initial_threshold_value = 150
        self.background_slider.setValue(initial_background_value)
        self.threshold_slider.setValue(initial_threshold_value)
        # lock class, ROI, Analysis
        from celer_sight_ai import config

        # lock ui
        config.global_signals.lock_ui_signal.emit(["left_group", "classes", "condition_buttons" , "interactive_tools"])


    def record_particle_settings_to_class_object(self, class_uuid=None):
        """
        Stores the values from the UI to the custom_list_widgets.py CustomClassListWidgetItem
        in self.classes from the custom class list widget
        """
        # record the current settings to the class object
        # get the current class object
        if not class_uuid:
            class_obj = (
                self.MainWindow.custom_class_list_widget.get_class_widget_by_uuid(
                    self.current_class_uuid
                )
            )
        else:
            class_obj = (
                self.MainWindow.custom_class_list_widget.get_class_widget_by_uuid(
                    class_uuid
                )
            )
        # record the settings
        class_obj.particle_settings = {
            "particle_background_value": self.remove_background_value_interactive,
            "particle_threshold_value": self.threshold_value_interactive,
            "particle_min_size_value": None,  # TODO: add this
            "particle_max_size_value": None,  # TODO: add this
            "particle_channel_name": self.channel_combobox.currentText(),
            "particle_min_circularity_value": None,  # TODO: add this
            "particle_max_circularity_value": None,  # TODO: add this
            "particle_min_convexity_value": None,  # TODO: add this
            "particle_max_convexity_value": None,  # TODO: add this
        }

    def read_particle_settings_from_class_object(self, class_uuid=None):
        """
        Reads the values from the custom_list_widgets.py CustomClassListWidgetItem in
        self.classes from the custom class list widget and applies them to the UI.
        This triggers when the user initiates the particle class analysis. (clicks on it)
        """
        if class_uuid == None:
            class_obj = (
                self.MainWindow.custom_class_list_widget.get_class_widget_by_uuid(
                    self.current_class_uuid
                )
            )
        else:
            class_obj = (
                self.MainWindow.custom_class_list_widget.get_class_widget_by_uuid(
                    class_uuid
                )
            )
        if class_obj.particle_settings:
            # read the settings
            self.remove_background_value_interactive = class_obj.particle_settings[
                "particle_background_value"
            ]
            self.threshold_value_interactive = class_obj.particle_settings[
                "particle_threshold_value"
            ]
            self.channel_combobox.setCurrentText(
                class_obj.particle_settings["particle_channel_name"]
            )
            # set the sliders
            self.background_slider.setValue(self.remove_background_value_interactive)
            self.threshold_slider.setValue(self.threshold_value_interactive)
            # get the current image object
            img_obj = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                .images[self.MainWindow.current_imagenumber]
            )
            self.process_substract_and_threshold(img_obj)
            return True
        return False

    def set_background_value(self, value=None):
        # set value
        if not value:
            value = self.remove_background_value_interactive
        else:
            self.remove_background_value_interactive = value
        if value:
            self.label.setText("Remove Background: " + str(value) + "px")
        else:
            self.label.setText("Disabled.")
            # adjust the threshold to min / max
            self.threshold_slider.setMinimum(0)
            from celer_sight_ai import config

            self.threshold_slider.setMaximum(255)

        # send signal to show the the substracted image form background
        self.remove_background_current_image(value)

    def set_threshold_value(self, value):
        # set value
        self.threshold_value_interactive = value
        self.label2.setText("Treshold: " + str(value))

        # send signal to show the the substracted image form background
        self.threshold_current_image(
            value,
            group_name="default",
            condition_name=self.MainWindow.DH.BLobj.get_current_condition(),
            img_id=self.MainWindow.current_imagenumber,
            preview=True,
        )

    def process_substract_and_threshold(self, image_object=None):
        from celer_sight_ai import config

        background_image = self.remove_background_current_image(
            val=self.remove_background_value_interactive,
            img_obj=image_object,
            return_image=True,
        )
        if isinstance(background_image, type(None)):
            return
        threshold_image = self.threshold_current_image(
            val=self.threshold_value_interactive,
            group_name=image_object.groupName,
            condition_name=image_object.get_treatment_uuid(),
            img_id=image_object.imgID,
            provided_image=background_image.copy(),
            dont_colorize=True,
        )
        # add as a mask object to the image
        config.global_signals.create_annotation_object_signal.emit(
            [
                image_object.get_treatment_uuid(),
                None,
                threshold_image,  # so its value is 1
                image_object.imgID,
                self.current_class_uuid,
                "bitmap",  # bitmap by default
            ]
        )

        return threshold_image

    def remove_background_current_image(
        self,
        val=5,
        img_obj=None,
        return_image=False,
    ):
        # use skimage rolling ball
        # arr needs to be single channel
        from skimage import restoration
        from celer_sight_ai import config
        import cv2
        import re

        channel = self.channel_combobox.currentText()
        if channel == "":
            return
        if "<font" in channel:
            regex = r"<font color=(.*?)>(.*?)</font>"
            match = re.search(regex, channel)
            if match:
                color = match.group(1)  # the color is the first group in the regex
                channel = match.group(2)  # the text is the second group in the regex
        # if the image is ultra high res, we cant do substract background

        # get stored image on ram from config
        if img_obj is None:
            condition = self.MainWindow.DH.BLobj.get_current_condition()
            img_id = self.MainWindow.current_imagenumber
            if self.MainWindow.DH.BLobj.groups["default"].conds[condition].images[
                img_id
            ]._is_ultra_high_res:
                logger.info("Image is ultra high res, background removal not supported")
                # disable the substract background slider
                self.background_slider.setEnabled(False)
                return
            else:
                # make sure its enabled
                self.background_slider.setEnabled(True)

            logger.debug("Getting image with id ", img_id)
            img = (
                self.MainWindow.DH.BLobj.groups["default"]
                .conds[condition]
                .getImage(
                    img_id,
                    to_uint8=True,  # because it doesnt not affect the measurmnet, just the particle generation
                    to_rgb=False,
                    channel_names_to_filter=[channel],
                    fast_load_ram=True,
                )
            )
        else:

            if img_obj._is_ultra_high_res:
                logger.info("Image is ultra high res, background removal not supported")
                config.global_signals.errorSignal.emit("Image is too large to analyze particles. Please use a lower resolution image.")
                self.despawn()
                return
            else:
                # make sure its enabled
                self.background_slider.setEnabled(True)

            img = img_obj.getImage(
                    to_uint8=True,  # because it doesnt not affect the measurmnet, just the particle generation
                    to_rgb=False,
                    channel_names_to_filter=[channel],
                    # fast_load_ram=True,
                )

        # if value is 0 just return the image as grayscale
        if val > 0:
            sub_img = cv2.subtract(img, restoration.rolling_ball(img, radius=val))
        else:
            sub_img = img

        self.current_substract_image = sub_img
        # get rgb val from channel name
        try:
            rgb = config.channel_colors[channel.lower()]
        except Exception as e:
            print(e)
            rgb = (255, 255, 255)
        # colorize to channel
        sub_img_color = (
            colorize_gray_image(sub_img.copy(), rgb)
        )
        if not return_image:
            config.global_signals.refresh_main_scene_image_only_signal.emit(
                sub_img_color
            )
        else:
            return sub_img

    def threshold_current_image(
        self,
        val=5,
        group_name=None,
        condition_name=None,
        img_id=None,
        provided_image=None,
        preview=False,
        dont_colorize=False,
    ):
        # use skimage rolling ball
        # arr needs to be single channel
        from skimage import restoration
        from celer_sight_ai import config

        import cv2
        import re
        if provided_image is None:
            if self.current_substract_image is None:
                # if the image is ultra high res
                # prompt the image to refresh with new tiles, tresholded
                
                return
            # get stored image on ram from config
            img = self.current_substract_image
        else:
            img = provided_image
        channel = self.channel_combobox.currentText()
        if channel == "":
            return None
        if "<font" in channel:
            regex = r"<font color=(.*?)>(.*?)</font>"
            match = re.search(regex, channel)
            if match:
                color = match.group(1)  # the color is the first group in the regex
                channel = match.group(2)  # the text is the second group in the regex
        # get stored image on ram from config
        # threshold image
        ret, thresh = cv2.threshold(img, val, 255, cv2.THRESH_BINARY)

        # get rgb val from class name , so that we can overlap
        try:
            color = (
                self.MainWindow.custom_class_list_widget.get_mask_color_from_class_uuid(
                    self.current_class_uuid
                )
            )
        except Exception as e:
            print(e)
            color = (255, 255, 255)
        # colorize to channel
        if not dont_colorize:
            thresh_orig = thresh.copy()
            thresh = colorize_gray_image(thresh, color)
            if preview:
                channels = (
                    self.MainWindow.DH.BLobj.groups[group_name]
                    .conds[condition_name]
                    .images[img_id]
                    .channel_list
                )
                viewer_bbox = self.MainWindow.viewer.viewport().rect().getRect()
                # if image is ultra high res, follow a different tactic, only get the portion of the
                # image that is visible
                if self.MainWindow.DH.BLobj.groups[group_name].conds[condition_name].images[img_id]._is_ultra_high_res:
                    return
                else:
                    img_original, min_val, max_val = post_proccess_image(
                        self.MainWindow.DH.BLobj.groups["default"]
                        .conds[self.MainWindow.DH.BLobj.get_current_condition()]
                        .getImage(
                            self.MainWindow.current_imagenumber, channel_names_to_filter = [channel]),
                        channels,
                        to_uint8=True,
                        to_rgb=True,
                        has_min_max=False,
                    )
                # Expand dimensions of mask to match the shape of original_image
                thresh_orig = np.expand_dims(thresh_orig, axis=-1)
                thresh_orig = np.repeat(thresh_orig, 3, axis=-1) / 255

                # Create the combined image using the mask
                combined_image = (
                    self.MainWindow.handle_adjustment_to_image(img_original)
                    * (1 - thresh_orig)
                    + (thresh * thresh_orig)
                ).astype(np.uint8)
                thresh = combined_image
                # combine the scene image with this image
        if provided_image is None:
            config.global_signals.refresh_main_scene_image_only_signal.emit(thresh)
        else:
            return thresh

    def adjust_threshold_value(self, value):
        # display the threshold from the current image
        self.threshold_value_interactive = value
        # trigger the viewer to compute and display that image

    def resize_to_position(self):
        # get right_side_frame_images pos
        p2 = self.MainWindow.right_side_frame_images.pos().x()
        # get group_pg1_left width
        w1 = self.MainWindow.group_pg1_left.width()
        # get window height
        h = self.MainWindow.MainWindow.height()
        wh = 190  # widget height
        extra_pad = 130
        # | <--- w1 ---> | <--- Particle Widget ---> |<--- w2 ---> |
        self.MainWindow.viewer.particle_analysis_settings_widget.move(
            w1, h - wh - extra_pad
        )
        self.MainWindow.viewer.particle_analysis_settings_widget.setFixedWidth(p2 - w1)
        self.MainWindow.viewer.particle_analysis_settings_widget.setFixedHeight(wh)

        left_pad = ((p2 - w1 - 211) // 2) + 2  # 211 is the len
        right_pad = ((p2 - w1 - 211) // 2) - 1
        self.main_groupbox.setStyleSheet(
            """QGroupBox::title#main_groupbox {
                margin-top:1px;
                padding: 6px ;
                padding-right:"""
            + str(right_pad)
            + """px;
                padding-left:+"""
            + str(left_pad)
            + "px;}"
        )

    def setupUi(self, Form):
        Form.setObjectName("ParticleAnalsyisWidgetForm")
        Form.resize(400, 200)
        # create the main background widget, which will be a groupbox
        self.main_groupbox = QtWidgets.QGroupBox(Form)
        # stretch groupbox with size policy
        self.main_groupbox.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.main_groupbox.setObjectName("main_groupbox")
        # set main layout
        self.main_layout_of_groupbox = QtWidgets.QVBoxLayout(self.main_groupbox)
        self.main_layout_of_groupbox.setObjectName("main_layout_of_groupbox")

        self.main_layout_of_groupbox_2_horizontal = QtWidgets.QHBoxLayout(
            self.main_groupbox
        )
        self.main_layout_of_groupbox_2_horizontal_widget = QtWidgets.QWidget(
            self.main_groupbox
        )
        self.main_layout_of_groupbox_2_horizontal.setObjectName(
            "main_layout_of_groupbox_2_horizontal"
        )
        self.main_layout_of_groupbox_2_horizontal.setContentsMargins(0, 0, 0, 0)
        self.main_layout_of_groupbox_2_horizontal_widget.setLayout(
            self.main_layout_of_groupbox_2_horizontal
        )
        # # set main layout of groupbox
        # self.main_layout = QtWidgets.QVBoxLayout(self.main_groupbox)
        # self.main_layout.setObjectName("main_layout")

        self.channel_label = QtWidgets.QLabel(self.main_groupbox)
        self.channel_label.setText("Select Channel")
        from celer_sight_ai.gui.custom_widgets.modern_qcombobox_widgets import (
            ModernSearchableQComboBox,
        )
        from celer_sight_ai.gui.custom_widgets.analysis_handler import HtmlDelegate

        self.channel_combobox = ModernSearchableQComboBox(self.main_groupbox)
        font = QtGui.QFont()
        font.setFamily(".AI Buyan PUA")
        font.setPointSize(9)

        self.channel_combobox.setEditable(True)
        self.channel_combobox.setLineEdit(QtWidgets.QLineEdit(self.channel_combobox))
        self.channel_combobox.lineEdit().setReadOnly(True)
        self.channel_combobox.lineEdit().hide()
        self.channel_combobox_label = QtWidgets.QLabel(self.channel_combobox)

        self.channel_combobox_label.setFont(font)
        self.channel_combobox.currentIndexChanged.connect(
            self.update_channel_combobox_label
        )
        self.channel_combobox.currentIndexChanged.connect(self.set_background_value)
        c_delegate = HtmlDelegate(self.channel_combobox)

        self.channel_combobox.setItemDelegate(c_delegate)

        # set main layout inside the groupbox
        self.main_groupbox.setLayout(self.main_layout_of_groupbox)
        self.main_layout_of_groupbox.addWidget(
            self.main_layout_of_groupbox_2_horizontal_widget
        )
        # set main layout inside the main widget
        self.vertical_main_layout = QtWidgets.QVBoxLayout(Form)
        self.vertical_main_layout.setObjectName("vertical_main_layout")
        self.vertical_main_layout.addWidget(self.main_groupbox)
        self.setStyleSheet(
            """
            
            QGroupBox{
               font-family:'Lato';
                font-weight: bold;
                font-size: 15px;    border: 1px solid;
                border-color: rgba(102, 102, 102,0);
                border-top : 0px solid black;
                margin-top: 30px;
                margin-bottom: 1px;
                border-top-left-radius: 0px;
                border-top-right-radius:0px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: rgba(45, 45, 45,200);
                padding-bottom: 0px;
                padding-left: 5px;
                padding-right: 5px;
            }
            QGroupBox::indicator{
            background-color:rgba(0,0,0,0);
            }
            QLabel{
                color: rgb(255, 255, 255);
                background-color: rgba(255, 255, 255, 0);
                }
            QWidget#ParticleAnalsyisWidgetForm{
                background-color: rgba(0, 0, 0, 250);
                border-radius: 3px;
                border: 0px solid black;
                }

            QFrame{
                background-color: rgba(255, 255, 255, 0);
                border-radius: 3px;
                border: 0px solid black;
            }
            #particle_background_widget_2{
                background-color:rgba(255, 255, 255, 0);
            }
            #particle_background_widget{
                background-color:rgba(255, 255, 255, 0);
            }
            QGroupBox::title{
                border : 1px solid;
                font: 17 "Lato";
                border-bottom : 0px solid;
                font-weight:bold;
                font-size: 12px;
                border-color: rgba(102, 102, 102,0);
                subcontrol-origin: margin;
                subcontrol-position: top left;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background-color: rgb(25, 25, 25);
                color:rgba( 255, 255, 255, 220);
            }
            QSlider{
            background-color:
                rgba(0, 0, 0,0);
            }
            QSlider::groove:horizontal {
                background-color: white;
                border: 0px solid black;
                height: 2px;
                border-radius: 1px;
                }
            QSlider::handle:horizontal {
                background-color: white;
                border: 2px solid black;
                width: 5px;
                height: 5px;
                line-height: 10px;
                margin-top: -8px;
                margin-bottom: -8px;
                border-radius: 10px;
                }
            
            
            """
        )
        #            QGroupBox::title#main_groupbox{
        # margin-top:1px;
        # padding: 6px ;
        # padding-right:36px;
        # padding-left:20px;
        # }
        # same as in the MainWindow UI
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(3)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.main_groupbox.setObjectName("main_groupbox")
        self.main_groupbox.setFont(font)
        self.main_groupbox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.particle_background_widget = QtWidgets.QWidget(Form)
        self.verticalLayout_particle_background = QtWidgets.QVBoxLayout()
        self.particle_background_widget.setObjectName("particle_background_widget")
        self.particle_background_widget_2 = QtWidgets.QWidget(Form)
        self.particle_background_widget_2.setObjectName("particle_background_widget_2")
        self.verticalLayout_channels_list = QtWidgets.QVBoxLayout()
        self.verticalLayout_channels_list.setObjectName("verticalLayout_channels_list")

        self.verticalLayout_channels_list_widget = QtWidgets.QWidget(Form)

        self.main_layout_of_groupbox_2_horizontal.addWidget(
            self.verticalLayout_channels_list_widget
        )
        self.verticalLayout_channels_list_widget.setLayout(
            self.verticalLayout_channels_list
        )
        self.verticalLayout_channels_list.addWidget(self.channel_label)
        self.verticalLayout_channels_list.addWidget(self.channel_combobox)

        self.verticalLayout_particle_threshdold = QtWidgets.QVBoxLayout()

        # create a slider
        self.background_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.background_slider.setObjectName("slider_particle_background")
        self.threshold_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.threshold_slider.setObjectName("slider_particle_threshold")
        self.verticalLayout_particle_background.setObjectName(
            "verticalLayout_particle_background"
        )
        self.verticalLayout_particle_threshdold.setObjectName(
            "verticalLayout_particle_threshdold"
        )

        self.particle_background_widget.setLayout(
            self.verticalLayout_particle_background
        )
        self.particle_background_widget_2.setLayout(
            self.verticalLayout_particle_threshdold
        )
        self.main_layout_of_groupbox_2_horizontal.addWidget(
            self.particle_background_widget
        )
        self.main_layout_of_groupbox_2_horizontal.addWidget(
            self.particle_background_widget_2
        )

        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # set horizontal label minimum policy
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setObjectName("label2")
        self.label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label2.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout_particle_background.addWidget(self.label)
        self.verticalLayout_particle_threshdold.addWidget(self.label2)

        self.verticalLayout_particle_background.addWidget(self.background_slider)
        self.verticalLayout_particle_threshdold.addWidget(self.threshold_slider)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        # add a button to the right
        self.done_button = GlowHoverButton(
            "Save and Apply", glow_color=QtGui.QColor(155, 155, 255)
        )
        self.done_button.clicked.connect(lambda: self.apply_threshold_to_MainWindow_process())
        self.done_button.setMaximumWidth(180)
        self.done_button.setMinimumHeight(30)
        self.done_button.setStyleSheet(
            """
            QPushButton{
                background-color: rgb(40,91,246);
                border-radius: 15px;
                color:rgb(255,255,255);
                padding-left: 10px;
                padding-right: 10px;
                padding-top:7px;
                padding-bottom:7px;
                font-size: 12px;
                font-family: 'Lato';
                font-weight: bold;
            }

            QPushButton:hover{
                border:0px solid;
                background-color: rgb(50,101,255);
            }
            """
        )
        self.accept_reject_layout = QtWidgets.QHBoxLayout(
            self.verticalLayout_channels_list_widget
        )
        self.main_layout_of_groupbox.addLayout(self.accept_reject_layout)
        self.accept_reject_layout.addWidget(self.done_button)

        self.reject_button = QtWidgets.QPushButton(
            self.verticalLayout_channels_list_widget
        )
        self.reject_button.setObjectName("reject_button")
        self.reject_button.setText("Cancel")
        self.reject_button.clicked.connect(lambda: self.cancel_action())
        self.reject_button.setMaximumWidth(180)
        self.reject_button.setMinimumHeight(30)
        self.reject_button.setStyleSheet(
            """
            QPushButton{
                background-color: rgba(146 ,91,40,0);
                border-radius: 15px;
                color:rgb(155,15,15);
                padding-left: 10px;
                padding-right: 10px;
                padding-top:7px;
                padding-bottom:7px;
                font-size: 12px;
                font-family: 'Lato';
                font-weight: bold;
            }

            QPushButton:hover{
                border:0px solid;
                background-color: rgba(255 ,101,50,0);
                color:rgb(255,25,25);

            }
            """
        )
        # add spacer item
        self.accept_reject_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.accept_reject_layout.addWidget(
            self.reject_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.accept_reject_layout.addWidget(
            self.done_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.accept_reject_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Particle Analysis"))
        self.label.setText(_translate("Form", "Remove Background"))
        self.label2.setText(_translate("Form", "Threshold"))
        self.main_groupbox.setTitle(_translate("Form", "Particle Analysis Settings"))

    def cancel_action(self):
        self.hide()
        from celer_sight_ai import config

        config.global_signals.ensure_not_particle_class_selected_signal.emit()
        # reload scene
        config.global_signals.load_main_scene_signal.emit()
        config.global_signals.unlock_ui_signal.emit()

    def update_channel_combobox_label(self, indx):
        self.channel_combobox_label.setFixedWidth(self.channel_combobox.width())
        self.channel_combobox_label.setFixedHeight(self.channel_combobox.height())
        self.channel_combobox_label.setContentsMargins(10, 0, 0, 0)
        text = self.channel_combobox.itemText(indx)
        self.channel_combobox_label.setText(text)

    def apply_threshold_to_MainWindow_process(self):
        self.MainWindow.DH.BLobj.delete_all_masks_with_class(self.current_class_uuid)
        self.apply_threshold_to_MainWindow_part_1()

    @config.threaded
    def apply_threshold_to_MainWindow_part_1(self):
        """
        1 ) generate threshold for every image
        2 ) for every parent mask, crop that area within the threshold
            image and generate a mask for that area -> this can generate
            multiple child masks for 1 parent mask
        """
        from celer_sight_ai import config
        all_image_objects = [i for i in self.MainWindow.DH.BLobj.get_all_image_objects()]

        config.global_signals.start_progress_bar_signal.emit({"title" : "", "main_text" : "Applying threshold to all images"})
        # make sure no particle bitmap masks are left from a previous
        # particle session.
        
        config.global_signals.unlock_ui_signal.emit()
        quant = 100 / len(all_image_objects)
        i = 0
        # iterate over all images
        for img_obj in all_image_objects:
            config.global_signals.update_progress_bar_progress_signal.emit({"percent" : quant * ( i+1)})
            self.process_substract_and_threshold(img_obj)
            i += 1
        config.global_signals.complete_progress_bar_signal.emit()
        self.apply_threshold_to_MainWindow_part_2_signal.emit()

    
    def apply_threshold_to_MainWindow_part_2(self):
        """
        None threaded part of the process. Record settings and unlock UI
        """
        # hide this window
        self.hide()
        # save to class
        self.record_particle_settings_to_class_object(self.current_class_uuid)
        self.current_class_uuid = None
        config.global_signals.ensure_not_particle_class_selected_signal.emit()
        # reload scene
        QtWidgets.QApplication.processEvents()
        config.global_signals.load_main_scene_signal.emit()




class GlowHoverButton(QtWidgets.QPushButton):
    def __init__(self, text=None, glow_color=None):
        super().__init__()
        self.glow_color = glow_color
        self.text = text
        self.setText(text)

        # Create a QGraphicsDropShadowEffect and set it to the button
        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setColor(QtGui.QColor(self.glow_color))
        self.shadow_effect.setOffset(0)

        self.setGraphicsEffect(self.shadow_effect)
        # Connect button's hover events to our custom slots
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            self.shadow_effect.setBlurRadius(20)
        elif event.type() == QtCore.QEvent.Type.HoverLeave:
            self.shadow_effect.setBlurRadius(0)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ParticleAnalysisSettingsWidgetUi()
    window.show()
    sys.exit(app.exec())
