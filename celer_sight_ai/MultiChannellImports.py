import sys
import lazy_import
import os

config = lazy_import.lazy_module("celer_sight_ai.config")


if config.is_executable:
    sys.path.append([str(os.environ["CELER_SIGHT_AI_HOME"])])
# Python file for Special imporder
print("before importing pyqt6")
from PyQt6 import QtCore, QtGui, QtWidgets

import traceback

print("Before importing draggable button")
from celer_sight_ai.gui.designer_widgets.testDragableButton import (
    Ui_Dialog as DialogMultichannelImporter,
)


import logging
import shutil

logger = logging.getLogger(__name__)
from celer_sight_ai.configHandle import getServerAddress, getLogInAddress
import requests
import json
import asyncio
import time
from enum import Enum


# a class to define network result format
# **detectionTasks** is an enumeration of all the possible tasks that can be performed by a detection
# algorithm
class detectionTasks(Enum):
    binaryMask = 0
    binaryMaskWithClass = 1
    polygonMask = 2
    polygonMaskWithClass = 3
    probabilityMask = 4
    probabilityMaskWithClass = 5
    string = 6
    binaryClassification = 7
    multiClassClassification = 8
    image = 9
    pointCloud3D = 10
    keyPoints = 11


class global_vars:
    #### initialize all variable that determine
    #### which organism and which area of the mody
    #### we are measuring
    organism = None
    area = None
    analysis = None
    aggregates_count = False
    aggregates_volume = False
    mean_fluorescent = False
    Fragmentation = False
    AnalysisType = None
    Display_green_ch = False
    Display_red_ch = False
    Display_blue_ch = False
    Measure_green_ch = False
    Measure_red_ch = False
    Measure_blue_ch = False
    first_ratio = None
    second_ratio = None
    masks_state = False
    mask_expantion = 0
    is_mask_button_selected = False
    mode_draw = "add_mask"  # or "  remove_mask", extend_mask, cut_mask
    selected_mask = -1  # mode that selects our visible_selected mask
    colour = [0, 0, 255]
    MeasuredImageChannels = []
    SourceImageChannels = []
    area_used = None
    Sourceorganism = None
    AnalysisType = None


class userAttributesClass:
    username = None
    seshIDServer = None
    inferenceSession = None
    currentCondition = None
    currentGroup = "default"
    current_image_number = None
    skipUpdate = True  # TODO: remove this
    lab_name = None
    lab_uuid = None
    user_uuid = None
    license = None
    is_admin = False


class ChannelPickerSignals(QtCore.QObject):
    photoChanged = QtCore.pyqtSignal()

    ########################
    ######## Hooks #########
    ########################
    change_image_hook = QtCore.pyqtSignal(
        object
    )  # triggers every time the image id changes / scene is refreshed

    # Log in UI signals
    show_log_in_dialog_signal = QtCore.pyqtSignal()
    hide_log_in_dialog_signal = QtCore.pyqtSignal()
    show_splash_screen_signal = QtCore.pyqtSignal()
    hide_splash_screen_signal = QtCore.pyqtSignal()
    set_text_log_in_error_signal = QtCore.pyqtSignal(str)
    start_log_in_spinner = QtCore.pyqtSignal()
    stop_log_in_spinner = QtCore.pyqtSignal()
    launch_main_window_after_log_in_signal = QtCore.pyqtSignal(object)

    # Importer signals
    IndiLayoutChangedSignal = QtCore.pyqtSignal()
    CombLayoutChangedSignal = QtCore.pyqtSignal()
    UniteToolSignal = QtCore.pyqtSignal()
    OpenFolderSignal = QtCore.pyqtSignal()
    DialogImportSettingsSignal = QtCore.pyqtSignal(int)
    OpenIndiImagesForConditionFINISHED = QtCore.pyqtSignal(object)
    StopCursorAnimationSignal = QtCore.pyqtSignal()
    ShowPopUpWidgetTools = QtCore.pyqtSignal()
    HidePopUpWidgetTools = QtCore.pyqtSignal()
    PopUpWindowAnimationSignal = QtCore.pyqtSignal()
    RestoreCursor = QtCore.pyqtSignal()

    # dialog signals ## TO BE REPLACED ##
    loading_dialog_signal_update_progress_percent = QtCore.pyqtSignal(int)
    loading_dialog_signal_close = QtCore.pyqtSignal()
    loading_dialog_set_text = QtCore.pyqtSignal(str)
    loading_dialog_show = QtCore.pyqtSignal()
    loading_dialog_center = QtCore.pyqtSignal()

    # particle analysis dialog signals
    move_threshold_slider_particle_analysis_signal = QtCore.pyqtSignal(int)
    move_background_slider_particle_analysis_signal = QtCore.pyqtSignal(int)
    accept_particle_analysis_dialog_signal = (
        QtCore.pyqtSignal()
    )  # in ui --> done button

    update_signal = QtCore.pyqtSignal()
    shut_down_signal = QtCore.pyqtSignal()

    ########################
    # Save / Read files signals
    ########################
    save_celer_sight_file_signal = QtCore.pyqtSignal()
    load_celer_sight_file_signal = QtCore.pyqtSignal()

    ########################
    # Analysis signals
    ########################
    start_analysis_signal = QtCore.pyqtSignal()

    ########################
    # Remote Annotation Signals
    ########################
    update_remote_annotation_signal = QtCore.pyqtSignal(object)
    download_remote_image_signal = QtCore.pyqtSignal(
        object
    )  # object = the actual image object

    ########################
    # Annotation signals
    ########################
    # instance segmetnation (def create_annotation_object)
    update_class_scene_color_signal = QtCore.pyqtSignal(int)
    create_annotation_object_signal = QtCore.pyqtSignal(
        object
    )  # used to create mask object to contain the properties of the mask
    create_annotations_objects_signal = QtCore.pyqtSignal(
        object
    )  # used to create mask object to contain the properties of the mask
    MaskToSceneSignal = QtCore.pyqtSignal(
        object
    )  # used to add the mask object to the scene
    load_all_current_image_annotations_signal = QtCore.pyqtSignal(object)
    ensure_not_particle_class_selected_signal = QtCore.pyqtSignal()
    update_annotations_color_signal = (
        QtCore.pyqtSignal()
    )  # update the annotations opacity on the scene.
    toggle_mask_class_visibility_signal = QtCore.pyqtSignal(str)  # class uuid

    set_magic_tool_enabled_signal = QtCore.pyqtSignal(str)
    set_magic_tool_disabled_signal = QtCore.pyqtSignal(str)

    deleteMaskFromMainWindow = QtCore.pyqtSignal(object)
    delete_hole_from_mask_signal = QtCore.pyqtSignal(object)
    deleteTrackFromMainWindow = QtCore.pyqtSignal(object)

    annotation_generator_spinner_signal_start = QtCore.pyqtSignal()
    annotation_generator_spinner_signal_stop = QtCore.pyqtSignal()
    annotation_generator_stop_signal = QtCore.pyqtSignal()
    annotation_generator_start_signal = QtCore.pyqtSignal()

    spawn_inference_tile_graphics_items_signal = QtCore.pyqtSignal()

    delete_all_masks_with_class_signal = QtCore.pyqtSignal(str)

    ########################
    # Inference signals
    ########################
    # mark the image as loading for inference
    # object  = [imgID, ConditionID, groupID]
    startInferenceAnimationSignal = QtCore.pyqtSignal(str)
    check_and_end_inference_animation_signal = QtCore.pyqtSignal(object)
    endAllInferenceLoadingSignals = QtCore.pyqtSignal()
    start_single_button_inference_loading_signal = QtCore.pyqtSignal(object)
    stop_single_button_inference_loading_signal = QtCore.pyqtSignal(object)
    add_inference_tile_graphics_item_signal = QtCore.pyqtSignal(
        object
    )  # tile coordinates

    # cloud inference signals
    # start_cloud_inference_retrival_signal = QtCore.pyqtSignal()
    stop_cloud_inference_retrieval_signal = QtCore.pyqtSignal()

    remove_inference_tile_graphics_item_signal = QtCore.pyqtSignal(object)
    remove_all_inference_tile_graphics_items_signal = QtCore.pyqtSignal()

    set_mask_suggestor_generating_signal = QtCore.pyqtSignal(bool)

    addToML_Canvas_FG = QtCore.pyqtSignal(object)
    addToML_Canvas_BG = QtCore.pyqtSignal(object)

    update_ML_BitMapScene = QtCore.pyqtSignal()

    removeFromML_Canvas = QtCore.pyqtSignal(object)

    loadButton = QtCore.pyqtSignal(object)
    delete_image_with_button_signal = QtCore.pyqtSignal(object)

    # ML Model button signals
    uncheck_ml_button_signal = QtCore.pyqtSignal(object)

    # Pop Up tool menu signals
    tool_signal = QtCore.pyqtSignal()
    tool_signal_to_main = QtCore.pyqtSignal()

    # Load Threaded Signals
    LoadThreadedCasherBatch = QtCore.pyqtSignal(object)
    LoadThreadedCasherFly = QtCore.pyqtSignal(str)
    loadedImageToRam = QtCore.pyqtSignal(object)

    # other signals
    CopySpreadSheetToClipboard = QtCore.pyqtSignal(str)
    update_category_icons_signal = QtCore.pyqtSignal()
    refresh_categories_signal = QtCore.pyqtSignal()

    tabChangedbtn = QtCore.pyqtSignal(int)

    updateAnalysisStatus = QtCore.pyqtSignal()

    # signals to check whether data has been corrupted
    check_data_corruption_signal = QtCore.pyqtSignal()

    # for the ML
    trainingLabelUpdateSignal = QtCore.pyqtSignal()
    predictingLabeUpdatelSignal = QtCore.pyqtSignal()
    PreProcessingLabeUpdatelSignal = QtCore.pyqtSignal()
    spawnLoadedMLModelSignal = QtCore.pyqtSignal()
    removeLoadedMLModelSignal = QtCore.pyqtSignal()

    blurAnimation_NewMenuSignal_ON = QtCore.pyqtSignal()
    blurAnimation_NewMenuSignal_OFF = QtCore.pyqtSignal()

    setSplashText = QtCore.pyqtSignal(str)

    # updater signals
    update_celer_sight_ai_signal = QtCore.pyqtSignal()

    lunchUpdaterWindowSignal = QtCore.pyqtSignal()
    UpdaterWindowPercentSignal = QtCore.pyqtSignal(float)
    updateIconsToolboxSignal = QtCore.pyqtSignal()
    loadSceneSignal = QtCore.pyqtSignal(object)

    ensure_current_image_button_visible_signal = QtCore.pyqtSignal()
    next_image_signal = QtCore.pyqtSignal()
    previous_image_signal = QtCore.pyqtSignal()

    reCheckNeuralNets_magicBoxSignal = QtCore.pyqtSignal()

    # For auto AI inference
    inferenceSessionLabelServer = QtCore.pyqtSignal(str)
    inferenceResultLabelServer = QtCore.pyqtSignal(str)

    complete_analysis_signal = QtCore.pyqtSignal(object)

    lunch_APP_LINK_FILE_downloader = QtCore.pyqtSignal()

    ##########################################
    #### Error / Warnings & notifications ####
    ##########################################
    warningSignal = QtCore.pyqtSignal(str)
    errorSignal = QtCore.pyqtSignal(str)
    fatalErrorSignal = QtCore.pyqtSignal(str)
    successSignal = QtCore.pyqtSignal(str)
    notificationSignal = QtCore.pyqtSignal(str)
    successSignal_short = QtCore.pyqtSignal(
        str
    )  #  Not working correctly, but also not implemented TODO: fix
    actionDialogSignal = QtCore.pyqtSignal(str, object)

    app_file_signal = QtCore.pyqtSignal(str)
    close_accept_notification_signal = QtCore.pyqtSignal()  # closes the current window

    ############################
    ###### Progress bar ########
    ############################
    start_progress_bar_signal = QtCore.pyqtSignal(object)  # object is a dict
    # The input of the start_progress_bar :  {"title" : "...",
    #  "main_text" : "this can be markdown"}
    update_progress_bar_progress_signal = QtCore.pyqtSignal(
        object
    )  # object is a dict --? {"percent": int}
    # The input of the update_progress_bar_progress
    complete_progress_bar_signal = QtCore.pyqtSignal()

    # Signals to get preview buttons setup in the UI and import the image and generate preview for the button
    create_button_instance_signal = QtCore.pyqtSignal(object)
    spawn_button_from_image_url_signal = QtCore.pyqtSignal(object)
    load_image_to_preview_button_signal = QtCore.pyqtSignal(object)
    refresh_image_preview_graphicsscene_signal = QtCore.pyqtSignal()
    AddPixmapFromImageSignal = QtCore.pyqtSignal(object)  # pixmap to the button

    ############################
    ##### Ultra High Res #######
    ############################
    create_pyramidal_tiff_for_image_object_signal = QtCore.pyqtSignal(
        object
    )  # object : image object for which to generate the pyramidal tiff  # runs on high res images that dont have pyrmadical support
    update_scene_ultra_high_res_plane_signal = QtCore.pyqtSignal(object)
    add_partial_slide_images_to_scene_signal = QtCore.pyqtSignal(object)
    check_and_update_high_res_slides_signal = QtCore.pyqtSignal()

    # lock ui signals
    lock_ui_signal = QtCore.pyqtSignal(
        object
    )  # can be workflow , left_group , image_viewer , condition_buttons
    unlock_ui_signal = QtCore.pyqtSignal()

    ############################
    ##### Image Viewer #########
    ############################
    # scene signals
    load_main_scene_gather_image_threaded_signal = QtCore.pyqtSignal(
        object
    )  # threaded part of reading the image, reads 2 images concurently in a threaded way and displays the original image
    load_main_scene_display_image_signal = QtCore.pyqtSignal(
        object
    )  # qt part of displaying the image in scene
    refresh_main_scene_image_only_signal = QtCore.pyqtSignal(object)
    load_main_scene_signal = QtCore.pyqtSignal()
    load_main_scene_and_fit_in_view_signal = QtCore.pyqtSignal()

    # treatment list widget signals
    RNAi_list_widget_update_signal = QtCore.pyqtSignal(object)
    RNAi_list_widget_start_editing_signal = QtCore.pyqtSignal(object)

    ##############################
    #### WINDOW STATE SIGNALS ####
    ##############################

    close_celer_sight_signal = QtCore.pyqtSignal()
    minimize_celer_sight_signal = QtCore.pyqtSignal()
    maximize_celer_sight_signal = QtCore.pyqtSignal()


