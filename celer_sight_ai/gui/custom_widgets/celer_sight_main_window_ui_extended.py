"""
This is a module that applies the css sepcified to the the whole app 
and brings the app together essensialy
"""

import os

if "CELER_SIGHT_AI_HOME" in os.environ:
    os.chdir(os.environ["CELER_SIGHT_AI_HOME"])

from celer_sight_ai.gui.designer_widgets_py_files.aboutSection import (
    Ui_Form as aboutSectionUiForm,
)
import sys

import os
from celer_sight_ai import config


if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])

from PyQt6 import QtCore, QtGui, QtWidgets

import ctypes

import logging

logger = logging.getLogger(__name__)
logger.info("starting to import UiBlocks")

if os.name == "nt":
    from ctypes import wintypes
    import win32api
    import win32con
    import win32gui

    logger.info("imported win32api, win32con, win32gui")
    # from PyQt6.QtWinExtras import QtWin

# class StylesheetApplierClass(self):
from celer_sight_ai.gui.designer_widgets_py_files.MainWindowUi import (
    Ui_MainWindow,
)  # Mainwindow_pg1_v2 import Ui_MainWindow

logger.info("imported Ui_MainWindow")
from celer_sight_ai.gui.custom_widgets.scene import PhotoViewer

logger.info("imported PhotoViewer")
from celer_sight_ai.gui.custom_widgets.scene import (
    ColorPrefsPhotoViewer as ColorPrefsPhotoViewer,
)

logger.info("imported ColorPrefsPhotoViewer")
# from PyQt6.QtCore import pyqtSlot
import numpy as np

logger.info("imported numpy")
from celer_sight_ai.gui.custom_widgets.animate_qpushbutton import (
    QuickToolButton,
    myRichTextEdit,
    mainButtonsLeftScreen,
)

logger.info("imported QuickToolButton, myRichTextEdit, mainButtonsLeftScreen")

# Mainwindow_pg1_v1_class = Mainwindow_pg1_v1()
logger.info("Ui Blocks initialized")
# Turn off sina logging
for name in ["matplotlib", "matplotlib.font", "matplotlib.pyplot"]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.CRITICAL)
    logger.disabled = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.disabled = False
from celer_sight_ai import config


if os.name == "nt":

    class MINMAXINFO(ctypes.Structure):
        _fields_ = [
            ("ptReserved", wintypes.POINT),
            ("ptMaxSize", wintypes.POINT),
            ("ptMaxPosition", wintypes.POINT),
            ("ptMinTrackSize", wintypes.POINT),
            ("ptMaxTrackSize", wintypes.POINT),
        ]


def dwm_composition_enabled():
    import ctypes

    try:
        DWM_EC_COMPOSITION_ENABLED = ctypes.c_int(0)
        DwmIsCompositionEnabled = ctypes.windll.dwmapi.DwmIsCompositionEnabled
        DwmIsCompositionEnabled.restype = ctypes.HRESULT
        DwmIsCompositionEnabled.argtypes = [ctypes.POINTER(ctypes.c_int)]

        enabled = ctypes.c_int()
        result = DwmIsCompositionEnabled(ctypes.byref(enabled))

        if result == 0:  # S_OK
            return bool(enabled.value)
        else:
            raise Exception(
                "DwmIsCompositionEnabled returned a non-zero value: {}".format(result)
            )

    except Exception as e:
        print("Failed to check DWM composition state:", e)
        return False


class myMainWindow(QtWidgets.QMainWindow):
    BorderWidth = 5
    gripSize = 15  # only for windows with custom grips

    def __init__(self, mwUi=None):
        super(myMainWindow, self).__init__()
        self.mwUi = mwUi
        self.installEventFilter(self)
        self.controlWidget = None

        if os.name == "nt":
            # install custom grips for windows
            self.grip = QtWidgets.QSizeGrip(self)
            self.grip.resize(self.gripSize, self.gripSize)

        self._rect = QtWidgets.QApplication.instance().primaryScreen().geometry()

        self.setWindowFlags(
            # QtCore.Qt.Window
            # |
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowSystemMenuHint
            | QtCore.Qt.WindowType.WindowMinimizeButtonHint
            | QtCore.Qt.WindowType.WindowMaximizeButtonHint
            | QtCore.Qt.WindowType.WindowCloseButtonHint
        )
        if os.name == "nt":
            self.setWindowFlags(
                # QtCore.Qt.Window
                # |
                QtCore.Qt.WindowType.FramelessWindowHint
                | QtCore.Qt.WindowType.WindowSystemMenuHint
                | QtCore.Qt.WindowType.WindowMinimizeButtonHint
                | QtCore.Qt.WindowType.WindowMaximizeButtonHint
                | QtCore.Qt.WindowType.WindowCloseButtonHint
            )

    def extend_frame_into_client_area(self):
        self._set_extended_frame(-1, -1, -1, -1)

    def reset_extended_frame(self):
        self._set_extended_frame(0, 0, 0, 0)

    def _set_extended_frame(self, left, top, right, bottom):
        MARGINS = ctypes.c_int * 4

        DwmExtendFrameIntoClientArea = ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea
        DwmExtendFrameIntoClientArea.restype = ctypes.HRESULT
        DwmExtendFrameIntoClientArea.argtypes = [
            ctypes.wintypes.HWND,
            ctypes.POINTER(MARGINS),
        ]

        hwnd = self.winId().__int__()
        margins = MARGINS(left, top, right, bottom)
        DwmExtendFrameIntoClientArea(hwnd, margins)

    # def setMyWidth(self):
    #     """
    #     Sets the width of the grab/menu bar
    #     """
    #     if self.mwUi:
    #         myWidth = self.window().windowHandle().screen().size().width();
    #         # self.mwUi.controlWidget.emptySpace.setFixedWidth(
    #         #     max(myWidth-620, 100))
    #         selfmenubar.set.mwUi.FixedWidth(myWidth)

    def focusInEvent(self, event):
        self.mwUi.viewer.setFocus()
        return super(myMainWindow, self).focusInEvent(event)

    def extend_frame_into_client_area(self):
        # Define constants
        MARGINS = ctypes.c_int * 4
        DWMNCRENDERINGPOLICY = ctypes.c_int(2)
        DWMWA_NCRENDERING_POLICY = ctypes.c_int(2)

        # Load the necessary functions from dwmapi.dll
        DwmExtendFrameIntoClientArea = ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea
        DwmExtendFrameIntoClientArea.restype = ctypes.HRESULT
        DwmExtendFrameIntoClientArea.argtypes = [
            ctypes.wintypes.HWND,
            ctypes.POINTER(MARGINS),
        ]

        DwmSetWindowAttribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        DwmSetWindowAttribute.restype = ctypes.HRESULT
        DwmSetWindowAttribute.argtypes = [
            ctypes.wintypes.HWND,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_uint,
        ]

        # Call the DwmSetWindowAttribute function to enable non-client area rendering
        hwnd = self.winId().__int__()
        policy = DWMNCRENDERINGPOLICY(1)
        DwmSetWindowAttribute(
            hwnd, DWMWA_NCRENDERING_POLICY, ctypes.byref(policy), ctypes.sizeof(policy)
        )

        # Call the DwmExtendFrameIntoClientArea function to extend the frame
        margins = MARGINS(-1, -1, -1, -1)
        DwmExtendFrameIntoClientArea(hwnd, margins)

    def set_right_side_frame_images_geometry(self):
        # make sure that the conditions and preview images are always where they are supposed to be
        self.mwUi.right_side_frame_images.move(
            self.mwUi.Images.width() - self.mwUi.right_side_frame_images.width() - 10,
            10,
        )

        # TODO: add this back when local models are supported
        self.mwUi.right_side_frame_images.setFixedHeight(self.mwUi.Images.height() - 20)

    def set_ai_model_settings_widget_position(self):
        # This method moves the ai suggestion widget
        # to the appropriate location
        distance_from_bottom = 10
        if not self.mwUi.ai_model_settings_widget:
            return
        # set the proper position, which is middle of the widget , and distance_from_bottom from the bottom
        self.mwUi.ai_model_settings_widget.move(
            round(
                self.mwUi.Images.width() / 2
                - self.mwUi.ai_model_settings_widget.width() / 2
            ),  # center of the widget
            self.mwUi.Images.height()
            - self.mwUi.ai_model_settings_widget.height()
            - distance_from_bottom,
        )

    def move_top_level_mainwindow_edge_widgets_to_position(self):
        # move treatments and image / buttons to the right
        self.set_right_side_frame_images_geometry()

        # set suggested widget geomtry if visible
        try:
            self.set_ai_model_settings_widget_position()
            self.mwUi.DH.warningHandler.updateNotificationPositions()
        except:
            pass

        # if particle analysis is visible, adjust the ui for that
        if self.mwUi.viewer._is_particle_ui_spawned:
            if self.mwUi.viewer.particle_analysis_settings_widget.isVisible():
                self.mwUi.viewer.particle_analysis_settings_widget.resize_to_position()
        if os.name == "nt":
            rect = self.rect()
            self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
            self.grip.raise_()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)

        # move widgets on the right side and bottom side on the right position (distance from the right or bottom)
        self.move_top_level_mainwindow_edge_widgets_to_position()
        return super(myMainWindow, self).resizeEvent(event)

    def eventFilter(self, source, event):

        if type(event) == QtCore.QEvent:
            # if its left mouse click only set the initial position
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    self.move_window_dragPosition = event.globalPosition()
                    return super(myMainWindow, self).eventFilter(source, event)
            if hasattr(self, "move_window_dragPosition"):
                # get mouse move event only when left button is pressed
                if (
                    event.type() == QtCore.QEvent.Type.MouseMove
                    and event.buttons() == QtCore.Qt.MouseButton.LeftButton
                ):
                    self.move(
                        self.pos()
                        + event.globalPosition()
                        - self.move_window_dragPosition
                    )
                    self.move_window_dragPosition = event.globalPosition()
                    return True
                # on double click maximize
                if event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
                    if event.button() == QtCore.Qt.MouseButton.LeftButton:
                        if self.isMaximized():
                            self.showNormal()
                        else:
                            self.showMaximized()
                        return True
            return super(myMainWindow, self).eventFilter(source, event)

        return False


class AnotherWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        # set size
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.setMinimumHeight(36)
        self.setMinimumWidth(56)
        # self.button = QPushButton("EXIT", clicked=app.exit)
        self.minimizebtn = QtWidgets.QPushButton("minimizebtn")
        self.maximizebtn = QtWidgets.QPushButton("maximizebtn")
        self.closebtn = QtWidgets.QPushButton("closetbn")
        self.emptySpace = QtWidgets.QWidget()
        self.minimizebtn.setText("")
        self.closebtn.setText("")
        self.maximizebtn.setText("")
        self.closebtn.setObjectName("mainCloseBtn")
        nS = QtCore.QSize(56, 36)

        self.minimizebtn.setMinimumSize(nS)
        self.closebtn.setMinimumSize(nS)
        self.maximizebtn.setMinimumSize(nS)
        self.minimizebtn.setMaximumSize(nS)
        self.closebtn.setMaximumSize(nS)
        self.maximizebtn.setMaximumSize(nS)
        self.setStyleSheet("border-radius:1px;")
        self.setAutoFillBackground(True)
        self.emptySpace.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        # custom property to check in native event
        self.emptySpace.isCornerWidget_cs = True
        self.emptySpace.setParent(self)
        self.emptySpace.setStyleSheet("background-color:rgba(244,0,0,0);")
        self._layout.addWidget(self.emptySpace)
        self._layout.addWidget(self.minimizebtn)
        self._layout.addWidget(self.maximizebtn)
        self._layout.addWidget(self.closebtn)

        self.setLayout(self._layout)


class CelerSightMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CelerSightMainWindow, self).__init__(parent)
        self.MainWindow = None
        # move window event functions
        self.move_window_status = False
        self.dragPosition = None

        # Set body parts bariables for buttons during startup
        self.WholeBodyBtn = None
        self.EmbryoBtn = None
        self.HeadBtn = None
        self.IntenstineBtn = None
        self.MuscleBtn = None
        self.SeamBtn = None
        self.GenericCellBtn = None
        self.ScratchAssaybtn = None
        self.Abnormalities_Detection_button = None
        self.Pneumothorax_Detection_button = None
        self.WholeBodyFliesBtn = None
        self.ai_model_settings_widget = None

        self.new_category_pop_up_widget = (
            None  # placeholder for the new category pip up widget
        )
        self.contribute_images_widget = None  # widget to provide images for training.

        if QtWidgets.QApplication.primaryScreen().size().height() < 1000:
            config.IS_SMALL_SCREEN = True
        else:
            config.IS_SMALL_SCREEN = False

    def SetupAll(self):
        """
        This function makes an instant of the Mainwinow and sets everything up
        """

        # Hide elements not allowed by user config
        from celer_sight_ai import config

        self.MainWindow = myMainWindow(mwUi=self)  # QtWidgets.QMainWindow()

        # self.FramelessWindow = QtWidgets.QWidget()
        self.currentTabIndexBtns = 0
        # self.FramelessWindow.set (self.MainWindow)
        # self.FramelessWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint);
        logger.info("before settings up main window")
        self.setupUi(self.MainWindow)
        logger.info("after setting up main window")
        self.tutorialCompleted = False

        from celer_sight_ai.gui.custom_widgets.custom_list_widgets import RNAiListWidget

        self.RNAi_list = RNAiListWidget(self.Conditions_frame, self)
        self.gridLayout_10.addWidget(
            self.RNAi_list, 1, 0, 1, 8
        )  # --> layout for Conditions_frame

        # Top right widget that allows the user to select a Pro or Lite model.
        # Pro models run on the cloud and have higher performace.
        # from celer_sight_ai.gui.pro_lite_model_toggle_component import AnimatedToggleButton
        # self.model_pro_lite_toggle_button = AnimatedToggleButton(self.MainWinowFrame , ["Pro" , "Lite"])
        # TODO: add this back later when local models are supported

        # # patch the eventFilter of the top_bar so that it moves when we move it
        self.top_bar.installEventFilter(self.top_bar)
        self.top_bar.mouseMoveEvent = self.mouseMoveEvent_top_bar
        self.top_bar.mousePressEvent = self.mousePressEvent_top_bar
        self.top_bar.mouseReleaseEvent = self.mouseReleaseEvent_top_bar
        self.top_bar.mouseDoubleClickEvent = self.mouseDoubleClickEvent_top_bar
        self.top_bar.setMouseTracking(True)

        # Add a tool button to create new categories on the region selection frame
        self.new_category_button = QtWidgets.QToolButton(self.FrameRegionSelection)
        self.new_category_button.move(10, 10)
        self.new_category_button.setFixedSize(70, 30)

        # Center the text and icon on the button

        # Set the plus icon directly on the QToolButton
        plus_icon = QtGui.QIcon(
            os.path.join(os.environ["CELER_SIGHT_AI_HOME"], "data/icons/plus_icon.png")
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
            lambda: self.spawn_create_new_category_dialog_on_organism_selection()
        )

        if os.name == "nt":
            # rename control widget
            self.controlWidget = self.top_bar

            self.menubar.setParent(None)
            self.menubar.setParent(self.top_bar)
            self.menubar.setMinimumWidth(200)
            self.horizontalLayout.removeWidget(self.top_btns)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum,
                QtWidgets.QSizePolicy.Policy.Maximum,
            )
            self.menubar.setSizePolicy(sizePolicy)
            self.horizontalLayout.addWidget(self.menubar)
            self.menuSpaceWidget = QtWidgets.QWidget()
            self.menuSpaceWidget.setStyleSheet("background-color:rgba(0,0,0,0);")
            self.menuSpaceWidget.setObjectName("menuSpaceWidget")
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
            self.menuSpaceWidget.setSizePolicy(sizePolicy)
            self.horizontalLayout.addWidget(self.menuSpaceWidget)
            self.horizontalLayout.addWidget(self.top_btns)

        self.actionSave_as.triggered.connect(lambda: self.save_celer_sight_file())

        self.actionSave_current_image.triggered.connect(
            lambda: self.saveCurrentImageGraphicsView()
        )
        self.actionSave.triggered.connect(lambda: self.save_celer_sight_file_decider())
        self.actionSave.setShortcut(QtGui.QKeySequence.StandardKey.Save)
        self.actionOpen.triggered.connect(lambda: self.load_celer_sight_file())

        self.actionZoom_in.triggered.connect(lambda: self.viewer.zoom_in())
        self.actionZoom_out.triggered.connect(lambda: self.viewer.zoom_out())
        # set current index to
        self.stackedWidget.setCurrentWidget(self.orgSelectionSection)

        self.MyVisualPlotHandler = None
        self.screenResolution = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry()
        )

        self.actionAbout_CelerSight.triggered.connect(lambda: self.execAboutDialog())
        self.actionimages.triggered.connect(
            lambda: self.myButtonHandler.import_images_with_file_dialog()
        )

        self.actionExport_to_COCO.triggered.connect(lambda: self.ExportCOCOTools())
        self.actionimport_from_coco.triggered.connect(lambda: self.import_coco_tools())

        self.actionSend_for_training.triggered.connect(
            self.launch_dialog_to_send_for_training
        )
        # Set up viewer
        logger.debug("Setting up viewer")
        self.viewer = PhotoViewer(self)  # Create an instance of the photoviwer
        self.viewer.viewport().installEventFilter(self)
        self.viewer.setMouseTracking(True)
        self.viewer.setAcceptDrops(True)
        self.ColorPrefsViewer = ColorPrefsPhotoViewer(self)
        self.ExtendUi()

        self.aboutCelerSightDialog = None

        # Add icons to toolbar
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("data/icons/draw_polygon.PNG"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("data/icons/icons_aa_tool/Assisted_line_on.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("data/icons/Selection(CHANGE THIS).png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )

        self.PolygonTool.triggered.connect(lambda: self.viewer.update_tool("polygon"))
        self.PolygonTool.triggered.connect(lambda: self.ApplyUiSelectionBtn("polygon"))
        self.actionAutoTool.triggered.connect(lambda: self.viewer.update_tool("auto"))
        self.actionAutoTool.triggered.connect(lambda: self.ApplyUiSelectionBtn("auto"))

        self.actionRF_MODE.triggered.connect(
            lambda: self.viewer.update_tool("RF_MODE_BINARY")
        )
        self.actionRF_MODE.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("RF_MODE_BINARY")
        )

        self.previous_clicked_class_widget = None

        self.actionRemoveSelectionTool.triggered.connect(
            lambda: self.viewer.update_tool("CELL_SPLIT_SEED")
        )
        self.actionRemoveSelectionTool.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("CELL_SPLIT_SEED")
        )

        self.actionKeypoint.triggered.connect(
            lambda: self.viewer.update_tool("keypoint_tool")
        )
        self.actionKeypoint.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("keypoint_tool")
        )

        self.actionErraseTool.triggered.connect(
            lambda: self.viewer.update_tool("erraseTool")
        )
        self.actionErraseTool.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("erraseTool")
        )

        self.actionSelectionTool.triggered.connect(
            lambda: self.viewer.update_tool("selection")
        )
        self.actionSelectionTool.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("selection")
        )
        self.MagicBrushMoveTool.triggered.connect(
            lambda: self.viewer.update_tool("magic_brush_move")
        )
        self.MagicBrushMoveTool.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("magic_brush_move")
        )
        self.actionMakeSpline.triggered.connect(
            lambda: self.viewer.update_tool("skeleton grabcut")
        )
        self.actionMakeSpline.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("skeleton grabcut")
        )
        self.actionBrushMask.triggered.connect(
            lambda: self.viewer.update_tool("brushMask")
        )
        self.actionBrushMask.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("brushMask")
        )
        self.actionKeypoint.triggered.connect(
            lambda: self.ApplyUiSelectionBtn("keypoint")
        )
        self.actionSet_Scale.triggered.connect(lambda: self.execScaleDialog())
        self.actionSelectionTool.setChecked(True)

        self.viewer.update_tool("selection")
        self.ApplyUiSelectionBtn("selection")

        self.pg1_Entity_btn.clicked.connect(lambda: self.ExecNewOrg())
        self.pg1_Analysis_btn.clicked.connect(lambda: self.ChangeAnalysisSettings())
        self.pg1_Network_btn.clicked.connect(lambda: self.ChangeAnalysisSettings())

        # self.toolBar.setOrientation(QtCore.Qt.Orientation.Vertical )
        self.toolBar.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self.toolBar.move(100, 100)
        self.toolBar.adjustSize()
        self.toolBar.show()
        self.add_images_btn.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )

        self.pg1_red_channel_button_visual.setCheckable(True)
        self.pg1_green_channel_button_visual.setCheckable(True)
        self.pg1_blue_channel_button_visual.setCheckable(True)

        self.pg1_red_channel_button_visual.clicked.connect(
            lambda: self.load_main_scene(self.current_imagenumber)
        )
        self.pg1_green_channel_button_visual.clicked.connect(
            lambda: self.load_main_scene(self.current_imagenumber)
        )
        self.pg1_blue_channel_button_visual.clicked.connect(
            lambda: self.load_main_scene(self.current_imagenumber)
        )

        self.pg1_red_channel_button_visual.setChecked(False)
        self.pg1_green_channel_button_visual.setChecked(False)
        self.pg1_blue_channel_button_visual.setChecked(False)
        #
        # self.add_images_btn.clicked.connect(lambda: QtWidgets.QApplication.processEvents())
        #

        self.pg2_savegraph_btn.clicked.connect(lambda: self.saveCurrentGraph())

        # self.canvas.setMinimumSize(QtCore.QSize(116, 700)) # TODO: maybe change this?
        #
        # SetUp New window that selects the analysis type, organism etc
        #

        # isntall organism selction class to the stackedWidget
        from celer_sight_ai.NewAnalysisSetUp import NewAnalysis, organismSelectionClass

        self.organism_selection = organismSelectionClass(self)
        self.organism_selection.myDialog.setParent(self.orgSelectionSection)
        self.gridLayout_orgSelectionSection.addWidget(
            self.organism_selection.myDialog, 0, 0, 1, 1
        )
        self.new_analysis_object = NewAnalysis(self)

        # check if the user has a small screen, if so adjust the size of the buttons accdingly

        if config.IS_SMALL_SCREEN:
            logger.info(
                "Small screen detected, adjusting button sizes and maximizing screen"
            )
            # for widget in
            all_entity_buttons = [
                i
                for i in self.organism_selection.mainframe.children()
                if type(i) == QtWidgets.QPushButton
            ]
            for button in all_entity_buttons:
                button.setMinimumSize(QtCore.QSize(220, 400))
                button.setMaximumSize(QtCore.QSize(220, 400))
            # trigger full screen mode
            self.MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMaximized)

        self.actionSet_Scale.setVisible(False)
        self.actionBrightness_and_Contrast.setVisible(False)

        if not config.user_cfg.ALLOW_ACTION_NEW:
            self.actionNew.setEnabled(False)
            self.actionNew.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_OPEN:
            self.actionOpen.setEnabled(False)
            self.actionOpen.setVisible(False)
        if not config.user_cfg.ALLOW_MENU_OPEN_AS:
            self.menuOpen_as.setEnabled(False)
            self.menuOpen_as.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_CLOSE:
            self.actionClose.setEnabled(False)
            self.actionClose.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_SAVE:
            self.actionSave.setEnabled(False)
            self.actionSave.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_SAVE_AS:
            self.actionSave_as.setEnabled(False)
            self.actionSave_as.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_PRINT:
            self.actionPrint.setEnabled(False)
            self.actionPrint.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_SEND_FOR_TRAINING:
            self.actionSend_for_training.setEnabled(False)
            self.actionSend_for_training.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_IMPORT_FROM_COCO:
            self.actionimport_from_coco.setEnabled(False)
            self.actionimport_from_coco.setVisible(False)
        if not config.user_cfg.ALLOW_ACTION_EXPORT_TO_IMAGEJ:
            self.actionExport_to_imagej.setEnabled(False)
            self.actionExport_to_imagej.setVisible(False)
        if not config.user_cfg.ALLOW_MENU_MODELS:
            self.menuModels.setEnabled(False)
            self.menuModels.setVisible(False)
        if not config.user_cfg.ALLOW_MENU_WORKFLOW:
            self.menuSample.setEnabled(False)
            self.menuSample.setVisible(False)
        if not config.user_cfg.ALLOW_MENU_IMAGE:
            self.menuImage.setEnabled(False)
            self.menuImage.setVisible(False)
        if not config.user_cfg.ALLOW_MENU_VIEW:
            self.menuView.setEnabled(False)
            self.menuView.setVisible(False)
        if not config.user_cfg.ALLOW_ABOUT:
            self.actionAbout_CelerSight.setEnabled(False)
            self.actionAbout_CelerSight.setVisible(False)
        if not config.user_cfg.ALLOW_SEND_LOGS:
            self.actionSend_logs_to_dev.setEnabled(False)
            self.actionSend_logs_to_dev.setVisible(False)
        if not config.user_cfg.ALLOW_PREFERENCES:
            self.actionPreferences.setEnabled(False)
            self.actionPreferences.setVisible(False)
        if not config.user_cfg.ALLOW_SUBMIT_ANNOTATIONS_ADMIN:
            self.actionsubmit_annotations_admin.setEnabled(False)
            self.actionsubmit_annotations_admin.setVisible(False)

        if not config.user_cfg.ALLOW_IMPORT_IMAGES_BUTTON:
            self.add_images_btn.setEnabled(False)

        self.viewer.QuickTools.RandomForestCellModeFrame.hide()
        self.pg1_settings_groupBox_analysis.hide()
        self.verticalLayout_5.addSpacerItem(
            QtWidgets.QSpacerItem(
                100,
                1,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
        )
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)

        from celer_sight_ai.gui.custom_widgets.PDModel import CustomTableView

        self.all_condition_analysis_table = CustomTableView(self)
        self.all_conditions.layout().addWidget(self.all_condition_analysis_table)

        self.reimplimentActionsForQuickTools()
        self.addConnections()

        # place the modern qcombobox in the data section
        from celer_sight_ai.gui.custom_widgets.modern_qcombobox_widgets import (
            ModernSearchableQComboBox,
            CustomComboBoxWithIcons,
        )

        old_combobox = self.Results_pg2_AnalysisTypeComboBox
        self.Results_pg2_AnalysisTypeComboBox = ModernSearchableQComboBox(self)
        self.horizontalLayout_data_buttons.replaceWidget(
            old_combobox, self.Results_pg2_AnalysisTypeComboBox
        )
        old_combobox.deleteLater()
        old_combobox.hide()
        old_combobox.setParent(None)

        # exchange old with new channel combobox widget
        old_combobox2 = self.channel_analysis_metrics_combobox
        self.channel_analysis_metrics_combobox = ModernSearchableQComboBox(self)
        self.horizontalLayout_data_buttons.replaceWidget(
            old_combobox2, self.channel_analysis_metrics_combobox
        )
        old_combobox2.deleteLater()
        old_combobox2.hide()
        old_combobox2.setParent(None)

        # change Roi combobox with a modern qcombobox

        old_combobox3 = self.ROI_analysis_metrics_combobox
        self.ROI_analysis_metrics_combobox = ModernSearchableQComboBox(self)
        self.horizontalLayout_data_buttons.replaceWidget(
            old_combobox3, self.ROI_analysis_metrics_combobox
        )
        old_combobox3.deleteLater()
        old_combobox3.hide()
        old_combobox3.setParent(None)

        # self.bottom_menus.setContentsMargins(0, 0, 0, 0)

        # Set up Fillers for QuickTools to Hide to Side
        from celer_sight_ai.gui.designer_widgets_py_files.quickToolStickAreaForm import (
            Ui_Form as quickToolsUiFormHide,
        )

        self.verticalQuickToolsSpotForm = quickToolsUiFormHide()
        self.horizontalQuickToolsSpotForm = quickToolsUiFormHide()
        self.verticalQuickToolsSpotForm.myWidget = QtWidgets.QWidget(self.viewer)
        self.horizontalQuickToolsSpotForm.myWidget = QtWidgets.QWidget(self.viewer)
        self.verticalQuickToolsSpotForm.setupUi(
            self.verticalQuickToolsSpotForm.myWidget
        )
        self.horizontalQuickToolsSpotForm.setupUi(
            self.horizontalQuickToolsSpotForm.myWidget
        )
        self.verticalQuickToolsSpotForm.myWidget.setFixedWidth(80)
        self.verticalQuickToolsSpotForm.myWidget.setFixedHeight(600)
        self.horizontalQuickToolsSpotForm.myWidget.setFixedWidth(600)
        self.horizontalQuickToolsSpotForm.myWidget.setFixedHeight(80)
        self.verticalQuickToolsSpotForm.myWidget.hide()
        self.horizontalQuickToolsSpotForm.myWidget.hide()

        self.classes_listWidget_left_main.parent().layout().removeWidget(
            self.classes_listWidget_left_main
        )
        self.classes_listWidget_left_main.setParent(None)

        self.classes_listWidget_left_main.deleteLater()
        self.classes_listWidget_left_main = None
        from celer_sight_ai.gui.custom_widgets.custom_list_widgets import (
            CustomClassListWidget,
        )

        self.custom_class_list_widget = CustomClassListWidget(
            self.pg1_settings_groupBox_classes, self
        )
        self.pg1_settings_groupBox_classes.layout().addWidget(
            self.custom_class_list_widget, 2, 0, 1, 2
        )
        self.custom_class_list_widget.itemClicked.connect(
            lambda: self.record_class_item_on_widget_click()
        )
        self.custom_class_list_widget.itemChanged.connect(
            lambda: self.update_class_items_widgets_on_change()
        )
        self.custom_class_list_widget.currentRowChanged.connect(
            lambda: self.updateClassColor_onIndexChange()
        )

        #
        # Set Up custom WIndow Borders, top
        #
        # self.ModernizeWindow()
        from celer_sight_ai import config

        config.global_signals.check_data_corruption_signal.connect(
            self.check_data_corruption
        )

        config.global_signals.updateIconsToolboxSignal.connect(
            lambda: self.setUpIconsQuickTools()
        )

        # self.setUpIconsQuickTools()

        from celer_sight_ai.gui.custom_widgets.burger_settings_button import (
            burger_settings_button,
        )

        self.burger_settings_button = burger_settings_button(self.viewer)
        self.burger_settings_button.move(10, 33)
        self.burger_settings_button.clicked.connect(
            lambda: self.handle_burger_settings_click()
        )

        from celer_sight_ai.config import MagicToolModes
        from celer_sight_ai.core.magic_box_tools import sdknn_tool

        # sdknn is used for the interactive / local ai inference
        self.sdknn_tool = sdknn_tool(self)
        # add ai model model top left with a qcombobox
        self.ai_model_combobox = CustomComboBoxWithIcons(self)
        self.ai_model_combobox.setObjectName("ai_model_combobox")
        self.ai_model_combobox.setFixedWidth(150)

        self.ai_model_combobox.addItem(
            "Magic ROI (S)",
            icon_path="data/icons/magic_star_icon.png",
            label_icon_width=15,
            mode=MagicToolModes.MAGIC_BOX_ROI_FINETUNE,
        )

        self.ai_model_combobox.addItem(
            "Magic ROI (G)",
            icon_path="data/icons/magic_star_icon.png",
            label_icon_width=15,
            mode=MagicToolModes.MAGIC_BOX_ROI_GENERIC,
        )

        self.ai_model_combobox.addItem(
            "Magic ROI Plus",
            icon_path="data/icons/suggested_ROI_icon.png",
            label_icon_width=30,
            mode=MagicToolModes.MAGIC_BOX_WITH_PREDICT,
        )

        self.ai_model_combobox.setIndexAsSelected(1)

        # add it on the main window, on the same height as the MasterTabWidgets
        pos = self.MasterTabWidgets.pos()
        self.ai_model_combobox.setParent(self.MainWinowFrame)
        self.ai_model_combobox.move(pos.x() + 4, pos.y() + 2)
        self.ai_model_combobox.hide()  # only show when the magic tool is selected
        self.ai_model_combobox.selectionChanged.connect(
            lambda: self.ai_model_settings_widget.update_visible()
        )
        from celer_sight_ai.mask_suggestion_widget import AnnotationAssistantWidget

        self.ai_model_settings_widget = AnnotationAssistantWidget(
            parent=self.Images,
            MainWindow=self.MainWindow,
            # initial_image_similarity_value =
        )
        self.ai_model_settings_widget.setMaximumWidth(350)
        self.ai_model_settings_widget.hide()

        # Hover for the group_pg1_left
        self.group_pg1_left.setParent(self.Images)
        self.gridLayout_images.removeWidget(self.group_pg1_left)
        self.group_pg1_left.show()
        self.group_pg1_left.move(0, 60)
        self.group_pg1_left.setFixedWidth(143)
        self.group_pg1_left.setFixedHeight(1000)
        self.group_pg1_left.raise_()
        self.group_pg1_left.setStyleSheet(
            """
            background-color: rgba(0,0,0,0);
            """
        )

        # hover for conditions and preview images
        right_side_frame_images_pos = self.right_side_frame_images.pos()
        self.right_side_frame_images.setParent(self.Images)
        self.gridLayout_images.removeWidget(self.right_side_frame_images)
        self.right_side_frame_images.show()
        self.right_side_frame_images.move(
            right_side_frame_images_pos.x(), right_side_frame_images_pos.y()
        )

        self.scrollArea_analysis_tools.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scrollArea_analysis_tools.verticalScrollBar().hide()
        self.scrollArea_analysis_tools.verticalScrollBar().resize(0, 0)

        self.SetUpButtons()
        self.viewer.QuickTools.videowidget.transformToBorderWidget(
            self.group_pg1_left.width(), 60
        )

        self.pg1_ML_advanced_minSpinBox.valueChanged.connect(
            lambda: self.FilterMinArea_ML_RF()
        )
        self.viewer.ML_brush_tool_object = None
        self.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.currentIndexChanged.connect(
            lambda: self.recalc_Featurs_by_MODE_ML()
        )
        self.pg1_ML_EXCLUDE_QUALITY_COMBOBOX.setCurrentIndex(1)
        # self.QuickTools.videowidget.move(50,50)
        self.g1_ML_settings_groupBox.hide()
        # Medical ai hide :
        self.pg1_MedicalAiHintsToolbox.hide()

        ####################################
        ## Set up Tabs on the main window ##
        ####################################

        tab_width_scale = 150

        icon3 = QtGui.QIcon()
        pixmap_off = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/imageTabv2_off.png"
            )
        )
        pixmap_off = pixmap_off.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        pixmap_on = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/imageTabv2_on.png"
            )
        )
        pixmap_on = pixmap_on.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        icon3.addPixmap(
            pixmap_off,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon3.addPixmap(
            pixmap_on,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        # scale icon
        self.MasterTabWidgets.setTabIcon(0, icon3)
        pixmap_off = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/dataTabv2_off.png"
            )
        )
        pixmap_off = pixmap_off.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        pixmap_on = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/dataTabv2_on.png"
            )
        )
        pixmap_on = pixmap_on.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            pixmap_off,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon3.addPixmap(
            pixmap_on,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.MasterTabWidgets.setTabIcon(1, icon3)
        pixmap_off = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/plotTabv2_off.png"
            )
        )
        pixmap_off = pixmap_off.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        pixmap_on = QtGui.QPixmap(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/plotTabv2_on.png"
            )
        )
        pixmap_on = pixmap_on.scaledToWidth(
            tab_width_scale, QtCore.Qt.TransformationMode.SmoothTransformation
        )
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            pixmap_off,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon3.addPixmap(
            pixmap_on,
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.MasterTabWidgets.setTabIcon(2, icon3)

        ##########################################################################
        #######  Set up Main Widget Left buttons -> Home , Info , Settings #######
        ##########################################################################

        # replace button
        self.HomeButtonMain = mainButtonsLeftScreen(self.top_menus)
        self.top_menus.layout().addWidget(
            self.HomeButtonMain, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.InfoButtonMain = mainButtonsLeftScreen(self.top_menus)
        self.top_menus.layout().addWidget(
            self.InfoButtonMain, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.SettingsButtonMain = mainButtonsLeftScreen(self.top_menus)
        self.top_menus.layout().addWidget(
            self.SettingsButtonMain, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.top_menus.layout().addStretch()

        home_button_non_selection_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/home_button_non_hover_non_selection_icon.png",
                )
            )
        )
        home_button_non_selection = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/home_button_non_hover_icon.png",
                )
            )
        )
        home_button_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/home_button_non_selection_icon.png",
                )
            )
        )

        info_button_non_selection_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/info_button_non_hover_non_selection_icon.png",
                )
            )
        )
        info_button_non_selection = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/info_button_hover_icon.png",
                )
            )
        )
        info_button_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/info_button_non_selection_icon.png",
                )
            )
        )

        settings_button_non_selection_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/settings_button_non_hover_non_selection_icon.png",
                )
            )
        )
        settings_button_non_selection = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/settings_button_hover_icon.png",
                )
            )
        )
        settings_button_non_hover = QtGui.QIcon(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/viewport/settings_button_non_selection_icon.png",
                )
            )
        )

        self.HomeButtonMain.setIcons(
            home_button_non_selection_non_hover,
            home_button_non_selection,
            home_button_non_hover,
        )
        self.InfoButtonMain.setIcons(
            info_button_non_selection_non_hover,
            info_button_non_selection,
            info_button_non_hover,
        )
        self.SettingsButtonMain.setIcons(
            settings_button_non_selection_non_hover,
            settings_button_non_selection,
            settings_button_non_hover,
        )
        # always switch to HomeButtonMain when starting the app
        self.HomeButtonMain.click()
        # ADD DROP SHADOW
        # ///////////////////////////////////////////////////////////////
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self.MainWindow)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 80))

        self.SettingsButtonMain.clicked.connect(
            lambda: self.new_analysis_object.updateSettings()
        )

        from celer_sight_ai import config

        self.CreateNewVButton_proceed.clicked.connect(
            lambda: self.create_new_enviroment_with_category()
        )

        self.CreateNewVButton_Back.clicked.connect(lambda: self.ExecNewOrg())

        self.HomeButtonMain.clicked.connect(lambda: self.home_button_click_handle())

        self.InfoButtonMain.clicked.connect(
            lambda: self.app_pages.setCurrentWidget(self.InfoPage)
        )
        self.InfoButtonMain.clicked.connect(lambda: self.update_user_info())
        # TODO: implement settings page
        self.SettingsButtonMain.hide()
        self.SettingsButtonMain.clicked.connect(
            lambda: self.app_pages.setCurrentWidget(self.SettingsPage)
        )

        self.SettingsButtonMain.clicked.connect(
            lambda: self.new_analysis_object.updateSettings()
        )
        self.InfoButtonMain.clicked.connect(
            lambda: self.new_analysis_object.updateSettings()
        )
        self.InfoButtonMain.clicked.connect(
            lambda: self.new_analysis_object.updateSettings()
        )

        self.viewer.QuickTools.BrushRadiusCellRandomForestSlider.setValue(
            self.loadSetting("BrushRadiusCellRandomForestSlider", 10)
        )
        self.pg1_ML_advanced_live_on_radiobutton.setChecked(
            self.loadSetting("pg1_ML_advanced_live_on_radiobutton", True)
        )

        self.pg1_ML_advanced_live_on_radiobutton.setChecked(
            self.loadSetting("pg1_ML_FILL_HOLES_RADIOBUTTON", True)
        )
        self.menubar.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.menubar.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.menubar.setStyleSheet(
            """
            QWidget{
                background-color: rgb(255,0,0);
            }                
            QMenuBar{
            font:"Lato";
            font-size: 13px;
            border: 0px solid;

            color: rgb(230,230,230);
            background-color:rgb(0,0,0);
            }

            
            QMenuBar::item{
                border: 0px solid;
                color: rgb(170,170,170);
                padding:4px;  
                padding-bottom:2px;  
                padding-top:2px;
                padding-left:10px;
                padding-right:10px;
                background-color: rgba(0,0,0,0);
            }
            QMenuBar::item:selected{
                color: rgb(230,230,230);
                background-color:rgb(55,55,55);
                border-radius:3px;
                border:0px solid;
            }  
            QMenu{
                border: 0px solid;
                border-radius: 10px;
                padding:5px;
                background-color: rgb(55,55,55);
            }
            
            QMenu::item{
                color: rgb(240,240,240);
                font:"Lato";
                font-size: 12px;
                padding-bottom:5px;  
                padding-top:5px;
                padding-left:20px;
                padding-right:20px;
                background-color: rgba(0,0,0,0);
            }
            QMenu::item:selected{
                color: rgb(230,230,230);
                background-color:rgb(75,75,75);
                border-radius:3px;
                border:0px solid;
            }  
            """
        )
        self.pg1_settings_groupBox_classes.setStyleSheet(
            "QGroupBox::title#pg1_settings_groupBox_classes{"
            "    margin-top:1px;"
            "    padding: 6px ;"
            "    padding-right:42px;"
            "    padding-left:24px;"
            "}"
        )

        import matplotlib
        import matplotlib.font_manager as font_manager

        listTTF = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
        listAFM = [f.name for f in matplotlib.font_manager.fontManager.afmlist]
        if not listAFM:
            allFonts = listTTF
        elif not listTTF:
            allFonts = listAFM
        else:
            allFonts = sorted(set(listTTF + listAFM))
        # logger.info(allFonts)
        for font in allFonts:
            self.fontComboBox.addItem(font)
        try:
            self.fontComboBox.setCurrentText("Helvetica")
        except:
            self.fontComboBox.setCurrentIndex(0)

        self.viewer.setStyleSheet(
            """
            QGraphicsView{
            border: 0px solid;
            border-radius:0px;
            border-color: rgb(45,45,45);
            background-color:  rgb(45,45,45);
            }
            """
        )

        # this is to close the project
        # an action on the top menu bar

        self.actionClose.triggered.connect(self.quit_project)
        self.actionNew.triggered.connect(self.quit_project)

        self.btnMinimize.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btnMaximize.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btnClose.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # connect close, minimize and maximize sigals
        config.global_signals.close_celer_sight_signal.connect(self.closeApp)
        config.global_signals.minimize_celer_sight_signal.connect(
            self.on_minimizedClicked
        )
        config.global_signals.maximize_celer_sight_signal.connect(
            self.on_btnMaximize_clicked
        )

        self.btnClose.clicked.connect(lambda: self.closeApp())
        self.btnMaximize.clicked.connect(lambda: self.on_btnMaximize_clicked())
        self.btnMinimize.clicked.connect(lambda: self.on_minimizedClicked())

        # self.viewer._scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(245,45,45), QtCore.Qt.BrushStyle.SolidPattern))

        my_font = QtGui.QFont("Lato", 12)
        # my_font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        # font_db = QtGui.QFontDatabase.addApplicationFont("data/font/Lato/Lato-Regular.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(
            "data/font/Lato/Lato-Regular.ttf"
        )

        # first refresh of viewer, loads the drag and drop background image
        self.load_main_scene()

    def update_user_info(self):
        logger.info("Updating user info")
        from celer_sight_ai import config, __version__

        cloud_credentials = config.cloud_user_variables

        if cloud_credentials and cloud_credentials.get("licenseID"):
            self.Licence_label_value.setText(
                cloud_credentials.get("licenseID", {}).get("license_type", "free")
            )
        self.AppVersion_label.setText(str(__version__))

    def spawn_create_new_category_dialog_on_main_scene(self):
        """
        Spawns a dialog for creating a new category.

        This method creates a new instance of NewCategoryWidget and displays it
        centered on the parent window. If a previous instance exists, it is closed
        before creating a new one.
        """
        from celer_sight_ai.gui.custom_widgets.category_and_contribution_widgets import (
            NewCategoryWidget,
        )

        # Close any existing new category dialog
        if self.new_category_pop_up_widget:
            self.new_category_pop_up_widget.close()

        # Create a new instance of NewCategoryWidget
        self.new_category_pop_up_widget = NewCategoryWidget(
            self.Images  # Pass the images widget as parent
        )

        # Center the new category dialog on the parent window
        self.new_category_pop_up_widget.title_hat.move(
            self.stackedWidget.geometry().center()
            - self.new_category_pop_up_widget.title_hat.geometry().center()
        )

    def spawn_create_new_category_dialog_on_organism_selection(self):
        """
        Spawns a dialog for creating a new category.

        This method creates a new instance of NewCategoryWidget and displays it
        centered on the parent window. If a previous instance exists, it is closed
        before creating a new one.
        """
        logger.info("Spawn new category dialog on organism selection")
        from celer_sight_ai.gui.custom_widgets.category_and_contribution_widgets import (
            NewCategoryWidget,
        )

        # Close any existing new category dialog
        if self.new_category_pop_up_widget:
            self.new_category_pop_up_widget.close()

        # Create a new instance of NewCategoryWidget
        self.new_category_pop_up_widget = NewCategoryWidget(
            self.chat  # Pass the images widget as parent
        )

        # Center the new category dialog on the parent window
        self.new_category_pop_up_widget.title_hat.move(
            self.stackedWidget.geometry().center()
            - self.new_category_pop_up_widget.title_hat.geometry().center()
        )

    def handle_burger_settings_click(self):
        button_state = self.burger_settings_button.is_on()
        logger.debug(f"handle_burger_settings_click {button_state}")
        if button_state:
            # hide the self.group_pg1_left widget
            self.group_pg1_left.hide()
            self.viewer.QuickTools.myquickToolsWidget.move(
                0, self.viewer.QuickTools.myquickToolsWidget.pos().y()
            )
        else:
            # show self.group_pg1_left widget
            self.group_pg1_left.show()
            self.viewer.QuickTools.myquickToolsWidget.move(
                self.group_pg1_left.width(),
                self.viewer.QuickTools.myquickToolsWidget.pos().y(),
            )

    def home_button_click_handle(self):
        """If we have created an expiriment , just show the main page, otherwise show the part and analysis selection window"""
        if self.current_home_display_widget == self.chat:
            self.app_pages.setCurrentWidget(self.chat)
        elif self.current_home_display_widget == self.MainInterface:
            self.stackedWidget.setCurrentWidget(self.MainInterface)
            # set focus to scene
            self.viewer.setFocus()
        else:
            self.stackedWidget.setCurrentWidget(self.orgSelectionSection)

    def mouseDoubleClickEvent_top_bar(self, event):
        """
        Repleacement for the traditional tittle bar double click event, if we are maximized then switch to windowed,
        else form windowed to maximized

        """
        if self.MainWindow.isMaximized():
            self.MainWindow.showNormal()
        else:
            self.MainWindow.showMaximized()
        return super(QtWidgets.QFrame, self.top_bar).mouseDoubleClickEvent(event)

    def mousePressEvent_top_bar(self, event):
        """
        If the left mouse button is pressed, set the move_window_status to True, and set the
        move_window_dragPosition to the position of the mouse
        top bar is the widget that we have replaced the traditional title bar with

        Args:
          event: The event that was triggered.

        Returns:
          The super class of the top_bar object.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.move_window_status = True
            self.move_window_dragPosition = event.position().toPoint()
            event.accept()
        return super(QtWidgets.QFrame, self.top_bar).mousePressEvent(event)

    def mouseReleaseEvent_top_bar(self, event):
        """
        Sets the move_window_status to False when we have released the cursor form the top bar widget
        top bar is the widget that we have replaced the traditional title bar with

        Args:
          event: The event that was triggered.

        Returns:
          The super class of the top_bar object.
        """
        self.move_window_status = False
        return super(QtWidgets.QFrame, self.top_bar).mouseReleaseEvent(event)

    def mouseMoveEvent_top_bar(self, event):
        """
        It moves the main window on the same rate as the top bar widget cursor moves
        top bar is the widget that we have replaced the traditional title bar with

        Args:
          event: the event that triggered the function

        Returns:
          The super class of the top_bar widget.
        """
        # move mainWindow on the same rate as this widget moves
        if self.move_window_status:
            p = (
                QtGui.QCursor.pos()
                - self.move_window_dragPosition
                - self.top_bar.geometry().topLeft()
            )
            if p.x() != 0 and p.y() != 0:
                self.MainWindow.move(p)
        return super(QtWidgets.QFrame, self.top_bar).mouseMoveEvent(event)

    def home_button_main_clicked(self):
        """
        Handles the action of the home button on the top left part of the main interface.
        If the user has already selected his organism and parts to be analysed, then just
        send the user to the main interface
        """
        from celer_sight_ai import config

        if config.home_selection_step == 0:
            self.stackedWidget.setCurrentWidget(self.orgSelectionSection)
        elif config.home_selection_step == 1:
            self.app_pages.setCurrentWidget(self.chat)
        else:
            self.stackedWidget.setCurrentWidget(self.MainInterface)
            self.viewer.setFocus()

    def get_screen_from_cursor_pos(self, cursor_pos):
        """
        It gets the screen that the cursor is currently on

        Args:
          cursor_pos: The position of the cursor on the screen.

        Returns:
          The screen that the cursor is on.
        """
        # currently not user, could be usfull in the future, leaving as is.
        screens = QtWidgets.QApplication.screens()
        for screen in screens:
            if screen.geometry().contains(cursor_pos):
                print("screen is ", screen.name())
                return screen

    def addShadowToWidget(self, widgetToAddShadow):
        """
        It takes a widget as an argument and returns the same widget with a shadow effect

        Args:
          widgetToAddShadow: The widget you want to add the shadow to.

        Returns:
          The widget with the shadow effect.
        """
        ShadowEffect = QtWidgets.QGraphicsDropShadowEffect()
        ShadowEffect.setColor(QtGui.QColor(0, 0, 0, 200))
        ShadowEffect.setBlurRadius(50)
        ShadowEffect.setOffset(0)
        widgetToAddShadow.setGraphicsEffect(ShadowEffect)
        return widgetToAddShadow

    def loadSetting(self, ValueString=None, defaultVal=0):
        # Loads a settings from ValueString and if there is no value it will return defaultVal
        assert ValueString != None
        settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        if settings.contains(ValueString):
            returnVal = settings.value(ValueString)
            if returnVal == "true" or returnVal == "True":
                return True
            return returnVal
        else:
            settings.setValue(ValueString, defaultVal)
            return defaultVal

    def setSetting(self, ValueString=None, defaultVal=0):
        assert ValueString != None
        settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        settings.setValue(ValueString, defaultVal)

    def record_class_item_on_widget_click(self):
        if self.custom_class_list_widget.count() == 0:
            return
        self.previous_clicked_class_widget = self.custom_class_list_widget.item(
            self.custom_class_list_widget.currentRow()
        ).text()
        self.previous_clicked_class_index = self.custom_class_list_widget.currentRow()

    def update_class_items_widgets_on_change(self):
        # Get current class names from the data model
        current_classes = set(self.DH.BLobj.classes_object_colors.keys())

        # Get class names from the widget
        widget_classes = set(
            self.custom_class_list_widget.item(i).text()
            for i in range(self.custom_class_list_widget.count())
        )

        # Check for duplicates in the widget
        if len(widget_classes) < self.custom_class_list_widget.count():
            # Revert the change if there's a duplicate
            self.custom_class_list_widget.item(
                self.previous_clicked_class_index
            ).setText(self.previous_clicked_class_widget)
            return

        # If no changes, exit early
        if current_classes == widget_classes:
            return

        # Handle renamed class
        if (
            self.previous_clicked_class_widget in current_classes
            and self.previous_clicked_class_widget not in widget_classes
        ):
            new_class_name = self.custom_class_list_widget.item(
                self.custom_class_list_widget.currentRow()
            ).text()
            self.DH.BLobj.classes_object_colors[new_class_name] = (
                self.DH.BLobj.classes_object_colors.pop(
                    self.previous_clicked_class_widget
                )
            )

        # Handle added/removed classes
        for class_name in widget_classes - current_classes:
            # Add new class with default color
            self.DH.BLobj.classes_object_colors[class_name] = (
                128,
                128,
                128,
                255,
            )  # Default gray color

        for class_name in current_classes - widget_classes:
            # Remove deleted class
            del self.DH.BLobj.classes_object_colors[class_name]

        # Update the old class reference for the next change
        self.previous_clicked_class_widget = self.custom_class_list_widget.item(
            self.custom_class_list_widget.currentRow()
        ).text()
        self.previous_clicked_class_index = self.custom_class_list_widget.currentRow()

    def updateClassColor_onIndexChange(self):
        # when we change index on the listwidget we also update the colors of the buttons
        logger.info(
            "current index is {}".format(self.custom_class_list_widget.currentRow())
        )
        if self.custom_class_list_widget.currentRow() == -1:
            return
        if not self.custom_class_list_widget.currentItemWidget():
            return
        currentItemClass = self.custom_class_list_widget.currentItemWidget().unique_id
        currentItemClass = self.custom_class_list_widget.classes[currentItemClass]
        color = currentItemClass.color
        if not color:
            return
        self.pg1_settings_all_masks_color_button.setStyleSheet(
            "background-color:" + self.RGB_to_HEX(color[0], color[1], color[2]) + ";"
        )
        self.viewer.QuickTools.pushButtonColorPolygonTool.setStyleSheet(
            "background-color:" + self.RGB_to_HEX(color[0], color[1], color[2]) + ";"
        )
        opacity = int(color[3])
        if opacity < 0:
            opacity = 0
        if opacity > 100:
            opacity = 100
        # stop the signal from being emitted, as we only need to change the value of the UI
        self.pg1_settings_mask_opasity_slider.blockSignals(True)
        self.pg1_settings_mask_opasity_slider.setValue(opacity)
        # restore
        self.pg1_settings_mask_opasity_slider.blockSignals(False)

    def clamp(self, x):
        return max(0, min(x, 255))

    def RGB_to_HEX(self, r, g, b):
        return "#{0:02x}{1:02x}{2:02x}".format(
            self.clamp(r), self.clamp(g), self.clamp(b)
        )

    def ChangeAnalysisSettings(self):
        # TODO add the rest of organisms here
        from celer_sight_ai import config

        no = self.new_analysis_object
        self.new_analysis_object.init_organism_settings()  # = NewAnalysis(self)
        # if self.new_analysis_object.organism != 1: # NewAnalysis.organism cells
        # self.QuickTools.RandomForestCellModeFrame.hide()

        if config.supercategory == "worm":
            self.organism_selection.CelegansMainButton.click()
        if config.supercategory == "cell":
            self.organism_selection.CellsMainButton.click()
        if config.supercategory == "tissue":
            self.organism_selection.TissueMainButton.click()

    def terminate_thread(self, thread):
        logger.debug(f"Terminating thread : {thread}")
        if not thread.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc
        )
        if res == 0:
            raise ValueError("Invalid thread ID")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread.ident), None
            )
            raise SystemError("Failed to forcefully exit thread")

    def closeApp(self):
        """Main method to close CelerSight AI"""
        # Hide MainWindow first to make it more responsive
        self.MainWindow.hide()
        # process events
        QtCore.QCoreApplication.processEvents()

        try:
            # Terminate all threads forcefully
            import javabridge

            if javabridge.get_env() is not None:
                javabridge.kill_vm()
        except:
            pass

        try:
            if hasattr(self, "onlineInfAll"):
                self.onlineInfAll.stop()
        except:
            pass
        from celer_sight_ai import clean_exit

        clean_exit()

        return

    def execAboutDialog(self):
        logger.debug("About dialog exec")
        self.aboutCelerSightDialog = aboutSectionClass(self)
        return

    def PolyArea(self, x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def recalc_Featurs_by_MODE_ML(self):
        if self.viewer.ML_brush_tool_object:
            self.viewer.ML_brush_tool_object.update_MODE_ML()

    def saveCurrentImageGraphicsView(self):
        """
        Captures the current scene content as an image and saves it to a user-specified location.
        """
        # if the viewer is not visible, then we cannot save the screenshot
        if not self.viewer.isVisible():
            return

        # Get save location from user
        file_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save Viewport Screenshot",
            "",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;TIFF Image (*.tif *.tiff)",
        )

        if not file_path:  # User cancelled
            return

        try:
            # Get the visible scene rect
            scene_rect = self.viewer.mapToScene(
                self.viewer.viewport().rect()
            ).boundingRect()

            # Create a pixmap to render the scene
            pixmap = QtGui.QPixmap(self.viewer.viewport().size())
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)

            # Create painter and render scene to pixmap
            painter = QtGui.QPainter(pixmap)
            self.viewer._scene.render(painter, QtCore.QRectF(pixmap.rect()), scene_rect)
            painter.end()

            # Save the pixmap
            pixmap.save(file_path)
            logger.info(f"Screenshot saved to: {file_path}")

        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
            QtWidgets.QMessageBox.critical(
                self.MainWindow, "Error", f"Failed to save screenshot: {str(e)}"
            )

    def FilterMinArea_ML_RF(self):
        from celer_sight_ai.gui.custom_widgets.scene import PolygonAnnotation

        if self.viewer.ML_brush_tool_object_state == True:
            numberFilterArea = self.pg1_ML_advanced_minSpinBox.value()
            if numberFilterArea != 0:
                for item in self.viewer._scene.items():
                    if type(item) == PolygonAnnotation:
                        allX = []
                        allY = []
                        for x in range(len(item.PolRef)):
                            allX.append(item.PolRef[x].x())
                            allY.append(item.PolRef[x].y())
                            currentArea = self.PolyArea(allX, allY)
                            if currentArea < numberFilterArea:
                                if (
                                    self.DH.BLobj.groups["default"]
                                    .conds[self.DH.BLobj.get_current_condition()]
                                    .images[self.current_imagenumber]
                                    .masks[item.MaskPosition]
                                    .visibility
                                    == True
                                ):
                                    self.DH.BLobj.groups["default"].conds[
                                        self.DH.BLobj.get_current_condition()
                                    ].images[self.current_imagenumber].masks[
                                        item.MaskPosition
                                    ].setVisibility(
                                        False
                                    )
                                    self.viewer._scene.removeItem(item)
                            if currentArea >= numberFilterArea:
                                if (
                                    self.DH.BLobj.groups["default"]
                                    .conds[self.DH.BLobj.get_current_condition()]
                                    .images[self.current_imagenumber]
                                    .masks[item.MaskPosition]
                                    .visibility
                                    == False
                                ):
                                    self.viewer._scene.addItem(item)
                                    self.DH.BLobj.groups["default"].conds[
                                        self.DH.BLobj.get_current_condition()
                                    ].images[self.current_imagenumber].masks[
                                        item.MaskPosition
                                    ].setVisibility(
                                        True
                                    )
        try:
            self.viewer.updateMaskCountLabel()
        except:
            pass

    def saveCurrentGraph(self):
        my_dir = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Select a file:",
            filter="Postscript (*.ps);;Encapsulated Postscript (*.eps);;Portable Document Format (*.pdf);;Portable Network Graphics (*.png);;Joint Photographic Experts Group(*.jpeg) ;; Tagged Image File Format(*.tif);;Tagged Image File Format(*tiff)",
        )
        # logger.info(my_dir)
        self.figure.savefig(my_dir[0])

    def reimplimentActionsForQuickTools(self):
        # add qtoolbar to floating widget "quicktools"

        # self.toolBar.setParent(None)
        # self.toolBar.setParent(self.viewer.QuickTools.myquickToolsWidget)
        # self.viewer.QuickTools.gridLayout_3.addWidget(self.toolBar,1,0)
        # clearout all actions except selection
        self.toolBar.hide()
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("C:/Users/manos/Documents/topfluov2/UiAssets/../data/NeedsAttribution/selection-box.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

        # reimpliment tools with shadow and other attributes
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsSelectionTool, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsErraseTool = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsErraseTool, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool = (
            self.ReplaceWidget(
                self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool,
                QuickToolButton,
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsPolygonTool, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsAutoSpline, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickTools_BrushMask, QuickToolButton
        )
        self.viewer.QuickTools.pushButtonQuickToolsKeypoint = self.ReplaceWidget(
            self.viewer.QuickTools.pushButtonQuickToolsKeypoint, QuickToolButton
        )

        # Set appropriate cursor
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )

        QtWidgets.QApplication.processEvents()

        # Connect Viewer reference to widget
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.viewerRef = (
            self.viewer
        )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.viewerRef = (
            self.viewer
        )

        # TODO: This is not clean, maybe do the feferencing in an other way.
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.viewerRef = self.viewer
        self.viewer.QuickTools.pushButtonQuickToolsKeypoint.viewerRef = self.viewer

        self.pg_2_Title_textedit = self.ReplaceWidget(
            self.pg_2_Title_textedit, myRichTextEdit
        )
        self.pg_2_Title_textedit.setAttributesInit(self, "title")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_Title_textedit, 1, 1, 1, 1
        )
        self.pg_2_x_axis_textedit = self.ReplaceWidget(
            self.pg_2_x_axis_textedit, myRichTextEdit
        )
        self.pg_2_x_axis_textedit.setAttributesInit(self, "xlabel")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_x_axis_textedit, 4, 1, 1, 1
        )
        self.pg_2_y_axis_textedit_2 = self.ReplaceWidget(
            self.pg_2_y_axis_textedit_2, myRichTextEdit
        )
        self.pg_2_y_axis_textedit_2.setAttributesInit(self, "ylabel")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_y_axis_textedit_2, 6, 1, 1, 1
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_y_axis_textedit_2.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_y_axis_textedit_2.setSizePolicy(sizePolicy)
        self.pg_2_y_axis_textedit_2.setMaximumSize(QtCore.QSize(100000, 30))
        self.pg_2_x_axis_textedit.setSizePolicy(sizePolicy)
        self.pg_2_x_axis_textedit.setMaximumSize(QtCore.QSize(100000, 30))
        self.pg_2_Title_textedit.setSizePolicy(sizePolicy)
        self.pg_2_Title_textedit.setMaximumSize(QtCore.QSize(100000, 30))

    def setTabIndex(self, indexNumber=0):
        """
        runs after the signal of the main tab button (top) is clicked to register the tab we are on now
        """
        logger.info("setting bnumber to ", indexNumber)
        self.currentTabIndexBtns = indexNumber
        return

    def addConnections(self):
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool.clicked.connect(
            lambda: self.actionSelectionTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.clicked.connect(
            lambda: self.actionRemoveSelectionTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.clicked.connect(
            lambda: self.MagicBrushMoveTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool.clicked.connect(
            lambda: self.PolygonTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.clicked.connect(
            lambda: self.actionAutoTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.clicked.connect(
            lambda: self.actionMakeSpline.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.clicked.connect(
            lambda: self.actionRF_MODE.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.clicked.connect(
            lambda: self.actionBrushMask.trigger()
        )

        self.viewer.QuickTools.pushButtonQuickToolsErraseTool.clicked.connect(
            lambda: self.actionErraseTool.trigger()
        )
        self.viewer.QuickTools.pushButtonQuickToolsKeypoint.clicked.connect(
            lambda: self.actionKeypoint.trigger()
        )

        self.viewer.QuickTools.ApplyAndDoneBtnRandomForestMode.clicked.connect(
            lambda: self.viewer.complete_RF_MODE()
        )

        self.pg1_ML_advanced_update_now_buttonl_2.clicked.connect(
            lambda: self.clearRF_CELLS_markers(withImage=False)
        )

        self.viewer.QuickTools.horizontalSliderlineWidthPolygonTool.valueChanged.connect(
            lambda: self.viewer.updateAllPolygonPen()
        )
        # initialize settings
        self.viewer.QuickTools.pushButtonColorBGTool.setStyleSheet(
            "background-color: rgba(0,0,255)"
        )
        self.actionSelectionTool.trigger()

        # correct size triggers:

        self.buttonToolList = [
            self.viewer.QuickTools.pushButtonQuickToolsSelectionTool,
            self.viewer.QuickTools.pushButtonQuickToolsErraseTool,
            self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool,
            self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush,
            self.viewer.QuickTools.pushButtonQuickToolsPolygonTool,
            self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox,
            self.viewer.QuickTools.pushButtonQuickToolsAutoSpline,
            self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE,
            self.viewer.QuickTools.pushButtonQuickTools_BrushMask,
        ]
        for tool in self.buttonToolList:
            tool.clicked.connect(
                lambda: self.viewer.QuickTools.videowidget.setHeightWidgetTight()
            )

    def saveMLModel(self):
        if self.viewer.ML_brush_tool_object:
            self.viewer.ML_brush_tool_object.saveBioMLModel()

    def loadMLModel(self):
        if not self.viewer.ML_brush_tool_object:
            from celer_sight_ai.core.ML_tools import ML_RF

            self.viewer.ML_brush_tool_object = ML_RF(
                self.DH.BLobj.groups["default"]
                .conds[self.DH.BLobj.get_current_condition()]
                .getImage(self.current_imagenumber)
                .copy(),
                self.viewer.ML_brush_tool_draw_foreground_array,
                self.viewer.ML_brush_tool_draw_background_array,
                self,
            )
        self.viewer.ML_brush_tool_object.loadBioMLModel()
        # self.START_getFeatures_Threaded()

    def clearRF_CELLS_markers(self, withImage=True):
        import numpy as np

        currentImg = (
            self.DH.BLobj.groups["default"]
            .conds[self.DH.BLobj.get_current_condition()]
            .getImage(self.current_imagenumber)
        )
        self.viewer.ML_brush_tool_draw_foreground_array = np.zeros(
            (currentImg.shape[0], currentImg.shape[1]), dtype=bool
        )
        self.viewer.ML_brush_tool_draw_background_array = np.zeros(
            (currentImg.shape[0], currentImg.shape[1]), dtype=bool
        )
        self.viewer.ML_brush_tool_draw_background_added = False
        self.viewer.ML_brush_tool_draw_foreground_added = False
        self.viewer.ML_brush_tool_draw_refreshed = False
        self.viewer.ML_brush_tool_draw_scene_items = []
        if withImage == False:
            self.DH.BLobj.groups["default"].conds[
                self.DH.BLobj.get_current_condition()
            ].images[self.current_imagenumber].clearMasks()
            # self.DH.mask_RNAi_slots_QPoints[self.DH.BLobj.get_current_condition()][self.current_imagenumber] = []
            self.ML_brush_tool_draw_continous_inference = True
        for item in self.viewer._scene.items():
            if type(item) != QtWidgets.QGraphicsPixmapItem:
                try:
                    self.viewer._scene.removeItem(item)
                except:
                    pass
        # self.load_main_scene(self.current_imagenumber)
        self.viewer.ML_brush_tool_draw_training_mode == "NORMAL"

    def setCellsRF_MODE(self, mode="FG"):
        logger.info("rf mode is ".format(mode))
        if mode == "FG":
            self.viewer.ML_brush_tool_draw_foreground_add = True
            self.viewer.ML_brush_tool_draw_background_add = False

        elif mode == "BG":
            self.viewer.ML_brush_tool_draw_foreground_add = False
            self.viewer.ML_brush_tool_draw_background_add = True

    def setUpIconsQuickTools(self):
        # always hide brush unless we aer on Auto RF mode
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.hide()

        # if config.supercategory == "worm":
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.hide()
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.hide()
        self.viewer.QuickTools.pushButtonQuickToolsKeypoint.hide()
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.hide()

        # put all icons on the corresponding tool qpushbuttons
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"],
                "data/icons/viewport/polygon_tool_icon.png",
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"],
                "data/icons/viewport/magic_tool_icon.png",
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"],
                "data/icons/viewport/selection_icon.png",
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsErraseTool.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/viewport/eraser_icon.png"
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/CellSplitTool.png"
            )
        )

        if config.supercategory == "cell" or config.supercategory == "flies":
            self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.setIconCustom(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/MagicClickTool.png"
                )
            )
        else:
            self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.setIconCustom(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/MagicLengthTool.png"
                )
            )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"],
                "data/icons/viewport/magic_brush_move_icon.png",
            )
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/MachineLearningTool.png"
            )
        )
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.setIconCustom(
            os.path.join(
                os.environ["CELER_SIGHT_AI_HOME"], "data/icons/paintbrush_ml.png"
            )
        )
        # icon6 = QtGui.QIcon()
        # icon6.addPixmap(QtGui.QPixmap("data/NeedsAttribution/areaselection.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

        # self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.setIconSize(QtCore.QSize(50,50))
        # put all icons on the corresponding tool qpushbuttons
        SizeResize = QtCore.QSize(30, 30)
        self.viewer.QuickTools.pushButtonQuickToolsPolygonTool.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoToolBox.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsSelectionTool.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsErraseTool.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsRemoveSelectionTool.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoSpline.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsMoveMagicBrush.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickToolsAutoRF_MODE.setInitIconSize(
            SizeResize
        )
        self.viewer.QuickTools.pushButtonQuickTools_BrushMask.setInitIconSize(
            SizeResize
        )

    def check_data_corruption(self):
        QtCore.QTimer.singleShot(3000, self.check_data_corruption_method)

    def runExportDialog(self):
        from celer_sight_ai.gui.custom_widgets.export_neural_settings_dialog import (
            ExportNeuralSettingsDialog,
        )

        self.tmpExportDialog = ExportNeuralSettingsDialog(self)
        self.tmpExportDialog.StartSelf()

    def on_btnMaximize_clicked(self):
        if self.MainWindow.windowState() == QtCore.Qt.WindowState.WindowMaximized:
            self.MainWindow.setWindowState(QtCore.Qt.WindowState.WindowNoState)

        else:
            self.MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMaximized)

    def on_minimizedClicked(self):
        logger.debug("Minimizing clicked")
        self.MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMinimized)

    def TestisChecked(self, button):
        logger.info("now.. ", button.isChecked())
        logger.info("for the.. ", button.objectName())

    def AddShadowToWidget(self, widget):
        BR = 40  # blur radius
        xo = -5  # xoffset
        yo = 7  # yoffset
        colorGUI = QtGui.QColor(0, 0, 0, 90)
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=BR, xOffset=xo, yOffset=yo, color=colorGUI
        )
        widget.setGraphicsEffect(shadow)

    def ModernizeWindow(self):
        # self.MainWindow.setWindowFlags( QtCore.Qt.WindowType.FramelessWindowHint)
        from PyQt6.QtCore import Qt as Qt

        self.MainWindow.setWindowFlags(Qt.Window)  # |Qt.FramelessWindowHint)

        # Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint |
        # Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        # FramelessWindowHint
        import win32api

        win32api.SetClassLong(
            eval(hex(self.MainWindow.winId().__int__())), -26, 0x0008 | 0x00020000
        )

    def ExtendUi(self, MainWindow=None):
        """
        This function gets the Ui that we have previoyusly build with the setup function(only the essentials)
         and adds all the compononents to the docks and hides the ones that should not be seen
        """
        # self.gridLayout_images.removeWidget(self.splitterImagesRight)
        # self.gridLayout_images.removeWidget(self.pushButtonminimizeMainToRight)

        self.pg_2_gridLayout_10.addWidget(self.viewer, 0, 0, 1, 1)
        self.viewer.setParent(self.pg_2_widget_graph_visualizer_3)

        # Create a QGraphicsScene and set it as the scene for the view of image preview
        from celer_sight_ai.gui.custom_widgets.scene import ImagePreviewGraphicsView

        self.images_preview_graphicsview = ImagePreviewGraphicsView(
            self.overview_tabs_image, self
        )
        self.images_preview_graphicsview.setObjectName("images_preview_graphicsview")
        self.overview_tabs_image_vertical_layout.addWidget(
            self.images_preview_graphicsview
        )

        import os
        import pathlib

        ROOTDIR = pathlib.Path(__file__).parent.absolute()
        os.chdir(ROOTDIR)

        # TODO: This for tabs fix
        from celer_sight_ai import config

        config.global_signals.tabChangedbtn.connect(self.setTabIndex)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/NeedsAttribution/selection-box.png",
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.PolygonTool.setIcon(icon)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/NeedsAttribution/magic-wand.png",
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionAutoTool.setIcon(icon1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/NeedsAttribution/arrow.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionSelectionTool.setIcon(icon2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/NeedsAttribution/move-selection-cursor.png",
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionMoveTool.setIcon(icon3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/NeedsAttribution/mouse-cursor.png",
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionRemoveSelectionTool.setIcon(icon4)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/NeedsAttribution/crest-lower-curve.png",
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.actionMakeSpline.setIcon(icon5)
        # PAge 2 Assets

        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/SubScirptIcon.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.Subscript_btnPlot.setIcon(icon6)
        self.Subscript_btnPlot.setIconSize(QtCore.QSize(15, 15))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/SuperScriptIcon.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.SuperScript_btnPlot.setIcon(icon6)
        self.SuperScript_btnPlot.setIconSize(QtCore.QSize(15, 15))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/FontSizeDown.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.fontSizeUp_btnPlot.setIcon(icon6)
        self.fontSizeUp_btnPlot.setIconSize(QtCore.QSize(15, 15))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/FontSizeUp.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.fontSizeDown_btnPlot.setIcon(icon6)
        self.fontSizeDown_btnPlot.setIconSize(QtCore.QSize(15, 15))

        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/PlotsSaveAs_icon.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.pg2_save_preset_btn.setIcon(icon6)
        self.pg2_save_preset_btn.setIconSize(QtCore.QSize(23, 23))

        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"], "data/icons/PlotsOpenAs_icon.png"
                )
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.pg2_load_preset_btn.setIcon(icon6)
        self.pg2_load_preset_btn.setIconSize(QtCore.QSize(23, 23))

        self.Subscript_btnPlot.clicked.connect(lambda: self.subscript_btn_action())
        self.SuperScript_btnPlot.clicked.connect(lambda: self.SuperScript_btn_action())
        self.fontSizeUp_btnPlot.clicked.connect(lambda: self.fontSizeUp_btn_action())
        self.fontSizeDown_btnPlot.clicked.connect(
            lambda: self.fontSizeDown_btn_action()
        )
        self.ItalicText_btnPlot.clicked.connect(lambda: self.ItalicText_btn_action())
        self.BoltText_btnPlot.clicked.connect(lambda: self.BoltText_btn_action())
        self.NormalText_btnPlot.clicked.connect(lambda: self.NormalText_btn_action())
        self.fontComboBox.currentIndexChanged.connect(
            lambda: self.assignFontsFamilyInPlotTab()
        )

        # Plot Settings Widget
        # from celer_sight_ai.gui.designer_widgets_py_files.plot_tools_widget_v4 import Ui_Plot_tools_widget as plot_tools_widget_v4
        # plot_tools_widget_v4.setupUi(self, self.scrollArea_for_plot_tools)  # add the widgets
        # plot_tools_widget_v4.retranslateUi(self, self.scrollArea_for_plot_tools)  # translate properties
        self.pg2_graphs_view.itemSelectionChanged.connect(
            self.show_only_active_plot_settings
        )
        self.pg2_graphs_view.itemSelectionChanged.connect(
            lambda: self.hideAllSpecificPlotWidgets()
        )

        self.pg2_graph_visulaizer_pallets.clicked.connect(
            lambda: self.MyVisualPlotHandler.spawnPalletePicker()
        )

        # function to plce the settings for all the plots and hide them, then show_only_active_plot_settings whoces which settings to use
        self.setup_widgets()

        # from celer_sight_ai.gui.designer_widgets_py_files.results_inspector_widgets import Ui_Form as results_inspector_widgets
        # results_inspector_widgets.setupUi(self, self.ReviewAreaWidget)  # add the widgets
        # results_inspector_widgets.retranslateUi(self, self.ReviewAreaWidget)  # translate properties

        # signal to update the spreadsheet on qcombobox change

        # Selected Mask DIalog set up>>>
        self.SelectedMaskDialog = QtWidgets.QDialog()
        from celer_sight_ai.gui.designer_widgets_py_files.SelectedSettintgsDialog import (
            Ui_Dialog as SelectedSettintgsDialog,
        )

        SelectedSettintgsDialog.setupUi(
            self, self.SelectedMaskDialog
        )  # add the widgets
        SelectedSettintgsDialog.retranslateUi(
            self, self.SelectedMaskDialog
        )  # translate properties

        # Set SelectedMaskDialog Attributes
        self.SelectedMaskDialog.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.SelectedMaskDialog.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )
        # for item in self.SelectedMaskDialog.children():
        # logger.info("Children are -- - -- - - -  ", item.objectName())
        self.SelectedMaskDialog.hide()
        self.pg_2_Source_Data_btn.clicked.connect(lambda: self.spawnAnnotationDialog())

    def spawnAnnotationDialog(self):
        from celer_sight_ai.gui.custom_widgets.plot_handler import AnnotationDialog

        self.myAnnotationPlotDialogs = AnnotationDialog(self.currentDataFrame, self)
        self.myAnnotationPlotDialogs.myDialog.show()
        self.myAnnotationPlotDialogs.myDialog.raise_()

    def subscript_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            myFocusWidget.setTexSubScript()

    def SuperScript_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            myFocusWidget.setTexSuperScript()

    def fontSizeUp_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            if myFocusWidget.typeTextEdit == "title":
                self.MyVisualPlotHandler.mainPlotTitleFontDict = {
                    "family": self.MyVisualPlotHandler.mainPlotTitleFontDict["family"],
                    "color": self.MyVisualPlotHandler.mainPlotTitleFontDict["color"],
                    "weight": self.MyVisualPlotHandler.mainPlotTitleFontDict["weight"],
                    "size": self.MyVisualPlotHandler.mainPlotTitleFontDict["size"] + 1,
                }
            elif myFocusWidget.typeTextEdit == "xlabel":
                self.xLabelPlotTextFontDict.mainPlotTitleFontDict = {
                    "family": self.xLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "family"
                    ],
                    "color": self.xLabelPlotTextFontDict.mainPlotTitleFontDict["color"],
                    "weight": self.xLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "weight"
                    ],
                    "size": self.xLabelPlotTextFontDict.mainPlotTitleFontDict["size"]
                    + 1,
                }
            elif myFocusWidget.typeTextEdit == "ylabel":
                self.yLabelPlotTextFontDict.mainPlotTitleFontDict = {
                    "family": self.yLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "family"
                    ],
                    "color": self.yLabelPlotTextFontDict.mainPlotTitleFontDict["color"],
                    "weight": self.yLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "weight"
                    ],
                    "size": self.yLabelPlotTextFontDict.mainPlotTitleFontDict["size"]
                    + 1,
                }

    def fontSizeDown_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            if myFocusWidget.typeTextEdit == "title":
                self.MyVisualPlotHandler.mainPlotTitleFontDict = {
                    "family": self.MyVisualPlotHandler.mainPlotTitleFontDict["family"],
                    "color": self.MyVisualPlotHandler.mainPlotTitleFontDict["color"],
                    "weight": self.MyVisualPlotHandler.mainPlotTitleFontDict["weight"],
                    "size": self.MyVisualPlotHandler.mainPlotTitleFontDict["size"] - 1,
                }
            elif myFocusWidget.typeTextEdit == "xlabel":
                self.xLabelPlotTextFontDict.mainPlotTitleFontDict = {
                    "family": self.xLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "family"
                    ],
                    "color": self.xLabelPlotTextFontDict.mainPlotTitleFontDict["color"],
                    "weight": self.xLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "weight"
                    ],
                    "size": self.xLabelPlotTextFontDict.mainPlotTitleFontDict["size"]
                    - 1,
                }
            elif myFocusWidget.typeTextEdit == "ylabel":
                self.yLabelPlotTextFontDict.mainPlotTitleFontDict = {
                    "family": self.yLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "family"
                    ],
                    "color": self.yLabelPlotTextFontDict.mainPlotTitleFontDict["color"],
                    "weight": self.yLabelPlotTextFontDict.mainPlotTitleFontDict[
                        "weight"
                    ],
                    "size": self.yLabelPlotTextFontDict.mainPlotTitleFontDict["size"]
                    - 1,
                }

    def assignFontsFamilyInPlotTab(self):
        if self.MyVisualPlotHandler:
            if self.MyVisualPlotHandler.prevSelectedTextComboBox == "title":
                self.MyVisualPlotHandler.myTitleFontFamily = (
                    self.fontComboBox.currentText().lower()
                )
            elif self.MyVisualPlotHandler.prevSelectedTextComboBox == "xlabel":
                self.MyVisualPlotHandler.myXTitleFontFamily = (
                    self.fontComboBox.currentText().lower()
                )
            elif self.MyVisualPlotHandler.prevSelectedTextComboBox == "ylabel":
                self.MyVisualPlotHandler.myYTitleFontFamily = (
                    self.fontComboBox.currentText().lower()
                )
            elif self.MyVisualPlotHandler.prevSelectedTextComboBox == "hover":
                self.MyVisualPlotHandler.myXTicksFontFamily = (
                    self.fontComboBox.currentText().lower()
                )
            self.plot_seaborn()

    def ItalicText_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            myFocusWidget.setTextItalic()

    def BoltText_btn_action(self):
        myFocusWidget = QtWidgets.QApplication.focusWidget()
        if type(myFocusWidget) == myRichTextEdit:
            myFocusWidget.setTextBold()

    def NormalText_btn_action(self):
        return

    def hideAllSpecificPlotWidgets(self):
        """
        Hide allWidgets, show onlyy the ones used
        """
        # if self.pg_2_graph_colors_groupBox_listWidget.count() != 0:
        for i in range(self.pg_2_graph_colors_groupBox_listWidget.count()):
            self.pg_2_graph_colors_groupBox_listWidget.item(i).setHidden(True)
            # specificItemWidget = self.pg_2_graph_colors_groupBox_listWidget.itemWidget(self.pg_2_graph_colors_groupBox_listWidget.item(i))
            # specificItemWidget.hide()
        if self.pg2_graphs_view.currentItem() != None:
            selectedText = self.pg2_graphs_view.currentItem().text()
        elif self.pg2_graphs_view.count() != 0:
            self.pg2_graphs_view.setCurrentRow(0)
            selectedText = self.pg2_graphs_view.currentItem().text()
        else:
            return
        logger.info(
            "specificPlotWidgetRef is ", self.MyVisualPlotHandler.specificPlotWidgetRef
        )
        if selectedText in self.MyVisualPlotHandler.specificPlotWidgetRef.keys():
            ListVisibleitems = self.MyVisualPlotHandler.specificPlotWidgetRef[
                selectedText
            ]
            for widget in ListVisibleitems:
                try:
                    widget.setHidden(False)
                except Exception as e:
                    logger.error(e)

    def ApplyStyleSheet(self):
        return
        try:
            orange = "orange1.stylesheet"
            blue = "blue1.stylesheet"
            with open(orange, "r") as fh:
                self.OrangeStylesheet = fh.read()
                self.MainWindow.setStyleSheet(self.OrangeStylesheet)
                self.SelectedMaskDialog.setStyleSheet(self.OrangeStylesheet)
        except:
            pass

    def setup_widgets(self):
        """
        function that sets up our widgets for plot and jitter, box bar etc...
        """
        from celer_sight_ai.gui.custom_widgets.swarm_plot_settings_widget_v2 import (
            Swarm_Ui_Form,
        )
        from celer_sight_ai.gui.custom_widgets.violin_plot_settings_widget_v2 import (
            Violin_Ui_Form,
        )
        from celer_sight_ai.gui.custom_widgets.plot_handler import (
            PlotViewerHandler,
            specificPlotWidget,
        )

        # Violin Plot
        self.violinplot_settings_user = Violin_Ui_Form()
        self.violinplot_settings_user.setupUi(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin
        )

        logger.info("wortking")

        # Save Values
        objects_list = [
            self.pg2_graph_saturation_spinBox_box_plot,
            self.pg2_graph_orientaitno_combobox_barplot,
            self.pg2_graph_bar_errwidth_spinBox_box_plot,
            self.pg2_graph_bar_width_spinBox_box_plot,
            self.pg2_graph_bar_ci_spinBox_box_plot,
            self.pg2_graph_flier_size_spinBox_box_plot,
            self.pg2_graph_border_width_spinBox_swarmplot,
            self.pg2_graph_size_spinBox_swarmplot,
            self.pg2_graph_just_width_spinbox_violinplot,
            self.pg2_graph_orientaitno_combobox_swarmplot,
            self.pg2_graph_violinplot_orienation_combobox,
            self.pg2_graph_border_width_spinBox_violinplot,
            self.pg2_graph_saturation_spinBox_violinplot,
            self.pg2_graph_cut_spinBox_vil,
            self.pg2_graph_scale_comboBox_violinplot,
            self.pg2_graph_width_spinBox_box_plot,
            self.pg_2_graph_boxplot_orientation_combobox,
            self.pg2_graph_saturation_spinBox_box_plot_2,
            self.pg2_graph_line_width_spinBox_box_plot,
            self.pg2_graph_bar_borderwidth_spinBox_box_plot,
            self.pg2_graph_cap_size_spinBox_box_plot,
        ]

        # # Set up all of the widget for the BAR PLOT
        for widget in objects_list:
            from PyQt6 import QtWidgets

            if type(widget) == QtWidgets.QComboBox:
                # Add signals:
                widget.currentIndexChanged.connect(lambda: self.RecordValues())
                widget.currentIndexChanged.connect(
                    lambda: self.ReadVariablesPlotTools()
                )
                widget.currentIndexChanged.connect(lambda: self.plot_seaborn())

            elif type(widget) == QtWidgets.QSpinBox:
                widget.textChanged.connect(lambda: self.RecordValues())
                widget.textChanged.connect(lambda: self.ReadVariablesPlotTools())
                widget.textChanged.connect(lambda: self.plot_seaborn())

            elif type(widget) == QtWidgets.QDoubleSpinBox:
                widget.textChanged.connect(lambda: self.RecordValues())
                widget.textChanged.connect(lambda: self.ReadVariablesPlotTools())
                widget.textChanged.connect(lambda: self.plot_seaborn())

    def RecordValues(self):
        # This needs to run every time we change a value
        # connect signal with this function and connect it like this:
        # Signals need to go in UI_Blocks in set_up_widgets
        # lambda function needs to be like this: lambda _, b=(Instance): self.RecordValues(MyInstacne=b))
        # get widget list item, convert to instance and then save
        if self.DuringPlotWidgetSwitch == True:
            return
        textGraphsView = self.pg2_graphs_view.currentItem().text()
        MyInstance = self.MyVisualPlotHandler.WidgetDictionary[textGraphsView]

        if MyInstance.type == "Bar Plot":
            logger.info("recording variables")
            # MyInstance.Bar_palette = self.pg_2_graph_barplot_pallete_style_combobox.currentText()
            # MyInstance.BarColor = self.pg_2_graph_colors_pallete_2_bar_plot.palette().button().color().name()
            # MyInstance.BarEdgeColor = self.pg_2_graph_colors_pallete_1_bar_plot.palette().button().color().name()
            MyInstance.BarSaturation = (
                self.pg2_graph_saturation_spinBox_box_plot.value()
            )
            MyInstance.BarOrient = (
                self.pg2_graph_orientaitno_combobox_barplot.currentText()
            )
            # MyInstance.BareColor = self.pg_2_graph_colors_pallete_3_bar_plot.palette().button().color().name()
            MyInstance.BareWidth = self.pg2_graph_bar_errwidth_spinBox_box_plot.value()
            MyInstance.BarOpacity = self.pg2_graph_bar_ci_spinBox_box_plot.value()
            MyInstance.BareCapSize = self.pg2_graph_flier_size_spinBox_box_plot.value()
            MyInstance.CheckedErrorBars = self.pg_2_errorBars_bool_checkBox.isChecked()
            MyInstance.BoxBorderWidth = (
                self.pg2_graph_bar_borderwidth_spinBox_box_plot.value()
            )
            MyInstance.BarWidth = self.pg2_graph_bar_width_spinBox_box_plot.value()

        elif MyInstance.type == "Box Plot":
            # MyInstance.Box_palette = self.pg_2_graph_boxplot_pallete_style_combobox.currentText()
            # MyInstance.Box_Color = self.pg_2_graph_colors_pallete_2_box_plot.palette().button().color().name()
            MyInstance.BoxWidth = self.pg2_graph_width_spinBox_box_plot.value()
            MyInstance.BoxOrient = (
                self.pg_2_graph_boxplot_orientation_combobox.currentText()
            )
            MyInstance.BoxSaturation = (
                self.pg2_graph_saturation_spinBox_box_plot_2.value()
            )
            MyInstance.BoxFlierSize = self.pg2_graph_cap_size_spinBox_box_plot.value()
            # MyInstance.Box_EdgeColor = self.pg_2_graph_colors_pallete_1_box_plot.palette().button().color().name()
            MyInstance.BoxBorderWidth = (
                self.pg2_graph_line_width_spinBox_box_plot.value()
            )
            # MyInstance.Box_eCapSize = self.pg2_graph_cap_size_spinBox_box_plot.value()
            # MyInstance.BoxIndex = self.pg2_graph_index_combobox_boxplot.currentText()

            # MyInstance.Box_eCapSize
        elif MyInstance.type == "Swarm Plot":
            # MyInstance.Swarm_palette = self.pg_2_graph_swarmplot_pallete_style_combobox.currentText()
            # MyInstance.Swarm_Color = self.pg_2_graph_colors_pallete_2_swarmplot_plot.palette().button().color().name()
            # MyInstance.Swarm_EdgeColor = self.pg_2_graph_colors_pallete_swarmplot_plot.palette().button().color().name()
            MyInstance.SwarmWidth = (
                self.pg2_graph_border_width_spinBox_swarmplot.value()
            )
            # MyInstance.Swarm_Condition = self.pg2_graph_index_combobox_swarmplot.currentText()
            MyInstance.SwarmSize = self.pg2_graph_size_spinBox_swarmplot.value()
            MyInstance.SwarmOrientation = (
                self.pg2_graph_orientaitno_combobox_swarmplot.currentText()
            )

        elif MyInstance.type == "Violin Plot":
            # MyInstance.Violin_palette = self.pg_2_graph_violinplot_pallete_style_combobox.currentText()
            MyInstance.ViolinBorderWidth = (
                self.pg2_graph_border_width_spinBox_violinplot.value()
            )
            MyInstance.ViolinOrient = (
                self.pg2_graph_violinplot_orienation_combobox.currentText()
            )
            MyInstance.ViolinSaturation = (
                self.pg2_graph_saturation_spinBox_violinplot.value()
            )
            MyInstance.ViolinWidth = (
                self.pg2_graph_just_width_spinbox_violinplot.value()
            )
            MyInstance.ViolinInner = (
                self.pg2_graph_violinplot_InnerVal_combobox.currentText()
            )
            # MyInstance.Violin_Condition = self.pg2_graph_index_label_barplot.text()
            # MyInstance.Violin_eWidth = self.pg2_graph_border_width_spinBox_violinplot.value()
            # MyInstance.Violin_ErrorColor = self.pg_2_graph_colors_pallete_3_bar_plot.palette().button().color().name()
            MyInstance.ViolinCut = self.pg2_graph_cut_spinBox_vil.value()
            MyInstance.ViolinScale = (
                self.pg2_graph_scale_comboBox_violinplot.currentText()
            )
        return

    def Bar_AssignColorDialogToButton_pg2(
        self, bar_button_pg2, bar_comboboxItem_pg2=None, bar_index_pg2=None
    ):
        from PyQt6 import QtCore, QtGui, QtWidgets

        """
        This functions opens a color picker and assigns the button of interest the selected color
        If we have a pallete color already set then we need to adjust the pallete color
        """
        bar_color_pg2 = QtWidgets.QColorDialog.getColor()
        bar_fg_pg2 = bar_color_pg2.name()

        # logger.info(self.pg_2_graph_barplot_pallete_style_combobox.currentText())
        # logger.info(bar_fg_pg2)
        if self.pg_2_graph_barplot_pallete_style_combobox.currentText() == "Custom":
            bar_button_pg2.setText("")
            bar_button_pg2.setStyleSheet("background-color:" + str(bar_fg_pg2) + ";")
        if bar_comboboxItem_pg2 != None:
            bar_comboboxItem_pg2.setItemData(
                bar_index_pg2, bar_color_pg2, QtCore.Qt.BackgroundRole
            )
        # self.RecordValues()

    def Box_AssignColorDialogToButton_pg2(
        self, box_button_pg2, box_comboboxItem_pg2=None, box_index_pg2=None
    ):
        from PyQt6 import QtCore, QtGui, QtWidgets

        """
        This functions opens a color picker and assigns the button of interest the selected color
        """
        box_color_pg2 = QtWidgets.QColorDialog.getColor()
        box_fg_pg2 = box_color_pg2.name()

        if self.pg_2_graph_boxplot_pallete_style_combobox.currentText() == "Custom":
            box_button_pg2.setText("")
            box_button_pg2.setStyleSheet("background-color:" + str(box_fg_pg2) + ";")
        if box_comboboxItem_pg2 != None:
            box_comboboxItem_pg2.setItemData(
                box_index_pg2, box_color_pg2, QtCore.Qt.BackgroundRole
            )
        # self.RecordValues()

    def Swarm_AssignColorDialogToButton_pg2(
        self, swarm_button_pg2, swarm_comboboxItem_pg2=None, swarm_index_pg2=None
    ):
        from PyQt6 import QtCore, QtGui, QtWidgets

        """
        This functions opens a color picker and assigns the button of interest the selected color
        """
        swarm_color_pg2 = QtWidgets.QColorDialog.getColor()
        swarm_fg_pg2 = swarm_color_pg2.name()

        if self.pg_2_graph_swarmplot_pallete_style_combobox.currentText() == "Custom":
            swarm_button_pg2.setText("")
            swarm_button_pg2.setStyleSheet(
                "background-color:" + str(swarm_fg_pg2) + ";"
            )
        if swarm_comboboxItem_pg2 != None:
            swarm_comboboxItem_pg2.setItemData(
                swarm_index_pg2, swarm_color_pg2, QtCore.Qt.BackgroundRole
            )
        self.RecordValues()

    def Violin_AssignColorDialogToButton_pg2(
        self, violin_button_pg2, violin_comboboxItem_pg2=None, violin_index_pg2=None
    ):
        from PyQt6 import QtCore, QtGui, QtWidgets

        """
        This functions opens a color picker and assigns the button of interest the selected color
        """
        violin_color_pg2 = QtWidgets.QColorDialog.getColor()
        violin_fg_pg2 = violin_color_pg2.name()

        if self.pg_2_graph_violinplot_pallete_style_combobox.currentText() == "Custom":
            violin_button_pg2.setText("")
            violin_button_pg2.setStyleSheet(
                "background-color:" + str(violin_fg_pg2) + ";"
            )
        if violin_comboboxItem_pg2 != None:
            violin_comboboxItem_pg2.setItemData(
                violin_index_pg2, violin_color_pg2, QtCore.Qt.BackgroundRole
            )
        self.RecordValues()

    def swarm_palette_custom_pg2(self):
        for count in range(self.pg_2_graph_swarmplot_pallete_style_combobox.count()):
            if count != 0:
                self.pg_2_graph_colors_pallete_2_swarmplot_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_2_swarmplot_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
                self.pg_2_graph_colors_pallete_swarmplot_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_swarmplot_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
        self.RecordValues()

    def violin_palette_custom_pg2(self):
        for count in range(self.pg_2_graph_violinplot_pallete_style_combobox.count()):
            if count != 0:
                self.pg_2_graph_colors_pallete_2_violinplot.setText("Pallet")
                self.pg_2_graph_colors_pallete_2_violinplot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
                self.pg2_graph_border_color_violinplot_pallete_button.setText("Pallet")
                self.pg2_graph_border_color_violinplot_pallete_button.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
        self.RecordValues()

    def bar_palette_custom_pg2(self):
        for count in range(self.pg_2_graph_barplot_pallete_style_combobox.count()):
            if count != 0:
                self.pg_2_graph_colors_pallete_2_bar_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_2_bar_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
                self.pg_2_graph_colors_pallete_3_bar_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_3_bar_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
                self.pg_2_graph_colors_pallete_1_bar_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_1_bar_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
        self.RecordValues()

    def box_palette_custom_pg2(self):
        for count in range(self.pg_2_graph_boxplot_pallete_style_combobox.count()):
            if count != 0:
                self.pg_2_graph_colors_pallete_2_box_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_2_box_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
                self.pg_2_graph_colors_pallete_1_box_plot.setText("Pallet")
                self.pg_2_graph_colors_pallete_1_box_plot.setStyleSheet(
                    "background-color: #4c4c4c;"
                )
        self.RecordValues()

    def ReadVariablesPlotTools(self):
        """
        Here We Get the value from the plot instances and put them in the ui.
        This is done to reflect the value in the instance, its

        """
        logger.info("reading variables")
        if not self.pg2_graphs_view.currentItem():
            return
        text = self.pg2_graphs_view.currentItem().text()
        if text in self.MyVisualPlotHandler.WidgetDictionary.keys():
            plot_instance = self.MyVisualPlotHandler.WidgetDictionary[text]
        else:
            return
        if plot_instance.type == "Bar Plot":
            # bar_palette_index = self.pg_2_graph_barplot_pallete_style_combobox.findText(plot_instance.Bar_palette)
            # self.pg_2_graph_barplot_pallete_style_combobox.setItemText(bar_palette_index, plot_instance.Bar_palette)
            # self.pg_2_graph_colors_pallete_2_bar_plot.setStyleSheet("background-color: " + str(plot_instance.Bar_Color))
            # self.pg_2_graph_colors_pallete_1_bar_plot.setStyleSheet("background-color: " + str(plot_instance.Bar_EdgeColor))
            self.pg2_graph_saturation_spinBox_box_plot.setValue(
                plot_instance.BarSaturation
            )
            bar_orientation = self.pg2_graph_orientaitno_combobox_barplot.findText(
                plot_instance.BarOrient
            )
            self.pg2_graph_orientaitno_combobox_barplot.setCurrentIndex(bar_orientation)
            self.pg_2_errorBars_bool_checkBox.setChecked(plot_instance.CheckedErrorBars)
            self.pg2_graph_bar_borderwidth_spinBox_box_plot.setValue(
                plot_instance.BoxBorderWidth
            )
            self.pg2_graph_bar_width_spinBox_box_plot.setValue(plot_instance.BarWidth)
            # self.pg2_graph_index_combobox_barplot.setItemText(bar_condition, plot_instance.Bar_Condition)
            # self.pg_2_graph_colors_pallete_3_bar_plot.setStyleSheet("background-color: " + str(plot_instance.Bar_eColor))
            # self.pg2_graph_bar_errwidth_spinBox_box_plot.setValue(plot_instance.Bar_eWidth)
            self.pg2_graph_bar_ci_spinBox_box_plot.setValue(plot_instance.BarOpacity)
            self.pg2_graph_flier_size_spinBox_box_plot.setValue(
                plot_instance.BareCapSize
            )
        elif plot_instance.type == "Box Plot":
            self.pg2_graph_width_spinBox_box_plot.setValue(plot_instance.BoxWidth)
            box_orientation = self.pg_2_graph_boxplot_orientation_combobox.findText(
                plot_instance.BoxOrient
            )
            self.pg_2_graph_boxplot_orientation_combobox.setItemText(
                box_orientation, plot_instance.BoxOrient
            )
            self.pg2_graph_saturation_spinBox_box_plot_2.setValue(
                plot_instance.BoxSaturation
            )
            self.pg2_graph_line_width_spinBox_box_plot.setValue(
                plot_instance.BoxBorderWidth
            )
            self.pg_2_errorBars_barPlot_bool_checkBox_2.setChecked(
                plot_instance.CheckedErrorBars
            )

        elif plot_instance.type == "Swarm Plot":
            # swarm_palette_index = self.pg_2_graph_swarmplot_pallete_style_combobox.findText(plot_instance.Swarm_palette)
            # self.pg_2_graph_swarmplot_pallete_style_combobox.setItemText(swarm_palette_index, plot_instance.Swarm_palette)
            # self.pg_2_graph_colors_pallete_2_swarmplot_plot.setStyleSheet("background-color: " + str(plot_instance.Swarm_Color))
            # self.pg_2_graph_colors_pallete_swarmplot_plot.setStyleSheet("background-color: " + str(plot_instance.Swarm_EdgeColor))
            self.pg2_graph_border_width_spinBox_swarmplot.setValue(
                plot_instance.SwarmWidth
            )
            # swarm_condition = self.pg2_graph_index_combobox_swarmplot.findText(plot_instance.Swarm_Condition)
            # self.pg2_graph_index_combobox_swarmplot.setItemText(swarm_condition, plot_instance.Swarm_Condition)
            swarm_orientation = self.pg2_graph_orientaitno_combobox_swarmplot.findText(
                plot_instance.SwarmOrient
            )
            self.pg2_graph_orientaitno_combobox_swarmplot.setItemText(
                swarm_orientation, plot_instance.SwarmOrient
            )
            self.pg2_graph_size_spinBox_swarmplot.setValue(plot_instance.SwarmSize)
        elif plot_instance.type == "Violin Plot":
            InnerIndex = self.pg2_graph_violinplot_InnerVal_combobox.findText(
                plot_instance.ViolinInner
            )
            self.pg2_graph_violinplot_InnerVal_combobox.setCurrentIndex(InnerIndex)

            self.pg2_graph_just_width_spinbox_violinplot.setValue(
                plot_instance.ViolinWidth
            )
            violin_Orient = self.pg2_graph_violinplot_orienation_combobox.findText(
                plot_instance.ViolinOrient
            )
            self.pg2_graph_violinplot_orienation_combobox.setCurrentIndex(violin_Orient)
            self.pg2_graph_saturation_spinBox_violinplot.setValue(
                plot_instance.ViolinSaturation
            )
            # self.pg2_graph_border_width_spinBox_violinplot.setValue(plot_instance.ViolinBorderWidth)
            self.pg2_graph_cut_spinBox_vil.setValue(plot_instance.ViolinCut)
            self.pg2_graph_scale_comboBox_violinplot.findText(
                plot_instance.ViolinOrient
            )

            # Width = self.MainWindow.pg2_graph_border_width_spinbox_violinplot.value()
            # Orientation = self.MainWindowpg2_graph_violinplot_orienation_combobox.currentText()
            # Saturation  = self.MainWindowpg2_graph_saturation_spinBox_violinplot.value()
            # BorderWidth = self.MainWindowpg2_graph_border_width_spinBox_violinplot.value()
            # Cut = self.MainWindowpg2_graph_cut_spinBox_vil.value()
            # Scale = self.MainWindowpg2_graph_scale_comboBox_violinplot.currentText()

        self.DuringPlotWidgetSwitch = False

    def ExecNewOrg(self):
        """
        Opens New widnow for new analysis
        """
        from celer_sight_ai import config

        config.home_selection_step = 0  # set to 0, when user clicks on the home button it gets to organism selection.
        self.current_home_display_widget = self.orgSelectionSection
        self.stackedWidget.setCurrentWidget(self.orgSelectionSection)

        if hasattr(self, "new_analysis_object"):
            self.new_analysis_object.init_organism_settings()

        QtWidgets.QApplication.processEvents()

    def create_new_enviroment_with_category(self):
        # if the create new category button is clicked, first pull up dialog to do that
        selected_buttons = [  # should just be one for now
            i for i in self.category_selection_grid.items if i.isChecked()
        ]
        if self.new_category_pop_up_widget:
            self.new_category_pop_up_widget.close()
        self.current_home_display_widget = self.MainInterface
        self.ExecNewFile()
        self.CreateProject()
        self.new_analysis_object.init_user_params()
        config.global_signals.updateAnalysisStatus.emit()
        config.global_signals.updateIconsToolboxSignal.emit()

    # TODO: change this to prev organism form globalvars
    def ExecNewFile(self, projectType=None, analysisType=None, AreaofInterest=None):
        """
        Opens New widnow for new analysis
        """
        from celer_sight_ai import config

        if not projectType:
            return
        config.home_selection_step = 2  # set to 2, when user clicks on the home button it gets him right to the home page.
        self.stackedWidget.setCurrentWidget(self.MainInterface)
        self.viewer.setFocus()

        self.new_analysis_object.setPriorSettings(
            config.supercategory, AreaofInterest, analysisType
        )

        self.new_analysis_object.set_organism(projectType)
        # set the text for the regions
        self.category_selection_grid.spawn_buttons()

    @staticmethod
    def rgb2hex(r, g, b):
        import matplotlib

        return matplotlib.colors.to_hex((r, g, b))

    def setUpSpecificPlotWidget(self, nameWidget):
        from celer_sight_ai.gui.custom_widgets.plot_handler import specificPlotWidget

        MyInstance = self.MyVisualPlotHandler.WidgetDictionary
        currentItem = self.pg2_graphs_view.currentItem()
        currentName = currentItem.text()
        currentInstance = MyInstance[currentName]
        plotItemsList = []
        color_list = self.MyVisualPlotHandler.getInitSnsPallete()
        counter = 0
        logger.info("color lis tis len ", len(color_list))
        for key, value in self.DH.BLobj.groups["default"].conds.items():
            C1 = color_list[counter]
            tmpWIdget = specificPlotWidget(
                self,
                Condition=key,
                myMainColor=self.rgb2hex(C1[0], C1[1], C1[2]),
                myEdgeColor="#000000",
            )
            listItemTmp = QtWidgets.QListWidgetItem()
            self.pg_2_graph_colors_groupBox_listWidget.addItem(listItemTmp)
            plotItemsList.append(listItemTmp)

            listItemTmp.setSizeHint(QtCore.QSize(200, 40))
            self.pg_2_graph_colors_groupBox_listWidget.setItemWidget(
                listItemTmp, tmpWIdget.MyWidget
            )
            counter += 1
        logger.info("CURRENT spefici plot widget ref is ", nameWidget)
        self.MyVisualPlotHandler.specificPlotWidgetRef[nameWidget] = plotItemsList

    def show_only_active_plot_settings(self):
        """
        function that shows only plot of interest
        """
        from celer_sight_ai.gui.designer_widgets_py_files.plot_tools_widget_v4 import (
            Ui_Plot_tools_widget as plot_tools_widget_v4,
        )

        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar.hide()
        # self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot.hide()
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box.hide()
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin.hide()
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm.hide()
        logger.info("only shown plot of interest")
        # logger.info(self.MyVisualPlotHandler.WidgetDictionary)
        # Get the RNAi_list
        items = []
        for x in range(self.RNAi_list.count()):
            items.append(self.RNAi_list.item(x).text())
        if self.pg2_graphs_view.count() != 0:
            CR_item = self.pg2_graphs_view.currentItem()
            if CR_item == None:
                return
            text = CR_item.text()
            if text in self.MyVisualPlotHandler.WidgetDictionary.keys():
                plot_instance = self.MyVisualPlotHandler.WidgetDictionary[text]
            else:
                return
            if plot_instance.type == "Bar Plot":
                logger.info("Bar Plot shown")
                self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar.show()
                self.RecordValues()
                # Add index in combobox
                # self.pg2_graph_index_combobox_barplot.clear()
                # self.pg2_graph_index_combobox_barplot.addItem('All')
                # for index in items:
                #    self.pg2_graph_index_combobox_barplot.addItem(str(index))
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.setEnabled(False))
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.blockSignals(True))
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: QtWidgets.QApplication.processEvents())
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.AssignDuringPlotWidgetSwitch())
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.ReadVariablesPlotTools())
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.setEnabled(True))
                # self.pg2_graphs_view.currentRowChanged.connect(lambda: self.blockSignals(False))
                return
            elif plot_instance.type == "Dot Plot":
                logger.info("Dot Plot shown")
                self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot.show()
                return
            if plot_instance.type == "Box Plot":
                logger.info("Box Plot shown")
                self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box.show()
                # Add index in combobox
                # self.pg2_graph_index_combobox_boxplot.clear()
                # self.pg2_graph_index_combobox_boxplot.addItem('All')
                # for index in items:
                #     self.pg2_graph_index_combobox_boxplot.addItem(str(index))
                return
            if plot_instance.type == "Violin Plot":
                logger.info("Violin Plot shown")
                self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin.show()
                # Add index in combobox
                # self.pg2_graph_index_combobox_violinplot.clear()
                # self.pg2_graph_index_combobox_violinplot.addItem('All')
                # for index in items:
                #     self.pg2_graph_index_combobox_violinplot.addItem(str(index))
                # return
            if plot_instance.type == "Swarm Plot":
                logger.info("Swarm Plot shown")
                self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm.show()
                # Add index in combobox
                # self.pg2_graph_index_combobox_swarmplot.clear()
                # self.pg2_graph_index_combobox_swarmplot.addItem('All')
                # for index in items:
                #     self.pg2_graph_index_combobox_swarmplot.addItem(str(index))
                return

    def AssignDuringPlotWidgetSwitch(self):
        self.DuringPlotWidgetSwitch = True

    def ApplyUiSelectionBtn(self, action: str = None) -> None:
        all_actions_items = {
            "polygon": self.PolygonTool,
            "auto": self.actionAutoTool,
            "CELL_SPLIT_SEED": self.actionRemoveSelectionTool,
            "selection": self.actionSelectionTool,
            "move_mask": self.actionMoveTool,
            "make_spline": self.actionMakeSpline,
            "magic_brush_move": self.MagicBrushMoveTool,
            "skeleton grabcut": self.actionMakeSpline,
            "RF_MODE_BINARY": self.actionRF_MODE,
            "erraseTool": self.actionErraseTool,
            "keypoint_tool": self.actionKeypoint,
        }
        if not self.viewer.hasPhoto():
            action = "selection"
        self.viewer.ui_tool_selection.selected_button = action
        # here we make sure we have auto exclusivity and the right tool selcted
        for key, action_val in all_actions_items.items():
            if key == action:
                all_actions_items[key].setChecked(True)
            else:
                all_actions_items[key].setChecked(False)

    def SetUpButtons(self):
        """
        This is a fucntion taht converts all of the qpushbuttons to animationbuttons
        TODO: change the name f the function, its named the sane ass in the Add btnClass.py
        """
        import os
        from celer_sight_ai.gui.custom_widgets.animate_qpushbutton import (
            RepeatTimer,
            Animation_Button,
        )

        self.add_images_btn = self.ReplaceWidget(self.add_images_btn, Animation_Button)
        self.initialize_analysis_button = self.ReplaceWidget(
            self.initialize_analysis_button, Animation_Button
        )
        self.get_roi_ai_button = self.ReplaceWidget(
            self.get_roi_ai_button, Animation_Button
        )
        frame_group_pg1_left_container_top_layout = (
            self.frame_group_pg1_left_container_top.layout()
        )
        frame_group_pg1_left_container_top_layout.setSpacing(5)

        self.add_images_btn.setIconSize(QtCore.QSize(60, 60))
        self.add_images_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.initialize_analysis_button.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.add_images_btn.setText("Add Images")
        self.initialize_analysis_button.setText("Analyze")
        self.get_roi_ai_button.setText("Get ROI (AI)")

        self.add_images_btn.setMinimumWidth(108)
        self.initialize_analysis_button.setMinimumWidth(108)
        self.get_roi_ai_button.setMinimumWidth(108)
        self.add_images_btn.setMaximumHeight(40)
        self.initialize_analysis_button.setMaximumHeight(40)
        self.get_roi_ai_button.setMaximumHeight(40)
        self.add_images_btn.setMinimumHeight(30)
        self.initialize_analysis_button.setMinimumHeight(30)
        self.get_roi_ai_button.setMinimumHeight(30)
        MainbtnStyleSheet = """
                            QPushButton{
                                background-color:rgb(40,40,40);
                                border-radius: 5px;
                                border: 0px solid rgb(255,255,255);
                            }
                            QPushButton:hover{
                               border: 0px solid rgb(255,255,255);
                                background-color:rgb(45,45,45);
                                color: rgb(255,255,255);
                                }

                            """
        self.add_images_btn.setStyleSheet(MainbtnStyleSheet)

        self.initialize_analysis_button.setStyleSheet(MainbtnStyleSheet)
        self.get_roi_ai_button.setStyleSheet(MainbtnStyleSheet)
        QtWidgets.QApplication.processEvents()

        # RNAi list tabs icons:
        RNAiUpButtonListIcon = QtGui.QIcon()

        RNAiUpButtonListIcon.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/icons_aa_tool/up_rnai.png",
                )
            )
        )
        self.up_button_list.setIcon(RNAiUpButtonListIcon)
        self.up_button_list.setIconSize(QtCore.QSize(40, 40))

        RNAiDownButtonListIcon = QtGui.QIcon()
        RNAiDownButtonListIcon.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/icons_aa_tool/down_rnai.png",
                )
            )
        )
        self.down_button_list.setIcon(RNAiDownButtonListIcon)
        self.down_button_list.setIconSize(QtCore.QSize(40, 40))

        RNAiTrashButtonListIcon = QtGui.QIcon()
        RNAiTrashButtonListIcon.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/icons_aa_tool/minus_rnai.png",
                )
            )
        )
        self.delete_button_list.setIcon(RNAiTrashButtonListIcon)
        self.delete_button_list.setIconSize(QtCore.QSize(40, 40))

        RNAiTrashButtonListIcon = QtGui.QIcon()
        RNAiTrashButtonListIcon.addPixmap(
            QtGui.QPixmap(
                os.path.join(
                    os.environ["CELER_SIGHT_AI_HOME"],
                    "data/icons/icons_aa_tool/plus_rnai.png",
                )
            )
        )
        self.addRNAi_button_list.setIcon(RNAiTrashButtonListIcon)
        self.addRNAi_button_list.setIconSize(QtCore.QSize(40, 40))

        self.pg1_Maskshandler_groupBox_ToolBox.hide()
        self.pg1_settings_groupBox_mask_appearance_2.hide()
        # self.pg1_settings_groupBox_classes.hide()

        # hide mask tabs
        #
        # Set Up animatin cursor class
        #
        # from celer_sight_ai.gui.animate_qpushbutton import AnimationCursor
        # self.CustomCursor = AnimationCursor(self)
        from celer_sight_ai import config

        config.global_signals.StopCursorAnimationSignal.connect(
            lambda: self.StopCursorAnimation()
        )
        config.global_signals.RestoreCursor.connect(
            lambda: self.RestoreCursorViewerAndMain()
        )

    def setUpTabButtons(self):
        import os
        from celer_sight_ai.gui.custom_widgets.animate_qpushbutton import (
            RepeatTimer,
            TabAnimationButton,
        )

        self.sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )

        # tab animations buttons

        # from celer_sight_ai.gui.animate_qpushbutton import RepeatTimer, Animation_Button_TAB
        self.tabImageBtn = None
        #  Animation_Button_TAB(myID = 0)
        # icon_RNAi = QtGui.QIcon()
        # icon_RNAi.addPixmap(QtGui.QPixmap('data/icons/imageTab/imageAnimTop 200.png'))
        # self.tabImageBtn.setInitIcon(icon_RNAi)
        # baseP = "data/icons/imageTab/"
        # frames = os.listdir(baseP)
        # self.tabImageBtn.setFrames(baseP, frames)
        # self.tabImageBtn.setIconSize(QtCore.QSize(200, 200))
        # self.tabImageBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        # # because it starts in the begining and its checked:
        # icon_RNAiFInal = QtGui.QIcon()
        # icon_RNAiFInal.addPixmap(QtGui.QPixmap('data/icons/imageTab/imageAnimTop 221.png'))
        # self.tabImageBtn.setIcon(icon_RNAiFInal)

        self.tabDataBtn = None
        #  = Animation_Button_TAB(myID = 1)
        # icon_RNAi = QtGui.QIcon()
        # icon_RNAi.addPixmap(QtGui.QPixmap('data/icons/dataTab/imageAnimTop 200.png'))
        # self.tabDataBtn.setInitIcon(icon_RNAi)
        # baseP = "data/icons/dataTab/"
        # frames = os.listdir(baseP)
        # self.tabDataBtn.setFrames(baseP, frames)
        # self.tabDataBtn.setIconSize(QtCore.QSize(200, 200))
        # self.tabDataBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.tabPlotBtn = None
        #  = Animation_Button_TAB(myID = 2)
        # icon_RNAi = QtGui.QIcon()
        # icon_RNAi.addPixmap(QtGui.QPixmap('data/icons/plotTab/imageAnimTop 2_1####00.png'))
        # self.tabPlotBtn.setInitIcon(icon_RNAi)
        # baseP = "data/icons/plotTab/"
        # frames = os.listdir(baseP)
        # self.tabPlotBtn.setFrames(baseP, frames)
        # self.tabPlotBtn.setIconSize(QtCore.QSize(200, 200))
        # self.tabPlotBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        # #initializw the proper tabs as checked:

        # self.tabImageBtn.setChecked(True)
        # self.tabDataBtn.setChecked(False)
        # self.tabPlotBtn.setChecked(False)

        # self.tabImageBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.tabDataBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # self.tabPlotBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # self.tabImageBtn.setMaximumWidth(200)
        # self.tabDataBtn.setMaximumWidth(200)
        # self.tabPlotBtn.setMaximumWidth(200)

        # self.tabImageBtn.setStyleSheet("background-color:rgba(0,0,0,0);")
        # self.tabDataBtn.setStyleSheet("background-color:rgba(0,0,0,0);")
        # self.tabPlotBtn.setStyleSheet("background-color:rgba(0,0,0,0);")

        # self.Top_tabs_layout_horizontalLayout.addWidget(self.tabImageBtn,QtCore.Qt.AlignmentFlag.AlignLeft)
        # self.Top_tabs_layout_horizontalLayout.addWidget(self.tabDataBtn,QtCore.Qt.AlignmentFlag.AlignLeft)
        # self.Top_tabs_layout_horizontalLayout.addWidget(self.tabPlotBtn,QtCore.Qt.AlignmentFlag.AlignLeft)

        # self.tabImageBtn.clicked.connect(lambda: self.tabImageBtn.playAnim())
        # self.tabDataBtn.clicked.connect(lambda: self.tabDataBtn.playAnim())
        # self.tabPlotBtn.clicked.connect(lambda: self.tabPlotBtn.playAnim())

        # self.tabImageBtn.clicked.connect(lambda: self.setTabButtonCheckedCorrectly(idTab = 0))
        # self.tabDataBtn.clicked.connect(lambda: self.setTabButtonCheckedCorrectly(idTab = 1))
        # self.tabPlotBtn.clicked.connect(lambda: self.setTabButtonCheckedCorrectly(idTab = 2))

        from celer_sight_ai import config

        # self.tabPageBtn = Animation_Button()

        # self.tabPageBtn.setMinimumSize((QtCore.QSize(600, 80)))
        # self.tabPageBtn.setMaximumSize((QtCore.QSize(1100, 80)))

        # self.tabPageBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # self.tabPageBtn.setParent(self.replace1_2)
        # # self.Top_tabs_layout_horizontalLayout.addWidget(self.tabPageBtn,QtCore.Qt.AlignmentFlag.AlignLeft)
        # verticalSpacer = QtWidgets.QSpacerItem(100, 40, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        # self.Top_tabs_layout_horizontalLayout.addItem(verticalSpacer)

        # self.myProjectSettingsButtons =  WorkflowSettingsMainWindowTopRight_UI(self)
        # self.myProjectSettingsButtons.myWidget.setParent(self.MasterTabWidgets)
        # self.Top_tabs_layout_horizontalLayout.addWidget(self.myProjectSettingsButtons.myWidget,QtCore.Qt.AlignmentFlag.AlignLeft)
        # self.myProjectSettingsButtons.myWidget.show()
        # # self.tabPageBtn.setStyleSheet(buttonTabStyle)
        # # self.tabPageBtn.setSizePolicy(self.sizePolicy)
        # verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        # self.Top_tabs_layout_horizontalLayout.addItem(verticalSpacer)

    def setTabButtonCheckedCorrectly(self, idTab=0):
        if idTab == 0:
            self.tabImageBtn.setChecked(True)
            self.tabDataBtn.setChecked(False)
            self.tabPlotBtn.setChecked(False)
            # self.tabPlotBtn._timer.stop()
            # self.tabDataBtn._timer.stop()
            self.tabImageBtn.checkCheckState()
            self.tabDataBtn.checkCheckState()
            self.tabPlotBtn.checkCheckState()

        elif idTab == 1:
            self.tabImageBtn.setChecked(False)
            self.tabDataBtn.setChecked(True)
            self.tabPlotBtn.setChecked(False)
            # self.tabPlotBtn._timer.stop()
            # self.tabImageBtn._timer.stop()
            self.tabImageBtn.checkCheckState()
            self.tabDataBtn.checkCheckState()
            self.tabPlotBtn.checkCheckState()

        elif idTab == 2:
            self.tabImageBtn.setChecked(False)
            self.tabDataBtn.setChecked(False)
            self.tabPlotBtn.setChecked(True)
            # self.tabDataBtn._timer.stop()
            # self.tabDataBtn._timer.stop()
            self.tabImageBtn.checkCheckState()
            self.tabDataBtn.checkCheckState()
            self.tabPlotBtn.checkCheckState()

    def StopCursorAnimation(self):
        """
        When the timer is finished it returns the cursor to the normal state
        """
        try:
            self.CustomCursor._timer.force_stop()
            self.CustomCursor._setFrame(0)
        except Exception as e:
            logger.info(e)

    def RestoreCursorViewerAndMain(self):
        try:
            self.CustomCursor.RestoreCursor()
        except Exception as e:
            pass

    def EnhanceQGroupBox(self, InstanceToEnhance):
        """
        We are updating the out-of-the-box groupbox with an improved versiont hat allows animations
        InstanceToEnhance = Instance to add the extrafeatures
        """
        #
        # AddShadow
        #
        self.AddShadowToWidget(InstanceToEnhance)

        AnimationDuration = 250
        InstanceToEnhance.setCheckable(True)
        InstanceToEnhance.setChecked(False)
        InstanceToEnhance.ParAnimation = QtCore.QParallelAnimationGroup()
        # Get Initial Variables
        BegginPosX = InstanceToEnhance.pos().x()
        BegginPosY = InstanceToEnhance.pos().y()
        BegginWidth = InstanceToEnhance.width()
        BegginHeight = InstanceToEnhance.height()
        GeometryAnimation = QtCore.QPropertyAnimation(InstanceToEnhance, b"geometry")
        GeometryAnimation.setDuration(AnimationDuration)
        # GeometryAnimation.setStartValue(QtCore.QRect(AnimstartPosX, AnimstartPosY, initialWidth / 4, initialHeight / 4))
        # GeometryAnimation.setEndValue(QtCore.QRect(initialX, initialY, initialWidth, initialHeight))

    def ReplaceWidget(self, WidgetToReplace, WidgetToBeReplacedWith):
        """
        This function gets a widget and replaces it with the widget
        of interest while mainteing geomtery and position in the frame
        """
        ParentWidget = WidgetToReplace.parentWidget()
        width = WidgetToReplace.frameGeometry().width()
        height = WidgetToReplace.frameGeometry().height()
        # logger.info(ParentWidget.layout())
        if type(ParentWidget.layout()) == QtWidgets.QGridLayout:
            # logger.info(type(ParentWidget.layout()))
            idx = ParentWidget.layout().indexOf(WidgetToReplace)
            Location = ParentWidget.layout().getItemPosition(idx)
        else:
            # logger.info(type(ParentWidget.layout()))
            for i in range(ParentWidget.layout().count()):
                # logger.info(ParentWidget.layout().itemAt(i))
                if ParentWidget.layout().itemAt(i).widget() == WidgetToReplace:
                    # logger.info("OK")
                    Location = 0
        WidgetToReplace.setParent(None)
        WidgetToReplace.deleteLater()
        WidgetToReplace = None
        NewWIdget = WidgetToBeReplacedWith(ParentWidget)
        if type(ParentWidget.layout()) == QtWidgets.QGridLayout:
            ParentWidget.layout().addWidget(
                NewWIdget, Location[0], Location[1], Location[2], Location[3]
            )

        else:
            pass
            # ParentWidget.layout().addWidget(NewWIdget, 2)
        NewWIdget.setMinimumSize(QtCore.QSize(width, height))
        NewWIdget.setMaximumSize(QtCore.QSize(width, height))
        return NewWIdget

    def addDropInShadow(self, widget):
        # widget.ShadowInnerLabel = transparentEventLabel(widget)
        # widget.ShadowInnerLabel.setParent(widget)
        # widget.ShadowInnerLabel.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents,True)
        # widget.ShadowInnerLabel.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground ,True)
        # widget.ShadowInnerLabel.setStyleSheet("""
        #                                         border : 10px solid black;
        #                                         background: transparent;
        #                                         """)
        # widget.ShadowInnerLabel.setGeometry(-20,-20,widget.width()+30,widget.height()+30 )
        # widget.installEventFilter(widget)
        # sf = QtWidgets.QGraphicsDropShadowEffect()
        # sf.setColor(QtGui.QColor(0,0,0,200))
        # sf.setBlurRadius(60)
        # widget.ShadowInnerLabel.setGraphicsEffect(sf)
        # widget.ShadowInnerLabel.show()
        # #make a frame or a widget drop shadw inside it
        widget.leftSide = QtWidgets.QWidget()
        widget.TopSide = QtWidgets.QWidget()
        widget.RightSide = QtWidgets.QWidget()
        widget.BottomSide = QtWidgets.QWidget()

        widget.leftSide.setParent(widget)
        widget.TopSide.setParent(widget)
        widget.RightSide.setParent(widget)
        widget.BottomSide.setParent(widget)
        widget.leftSide.setGeometry(-30, -25, 25, widget.height() + 50)
        widget.TopSide.setGeometry(-25, -30, widget.width(), 25)
        widget.RightSide.setGeometry(widget.width(), 0, 25, widget.height())
        widget.BottomSide.setGeometry(0, widget.height(), widget.width(), 25)
        widget.installEventFilter(widget)
        sf = QtWidgets.QGraphicsDropShadowEffect()
        sf.setColor(QtGui.QColor(0, 0, 0, 200))
        sf.setBlurRadius(60)

        widget.leftSide.setGraphicsEffect(sf)
        sf = QtWidgets.QGraphicsDropShadowEffect()
        sf.setColor(QtGui.QColor(0, 0, 0, 200))
        sf.setBlurRadius(60)
        widget.TopSide.setGraphicsEffect(sf)
        sf = QtWidgets.QGraphicsDropShadowEffect()
        sf.setColor(QtGui.QColor(0, 0, 0, 200))
        sf.setBlurRadius(60)
        widget.RightSide.setGraphicsEffect(sf)
        sf = QtWidgets.QGraphicsDropShadowEffect()
        sf.setColor(QtGui.QColor(0, 0, 0, 200))
        sf.setBlurRadius(60)
        widget.BottomSide.setGraphicsEffect(sf)

    @staticmethod
    def csEventFilter(source, event):
        if event.type() == QtCore.QEvent.Type.Resize:
            source.leftSide.setGeometry(-30, 0, 25, source.height())
            source.TopSide.setGeometry(0, -30, source.width(), 25)
            source.RightSide.setGeometry(source.width() + 5, 0, 25, source.height())
            source.BottomSide.setGeometry(0, source.height() + 5, source.width(), 25)

        #     try:
        #         source.ShadowInnerLabel.setGeometry(-20,-20,source.width()+30,source.height()+30 )
        #     except Exception as e:
        #         logger.info(e)
        #     return True
        return True

    def ApplyAttributesToAllImages(self):
        """
        This is a function that is connected to the Apply To All Images and changes all of the buttons attributes to the current ones
        """
        logger.info("works!")
        try:
            for i in range(
                len(
                    self.DH.AssetMaskDictionaryBool[
                        self.DH.BLobj.get_current_condition()
                    ]
                )
            ):
                for x in range(
                    len(
                        self.DH.AssetMaskDictionaryBool[
                            self.DH.BLobj.get_current_condition()
                        ][i]
                    )
                ):
                    self.DH.AssetMaskDictionaryBool[
                        self.DH.BLobj.get_current_condition()
                    ][i][x].RegionAttribute = self.MasterMaskLabelcomboBox.currentText()
                    self.DH.AssetMaskDictionaryBool[
                        self.DH.BLobj.get_current_condition()
                    ][i][x].BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                        self.MasterMaskLabelcomboBox.currentText()
                    )
            for i in range(
                len(
                    self.DH.AssetMaskDictionaryPolygon[
                        self.DH.BLobj.get_current_condition()
                    ]
                )
            ):
                for x in range(
                    len(
                        self.DH.AssetMaskDictionaryPolygon[
                            self.DH.BLobj.get_current_condition()
                        ][i]
                    )
                ):
                    self.DH.AssetMaskDictionaryPolygon[
                        self.DH.BLobj.get_current_condition()
                    ][i][x].RegionAttribute = self.MasterMaskLabelcomboBox.currentText()
                    self.DH.AssetMaskDictionaryPolygon[
                        self.DH.BLobj.get_current_condition()
                    ][i][x].BBWidget.MaskPropertiesWidgetLabelcomboBox.setText(
                        self.MasterMaskLabelcomboBox.currentText()
                    )
            self.load_main_scene(self.current_imagenumber)
        except Exception as e:
            logger.info(e)

    # def decide_mask_generation_off_on_line(self):
    #     if self.comboBox_for_mask_generation.currentText == "Assisted":

    #     if self.comboBox_for_mask_generation.currentText == "Standalone":


class transparentEventLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self, parent)
        self.myParent = parent
        self.myParentType = type(self.myParent)


class aboutSectionClass(aboutSectionUiForm):
    def __init__(self, MainWindow=None):
        self.mydialog = QtWidgets.QDialog()
        # self.mydialog.setParent(MainWindow)
        self.setupUi(self.mydialog)
        from celer_sight_ai import config

        self.label_2.setText(str(config.APP_VERSION))

        self.mydialog.show()
        self.mydialog.raise_()

    def AddShadowToWidget(self, widget):
        BR = 40  # blur radius
        xo = -5  # xoffset
        yo = 7  # yoffset
        colorGUI = QtGui.QColor(0, 0, 0, 90)
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=BR, xOffset=xo, yOffset=yo, color=colorGUI
        )
        widget.setGraphicsEffect(shadow)


logger.info("Importing UiBlocks completed.")
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # TO make it work it just needs this:
    ui = CelerSightMainWindow()
    ui.SetupAll()
    sys.exit(app.exec())
