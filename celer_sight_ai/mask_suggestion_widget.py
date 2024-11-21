from PyQt6 import QtWidgets, QtGui, QtCore
import logging
import os

logger = logging.getLogger(__name__)


class AnimatedGroupBox(QtWidgets.QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self._expanded = False
        # self.setMinimumHeight
        self.animation = QtCore.QPropertyAnimation(self, b"maximumHeight")
        self.animation.setDuration(500)  # Duration of the animation in milliseconds
        self.animation.setEasingCurve(
            QtCore.QEasingCurve.Type.InOutQuad
        )  # Smooth animation curve
        self.originalHeight = self.sizeHint().height()
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(lambda: self.toggle())
        # if windows
        if os.name == "nt":
            self.max_height_min = 14
        else:
            self.max_height_min = 19
        # self.setMaximumHeight(self.max_height_min)

        self.extra_widget_space = 60

    def initialize_position(self):
        self.maximumHeight = self.max_height_min

    # on size change, adjust parent widget height
    @QtCore.pyqtProperty(int)
    def maximumHeight(self):
        return super().maximumHeight()

    @maximumHeight.setter
    def maximumHeight(self, height):
        super().setMaximumHeight(height)
        self.parent().parent().setFixedHeight(height + self.extra_widget_space)

        # Has to be the same with the spawning method --> set_ai_model_settings_widget_position
        total_width = (
            self.parent().parent().parent().width()
        )  # MainWindow.Images.width()
        total_height = (
            self.parent().parent().parent().height()
        )  # MainWindow.Images.height()
        distance_from_bottom = 80
        # set the proper position, which is middle of the widget , and distance_from_bottom from the bottom
        self.parent().parent().move(
            round(total_width / 2 - self.width() / 2),  # center of the widget
            total_height - self.height() - distance_from_bottom,
        )

    def toggle(self):
        self._expanded = not self._expanded
        self.animation.setStartValue(self.height())
        endValue = (
            self.originalHeight if not self._expanded else self.sizeHint().height()
        )
        endValue = max(endValue, self.max_height_min)
        self.animation.setEndValue(endValue)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animation.start()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("mask_suggestion_widget")
        Form.resize(555, 226)

        self.main_widget = QtWidgets.QGroupBox(Form)
        self.main_widget.setObjectName("main_widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addWidget(self.main_widget)
        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.roi_assistant_cancel_button = QtWidgets.QPushButton(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.roi_assistant_cancel_button.sizePolicy().hasHeightForWidth()
        )
        self.roi_assistant_cancel_button.setSizePolicy(sizePolicy)
        self.roi_assistant_cancel_button.setObjectName("roi_assistant_cancel_button")

        self.gridLayout.addWidget(self.roi_assistant_cancel_button, 1, 1, 1, 1)

        self.roi_assistant_generate_button = QtWidgets.QPushButton(parent=Form)
        self.roi_assistant_generate_button.setObjectName(
            "roi_assistant_generate_button"
        )
        self.gridLayout.addWidget(self.roi_assistant_generate_button, 1, 2, 1, 1)
        self.roi_assistant_accept_button = QtWidgets.QPushButton(parent=Form)
        if os.environ.get("CELER_SIGHT_AI_HOME"):
            icon = QtGui.QIcon(
                os.environ.get("CELER_SIGHT_AI_HOME")
                + "data/icons/enter_icon_white.png"
            )  # Replace "icon.png" with the path to your icon file
            self.roi_assistant_accept_button.setIcon(icon)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.roi_assistant_accept_button.sizePolicy().hasHeightForWidth()
        )
        self.roi_assistant_accept_button.setSizePolicy(sizePolicy)
        self.roi_assistant_accept_button.setObjectName("roi_assistant_accept_button")
        self.gridLayout.addWidget(self.roi_assistant_accept_button, 1, 3, 1, 1)
        self.ROI_assistant_label = QtWidgets.QLabel(parent=Form)
        self.ROI_assistant_label.setObjectName("ROI_assistant_label")
        self.gridLayout.addWidget(self.ROI_assistant_label, 1, 0, 1, 1)
        self.roi_assistant_advanced_groupbox = AnimatedGroupBox("Advanced", parent=Form)
        self.roi_assistant_advanced_groupbox.setObjectName(
            "roi_assistant_advanced_groupbox"
        )
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.roi_assistant_advanced_groupbox
        )
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.positive_roi_threshold_layout = QtWidgets.QHBoxLayout()
        self.positive_roi_threshold_layout.setObjectName(
            "positive_roi_threshold_layout"
        )
        self.positive_roi_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.positive_roi_threshold_label.setObjectName("positive_roi_threshold_label")
        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_label)
        self.positive_roi_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.positive_roi_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.positive_roi_threshold_number.setIndent(10)
        self.positive_roi_threshold_number.setObjectName(
            "positive_roi_threshold_number"
        )

        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_number)
        self.positive_roi_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.positive_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        )

        self.positive_roi_threshold_slider.setSizePolicy(sizePolicy)
        self.positive_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        self.positive_roi_threshold_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.positive_roi_threshold_slider.setObjectName(
            "positive_roi_threshold_slider"
        )
        self.positive_roi_threshold_layout.addWidget(self.positive_roi_threshold_slider)
        self.verticalLayout_3.addLayout(self.positive_roi_threshold_layout)
        # self.negative_roi_threshold_layout = QtWidgets.QHBoxLayout()
        # self.negative_roi_threshold_layout.setObjectName(
        #     "negative_roi_threshold_layout"
        # )
        # self.negative_roi_threshold_label = QtWidgets.QLabel(
        #     parent=self.roi_assistant_advanced_groupbox
        # )
        # self.negative_roi_threshold_label.setObjectName("negative_roi_threshold_label")
        # self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_label)
        # self.negative_roi_threshold_number = QtWidgets.QLabel(
        #     parent=self.roi_assistant_advanced_groupbox
        # )
        # self.negative_roi_threshold_number.setAlignment(
        #     QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        # )
        # self.negative_roi_threshold_number.setIndent(10)
        # self.negative_roi_threshold_number.setObjectName(
        #     "negative_roi_threshold_number"
        # )
        # self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_number)
        # self.negative_roi_threshold_slider = QtWidgets.QSlider(
        #     parent=self.roi_assistant_advanced_groupbox
        # )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.negative_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        # )
        # self.negative_roi_threshold_slider.setSizePolicy(sizePolicy)
        # self.negative_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        # self.negative_roi_threshold_slider.setOrientation(
        #     QtCore.Qt.Orientation.Horizontal
        # )
        # self.negative_roi_threshold_slider.setObjectName(
        #     "negative_roi_threshold_slider"
        # )
        # self.negative_roi_threshold_layout.addWidget(self.negative_roi_threshold_slider)
        # self.verticalLayout_3.addLayout(self.negative_roi_threshold_layout)
        self.shape_similarity_threshold_layout = QtWidgets.QHBoxLayout()
        self.shape_similarity_threshold_layout.setObjectName(
            "shape_similarity_threshold_layout"
        )
        self.shape_roi_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.shape_roi_threshold_label.setObjectName("shape_roi_threshold_label")
        self.shape_similarity_threshold_layout.addWidget(self.shape_roi_threshold_label)
        self.shape_roi_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.shape_roi_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.shape_roi_threshold_number.setIndent(10)
        self.shape_roi_threshold_number.setObjectName("shape_roi_threshold_number")
        self.shape_similarity_threshold_layout.addWidget(
            self.shape_roi_threshold_number
        )
        self.shape_roi_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.shape_roi_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.shape_roi_threshold_slider.setSizePolicy(sizePolicy)
        self.shape_roi_threshold_slider.setMaximumSize(QtCore.QSize(250, 16777215))
        self.shape_roi_threshold_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.shape_roi_threshold_slider.setObjectName("shape_roi_threshold_slider")
        self.shape_similarity_threshold_layout.addWidget(
            self.shape_roi_threshold_slider
        )
        self.verticalLayout_3.addLayout(self.shape_similarity_threshold_layout)
        self.image_similarity_threshold_layout = QtWidgets.QHBoxLayout()
        self.image_similarity_threshold_layout.setObjectName(
            "image_similarity_threshold_layout"
        )
        self.image_similarity_threshold_label = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.image_similarity_threshold_label.setObjectName(
            "image_similarity_threshold_label"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_label
        )
        self.image_similarity_threshold_number = QtWidgets.QLabel(
            parent=self.roi_assistant_advanced_groupbox
        )
        self.image_similarity_threshold_number.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.image_similarity_threshold_number.setIndent(10)
        self.image_similarity_threshold_number.setObjectName(
            "image_similarity_threshold_number"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_number
        )
        self.image_similarity_threshold_slider = QtWidgets.QSlider(
            parent=self.roi_assistant_advanced_groupbox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.image_similarity_threshold_slider.sizePolicy().hasHeightForWidth()
        )
        self.image_similarity_threshold_slider.setSizePolicy(sizePolicy)
        self.image_similarity_threshold_slider.setMaximumSize(
            QtCore.QSize(250, 16777215)
        )
        self.image_similarity_threshold_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.image_similarity_threshold_slider.setObjectName(
            "image_similarity_threshold_slider"
        )
        self.image_similarity_threshold_layout.addWidget(
            self.image_similarity_threshold_slider
        )
        self.verticalLayout_3.addLayout(self.image_similarity_threshold_layout)
        self.gridLayout.addWidget(self.roi_assistant_advanced_groupbox, 2, 0, 1, 4)

        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.roi_assistant_cancel_button.setText(_translate("Form", "Cancel"))
        self.roi_assistant_generate_button.setText(_translate("Form", "Generate"))
        self.roi_assistant_accept_button.setText(_translate("Form", "Accept"))
        self.ROI_assistant_label.setText(_translate("Form", ""))
        self.roi_assistant_advanced_groupbox.setTitle(_translate("Form", "Advanced"))
        self.positive_roi_threshold_label.setText(_translate("Form", "Confidence (+)"))
        self.positive_roi_threshold_number.setText(_translate("Form", "42"))
        # self.negative_roi_threshold_label.setText(_translate("Form", "Confidence (-)"))
        # self.negative_roi_threshold_number.setText(_translate("Form", "42"))
        self.shape_roi_threshold_label.setText(_translate("Form", "Shape similarity"))
        self.shape_roi_threshold_number.setText(_translate("Form", "42"))
        self.image_similarity_threshold_label.setText(
            _translate("Form", "Color similarity")
        )
        self.image_similarity_threshold_number.setText(_translate("Form", "42"))
        self.main_widget.setTitle(_translate("Form", "Mask Suggestion Settings"))


class AnnotationAssistantWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(
        self,
        parent=None,
        MainWindow=None,
    ):
        super(AnnotationAssistantWidget, self).__init__(parent)
        from celer_sight_ai.gui.custom_widgets.widget_spinner import WaitingSpinner

        # TranslucentBackground
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.MainWindow = MainWindow
        # state attributes
        self.is_generating = False
        self.is_auto_generate = False  # on by default, once stoped, its off

        self.setupUi(self)
        if MainWindow:
            # record the inial position on the self.MainWindow.mwUi.Images widget
            # from sam suggestor put the attributes in the widget
            initial_positive_roi_value = (
                self.MainWindow.mwUi.sdknn_tool.magic_box_2._positive_roi_threshold
            )
            # initial_negative_roi_value = (
            #     self.MainWindow.mwUi.sdknn_tool.magic_box_2._negative_roi_threshold
            # )
            initial_shape_roi_value = (
                self.MainWindow.mwUi.sdknn_tool.magic_box_2._shape_similarity_threshold
            )
            initial_image_similarity_value = (
                self.MainWindow.mwUi.sdknn_tool.magic_box_2._image_similarity_threshold
            )
        else:
            initial_positive_roi_value = 5
            # initial_negative_roi_value = 5
            initial_shape_roi_value = 5
            initial_image_similarity_value = 5
        self.image_similarity_threshold_slider.setValue(initial_image_similarity_value)
        self.positive_roi_threshold_slider.setValue(initial_positive_roi_value)
        # self.negative_roi_threshold_slider.setValue(initial_negative_roi_value)
        self.shape_roi_threshold_slider.setValue(initial_shape_roi_value)
        self.image_similarity_threshold_number.setText(
            str(round(initial_image_similarity_value / 100, 3))
        )
        self.shape_roi_threshold_number.setText(
            str(round(initial_shape_roi_value / 100, 3))
        )
        # self.negative_roi_threshold_number.setText(
        #     str(round(initial_negative_roi_value / 100, 3))
        # )
        self.positive_roi_threshold_number.setText(
            str(round(initial_positive_roi_value / 100, 3))
        )
        self._setup_connections()
        # make_expandable(self.roi_assistant_advanced_groupbox)
        self._setup_ui()  # further adjust the UI elements looks and extra functionality
        self.original_height = self.height()

        btn_fixed_height = 30
        btn_fixed_width = 75

        self.positive_roi_threshold_label.setMinimumHeight(20)
        # self.negative_roi_threshold_label.setMinimumHeight(20)
        self.shape_roi_threshold_label.setMinimumHeight(20)
        self.image_similarity_threshold_label.setMinimumHeight(20)
        self.roi_assistant_cancel_button.setMinimumHeight(30)
        self.roi_assistant_generate_button.setMinimumHeight(btn_fixed_height)
        self.roi_assistant_accept_button.setMinimumHeight(btn_fixed_height)
        self.roi_assistant_accept_button.setFixedWidth(btn_fixed_width)
        self.roi_assistant_generate_button.setFixedWidth(btn_fixed_width)
        self.roi_assistant_accept_button.raise_()
        self.roi_assistant_generate_button.raise_()

        # Hide the cancel button for now
        self.roi_assistant_cancel_button.hide()
        # Hide the negative prompt for now
        # self.negative_roi_threshold_slider.hide()
        # self.negative_roi_threshold_label.hide()
        # self.negative_roi_threshold_number.hide()

        # spinner that runs while we are generating in.
        self.roi_assistant_generate_button.enterEvent = (
            self.generate_button_hover_enter_override
        )
        self.roi_assistant_generate_button.leaveEvent = (
            self.generate_button_hover_leave_override
        )

        self.roi_assistant_generate_button_spinner = WaitingSpinner(
            self.roi_assistant_generate_button,
            roundness=100.0,
            fade=40.0,
            radius=3,
            lines=38,
            line_length=7,
            line_width=8,
            speed=0.5,
            color=(0, 235, 35),
        )
        from celer_sight_ai import config

        self.roi_assistant_generate_button.clicked.connect(
            lambda: self.cancel_generating()
        )
        config.global_signals.set_mask_suggestor_generating_signal.connect(
            self.set_generating
        )
        self.setStyleSheet(
            """
            #main_widget{
                border-radius: 5px;
                background-color: rgb(45,45,45);
                }
            QLabel{
                color: rgb(255,255,255);
                font-weight: bold;
                font-size: 12px;
                background-color: transparent;
            }
            QPushButton{
                margin-top: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover{
                margin-top: 5px;
                border: 0px solid gray;
            }
            #roi_assistant_cancel_button{
                color: rgba(185,90,90,140);
                background-color: rgba(100,60,60,40);
                border-radius: 5px;
            }
            #roi_assistant_cancel_button:hover{
                color: rgb(255,100,100);
                background-color: rgba(100,0,0,50);
                border-radius: 5px;
            }
            #roi_assistant_generate_button{
                color: rgba(90,185,90,140);
                background-color: rgba(60,100,60,40);
                border-radius: 5px;
            }
            #roi_assistant_generate_button:hover{
                color: rgb(100,255,100);
                background-color: rgba(0,100,0,50);
                border-radius: 5px;
            }
            #roi_assistant_accept_button{
                color: rgba(30,120,225,240);
                background-color: rgba(30,120,200,20);
                border-radius: 5px;
            }
            #roi_assistant_accept_button:hover{
                color: rgb(255,255,255);
                background-color: rgba(30,100,255,150);
                border-radius: 5px;
            }
            QSlider{
                background-color: transparent;
            }
            QSlider::sub-page{
                    background-color:rgb(210, 210, 210);
                    margin-left:4px;
            }
            QSlider::groove{
            background-color:rgb(92, 92, 92);
            border: 0px solid black;
            height: 2px;
            border-radius: 1px;
            margin-left:2px;
            }

            QSlider::handle{
            background-color: rgb(192,192,192);
            border: 1px solid rgb(210,210,210); 
            width: 9px; 
            height: 9px; 
            line-height: 4px; 
            margin-top: -4px; 
            margin-bottom: -4px; 
            border-radius:5px;		
            }
            
        QGroupBox {
            font-weight: bold;
            font-size: 12px;
            color: rgb(255,255,255);
            border: 0px solid gray;
            border-radius: 5px;
            margin-top: 3ex; /* leave space at the top for the title */
        }

        QGroupBox::title {
            font-weight: bold;
            font-size: 14px;
            subcontrol-origin: margin;
            subcontrol-position: top left; /* position at the top center */
            padding: 0 0px;
        }

        QGroupBox::indicator {
            width: 13px;
            height: 13px;
        }

        QGroupBox::indicator:unchecked {
            image: url(data/icons/checkbox_unchecked.png);
        }

        QGroupBox::indicator:checked {
            image: url(data/icons/checkbox_checked.png);
        }
            
            """
        )

    def resizeEvent(self, event=None):
        # get text width
        text_width = (
            self.main_widget.fontMetrics()
            .boundingRect(self.main_widget.title())
            .width()
        )

        # if on mac:
        if os.name == "posix":
            # calculate the padding
            left_pad = ((self.width() - text_width) // 2) - 2
            right_pad = left_pad - 2

            self.main_widget.setStyleSheet(
                """QGroupBox::title#main_widget{
                    border-radius: 5px;
                    color: rgb(255,255,255);
                    background-color: rgb(25,25,25);
                    margin-top:1px;
                    padding: 6px ;
                    padding-right:"""
                + str(right_pad)
                + """px;
                    padding-left:+"""
                + str(left_pad)
                + "px;}"
            )
        else:
            # calculate the padding
            left_pad = ((self.width() - text_width) // 2) - 2
            right_pad = left_pad

            self.main_widget.setStyleSheet(
                """QGroupBox::title#main_widget{
                    border-radius: 5px;
                    color: rgb(255,255,255);
                    background-color: rgb(25,25,25);
                    margin-top: 0px;
                    padding: 2px ;
                    padding-right:"""
                + str(right_pad)
                + """px;
                    padding-left:+"""
                + str(left_pad)
                + "px;}"
            )

    def update_visible(self):
        # if the suggestor is selected, make visible, if not, hide,
        # also update the position on the screen
        from celer_sight_ai.config import MagicToolModes

        if (
            self.MainWindow.mwUi.ai_model_combobox.text()
            == "Magic ROI Plus"  # TODO fix this to MagicToolModes.MAGIC_BOX_WITH_PREDICT
        ):
            self.show()
            self.roi_assistant_advanced_groupbox.initialize_position()  # bring to non visible position
            self.MainWindow.set_ai_model_settings_widget_position()
        else:
            self.hide()

    def cancel_generating(self):
        from celer_sight_ai import config

        if self.is_generating:
            self.MainWindow.mwUi.sdknn_tool.magic_box_2.stop_mask_suggestion_generator_process()
            self.MainWindow.mwUi.sdknn_tool.magic_box_2.cleanup_memory()
            self.set_generating(False)
            # clear all the suggested masks
            self.reset_suggestions()
            config.global_signals.unlock_ui_signal.emit()

    def prompt_user_to_save_or_delete_suggestions(self):
        from celer_sight_ai import config
        from functools import partial

        # prompt user to add multiple treatments
        config.global_signals.actionDialogSignal.emit(
            "ROI suggested annotations are not saved, do you want to save them?",
            {
                "Save": partial(
                    self.MainWindow.mwUi.sdknn_tool.magic_box_2.accept_current_suggested_annotations,
                ),
                "Delete": partial(
                    self.reset_suggestions,
                ),
            },
        )

    def generate_button_hover_enter_override(self, event):
        if self.is_generating:
            from celer_sight_ai import config

            config.global_signals.annotation_generator_spinner_signal_stop.emit()
            self.roi_assistant_generate_button.setText("Cancel")
            self.roi_assistant_generate_button.setStyleSheet(
                """
                QPushButton{
                margin-top: 5px;
                color: rgba(185,90,90,140);
                background-color: rgba(100,60,60,40);
                border-radius: 5px;
                }
                QPushButton:hover{
                    margin-top: 5px;
                    color: rgb(255,100,100);
                    background-color: rgba(100,0,0,50);
                    border-radius: 5px;
                }
                """
            )

        super().enterEvent(event)

    def generate_button_hover_leave_override(self, event):
        if self.is_generating:
            # set back to spinner
            from celer_sight_ai import config

            self.roi_assistant_generate_button.setText("")
            # spinner that runs while we are logging in.
            config.global_signals.annotation_generator_spinner_signal_start.emit()
        super().leaveEvent(event)

    def set_generating(self, value=None):
        # sets the button to cancel to indicate its generating
        from celer_sight_ai import config

        if self.is_generating == value:
            # when we dont change state do nothing
            return
        self.is_generating = value
        if value:
            # if the user is hover on the button, then dont change the text
            from celer_sight_ai import config

            self.roi_assistant_generate_button.show()
            self.roi_assistant_generate_button.setText("")

            config.global_signals.annotation_generator_spinner_signal_start.emit()
        else:
            self.roi_assistant_generate_button.show()
            config.global_signals.annotation_generator_spinner_signal_stop.emit()
            self.roi_assistant_generate_button.setText("Generate")

    def reset_suggestions(self):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation
        import time
        from celer_sight_ai import config

        # if mask suggestion is running, stop it
        # wait until not runnning any more
        start = time.time()
        while (
            config.group_running["start_suggested_mask_generator"]
            or time.time() - start > 1.5  # wait a maximum of 1.5 seconds
        ):
            time.sleep(0.03)
        # cancel the ROI assistant
        # get all masks from the scene that are suggested
        all_polygon_masks = [
            i
            for i in self.MainWindow.mwUi.viewer._scene.items()
            if isinstance(i, PolygonAnnotation) and i.is_suggested
        ]
        # delete all of them
        logger.debug(
            f"Found {len(all_polygon_masks)} suggested masks to delete from the scene"
        )
        logger.debug(f"Deleting suggested masks")
        for mask in all_polygon_masks:

            mask.DeleteMask()
        logger.debug(f"Done deleting suggested masks")

        self.set_generating(False)

    def _setup_connections(self) -> None:
        from celer_sight_ai import config

        self.roi_assistant_cancel_button.clicked.connect(
            lambda: self._on_roi_assistant_cancel_button_clicked()
        )
        self.roi_assistant_accept_button.clicked.connect(
            lambda: self.MainWindow.mwUi.sdknn_tool.magic_box_2.accept_current_suggested_annotations()
        )
        self.positive_roi_threshold_slider.valueChanged.connect(self.update_text_values)
        # self.negative_roi_threshold_slider.valueChanged.connect(self.update_text_values)
        self.shape_roi_threshold_slider.valueChanged.connect(self.update_text_values)
        self.image_similarity_threshold_slider.valueChanged.connect(
            self.update_text_values
        )
        # spinner connections
        config.global_signals.annotation_generator_spinner_signal_start.connect(
            self.start_roi_assistant_generate_button_spinner
        )
        config.global_signals.annotation_generator_spinner_signal_stop.connect(
            self.stop_roi_assistant_generate_button_spinner
        )

    def start_roi_assistant_generate_button_spinner(self):
        self.roi_assistant_generate_button.show()
        self.roi_assistant_generate_button_spinner.start()
        self.roi_assistant_generate_button.setText("")

    def stop_roi_assistant_generate_button_spinner(self):
        self.roi_assistant_generate_button_spinner.stop()
        self.roi_assistant_generate_button.show()
        self.roi_assistant_generate_button.setText("Generate")
        self.roi_assistant_generate_button.setStyleSheet(
            """QPushButton{
            margin-top: 5px;
            color: rgba(90,185,90,140);
            background-color: rgba(60,100,60,40);
            border-radius: 5px;
            }
            QPushButton:hover{
                margin-top: 5px;
                color: rgb(100,255,100);
                background-color: rgba(0,100,0,50);
                border-radius: 5px;
            }
        """
        )

    def update_text_values(self):
        """
        This method updates the text values of the ROI (Region of Interest) threshold sliders.

        The method performs the following steps:
        1. Blocks signals from all sliders to prevent any unwanted side effects during the update process.
        2. Updates the text values of the sliders by rounding the slider values and dividing by 100.
        3. Updates the values in the application's configuration settings.
        4. Emits a signal to start the annotation generator and processes any pending events.
        5. Unblocks the signals to allow further user interaction.

        The method assumes that the sliders and the configuration settings are correctly initialized and accessible.
        """
        # disable signals
        self.positive_roi_threshold_slider.blockSignals(True)
        # self.negative_roi_threshold_slider.blockSignals(True)
        self.shape_roi_threshold_slider.blockSignals(True)
        self.image_similarity_threshold_slider.blockSignals(True)

        self.image_similarity_threshold_number.setText(
            str(round(self.image_similarity_threshold_slider.value() / 100, 3))
        )
        self.shape_roi_threshold_number.setText(
            str(round(self.shape_roi_threshold_slider.value() / 100, 3))
        )
        self.positive_roi_threshold_number.setText(
            str(round(self.positive_roi_threshold_slider.value() / 100, 3))
        )

        # update the values in qsettings
        from celer_sight_ai import config

        config.settings.setValue(
            "roi_suggestor_positive_roi_threshold",
            self.positive_roi_threshold_slider.value(),
        )
        config.settings.setValue(
            "roi_suggestor_shape_similarity_threshold",
            self.shape_roi_threshold_slider.value(),
        )
        config.settings.setValue(
            "roi_suggestor_image_similarity_threshold",
            self.image_similarity_threshold_slider.value(),
        )
        generating_prior = self.is_generating
        self._on_roi_assistant_cancel_button_clicked()  # cancel the current session (if there is one)

        # enable signals
        self.positive_roi_threshold_slider.blockSignals(False)
        # self.negative_roi_threshold_slider.blockSignals(False)
        self.shape_roi_threshold_slider.blockSignals(False)
        self.image_similarity_threshold_slider.blockSignals(False)
        # stop any ongoing image generation and restart it
        if generating_prior:
            # restart it
            self.set_generating(True)
            config.global_signals.annotation_generator_start_signal.emit()
        self.set_generating(False)
        QtWidgets.QApplication.processEvents()

    # def _on_roi_assistant_accept_button_clicked(self) -> None:
    #     """
    #     Convert all existing suggested masks to accepted masks in the scene
    #     """
    #     from celer_sight_ai.gui.Utilities.scene import PolygonAnnotation

    def _on_roi_assistant_cancel_button_clicked(self) -> None:
        """
        Delete all the suggested masks from the scene, leaves the orignal mask on
        """
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        # cancel the ROI assistant
        # get all masks from the scene that are suggested
        all_polygon_masks = [
            i
            for i in self.MainWindow.mwUi.viewer._scene.items()
            if isinstance(i, PolygonAnnotation) and i.is_suggested
        ]
        # delete all of them
        logger.debug(
            f"Found {len(all_polygon_masks)} suggested masks to delete from the scene"
        )
        for mask in all_polygon_masks:
            mask.DeleteMask()
        self.set_generating(False)

    def _setup_ui(self):
        self._setup_image_viewer()
        # self._setup_mask_viewer()

    def _setup_image_viewer(self):
        # self.image_viewer = ImageViewerWidget()
        pass


class TempMainWindow(QtWidgets.QMainWindow):
    def __init__(self, widget, parent=None):
        super(TempMainWindow, self).__init__(parent)
        self.setCentralWidget(widget)
        self.setGeometry(
            int(QtWidgets.QApplication.primaryScreen().geometry().width() * 0.1),
            int(QtWidgets.QApplication.primaryScreen().geometry().height() * 0.1),
            int(QtWidgets.QApplication.primaryScreen().geometry().width() * 0.8),
            int(QtWidgets.QApplication.primaryScreen().geometry().height() * 0.8),
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    centeral_widget = QtWidgets.QWidget()
    mainWindow = TempMainWindow(centeral_widget)
    widget = AnnotationAssistantWidget(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