class MultiChannelImporter(QtWidgets.QDialog):
    def __init__(self):
        super(MultiChannelImporter, self).__init__()
        pass


class MultiChannelImporterUi(DialogMultichannelImporter):
    def __init__(self, MainWindow):
        super(MultiChannelImporterUi, self).__init__()
        self.MultiChannelImporterForm = MultiChannelImporter()
        self.setupUi(self.MultiChannelImporterForm)
        self.retranslateUi(self.MultiChannelImporterForm)
        self.MultiChannelImporterForm.show()
        self.MultiChannelImporterForm.closeEvent = self.closeEvent
        self.Condition = None
        self.MainWindow = MainWindow
        self.allContainedDraggableButtons = []
        # self.gridLayout_2.removeWidget(self.graphicsView)
        # self.graphicsView.hide()
        # self.graphicsView.deleteLater()
        # QtWidgets.QApplication.processEvents()
        self.graphicsView = ChannelViewer(self.MultiChannelImporterForm)
        self.graphicsView.setStyleSheet(self.frame.styleSheet())
        self.gridLayout_2.addWidget(self.graphicsView, 3, 1, 1, 1)

        self._scene = QtWidgets.QGraphicsScene(self.graphicsView)
        from celer_sight_ai.gui.custom_widgets.scene import BackgroundGraphicsItem

        self._photo = BackgroundGraphicsItem()
        self._photo.setZValue(-50)
        self._scene.addItem(self._photo)
        self.graphicsView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.graphicsView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.graphicsView.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self.UniteToolButton.clicked.connect(
            lambda: self.graphicsView.ToggleOverlayMode()
        )
        # self.BtDct = {
        #     "pushButton" : self.pushButton,
        #     "pushButton_2" : self.pushButton_2,
        #     "pushButton_3" : self.pushButton_3,F
        #     "pushButton_4" : self.pushButton_4,
        #     "pushButton_5" : self.pushButton_5,
        #     "pushButton_6" : self.pushButton_6,
        #     "pushButton_7" : self.pushButton_7,
        #     "pushButton_8" : self.pushButton_8,
        #     "pushButton_9" : self.pushButton_9
        # }

        listWidgetsToAddShadow = [
            self.frame_2,
            self.CombinedChannelsLabel,
            self.frame_3,
            self.IndividualChannelsLabel,
            self.frame_5,
            self.ImportButton,
            self.CancelButton,
            self.Channels,
        ]
        for SomeWidget in listWidgetsToAddShadow:
            self.MainWindow.AddShadowToWidget(SomeWidget)

        self.DeleteAllbuttons()
        from celer_sight_ai import config

        config.global_signals.IndiLayoutChangedSignal.connect(
            lambda: self.ChangeLayoutIndi()
        )
        config.global_signals.OpenIndiImagesForConditionFINISHED.connect(
            self.IndiImportMultiThreaded
        )

        self.OpenFolderButton.hide()
        self.UniteToolButton.hide()
        self.SplitterButton.hide()
        self.SeparateViewsButton.hide()

        # self.ImportButton.clicked.connect(lambda: self.ImportAllCombinedButtons())
        self.CancelButton.clicked.connect(lambda: self.Cancel())
        self.DetermineNewCondition()

    def closeEvent(self, event):
        logger.info("closing")
        from celer_sight_ai import config

        config.global_signals.IndiLayoutChangedSignal.disconnect()
        config.global_signals.OpenIndiImagesForConditionFINISHED.disconnect()
        try:
            config.global_signals.loadButton.disconnect()
        except:
            pass

    def IndiImportMultiThreaded(self, my_files_list=None):
        # Animated Bar for progress on importing images to multichannel importer

        from celer_sight_ai.gui.designer_widgets_py_files.LoadingAnimation1 import (
            Ui_Dialog as LoadingAnimationDialogForm,
        )

        self.MyLoadingAnimationDialogForm = LoadingAnimationDialogForm()
        self.LoadingAnimationWidget = QtWidgets.QDialog()
        self.MyLoadingAnimationDialogForm.setupUi(self.LoadingAnimationWidget)
        self.MyLoadingAnimationDialogForm.retranslateUi(self.LoadingAnimationWidget)
        self.LoadingAnimationWidget.show()

        QtWidgets.QApplication.processEvents()
        import math

        self.image_list = []
        self.name_list = []
        # set up the start part:
        self.IncrementCount = 0
        self.Increment = 100 / (len(my_files_list))
        self.prevNumOfItems = self.gridLayout.count()
        self.CombinedListLen = len(my_files_list) + self.prevNumOfItems
        self.SpacingBetweenBtns = 6
        self.ItemsWidthNum = 8
        logger.info("combined items are ", self.CombinedListLen)
        self.heightval = math.floor(self.CombinedListLen / self.ItemsWidthNum) + 1
        self.positions = [
            (i, j) for i in range(self.heightval) for j in range(self.ItemsWidthNum)
        ]
        logger.info("positions are ", self.positions)
        for u in range(self.prevNumOfItems):
            self.image_list.insert(0, None)

        x = 0

        from celer_sight_ai import config

        config.global_signals.loadButton.connect(self.FillButtonsFromListMainThread)

        # Set up multiprocess
        self.MyThreadPool = None
        from celer_sight_ai.core.Workers import Worker

        self.FillButtonsFromListThreaded = Worker(
            self.FIllButtonsfromListParallel, my_files_list
        )
        self.MyThreadPool = QtCore.QThreadPool()  # self.MyThreadPool.start(MyWorker)
        self.MyThreadPool.start(self.FillButtonsFromListThreaded)
        self.FillButtonsFromListThreaded.signals.finished.connect(
            self.OnFinishImportingToMultiChannel
        )

    # self.FillButtonsFromListThreaded.signals.finished.
    # deleteLater()
    #         logger.info("IndiImportMultiThreaded finished just now ")

    def OnFinishImportingToMultiChannel(self):
        self.LoadingAnimationWidget.close()

    def DetermineNewCondition(self):
        """
        Determines the name that goes to ConditionName plain text edit
        runs everytime the window pops up
        """
        if self.Condition == None:
            #
            # Set Current Condition
            #
            self.Condition = "Control"
            self.ConditionName.setText(self.Condition)
        else:
            self.Comdotopm = "Condition 1"
            self.ConditionName.setText(self.Condition)

    def CollectImages(self, MODE=0):
        """
        Depending on the modes we gother images
        0,0 = 0 None
        1,0 = 1 Combined only
        0,1 = 2 indi only
        1,1 = 3
        """
        allImages = []
        if MODE == 0:
            return
        elif MODE == 1:
            items = (
                self.gridLayout_7.itemAt(i) for i in range(self.gridLayout_7.count())
            )
            for w in items:
                if w.widget().Image1 != None:
                    allImages.append(
                        w.widget()
                        .FuseImages(w.widget().Image1, w.widget().Image2)
                        .copy()
                    )
        elif MODE == 2:
            items = (self.gridLayout.itemAt(i) for i in range(self.gridLayout.count()))
            for w in items:
                allImages.append(w.widget().Image.copy())
        elif MODE == 3:
            items = (
                self.gridLayout_7.itemAt(i) for i in range(self.gridLayout_7.count())
            )
            for w in items:
                if w.widget().Image1 != None:
                    allImages.append(
                        w.widget()
                        .FuseImages(w.widget().Image1, w.widget().Image2)
                        .copy()
                    )
            items = (self.gridLayout.itemAt(i) for i in range(self.gridLayout.count()))
            for w in items:
                allImages.append(w.widget().Image.copy())
        return allImages

    def Cancel(self):
        """
        We are clearing out all buttons from memory
        """
        # AllCols = self.gridLayout_7.columnCount()
        # AllRows =  self.gridLayout_7.rowCount()
        # allImages= []
        # for x in range(AllCols):
        #     for y in range(AllRows):
        #         try:
        #             item1 = self.gridLayout_7.itemAtPosition(y,x)
        #             self.gridLayout_7.removeItem(item1)
        #             item1.widget().deleteLater()
        #         except Exception as e:
        #             logger.info(e)
        #             pass
        # AllCols = self.gridLayout.columnCount()
        # AllRows =  self.gridLayout.rowCount()
        # allImages= []
        # for x in range(AllCols):
        #     for y in range(AllRows):
        #         try:
        #             item1 = self.gridLayout.itemAtPosition(y,x)
        #             self.gridLayout_7.removeItem(item1)
        #             item1.widget().deleteLater()
        #         except Exception as e:
        #             logger.info(e)
        #             pass
        self.MultiChannelImporterForm.close()
        self.MultiChannelImporterForm.deleteLater()

    def ImportAllCombinedButtons(self):
        """
        For all of the Combined buttons generate iamge and put to main Window DH
        """
        AllCols = self.gridLayout_7.columnCount()
        AllRows = self.gridLayout_7.rowCount()
        allImages = []
        for x in range(AllCols):
            for y in range(AllRows):
                if self.gridLayout_7.itemAtPosition(x, y) == None:
                    continue
                else:
                    myImage = (
                        self.gridLayout_7.itemAtPosition(x, y)
                        .widget()
                        .FuseImages(
                            self.gridLayout_7.itemAtPosition(x, y)
                            .widget()
                            .FuseImages(
                                self.gridLayout_7.itemAtPosition(x, y)
                                .widget()
                                .MyImage1,
                                self.gridLayout_7.itemAtPosition(x, y)
                                .widget()
                                .MyImage2,
                            )
                        )
                    )
                allImages.append(myImage)
        import cv2

        logger.info(len(allImages))
        for i in range(len(allImages)):
            allImages[i] = cv2.cvtColor(allImages[i], cv2.COLOR_BGR2RGB)
        return allImages

    def CountUsedColumns(self, Layout):
        AllCols = Layout.columnCount()
        AllRows = Layout.rowCount()
        Count = 0
        for x in range(AllCols):
            HasWidget = False
            for y in range(AllRows):
                tmpWidget = Layout.itemAtPosition(y, x)
                if HasWidget == False and tmpWidget != None:
                    HasWidget = True
            if HasWidget == True:
                Count += 1
        return Count

    def ChangeLayoutIndi(self):
        SpacingBetweenBtns = 6
        self.ItemsWidthNum = self.CountUsedColumns(self.gridLayout)
        self.ItemsHeightNum = self.gridLayout.rowCount()
        logger.info("Col count is ", self.ItemsWidthNum)
        minimWidth = (150 * self.ItemsWidthNum) + (
            self.ItemsWidthNum + SpacingBetweenBtns
        )
        minimHeight = (150 * self.ItemsHeightNum) + (
            self.ItemsHeightNum + SpacingBetweenBtns
        )
        # self.frame.setMinimumWidth(minimWidth)
        # self.frame.setMaximumHeight(minimHeight)
        logger.info(minimWidth)

    def DetectMatches2(self, im1, im2):
        import cv2
        import numpy as np

        """
        Substract the channels from the images and return the
        """
        ch1 = self.GetCurrentChannel(im1)
        ch2 = self.GetCurrentChannel(im2)
        # if ch1 != ch2:
        return np.mean(im1[:, :, ch1] - im2[:, :, ch2])
        # else:
        #     return int(255)

    def GetCurrentChannel(self, image):
        """
        Finds the largest intensity in the 3 avaiblable channels
        """
        import numpy as np

        ch1 = 0
        ch2 = 0
        ch3 = 0
        ch1 = np.mean(image[:, :, 0])
        ch2 = np.mean(image[:, :, 1])
        ch3 = np.mean(image[:, :, 2])
        if ch1 > ch2 and ch1 > ch3:
            return 0
        if ch3 > ch2 and ch3 > ch1:
            return 2
        if ch2 > ch1 and ch2 > ch3:
            return 1

    def DetectMatches(self, im1, im2):
        import cv2
        import numpy as np

        gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # initialize the AKAZE descriptor, then detect keypoints and extract
        # local invariant descriptors from the image
        detector = cv2.AKAZE_create()
        (kps1, descs1) = detector.detectAndCompute(gray1, None)
        (kps2, descs2) = detector.detectAndCompute(gray2, None)

        # logger.info("keypoints: {}, descriptors: {}".format(len(kps1), descs1.shape))
        # logger.info("keypoints: {}, descriptors: {}".format(len(kps2), descs2.shape))

        # Match the features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(descs1, descs2, k=2)  # typo fixed

        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.9 * n.distance:
                good.append([m])
        return len(good)
        # # cv2.drawMatchesKnn expects list of lists as matches.
        # im3 = cv2.drawMatchesKnn(im1, kps1, im2, kps2, good[1:200], None, flags=2)
        # cv2.imshow("AKAZE matching", im3)
        # cv2.waitKey(0)

    def DeleteAllbuttons(self):
        items = (self.gridLayout.itemAt(i) for i in range(self.gridLayout.count()))
        for w in items:
            if w.widget() != None:
                w.widget().deleteLater()

    def FIllButtonsfromListParallel(self, MyList=None, progress_callback=None):
        "contains only the part of importing images"
        # This should be deprecated
        from celer_sight_ai import config

        import numpy as np
        import glob
        import cv2
        import math
        import os
        from skimage.transform import resize

        ImageId = 0
        ReduceBy = 3
        for filename in MyList:  # assuming gif
            im, result_dict = self.readImage(filename)
            if not isinstance(im, (np.ndarray, np.generic)):
                continue
            if not np.any(im):
                continue
            resizedImage = resize(
                im,
                (im.shape[0] // ReduceBy, im.shape[1] // ReduceBy),
                anti_aliasing=False,
                preserve_range=True,
            )

            config.global_signals.loadButton.emit([im, ImageId, filename, resizedImage])
            logger.debug("Signal emited for fill buttons")
            ImageId += 1
        return None

    def FillButtonsFromListMainThread(self, MyList=[]):
        "only the setting up dutton part of 1 button"

        self.MyLoadingAnimationDialogForm.ImportingLabel.setText("Importing Images..")
        image = MyList[0]
        MyID = MyList[1]
        FileName = MyList[2]
        resizedImage = MyList[3]
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        logger.debug(f"at pos {MyID+self.prevNumOfItems}")
        logger.debug(f"{len(self.positions)}")
        AddedPos = self.positions[MyID + self.prevNumOfItems]
        # logger.info("adding at : ", *position)
        btntmp = DragButton(self)
        self.allContainedDraggableButtons.append(btntmp)
        btntmp.setSizePolicy(sizePolicy)
        btntmp.setMinimumSize(QtCore.QSize(150, 150))
        btntmp.setMaximumSize(QtCore.QSize(150, 150))
        btntmp.setObjectName(FileName)
        btntmp.imageFileName = FileName
        self.gridLayout.addWidget(btntmp, AddedPos[0], AddedPos[1])  # ,0,0)
        btntmp.resizedImage = resizedImage
        btntmp.Image = image
        btntmp.SetSelfImage(image)
        btntmp.SetProperties()
        # x +=1
        self.IncrementCount += self.Increment
        self.MyLoadingAnimationDialogForm.progressBar.setValue(int(self.IncrementCount))

        logger.info("Setting up images for new condition.")

    def FillButtonsFromList(self, MyList=None, progress_callback=None):
        # Needs to be deprecated
        import glob
        import cv2
        import math
        import os
        import numpy as np

        image_list = []
        nameList = []
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())

        self.MyLoadingAnimationDialogForm.ImportingLabel.setText("Importing Images..")

        IncrementCount = 0
        Increment = 100 / (2 * len(MyList))
        for filename in MyList:  # assuming gif
            im, result_dict = self.readImage(filename)
            if not isinstance(im, (np.ndarray, np.generic)):
                continue
            image_list.append(im)
            nameList.append(os.path.basename(filename))
            IncrementCount += Increment

            self.MyLoadingAnimationDialogForm.progressBar.setValue(int(IncrementCount))
            QtWidgets.QApplication.processEvents()
        x = 0

        # This needs to be added so that we dont overlap objects:
        prevNumOfItems = self.gridLayout.count()
        CombinedListLen = len(MyList) + prevNumOfItems

        SpacingBetweenBtns = 6
        self.ItemsWidthNum = 8
        heightval = math.floor(CombinedListLen / self.ItemsWidthNum) + 1
        positions = [
            (i, j) for i in range(heightval) for j in range(self.ItemsWidthNum)
        ]

        self.MyLoadingAnimationDialogForm.ImportingLabel.setText("Setting up buttons..")
        logger.info("positions are ", positions)
        # fill up image list so that already aded images are none and length is previous images + new ones
        for u in range(prevNumOfItems):
            image_list.insert(0, None)
        it = 0
        for position, image in zip(positions, image_list):
            if prevNumOfItems != 0:
                prevNumOfItems -= 1
                logger.info("skiping")
                continue
            logger.info("adding at : ", *position)
            btntmp = DragButton(self)
            btntmp.setSizePolicy(sizePolicy)
            btntmp.setMinimumSize(QtCore.QSize(150, 150))
            btntmp.setMaximumSize(QtCore.QSize(150, 150))
            btntmp.setObjectName(nameList[x])
            # logger.info("name is",nameList[x])
            logger.info(*position)
            self.gridLayout.addWidget(btntmp, *position)  # ,0,0)
            btntmp.Image = image
            btntmp.SetSelfImage(image, MyList[it])
            btntmp.SetProperties()
            x += 1
            IncrementCount += Increment
            self.MyLoadingAnimationDialogForm.progressBar.setValue(int(IncrementCount))
            QtWidgets.QApplication.processEvents()
            it += 1
        minimWidth = (150 * self.ItemsWidthNum) + (
            self.ItemsWidthNum + SpacingBetweenBtns
        )
        self.ItemsHeightNum = self.gridLayout.rowCount()
        minimHeight = (150 * self.ItemsHeightNum) + (
            self.ItemsHeightNum + SpacingBetweenBtns
        )
        self.frame.setMinimumWidth(minimWidth)
        self.frame.setMinimumHeight(minimHeight)
        self.LoadingAnimationWidget.close()
        return


class CombinedDragButton(QtWidgets.QPushButton):
    def __init__(self, MainWidget=None):
        super(CombinedDragButton, self).__init__()
        self.MainWidget = MainWidget
        self.WidgetSize = QtCore.QSize(150, 150)
        self.Image1 = None
        self.Image2 = None
        # self.HoverImage = None # when the cursor is over image
        self.DragImage = None  # whem the button is drugged
        self.contextMenu = QtWidgets.QMenu(self)
        SeparateChannelsAction = self.contextMenu.addAction("Separate Channels")
        RemoveRedAction = self.contextMenu.addAction("Remove Red")
        RemoveGreenAction = self.contextMenu.addAction("Remove Green")
        RemoveBlueAction = self.contextMenu.addAction("Remove Blue")

        SeparateChannelsAction.triggered.connect(lambda: self.SeparateChannels())
        # RemoveRedAction.triggered.connect(lambda: self.SetAnalysisStatus(Status=False))
        self.imgPath = None

    def GetCurrentChannel(self, image):
        """
        Finds the largest intensity in the 3 avaiblable channels
        """
        import numpy as np

        ch1 = 0
        ch2 = 0
        ch3 = 0
        ch1 = np.mean(image[:, :, 0])
        ch2 = np.mean(image[:, :, 1])
        ch3 = np.mean(image[:, :, 2])
        if ch1 > ch2 and ch1 > ch3:
            return 0
        if ch3 > ch2 and ch3 > ch1:
            return 2
        if ch2 > ch1 and ch2 > ch3:
            return 1

    def FuseImages(self, image1, image2):
        FusedImage = image1.copy()
        ch1 = self.GetCurrentChannel(image1)
        ch2 = self.GetCurrentChannel(image2)
        if ch1 != ch2:
            FusedImage[:, :, ch2] = image2[:, :, ch2]
            return FusedImage.copy()
        else:
            logger.info("error fused")

    def SeparateChannels(self):
        spot1, spot2 = self.GetNextAvailableSpotInLayout(self.MainWidget.gridLayout)
        try:
            if self.PushButton1 != None:
                self.MainWidget.gridLayout.addWidget(
                    self.PushButton1, spot1, spot2, 1, 1
                )
                self.PushButton1.show()
        except:
            pass
        try:
            if self.PushButton2 != None:
                spot1, spot2 = self.GetNextAvailableSpotInLayout(
                    self.MainWidget.gridLayout
                )
                self.MainWidget.gridLayout.addWidget(
                    self.PushButton2, spot1, spot2, 1, 1
                )
                config.global_signals.IndiLayoutChangedSignal.emit()
                self.PushButton2.show()
        except:
            pass
        self.MainWidget.gridLayout_7.removeWidget(self)
        self.hide()
        self.deleteLater()

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec(self.mapToGlobal(event.position()))

    def SetProperties(self):
        self.Iam = 1  # combinedObject

    def CreatePushButtons(self, PushButton1, PushButton2):
        self.PushButton1 = PushButton1
        self.PushButton2 = PushButton2

        self.setText("")
        self.setObjectName("")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.setSizePolicy(sizePolicy)
        self.MyImage1 = self.PushButton1.Image.copy()
        self.MyImage2 = self.PushButton2.Image.copy()
        self.Combine2Channels(self.PushButton1.Image, self.PushButton2.Image)
        self.HovedImage = self.GetBorders(self.Image.copy())

        piximage1 = QtGui.QImage(
            self.Image.data,
            self.Image.shape[1],
            self.Image.shape[0],
            self.Image.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOn = QtGui.QPixmap(piximage1)
        piximage2 = QtGui.QImage(
            self.HovedImage.data,
            self.HovedImage.shape[1],
            self.HovedImage.shape[0],
            self.HovedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOff = QtGui.QPixmap(piximage2)

        self.MyIconOn = QtGui.QIcon(self.pixmapOn)
        self.MyIconOff = QtGui.QIcon(self.pixmapOff)
        self.setMinimumSize(self.WidgetSize)
        self.setMaximumSize(self.WidgetSize)

    def Combine2Channels(self, image1, image2):
        import numpy as np

        width = image1.shape[1]
        self.MidPoint = int(width / 2)
        CombinedImage = np.hstack(
            (image1[:, : self.MidPoint], image2[:, self.MidPoint :])
        )
        self.Image = CombinedImage
        # self.HoverImage = rect_with_rounded_corners(self.Image.copy()\
        #     ,40,5,(0,255,255)).astype(np.uint8).copy()
        # self.DragImage = rect_with_rounded_corners(self.Image.copy()\
        #     ,40,5,(255,255,0)).astype(np.uint8).copy()

        image = QtGui.QImage(
            CombinedImage.data,
            CombinedImage.shape[1],
            CombinedImage.shape[0],
            CombinedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap(image)
        size = self.WidgetSize
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)

    def SetSelfImage(self, image):
        import numpy as np
        import cv2

        # self.Image = image.copy()
        self.HovedImage = self.GetBorders(self.Image.copy())
        self.QImageOff = QtGui.QIcon()

        tmpBGRImage = cv2.cvtColor(self.Image.copy(), cv2.COLOR_RGB2BGR)
        piximage1 = QtGui.QImage(
            tmpBGRImage.data,
            tmpBGRImage.shape[1],
            tmpBGRImage.shape[0],
            tmpBGRImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOn = QtGui.QPixmap(piximage1)
        piximage2 = QtGui.QImage(
            self.HovedImage.data,
            self.HovedImage.shape[1],
            self.HovedImage.shape[0],
            self.HovedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOff = QtGui.QPixmap(piximage2)

        self.CurrentCollumn = None
        size = self.WidgetSize
        self.MyIconOn = QtGui.QIcon(self.pixmapOn)
        self.MyIconOff = QtGui.QIcon(self.pixmapOff)
        self.setIcon(self.MyIconOn)
        self.setIconSize(size)

        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumSize(QtCore.QSize(150, 150))
        # self.HoverImage = rect_with_rounded_corners(self.Image.copy(),40,5,(0,255,255)).astype(np.uint8).copy()
        # self.HoverImage = cv2.cvtColor(self.HoverImage.copy(), cv2.COLOR_RGB2BGR).copy()

    def DropCollumn(self, CollumnPos=None, RowPos=None):
        """
        when we fuse an item on a collumns all of the items above the "deleted" item are brought down 1 place.
        """
        # StartingPos position where the drop is going to start from
        # CollumnPos  position where the collumn is located
        # DropValue if there is empty cells then we need to drop the upper widgets down further

        DropValue = 0
        Width = self.MainWidget.frame.width()
        Heigth = self.MainWidget.frame.height()
        ColNum = self.MainWidget.gridLayout.columnCount()
        RowNum = self.MainWidget.gridLayout.rowCount()
        logger.info("ok DropCollumn")
        logger.info("COl is ", CollumnPos, " Row is ", RowPos)
        logger.info("RowPos ", RowPos, "RowNum - 1 is ", RowNum - 1)
        for x in range(RowPos, RowNum):
            # logger.info("row pos is ", RowPos)
            # logger.info("row num is ", RowNum)
            logger.info(x, "  ", CollumnPos)
            # itemOfInterest = self.MainWidget.gridLayout.itemAtPosition(x,CollumnPos)
            NextItem = self.MainWidget.gridLayout.itemAtPosition(x + 1, CollumnPos)
            if NextItem == None:
                DropValue += 1
                continue

            self.MainWidget.gridLayout.removeItem(NextItem)
            self.MainWidget.gridLayout.addItem(
                NextItem, x + DropValue, CollumnPos, 1, 1
            )
            QtWidgets.QApplication.processEvents()

    def MakeAllIconOn(self):
        items = (
            self.MainWidget.gridLayout.itemAt(i)
            for i in range(self.MainWidget.gridLayout.count())
        )
        for w in items:
            w.widget().setIcon(w.widget().MyIconOn)

    def GetBorders(self, image):
        import cv2

        bordersize = 100
        border = cv2.copyMakeBorder(
            image.copy(),
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 255],
        )
        return border

    def SetIconFromImage(self, image):
        # self.Image =image
        import cv2

        image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR).copy()
        image = QtGui.QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            image.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap(image)
        size = QtCore.QSize(150, 150)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)

    def HoveredSetIconColor(self):
        self.HovedImage = self.GetBorders(self.Image.copy())
        image = QtGui.QImage(
            self.HovedImage.data,
            self.HovedImage.shape[1],
            self.HovedImage.shape[0],
            self.HovedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap(image)
        size = QtCore.QSize(250, 250)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)
        self.update()

    def SetProperties(self):
        self.GlowHover = """
        QPushButton:
        {
        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);

        }

        """
        self.setStyleSheet(
            """

        QPushButton{
            border-color: rgba(0,0,0,0);
            background-color: rgba(0,0,0,0)}
        """
        )
        self.PreviousHoveredWidget = self
        self.isBeingHovered = False
        self.effectOP = QtWidgets.QGraphicsOpacityEffect()
        self.effectOP.setOpacity(1)
        self.setGraphicsEffect(self.effectOP)
        self.HoveredSetIconColor()
        self.isTriggered = False
        self.Detached = False
        self.PreviousSelectedWidget = None
        self.setMinimumSize(150, 150)
        self.Iam = 0  # combinedObject
        self.SetSelfImage(self.Image)

    def SetSelfChannel(self, channel):
        self.channel = channel

    def AddSignal(self, SignalToAdd):
        self.RemoveObject = SignalToAdd

    def GetNextAvailableSpotInLayout(self, Layout, maxWidth=4):
        ColNum = Layout.columnCount()
        RowNum = Layout.rowCount()
        logger.info("----------")
        logger.info(ColNum)
        logger.info(RowNum)
        if RowNum >= 1:
            for x in range(RowNum):
                if ColNum >= maxWidth:
                    for y in range(ColNum):
                        logger.info("x is ", x, " y is ", y)
                        if Layout.itemAtPosition(x, y) == None:
                            return x, y
                else:
                    return RowNum - 1, ColNum + 1
        else:
            return 0, 0
        return RowNum + 1, 0

    def ToPastePosition(self):
        from math import floor

        Width = self.MainWidget.frame.width()
        Heigth = self.MainWidget.frame.height()
        ColNum = self.MainWidget.gridLayout.columnCount()
        RowNum = self.MainWidget.gridLayout.rowCount()
        DestinationCol = floor(self.pos().x() / (Width / ColNum))
        DestinationRow = floor(self.pos().y() / (Heigth / RowNum))
        if DestinationCol < 0:
            DestinationCol = 0
        if DestinationRow < 0:
            DestinationRow = 0
        return (DestinationCol, DestinationRow)

    def enterEvent(self, event):
        import numpy as np
        import cv2

        logger.info("hover enter works 1")

        # cv2.imshow("ImageWorkginWith",ImageWorkginWith)
        # cv2.waitKey()
        # self.SetIconFromImage(self.HoverImage.copy())
        image = QtGui.QImage(
            self.Image.data,
            self.Image.shape[1],
            self.Image.shape[0],
            self.Image.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        # pixmap = QtGui.QPixmap(image)
        # self.MainWidget._photo.setPixmap(pixmap)
        # self.MainWidget._scene.addItem( self.MainWidget._photo)

        # self.MainWidget.graphicsView.setScene(self.MainWidget._scene)
        viewer = self.MainWidget.graphicsView
        viewer.setBothPhotosViewer(self.MyImage1, self.MyImage2)
        rect = QtCore.QRectF(self.MainWidget._photo.pixmap().rect())
        unity = viewer.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        viewer.scale(1 / unity.width(), 1 / unity.height())
        viewrect = viewer.viewport().rect()
        scenerect = viewer.transform().mapRect(rect)
        factor = min(
            viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height()
        )
        viewer.scale(factor, factor)
        super(CombinedDragButton, self).enterEvent(event)

    def leaveEvent(self, event):
        # self.SetIconFromImage(self.Image)
        super(CombinedDragButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        logger.info("Press is working")  # .layout()
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.__mousePressPos = event.globalPosition()
            self.__mouseMovePos = event.globalPosition()
        super(CombinedDragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPosition()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.__mouseMovePos = globalPos
        super(CombinedDragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        Tpl = self.ToPastePosition()

        if self.__mousePressPos is not None:
            moved = event.globalPosition() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(CombinedDragButton, self).mouseReleaseEvent(event)


class MasterButtonHandler(object):
    def __init__(self):
        self.ListOfButtonsHovering = []


#
#
#
# Drug button!
#
#
#
#


class DragButton(QtWidgets.QPushButton):
    def __init__(self, MainWidget=None):
        super(DragButton, self).__init__()
        self.IsActive = True
        self.MainWidget = MainWidget
        self.WidgetSize = QtCore.QSize(150, 150)
        self.contextMenu = QtWidgets.QMenu(self)
        RemoveImageAction = self.contextMenu.addAction("Remove image")
        # IsMergedAction = self.contextMenu.addAction("Ass ign As Merged")
        RemoveImageAction.triggered.connect(lambda: self.RemoveCurrentImage())
        self.previousPosAtFrame = (None, None)
        # def IsAlreadyMerged(self):
        #     """
        #     If the current widget is already merged then just promote it to combinedwidget and take the channels
        #     """
        self.imgPath = None
        self.ignoreDrag = True

    def RemoveCurrentImage(self):
        """
        Deletes current widget
        """
        self.MainWidget.gridLayout.removeWidget(self)
        try:
            self.deleteLater()
            self.allContainedDraggableButtons.remove(self)
        except:
            pass
        try:
            self.hide()
            self.IsActive = False
        except:
            pass

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec(self.mapToGlobal(event.position()))

    def setSignal(self, signal):
        self.MySignal = signal

    def SetSelfImage(self, image, imgPath=None):
        import numpy as np
        import cv2

        # self.Image = image.copy()
        self.imgPath = imgPath
        self.HovedImage = self.GetBorders(self.Image.copy())
        self.QImageOff = QtGui.QIcon()

        tmpBGRImage = cv2.cvtColor(self.Image.copy(), cv2.COLOR_RGB2BGR).copy()
        piximage1 = QtGui.QImage(
            tmpBGRImage.data,
            tmpBGRImage.shape[1],
            tmpBGRImage.shape[0],
            tmpBGRImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOn = QtGui.QPixmap(piximage1)
        piximage2 = QtGui.QImage(
            self.HovedImage.data,
            self.HovedImage.shape[1],
            self.HovedImage.shape[0],
            self.HovedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.pixmapOff = QtGui.QPixmap(piximage2)

        self.CurrentCollumn = None
        size = self.WidgetSize
        self.MyIconOn = QtGui.QIcon(self.pixmapOn)
        self.MyIconOff = QtGui.QIcon(self.pixmapOff)
        self.setIcon(self.MyIconOn)
        self.setIconSize(size)

        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumSize(QtCore.QSize(150, 150))
        # self.HoverImage = rect_with_rounded_corners(self.Image.copy(),40,5,(0,255,255)).astype(np.uint8).copy()
        # self.HoverImage = cv2.cvtColor(self.HoverImage.copy(), cv2.COLOR_RGB2BGR).copy()

    def DropCollumn(self, CollumnPos=None, RowPos=None):
        """
        when we fuse an item on a collumns all of the items above the "deleted" item are brought down 1 place.
        """
        # StartingPos position where the drop is going to start from
        # CollumnPos  position where the collumn is located
        # DropValue if there is empty cells then we need to drop the upper widgets down further

        DropValue = 0
        Width = self.MainWidget.frame.width()
        Heigth = self.MainWidget.frame.height()
        ColNum = self.MainWidget.gridLayout.columnCount()
        RowNum = self.MainWidget.gridLayout.rowCount()
        logger.info("ok DropCollumn")

        totalItems = []
        import math

        for i in range(self.MainWidget.gridLayout.count()):
            itemAtPos = self.MainWidget.gridLayout.itemAt(i)
            if itemAtPos:
                totalItems.append(itemAtPos.widget())
            self.MainWidget.gridLayout.removeWidget(totalItems[-1])
            totalItems[-1].hide()
        logger.info("len of total items are ", len(totalItems))
        logger.info("totalItems are ", totalItems)
        ItemsWidthNum = 8
        logger.info(self.MainWidget.allContainedDraggableButtons)
        heightval = math.floor(len(self.MainWidget.allContainedDraggableButtons) / 2)
        positions = [(i, j) for i in range(heightval) for j in range(ItemsWidthNum)]
        for position, someButton in zip(
            positions, self.MainWidget.allContainedDraggableButtons
        ):
            self.MainWidget.gridLayout.addWidget(someButton, *position)
            someButton.previousPosAtFrame = (position[0], position[1], 0, 0)
            someButton.show()
        # for x in range(RowPos, RowNum):
        #     # logger.info("row pos is ", RowPos)
        #     # logger.info("row num is ", RowNum)
        #     logger.info(x,"  ",CollumnPos)
        #     # itemOfInterest = self.MainWidget.gridLayout.itemAtPosition(x,CollumnPos)
        #     NextItem = self.MainWidget.gridLayout.itemAtPosition(x+1,CollumnPos)
        #     if NextItem ==None:
        #         DropValue+=1
        #         continue
        #     # logger.info(itemOfInterest)
        #     self.MainWidget.gridLayout.removeItem(NextItem)
        #     self.MainWidget.gridLayout.addItem(NextItem,x + DropValue,CollumnPos,1,1 )
        #     QtWidgets.QApplication.processEvents()

        config.global_signals.IndiLayoutChangedSignal.emit()

        logger.info("end 1")

    def MakeAllIconOn(self):
        items = (
            self.MainWidget.gridLayout.itemAt(i)
            for i in range(self.MainWidget.gridLayout.count())
        )
        for w in items:
            w.widget().setIcon(w.widget().MyIconOn)

    def GetBorders(self, image):
        import cv2

        bordersize = 100
        border = cv2.copyMakeBorder(
            image.copy(),
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 255],
        )
        return border

    def SetIconFromImage(self, image):
        # self.Image =image
        import cv2

        image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR).copy()
        image = QtGui.QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            image.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap(image)
        size = QtCore.QSize(150, 150)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)

    def HoveredSetIconColor(self):
        self.HovedImage = self.GetBorders(self.Image.copy())
        image = QtGui.QImage(
            self.HovedImage.data,
            self.HovedImage.shape[1],
            self.HovedImage.shape[0],
            self.HovedImage.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap(image)
        size = QtCore.QSize(250, 250)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)
        self.update()

    def SetProperties(self):
        self.GlowHover = """
        QPushButton:
        {
        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);

        }

        """
        self.setStyleSheet(
            """

        QPushButton{
            border-color: rgba(0,0,0,0);
            background-color: rgba(0,0,0,0)}
        """
        )
        self.PreviousHoveredWidget = self
        self.isBeingHovered = False
        self.effectOP = QtWidgets.QGraphicsOpacityEffect()
        self.effectOP.setOpacity(1)
        self.setGraphicsEffect(self.effectOP)
        self.HoveredSetIconColor()
        self.isTriggered = False
        self.Detached = False
        self.PreviousSelectedWidget = None
        self.setMinimumSize(150, 150)
        self.Iam = 0  # combinedObject
        self.SetSelfImage(self.Image)

    def SetSelfChannel(self, channel):
        self.channel = channel

    def AddSignal(self, SignalToAdd):
        self.RemoveObject = SignalToAdd

    def AnimateSizeTakeOff(self):
        # return
        AnimationDuration = 500
        # self.SeqAnimation = QtCore.QSequentialAnimationGroup()
        self.ParAnimation = QtCore.QParallelAnimationGroup()
        logger.info("animating")
        self.animminimumSize = QtCore.QPropertyAnimation(self, b"minimumSize")
        self.animminimumSize.setDuration(AnimationDuration)
        start = self.minimumSize()
        self.animminimumSize.setStartValue(start)
        self.animminimumSize.setEndValue(start)
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)
        self.animminimumSize.setEasingCurve(curve)
        # self.animminimumSize.start()
        self.ParAnimation.addAnimation(self.animminimumSize)
        self.OpacityAnimation = QtCore.QPropertyAnimation(self.effectOP, b"opacity")
        self.OpacityAnimation.setDuration(AnimationDuration)
        self.OpacityAnimation.setStartValue(1)
        self.OpacityAnimation.setEndValue(0.75)
        self.OpacityAnimation.start()
        self.animiconSize = QtCore.QPropertyAnimation(self, b"iconSize")
        self.animiconSize.setDuration(AnimationDuration)
        self.animiconSize.setStartValue(QtCore.QSize(100, 100))
        self.animiconSize.setEndValue(QtCore.QSize(150, 150))
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)
        self.animiconSize.setEasingCurve(curve)
        self.ParAnimation.addAnimation(self.animiconSize)
        self.ParAnimation.start()

    def AnimateSizeTakeOn(self):
        # return
        AnimationDuration = 500
        # self.SeqAnimation = QtCore.QSequentialAnimationGroup()
        self.ParAnimation = QtCore.QParallelAnimationGroup()
        logger.info("animating")
        self.animminimumSize = QtCore.QPropertyAnimation(self, b"minimumSize")
        self.animminimumSize.setDuration(AnimationDuration)
        start = self.minimumSize()
        self.animminimumSize.setStartValue(start)
        self.animminimumSize.setEndValue(self.WidgetSize)
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)
        self.animminimumSize.setEasingCurve(curve)
        # self.animminimumSize.start()
        self.ParAnimation.addAnimation(self.animminimumSize)
        self.OpacityAnimation = QtCore.QPropertyAnimation(self.effectOP, b"opacity")
        self.OpacityAnimation.setDuration(AnimationDuration)
        self.OpacityAnimation.setStartValue(1)
        self.OpacityAnimation.setEndValue(0.75)
        self.OpacityAnimation.start()
        self.animiconSize = QtCore.QPropertyAnimation(self, b"iconSize")
        self.animiconSize.setDuration(AnimationDuration)
        # logger.info(self.minimumSize())
        # start = self.minimumSize()
        self.animiconSize.setStartValue(QtCore.QSize(200, 200))
        self.animiconSize.setEndValue(self.WidgetSize)
        # self.animiconSize.start()
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.Type.OutElastic)
        self.animiconSize.setEasingCurve(curve)
        self.ParAnimation.addAnimation(self.animiconSize)
        self.ParAnimation.start()

    def SetIconNumpy(self, imageName):
        import cv2

        return
        # stream = open(filename, "rb")
        # bytes = bytearray(stream.read())
        # numpyarray = np.asarray(bytes, dtype=np.uint8)
        # CombinedImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        # #CombinedImage = cv2.imread(imageName)
        # self.Image = CombinedImage.copy()
        # image = QtGui.QImage(CombinedImage.data, CombinedImage.shape[1], CombinedImage.shape[0],\
        #      CombinedImage.strides[0], QtGui.QImage.Format.Format_RGB888)
        # pixmap = QtGui.QPixmap(image)
        # size = QtCore.QSize(250, 250)
        # self.setIcon(QtGui.QIcon(pixmap))
        # self.setIconSize(size)

    def CountUsedColumns(self, Layout):
        AllCols = Layout.columnCount()
        AllRows = Layout.rowCount()
        Count = 0
        for x in range(AllCols):
            # logger.info("AllCols, " ,x)
            HasWidget = False
            for y in range(AllRows):
                tmpWidget = Layout.itemAtPosition(y, x)
                # logger.info(tmpWidget)
                if HasWidget == False and tmpWidget != None:
                    HasWidget = True
            if HasWidget == True:
                Count += 1
        return Count

    def widgets_at(self, pos):
        """Return ALL widgets at `pos`

        Arguments:
            pos (QPoint): Position at which to get widgets

        """

        widgets = []
        widget_at = QtWidgets.QApplication.widgetAt(pos)

        while widget_at:
            widgets.append(widget_at)

            # Make widget invisible to further enquiries
            widget_at.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )
            widget_at = QtWidgets.QApplication.widgetAt(pos)

        # Restore attribute
        for widget in widgets:
            widget.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
            )

        return widgets

    def GetWidgetFromPosition(self):
        try:
            widget = QtWidgets.QApplication.widgetAt(
                self.mapToGlobal(self.parent().pos())
            )
            return widget
        except:
            pass

    def ToPastePosition(self):
        from math import floor

        return 0, 0
        Width = self.MainWidget.frame.width()
        Heigth = self.MainWidget.frame.height()
        ColNum = (
            self.MainWidget.gridLayout.rowCount()
        )  # self.CountUsedColumns(self.MainWidget.gridLayout)
        RowNum = self.MainWidget.gridLayout.rowCount()
        DestinationCol = floor((self.pos().x() + 70) / ((Width / ColNum) + (6)))
        DestinationRow = floor((self.pos().y() + 70) / ((Heigth / RowNum) + (6)))
        logger.info("DestinationCol is ", DestinationCol)
        logger.info("DestinationRow is ", DestinationRow)

        if DestinationCol < 0:
            DestinationCol = 0
        if DestinationRow < 0:
            DestinationRow = 0
        return (DestinationCol, DestinationRow)

    # def mouseReleaseEvent(self,event):
    def mousePressEvent(self, event):
        if self.ignoreDrag == False:
            # super(DragButton, self).mousePressEvent(event)
            self.previousLayoutPos = (
                self.ToPastePosition()
            )  # can be used to access the current collumn when we fush buttons
            self.raise_()
            self.DragedWidget = self.MainWidget.gridLayout.itemAtPosition(
                self.previousLayoutPos[1], self.previousLayoutPos[0]
            )
            # self.DragedWidget = None
            self.__mousePressPos = None
            self.__mouseMovePos = None
            self.StartingPressPos = None
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.StartingPressPos = event.globalPosition()
                self.isTriggered = False
                # self.MainWidget.gridLayout.removeWidget(self)
                self.raise_()
                self.__mousePressPos = event.globalPosition()
                self.__mouseMovePos = event.globalPosition()
                self.previousPosAtFrame
            super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self.ignoreDrag == False:
                currPos = self.mapToGlobal(self.pos())
                globalPos = event.globalPosition()
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.move(newPos)
                if self.Detached == False:
                    logger.info("Detached works?!")
                    self.AnimateSizeTakeOff()
                    self.Detached = True
                self.__mouseMovePos = globalPos
                self.ItemAtPastePos = self.DragedWidget
                Tpl = self.ToPastePosition()
                DestinationWidget = self.MainWidget.gridLayout.itemAtPosition(
                    Tpl[1], Tpl[0]
                )
                if self.ItemAtPastePos != None:
                    self.setAttribute(
                        QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
                    )
                    Tpl = self.ToPastePosition()
                    # DestinationWidget =  self.MainWidget.gridLayout.itemAtPosition(Tpl[1],Tpl[0])
                    DestinationWidget = self.GetWidgetFromPosition()
                    if DestinationWidget == None:
                        return True
                        super(DragButton, self).mouseMoveEvent(event)
                    if self.PreviousHoveredWidget != None:
                        """
                        If the previous widget is not none, should be:
                        self at first and then assignedduring a change event

                        """
                        if DestinationWidget != None:
                            if (
                                DestinationWidget != self.PreviousHoveredWidget
                                and type(DestinationWidget) == DragButton
                            ):
                                """
                                Destination widget should be the same as self at first but then it should change
                                """
                                if self.PreviousHoveredWidget != None:
                                    if (
                                        type(self.PreviousHoveredWidget) == DragButton
                                    ):  # So that we dont capture other widgets
                                        self.PreviousHoveredWidget.setIcon(
                                            self.PreviousHoveredWidget.MyIconOn
                                        )
                                        self.PreviousHoveredWidget = DestinationWidget
                                        super(DragButton, self).mouseMoveEvent(event)
                    if (
                        type(DestinationWidget) == DragButton
                    ):  # and DestinationWidget.widget().Iam ==0:
                        if DestinationWidget.isBeingHovered == False:
                            DestinationWidget.isBeingHovered = True
                            if self.PreviousHoveredWidget != None:
                                self.PreviousHoveredWidget.setIcon(
                                    self.PreviousHoveredWidget.MyIconOff
                                )
                                self.PreviousHoveredWidget.isBeingHovered = False
                    super(DragButton, self).mouseMoveEvent(event)
                super(DragButton, self).mouseMoveEvent(event)
            # return True
        super(DragButton, self).mouseMoveEvent(event)

    def calculateDistance(self, x1, y1, x2, y2):
        import math

        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        logger.info(dist)
        return dist

    def HandlePastingWidget(self, event):
        logger.info("releasing button")
        self.ItemAtPastePos = self

        Tpl = self.ToPastePosition()
        DestinationWidget = (
            self.GetWidgetFromPosition()
        )  # self.MainWidget.gridLayout.itemAtPosition(Tpl[1],Tpl[0])
        logger.info("type is ", DestinationWidget)
        if type(DestinationWidget) == DragButton:
            pass
        else:
            logger.info("type is qframe")
            DestinationWidget = None  # self.MainWidget.gridLayout.itemAtPosition(Tpl[1],Tpl[0]).widget()
            config.global_signals.IndiLayoutChangedSignal.emit()
            self.AnimateSizeTakeOn()
            self.MakeAllIconOn()
            return False
        # else:return False
        # logger.info(DestinationWidget)
        # if DestinationWidget == None:# or not DestinationWidget.isVisible():
        #     self.MainWidget.gridLayout.removeWidget(self)
        #     self.MainWidget.gridLayout.addWidget(self,Tpl[1],Tpl[0],1,1 )
        #     # self.previousPosAtFrame = (Tpl[1],Tpl[0],1,1 )
        #     config.global_signals.IndiLayoutChangedSignal.emit()
        #     self.AnimateSizeTakeOn()
        #     self.MakeAllIconOn()
        #     return False
        Tpl = self.ToPastePosition()
        DestinationWidget = (
            self.GetWidgetFromPosition()
        )  # self.MainWidget.gridLayout.itemAtPosition(Tpl[1],Tpl[0])

        if DestinationWidget != None and DestinationWidget.Iam == 0:
            """
            I we are actiallyu pasting somehwere and Destination widget is mergable do:
            """
            if DestinationWidget.isVisible() == False:
                logger.info("pasting ontop of invisible widget")
                self.MainWidget.gridLayout.removeWidget(self)
                self.MainWidget.gridLayout.addWidget(self, Tpl[1], Tpl[0], 1, 1)
                config.global_signals.IndiLayoutChangedSignal.emit()

            else:
                gridLayout = self.MainWidget.gridLayout
                logger.info("removing old buttons ", type(self.ItemAtPastePos))
                logger.info("Grab Object ", self.ItemAtPastePos.objectName())
                logger.info("Destination Object ", DestinationWidget.objectName())
                if DestinationWidget != self.ItemAtPastePos:
                    # returnOfFuse= self.MainWidget.graphicsView.FuseImages(self.Image.copy(), DestinationWidget.Image.copy() )
                    # NoneType = type(None)
                    # if isinstance(returnOfFuse,NoneType):
                    #     return
                    MyDragButton = CombinedDragButton(self.MainWidget)
                    MyDragButton.CreatePushButtons(self, DestinationWidget)

                    MyDragButton.SetProperties()
                    # MyDragButton.Combine2Channels(self.Image.copy(),DestinationWidget.widget().Image)
                    # self.DragedWidget.widget().hide()
                    nameWidgetDest = DestinationWidget.objectName()
                    nameWidgetOrg = self.objectName()
                    self.MainWidget.gridLayout.removeWidget(self)
                    self.hide()
                    self.DropCollumn(
                        self.previousLayoutPos[0], self.previousLayoutPos[1]
                    )

                    self.MainWidget.gridLayout.removeWidget(DestinationWidget)
                    # moves a position down of the other widgets
                    self.DropCollumn(Tpl[0], Tpl[1])
                    # logger.info("destination widget position is ")
                    logger.info("removing objects: ", nameWidgetDest)
                    logger.info("removing objects: ", nameWidgetDest)
                    WidgetToRemove1 = self.parent().findChild(
                        DragButton, nameWidgetDest
                    )
                    WidgetToRemove2 = self.parent().findChild(DragButton, nameWidgetOrg)
                    WidgetToRemove1.setParent(None)
                    WidgetToRemove2.setParent(None)
                    self.MainWidget.allContainedDraggableButtons.remove(WidgetToRemove1)
                    self.MainWidget.allContainedDraggableButtons.remove(WidgetToRemove2)
                    WidgetToRemove1.hide()
                    WidgetToRemove2.hide()

                    spot1, spot2 = MyDragButton.GetNextAvailableSpotInLayout(
                        self.MainWidget.gridLayout_7, maxWidth=2
                    )
                    self.MainWidget.gridLayout_7.addWidget(
                        MyDragButton, spot1, spot2, 1, 1
                    )
                    config.global_signals.IndiLayoutChangedSignal.emit()
                    MyDragButton.show()

        else:
            # logger.info("Bring back widget: ",self.DragedWidget.widget() )
            # self.MainWidget.gridLayout.removeWidget(self.DragedWidget.widget())
            self.MainWidget.gridLayout.addWidget(
                self, self.previousLayoutPos[1], self.previousLayoutPos[0], 1, 1
            )
            config.global_signals.IndiLayoutChangedSignal.emit()

    def enterEvent(self, event):
        import numpy as np
        import cv2

        logger.info("hover enter works 2")

        # cv2.imshow("ImageWorkginWith",ImageWorkginWith)
        # cv2.waitKey()
        # self.SetIconFromImage(self.HoverImage.copy())
        if self.MainWidget._photo in self.MainWidget._scene.items():
            self.MainWidget._scene.removeItem(self.MainWidget._photo)
        image = QtGui.QImage(
            self.Image.data,
            self.Image.shape[1],
            self.Image.shape[0],
            self.Image.strides[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.Cpixmap = QtGui.QPixmap(image)
        self.MainWidget._photo.setPixmap(self.Cpixmap)
        self.MainWidget._scene.addItem(self.MainWidget._photo)
        self.MainWidget.graphicsView.setScene(self.MainWidget._scene)
        viewer = self.MainWidget.graphicsView
        rect = QtCore.QRectF(self.MainWidget._photo.pixmap().rect())
        unity = viewer.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        viewer.scale(1 / unity.width(), 1 / unity.height())
        viewrect = viewer.viewport().rect()
        scenerect = viewer.transform().mapRect(rect)
        factor = min(
            viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height()
        )
        viewer.scale(factor, factor)
        logger.info("comples enteer event")
        super(DragButton, self).enterEvent(event)

    def leaveEvent(self, event):
        # logger.info("leave event 1")
        # if self.Image:
        #     self.SetIconFromImage(self.Image)
        super(DragButton, self).leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.ignoreDrag == False:
            self.Detached = False
            logger.info("previuys poss at frame is ", self.previousPosAtFrame)
            if len(self.previousPosAtFrame) == 0:
                super(DragButton, self).mouseReleaseEvent(event)
            if (
                self.previousPosAtFrame[0] == None
                or self.self.previousPosAtFrame[1] == None
            ):
                super(DragButton, self).mouseReleaseEvent(event)

            elif self.__mousePressPos is not None:
                logger.info("mouse press pos is not none")
                if self.HandlePastingWidget(event):
                    moved = event.globalPosition() - self.__mousePressPos
                    self.setAttribute(
                        QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
                    )
                    if moved.manhattanLength() > 3:
                        event.ignore()
                        return
                else:
                    logger.info("realising into space!")

                    self.MainWidget.gridLayout.addWidget(self, *self.previousPosAtFrame)
                    logger.info("addint at ", self.previousPosAtFrame)
                    self.setParent(self.MainWidget.frame_5)
                    self.setAttribute(
                        QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False
                    )
        super(DragButton, self).mouseReleaseEvent(event)


class ChannelViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, MainWindow=None):
        super(ChannelViewer, self).__init__()
        # super(Ui_MainWindow, self).__init__()
        self.Image1 = None
        self.Image2 = None
        self.Single = 0
        self.Double = 1
        self.OverlayMode = 1  # 0 is separator and 1 is fused
        self.Triple = 2
        self.ln = None
        self.modeImage = self.Single  # 0 is single,
        self.LinePoint = None
        self._scene = QtWidgets.QGraphicsScene(self)

        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setZValue(-50)
        self._scene.addItem(self._photo)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        config.global_signals.photoChanged.connect(self.UpdateImage)

    def GetCurrentChannel(self, image):
        """
        Finds the largest intensity in the 3 avaiblable channels
        """
        import numpy as np

        ch1 = 0
        ch2 = 0
        ch3 = 0
        ch1 = np.mean(image[:, :, 0])
        ch2 = np.mean(image[:, :, 1])
        ch3 = np.mean(image[:, :, 2])
        logger.info("-----------------------------------")
        logger.info(ch1)
        logger.info(ch2)
        logger.info(ch3)
        if ch1 > ch2 and ch1 > ch3:
            logger.info("return 1")
            return 0
        if ch3 > ch2 and ch3 > ch1:
            logger.info("return 2")

            return 2
        if ch2 > ch1 and ch2 > ch3:
            logger.info("return 3")

            return 1

    def FuseImages(self, image1, image2):
        """
        Fuses both of the channels of the two images
        """
        FusedImage = image1.copy()
        ch1 = self.GetCurrentChannel(image1)
        ch2 = self.GetCurrentChannel(image2)
        if ch1 != ch2:
            FusedImage[:, :, ch2] = image2[:, :, ch2]
            return FusedImage.copy()
        else:
            config.global_signals.errorSignal.emit("Something went wrong.")
            return None

    def ToggleOverlayMode(self):
        logger.info("overidemode is", self.OverlayMode)
        if self.OverlayMode == 0:
            self.OverlayMode = 1
        else:  # self.OverlayMode == 1:
            self.OverlayMode = 0

    def setPhotoViewer(self, image):
        self.CurrentImage = image.copy()
        self.modeImage = self.Single

    def CheckDim(self):
        if self.Image1.shape[1] != self.Image2.shape[1]:
            return False
        return True

    def UpdateImage(self):
        import numpy as np

        if self.OverlayMode == 0:
            if self.ln:
                # logger.info(self.ln.pos())
                # logger.info(self.ln.pos().x())
                try:
                    change = int(self.ln.pos().x())
                    tmpLinePoint = self.LinePoint + change
                except:
                    return
                logger.info("LinePoint is", tmpLinePoint)
                self._scene.removeItem(self._photo)
                stackImage = np.hstack(
                    (self.Image1[:, :tmpLinePoint], self.Image2[:, tmpLinePoint:])
                ).copy()
                image = QtGui.QImage(
                    stackImage.data,
                    stackImage.shape[1],
                    stackImage.shape[0],
                    stackImage.strides[0],
                    QtGui.QImage.Format.Format_RGB888,
                )
                # self.pixmap = QtGui.QPixmap(image.copy())
                self._photo = QtWidgets.QGraphicsPixmapItem()
                self._photo.setZValue(-50)
                self._photo.setPixmap(QtGui.QPixmap(image.copy()))
                self._photo.setZValue(-50)
                self._scene.addItem(self._photo)
                self._scene.addItem(self.ln)
                # self._scene.addItem(self.ln2)
                # self.setScene(self._scene)

    def setBothPhotosViewer(self, image1, image2):
        import numpy as np
        import cv2

        self._scene.clear()
        # if self.Image1 == None and self.Image2 == None:
        #     logger.info("both images are none!")
        #     return
        try:
            if len(self.Image1) == 0:
                self.Image1 = self.Image2
        except:
            logger.info("error for image 1")
        try:
            if len(self.Image2) == 0:
                self.Image2 = self.Image1
        except:
            logger.info("error for image 2")
        self.Image1 = cv2.cvtColor(image1.copy(), cv2.COLOR_BGR2RGB)
        self.Image2 = cv2.cvtColor(image2.copy(), cv2.COLOR_BGR2RGB)
        self.modeImage = self.Double  # means its two images 1

        NoneType = type(None)
        logger.info("overlay mode is ", self.OverlayMode)
        self._scene.clear()
        if self.OverlayMode == 1:
            FusedImage = self.FuseImages(self.Image1, self.Image2)
            # logger.info('fused image is', FusedImage)
            if not isinstance(FusedImage, NoneType):
                self._photo = QtWidgets.QGraphicsPixmapItem()
                self._photo.setZValue(-50)
                image = QtGui.QImage(
                    FusedImage.data,
                    FusedImage.shape[1],
                    FusedImage.shape[0],
                    FusedImage.strides[0],
                    QtGui.QImage.Format.Format_RGB888,
                )
                self._photo.setPixmap(QtGui.QPixmap(image.copy()))
                self._scene.addItem(self._photo)
                self.setScene(self._scene)
            else:
                return
        else:
            self.LinePoint = int(self.Image1.shape[1] / 2)  # halh point width

            start = QtCore.QPointF(self.LinePoint, 0)
            end = QtCore.QPointF(self.LinePoint, self.Image1.shape[0])

            pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            pen.setWidth(10)
            self.ln = LineDragItem(QtCore.QLineF(start, end))
            self.ln.setPen(pen)
            # logger.info(dir(self.ln))
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.white)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            pen.setWidth(5)
            point = QtCore.QPointF(-150, 150)
            angle = 0
            import math

            end = 100 * QtCore.QPointF(math.cos(angle), math.sin(angle))
            line = QtCore.QLineF(QtCore.QPointF(), end)
            self.ln.line = line.translated(self.ln.pos())
            self.ln2 = LineDragItem(QtCore.QLineF(start, end))
            self.ln2.setPen(pen)
            stackImage = np.hstack(
                (image1[:, : self.LinePoint], image2[:, self.LinePoint :])
            ).copy()
            image = QtGui.QImage(
                stackImage.data,
                stackImage.shape[1],
                stackImage.shape[0],
                stackImage.strides[0],
                QtGui.QImage.Format.Format_RGB888,
            )
            self._photo = QtWidgets.QGraphicsPixmapItem()
            self._photo.setZValue(-50)
            self._photo.setPixmap(QtGui.QPixmap(image.copy()))
            self._scene.addItem(self._photo)
            self._scene.addItem(self.ln)
            self.setScene(self._scene)

    def adjustPhotoLinePoint(self, HalfWayPoint):
        self.CurrentImage


# class LineDragItem(QtWidgets.QGraphicsLineItem):


class LineDragItem(QtWidgets.QGraphicsLineItem):
    photoChanged = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        self._line = QtCore.QLineF()
        super().__init__(*args, **kwargs)
        # Flags to allow dragging and tracking of dragging.
        self.setFlags(
            self.flags()
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    def itemChange(self, change, value):
        if (
            change == QtWidgets.QGraphicsItem.ItemPositionChange
            and self.isSelected()
            and not self.line.isNull()
        ):
            logger.info("emiting!")
            config.global_signals.photoChanged.emit()
            # http://www.sunshine2k.de/coding/java/PointOnLine/PointOnLine.html
            p1 = self.line.p1()
            p2 = self.line.p2()
            e1 = p2 - p1
            e2 = value - p1
            dp = QtCore.QPointF.dotProduct(e1, e2)
            l = QtCore.QPointF.dotProduct(e1, e1)
            p = p1 + dp * e1 / l
            return p
        return super().itemChange(change, value)


def rect_with_rounded_corners(image, r, t, c, backroundColor=(0, 0, 0)):
    """
    :param image: image as NumPy array
    :param r: radius of rounded corners
    :param t: thickness of border
    :param c: color of border
    :return: new image as NumPy array with rounded corners
    """

    import numpy as np
    import cv2

    c += (255,)

    h, w = image.shape[:2]

    # Create new image (three-channel hardcoded here...)
    new_image = np.ones((h + 2 * t, w + 2 * t, 4), np.uint8) * 0
    new_image[:, :, 3] = 0

    # Draw four rounded corners
    new_image = cv2.ellipse(
        new_image, (int(r + t / 2), int(r + t / 2)), (r, r), 180, 0, 90, c, t
    )
    new_image = cv2.ellipse(
        new_image,
        (int(w - r + 3 * t / 2 - 1), int(r + t / 2)),
        (r, r),
        270,
        0,
        90,
        c,
        t,
    )
    new_image = cv2.ellipse(
        new_image, (int(r + t / 2), int(h - r + 3 * t / 2 - 1)), (r, r), 90, 0, 90, c, t
    )
    new_image = cv2.ellipse(
        new_image,
        (int(w - r + 3 * t / 2 - 1), int(h - r + 3 * t / 2 - 1)),
        (r, r),
        0,
        0,
        90,
        c,
        t,
    )

    # Draw four edges
    new_image = cv2.line(
        new_image,
        (int(r + t / 2), int(t / 2)),
        (int(w - r + 3 * t / 2 - 1), int(t / 2)),
        c,
        t,
    )
    new_image = cv2.line(
        new_image,
        (int(t / 2), int(r + t / 2)),
        (int(t / 2), int(h - r + 3 * t / 2)),
        c,
        t,
    )
    new_image = cv2.line(
        new_image,
        (int(r + t / 2), int(h + 3 * t / 2)),
        (int(w - r + 3 * t / 2 - 1), int(h + 3 * t / 2)),
        c,
        t,
    )
    new_image = cv2.line(
        new_image,
        (int(w + 3 * t / 2), int(r + t / 2)),
        (int(w + 3 * t / 2), int(h - r + 3 * t / 2)),
        c,
        t,
    )

    # Generate masks for proper blending
    mask = new_image[:, :, 3].copy()
    mask = cv2.floodFill(mask, None, (int(w / 2 + t), int(h / 2 + t)), 128)[1]
    mask[mask != 128] = 0
    mask[mask == 128] = 1
    mask = np.stack((mask, mask, mask), axis=2)

    # Blend images
    temp = np.zeros_like(new_image[:, :, :3])
    temp[(t - 1) : (h + t - 1), (t - 1) : (w + t - 1)] = image.copy()
    new_image[:, :, :3] = new_image[:, :, :3] * (1 - mask) + temp * mask

    # Set proper alpha channel in new image
    temp = new_image[:, :, 3].copy()
    new_image[:, :, 3] = cv2.floodFill(
        temp, None, (int(w / 2 + t), int(h / 2 + t)), 255
    )[1]
    return new_image


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


from celer_sight_ai.gui.designer_widgets_py_files.ImportSettings import (
    Ui_Dialog as ImportDialogUi,
)


class ImportDialogSetUp(ImportDialogUi):
    def __init__(self):
        super(ImportDialogSetUp, self).__init__()
        self.Dialog = MultiChannelImporter()
        self.setupUi(self.Dialog)
        self.retranslateUi(self.Dialog)
        self.Dialog.show()
        self.Dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.buttonBox.accepted.connect(lambda: self.OnAccepted())

    def OnAccepted(self):
        """
        When we click acccept we need to pass the ques to the Multichannel inmporter for the proccess to move on

        if both are clicked then 1 and 1 is returned
        0,0 = 0 None
        1,0 = 1 Combined only
        0,1 = 2 indi only
        1,1 = 3
        """
        if self.checkBox.isChecked():
            if self.checkBox_2.isChecked():
                logger.info("on accepted is workign!")

                config.global_signals.DialogImportSettingsSignal.emit(3)
                self.Dialog.accept()
                # self.Dialog.close()
            else:
                config.global_signals.DialogImportSettingsSignal.emit(1)
                # self.Dialog.close()
                self.Dialog.accept()
        else:
            if self.checkBox_2.isChecked():
                config.global_signals.DialogImportSettingsSignal.emit(2)
                # self.Dialog.close()
                self.Dialog.accept()
            else:
                config.global_signals.DialogImportSettingsSignal.emit(0)
                self.Dialog.accept()
                # self.Dialog.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    TestWindow = MultiChannelImporterUi()
    sys.exit(app.exec())

    # app = QtWidgets.QApplication(sys.argv)
    # ui =CelerSightMainWindow()
    # ui.SetupAll()
    # sys.exit(app.exec())
