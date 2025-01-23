import logging
import os
import sys

from PyQt6.QtCore import Qt

from celer_sight_ai.configHandle import getLocal

logger = logging.getLogger(__name__)
import os
import pathlib

os.chdir(os.environ["CELER_SIGHT_AI_HOME"])
import copy
import os
import sys
import time
import traceback
from pathlib import Path
from threading import Thread

import cv2
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config
from celer_sight_ai.gui.custom_widgets.celer_sight_main_window_ui_extended import (
    CelerSightMainWindow,
)
from celer_sight_ai.gui.custom_widgets.scene import (
    CropItem,
    create_pyramidal_tiff_for_image_object,
    readImage,
)
from celer_sight_ai.gui.designer_widgets_py_files.userSettings import (
    Ui_Dialog as settingsDialog1,
)
from celer_sight_ai.io.data_handler import (
    DataHandler,
)


class Master_MainWindow(CelerSightMainWindow):
    """
    The Main Window that we use, inherits from CelerSightMainWindow and has the majority of the functions
    responsible for handling the data.
    """

    photoClicked = QtCore.pyqtSignal(
        QtCore.QPoint
    )  # singal for when we draw the polygon
    mouse_move = QtCore.pyqtSignal(QtCore.QPoint)  # not usepd
    MasterMaskLabelcomboBoxSIGNAL = QtCore.pyqtSignal(object)
    # OpenIndiImagesForConditionFINISHED = QtCore.pyqtSignal(object)
    signal = QtCore.pyqtSignal()
    signal_hide_dialog = QtCore.pyqtSignal()  # not needed?

    def __init__(self, parent=None):
        super(Master_MainWindow, self).__init__(parent)
        from celer_sight_ai import config

        # a class to process all variables and to hadnle storage
        self.DH = DataHandler(self)
        self.current_home_display_widget = None  # the widget displayed on the home tabe
        self.SelectionStateRegions = False

        self.previous_item_name_RNAi_list = None  # The previous item on the self.RNAi_list widget on the bottom left of the UI
        self.submitted = self.signal
        self.signal_hide_dialog = self.signal_hide_dialog  # not needed

        # items copied from the main qgraphicsscene
        self.copied_items = []

        # if we relealse but we are in a drawing mode then we still are in remove mode
        # if we just release or finish drawing then back to false
        self.during_drawing = (
            False  # Indicates if we are currently drawing a mask (for the event filter)
        )
        # wether we are adding forground or background in the auto tool review mode
        self.previous_clicked_treatment_item = None
        self.i_am_drawing_state_bbox = (
            False  # Indicates weather we are in the process of auto tool
        )
        self.i_am_drawing_state = (
            False  # Indicates weather we are in the process of polygon draw
        )

        self.during_scene_refresh = False
        self.during_load_main_scene_display = False
        self.load_main_scene_thread = None
        self.no_image_displayed = True  # Image of drag and drop is displayed
        self.worm_mask_points_x = []  # Init variable
        self.worm_mask_points_y = []  # Init variable
        self.setMouseTracking(True)
        self.selected_mask = -1  # the number of the selected mask in the masks list
        self.selected_mask_origin = "BOOL"  # or "POLYGON"
        self.final_mask_number = 0  # I dont think this is used
        self.temp_mask_to_use_Test_x = []  # variable for draw_polygon
        self.temp_mask_to_use_Test_y = []
        self.counter_tmp = 0  # variable that counts iterations for draw_polygon
        self.add_mask_btn_state = False  # Indicates weather we can add a polygon mask
        self.layout_changing = False  # During a resize of the layout (specificaly of the Asset buttons at the overview tabs on the bottom left) this is set to true to prevent an infinite loop
        self.layout_changing_buffer = 5
        self.delete_counter = 0  # a counter that helps with the delete paradox of deletelater that runs at the end of the eventloop
        self.setCurrentImageNumber(0)
        self.previous_imagenumber = 0
        self.selection_state = False  # weather or not we can aselect a mask
        self.imagenumber = 0  # Indicates the image number that is active on the viewport from the pixon_list_opencv (which should be the same as the other variables)
        self.all_stacked_images = []  # Should be the same as pixon_list_opencv

        self._locked_ui_elements = []  # used by lock_ui() and unlock_ui()

        self.pixelScalePerUnit = None
        self.pixelSet = False

        self.useSDK_NN = True  # wether or not use of onnx models localy
        self.sdknn_tool = None  # instance is zero

        # self.DH.BLobj.set_current_group("default")

        self.LabelMasksNumber = None

        self.undoStack = QtGui.QUndoStack()

        # init action
        self.undoAction = self.undoStack.createUndoAction(self, "Undo")
        self.redoAction = self.undoStack.createRedoAction(self, "Redo")

        self.addAction(self.undoAction)
        self.addAction(self.redoAction)

        self.MasterMaskLabelcomboBox_CurrentIndex = (
            0  # A varible for keeping track of the index in the combobox
        )
        self.SetupAll()

        self.DuringPlotWidgetSwitch = False  # variable that indicates when we are switvhing widgets so that  we dont catch extra signals

        self.pg1_settings_all_masks_color_button.setStyleSheet(
            "background-color: rgb(0,0,255);"
        )
        from celer_sight_ai.gui.designer_widgets_py_files.LoadingAnimation1 import (
            ProgressDialog,
        )

        self.progress_dialog = ProgressDialog(self.centralwidget)

        self.add_classes_btn.clicked.connect(lambda: self.spawn_add_class_dialog())
        self.sub_classes_btn.clicked.connect(lambda: self.remove_class_item())

        config.global_signals.load_main_scene_display_image_signal.connect(
            self.load_main_scene_display_image
        )
        config.global_signals.load_main_scene_gather_image_threaded_signal.connect(
            self.load_main_scene_gather_image
        )
        config.global_signals.refresh_main_scene_image_only_signal.connect(
            self.refresh_main_scene_image_only
        )
        config.global_signals.refresh_main_scene_pixmap_only_signal.connect(
            self.refresh_main_scene_pixmap_only
        )
        config.global_signals.lock_ui_signal.connect(self.lock_ui)
        config.global_signals.unlock_ui_signal.connect(self.unlock_ui)
        config.global_signals.ensure_not_particle_class_selected_signal.connect(
            self.ensure_not_particle_class_selected
        )
        config.global_signals.delete_image_with_button_signal.connect(
            self.delete_image_with_button
        )
        # emit twice with a delay
        config.global_signals.ensure_not_particle_class_selected_signal.connect(
            lambda: QtCore.QTimer.singleShot(
                200, lambda: self.ensure_not_particle_class_selected()
            )
        )

        config.global_signals.start_single_button_inference_loading_signal.connect(
            self.start_single_button_inference_loading
        )

        config.global_signals.start_analysis_signal.connect(
            lambda: self.sendAnnotatedImagesToServer()
        )
        config.global_signals.spawn_channels_signal.connect(
            self.channel_picker_widget.spawn_channels
        )
        self.viewer.LeftArrowChangeButton.updatePositionViewer()
        self.viewer.RightArrowChangeButton.updatePositionViewer()
        self.MainWindow.closeEvent = self.closeEvent

        from celer_sight_ai import config

        config.global_signals.reCheckNeuralNets_magicBoxSignal.connect(
            lambda: self.sdknn_tool.load_specialized_model()
        )
        config.global_signals.toggle_mask_class_visibility_signal.connect(
            self.toggle_mask_class_visibility
        )

        config.global_signals.load_main_scene_signal.connect(self.load_main_scene)
        config.global_signals.load_main_scene_and_fit_in_view_signal.connect(
            self.load_main_scene_and_fit_in_view
        )
        config.global_signals.update_celer_sight_ai_signal.connect(
            config.update_celer_sight_ai
        )
        if not config.user_cfg.ALLOW_IMPORT_IMAGES_BUTTON:
            self.add_images_btn.setEnabled(False)
            self.add_images_btn.setVisible(False)

        from celer_sight_ai import config

        config.register_url_scheme()
        QtGui.QDesktopServices.setUrlHandler("CelerSight", self.handle_custom_url)

        config.check_for_update()  # threaded check for update

    def handle_custom_url(self, url):
        if url.host() == "patreon-connected":
            # Bring window to front
            self.MainWindow.show()
            self.MainWindow.raise_()
            self.MainWindow.activateWindow()
            # Handle successful Patreon connection
            # Update UI, etc.
            self.handle_patreon_connected()

    def hoverLeaveSpecial(self, event):
        return super(type(self.widgetAttached), self.widgetAttached).hoverLeaveEvent(
            event
        )

    def ExecAnalysisDialog(self, force_continue=False):
        """
        Runs analysis Dialog
        """
        from functools import partial

        # if particle analysis is selected, make sure that atleast one particle class has been generated
        if (
            config.global_params.analysis
            == self.new_analysis_object.analysis_map["particles"]
        ):
            particle_found = False
            # check on the first image, if any of the classes are particle class
            for i in self.DH.BLobj.get_all_image_objects():
                # iterate over all masks
                for m in i.masks:
                    if m.is_particle():
                        particle_found = True
                        break
                break
            if not particle_found:
                # analysis for particles cannot proceeed
                config.global_signals.errorSignal.emit(
                    "Analysis aborted. No particles are configured for this particle experiment.\nPlease configure particles by clicking on the 'particle' class (left)."
                )
                return

        # make sure that all of the channels across all images and treatments are the same
        # if not, give a warning to the user that it might lead tonexpected behavior

        all_images = self.DH.BLobj.get_all_image_objects()
        all_channels = [
            tuple(i.channel_list) if i.channel_list else tuple() for i in all_images
        ]
        if len(set([str(i) for i in all_channels])) > 1:
            if not force_continue:
                config.global_signals.actionDialogSignal.emit(
                    "Multiple channels detected across images. This might lead to unexpected behavior.\n Continue?",
                    {
                        "Yes": partial(self.ExecAnalysisDialog, force_continue=True),
                        "No": lambda: None,
                    },
                )
                return

        # check if there are any annotations, if not then give an error and abort
        if len([i for i in self.DH.BLobj.get_all_mask_objects()]) == 0:
            config.global_signals.errorSignal.emit(
                "No ROI's found, please create ROI's first and then analyze."
            )
            return
        config.global_signals.start_analysis_signal.emit()

        return  #  intensity analysis does not need a prompt

    def FinalizeMainWindow(self):
        # Set up dialog for analysis, runs after log in.

        # #######################################################################
        #         # MainWindow Options
        # #######################################################################

        self.under_window_comments.setText("")
        # Add near the beginning of the method
        self.undoAction.setShortcut(QtGui.QKeySequence.StandardKey.Undo)
        self.redoAction.setShortcut(QtGui.QKeySequence.StandardKey.Redo)
        self.initialize_analysis_button.setEnabled_(False)  # before we add RNAi
        self.get_roi_ai_button.setEnabled_(False)  # before we add RNAi
        config.global_signals.RNAi_list_widget_update_signal.connect(
            self.updateDictionariesWithNewKeys
        )  # triger this by RNAi_list_widget_update_signal signals
        self.RNAi_list.itemClicked.connect(
            self.switch_treatment_onchange  #  can be internal in the custom list widget
        )  # removes mask asset/image buttons from the overview tabs

        self.addRNAi_button_list.clicked.connect(
            lambda: self.images_preview_graphicsview.clear_out_visible_buttons()
        )
        self.addRNAi_button_list.clicked.connect(lambda: self.add_new_treatment_item())
        self.addRNAi_button_list.clicked.connect(lambda: self.load_main_scene())

        self.delete_button_list.clicked.connect(lambda: self.delete_RNAi_list_item())

        self.add_images_btn.clicked.connect(
            lambda: self.add_images_btn._timer.force_stop()
        )  # Stops the timer for the animation of the button
        self.add_images_btn.clicked.connect(
            lambda: self.add_images_btn.setIcon(icon_RNAi)
        )  # When the animation stops, we set the first icon again
        self.add_images_btn.clicked.connect(
            lambda: self.Ui_control(lock_wdigets=True)
        )  # All Widgets are locked when importing Images
        self.add_images_btn.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )  # Apply Past events up to here
        # self.add_images_btn.clicked.connect(lambda: self.get_folder_list_files())
        self.add_images_btn.clicked.connect(lambda: self.ImportDecider())

        self.add_images_btn.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.add_images_btn.clicked.connect(lambda: self.Ui_control(lock_wdigets=False))

        icon_RNAi = QtGui.QIcon()
        icon_RNAi.addPixmap(QtGui.QPixmap("data/icons/add_rnai_V1/cross_v100.png"))

        # self.auto_aa_tool_gui.signal_add_FG.connect(lambda: self.viewer.aa_signal_handler(add_fg = True, add_bg = False) )
        # self.auto_aa_tool_gui.signal_add_BG.connect(lambda: self.viewer.aa_signal_handler(add_fg = False, add_bg = True))
        from celer_sight_ai.gui.custom_widgets.analysis_handler import Ui_AnalysisDialog
        from celer_sight_ai.inference_handler import InferenceHandler

        self.AnalysisSettings = Ui_AnalysisDialog(self)

        self.MyInferenceHandler = InferenceHandler(MainWindowRef=self)
        if config.user_cfg.ALLOW_PLOTTING_TOOLS == False:
            # self.MasterTabWidgets.setTabEnabled(2, False)
            self.fillerPlotWidget = QtWidgets.QWidget()
            self.fillerPlotWidget.setFixedSize(QtCore.QSize(2000, 2000))
            self.fillerPlotWidget.setParent(self.plots)
            self.fillerPlotWidget.move(0, 0)
            self.fillerPlotWidget.setStyleSheet("background-color:rgba(0,0,0,240);")

        self.get_roi_ai_button.clicked.connect(
            lambda: self.get_roi_ai_button._timer.force_stop()
        )
        self.get_roi_ai_button.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.get_roi_ai_button.clicked.connect(
            lambda: self.MyInferenceHandler.DoInferenceAllImagesOnlineThreaded()
        )

        self.initialize_analysis_button.clicked.connect(
            lambda: self.ExecAnalysisDialog()
        )

        # if
        self.endThreadContribNets = False

        self.threadpool = QtCore.QThreadPool()

        self.actionPatreon.triggered.connect(lambda: self.spawn_patreon_widget())

        self.up_button_list.clicked.connect(lambda: self.up_button_list_item())
        self.down_button_list.clicked.connect(lambda: self.down_button_list_item())

        # TODO: update this
        self.pg1_Maskshandler_DeleteAll_button.clicked.connect(
            lambda: self.myButtonHandler.button_instance.DeleteAllCurrentMasks()
        )
        self.pg1_Maskshandler_DeleteAllBit_button.clicked.connect(
            lambda: self.myButtonHandler.button_instance.DeleteAllMasksAllImagesAllConditions()
        )

        self.actionExport_to_imagej.triggered.connect(lambda: self.ExportimagejROI())

        actionSelectAll = QtGui.QAction("Select All", self)
        actionSelectAll.setShortcut("Ctrl+A")
        self.menuEdit.addAction(actionSelectAll)

        config.global_signals.loadSceneSignal.connect(self.loadSceneSignalMethod)
        config.global_signals.change_image_hook.connect(self.change_image_hook_method)

        self.pg1_settings_contras_slider.valueChanged.connect(
            lambda: self.load_main_scene_if_photo()
        )

        self.actionSend_logs_to_dev.triggered.connect(lambda: self.sendLogsToServer())

        # TODO: fix here

        config.global_signals.DialogImportSettingsSignal.connect(
            lambda: self.OnImportGetImagefromButtons()
        )
        config.global_signals.MaskToSceneSignal.connect(self.appendMaskToScene)
        config.global_signals.load_all_current_image_annotations_signal.connect(
            self.load_all_current_image_annotations
        )

        config.global_signals.update_class_scene_color_signal.connect(
            lambda: self.viewer.update_class_scene_color()
        )

        self.pg1_settings_all_masks_color_button.clicked.connect(
            lambda: self.assign_color_to_current_class()
        )

        self.pg1_settings_all_masks_color_button.clicked.connect(
            lambda: self.viewer.updateAllPolygonPen()
        )

        self.pg1_settings_mask_opasity_slider.valueChanged.connect(
            lambda: self.viewer.updateAllPolygonPen()
        )

        self.pg1_Maskshandler_DeleteAll_button.clicked.connect(
            lambda: self.ApplyAttributesToAllImages()
        )

        """
        Plot tools and all plot connections and settings:
        """

        from celer_sight_ai.gui.custom_widgets.plot_handler import (
            PlotViewerHandler,
            plotStylesHandler,
        )

        self.canvas = None  # FigureCanvas(Figure())
        self.pg2_plot_btn.clicked.connect(lambda: self.delete_canvas())
        self.pg2_plot_btn.clicked.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.pg2_plot_btn.clicked.connect(lambda: self.plot_seaborn())
        self.pg2_clear_btn.clicked.connect(lambda: self.delete_canvas())

        self.Results_pg2_AnalysisTypeComboBox.currentIndexChanged.connect(
            lambda: self.plot_seaborn()
        )
        self.channel_analysis_metrics_combobox.currentIndexChanged.connect(
            lambda: self.plot_seaborn()
        )

        self.ROI_analysis_metrics_combobox.currentIndexChanged.connect(
            lambda: self.plot_seaborn()
        )
        self.Results_pg2_AnalysisTypeComboBox.currentIndexChanged.connect(
            lambda: QtWidgets.QApplication.processEvents()
        )
        self.Results_pg2_AnalysisTypeComboBox.currentIndexChanged.connect(
            lambda: self.compute_transform_and_display_analysis()
        )
        self.channel_analysis_metrics_combobox.currentIndexChanged.connect(
            lambda: self.compute_transform_and_display_analysis()
        )
        self.ROI_analysis_metrics_combobox.currentIndexChanged.connect(
            lambda: self.compute_transform_and_display_analysis()
        )
        self.pg2_remove_plot_button.clicked.connect(lambda: self.DeletePlotInstances())
        self.pg2_add_plot_button.clicked.connect(lambda: self.AddNewPlot())
        self.MyVisualPlotHandler = PlotViewerHandler(self)
        self.myPlotStylesHandler = plotStylesHandler(self)
        self.pg2_save_preset_btn.clicked.connect(
            lambda: self.myPlotStylesHandler.saveStyleDictionary()
        )
        self.pg2_load_preset_btn.clicked.connect(
            lambda: self.myPlotStylesHandler.loadStyleDictionary()
        )

        # Plot ToolsWidget Signals:
        self.pg2_graph_type_comboBox.currentIndexChanged.connect(
            lambda: self.pg2_graph_type_comboBox.blockSignals(True)
        )
        self.pg2_graph_type_comboBox.currentIndexChanged.connect(
            lambda: self.pg2_graph_type_comboBox.setEnabled(False)
        )
        QtWidgets.QApplication.processEvents()
        self.pg2_graph_type_comboBox.currentIndexChanged.connect(
            lambda: self.show_only_active_plot_settings()
        )

        self.pg2_graph_type_comboBox.currentIndexChanged.connect(
            lambda: self.pg2_graph_type_comboBox.setEnabled(True)
        )
        self.pg2_graph_type_comboBox.currentIndexChanged.connect(
            lambda: self.pg2_graph_type_comboBox.blockSignals(False)
        )

        # Copy to clipboard signals Review variables
        self.CopyDecimalDot.clicked.connect(
            lambda: config.global_signals.CopySpreadSheetToClipboard.emit("dot")
        )
        self.CopyDecimalComma.clicked.connect(
            lambda: config.global_signals.CopySpreadSheetToClipboard.emit("comma")
        )

        self.actionPreferences.triggered.connect(
            lambda: self.Lunch_application_after_authenticationSettings()
        )
        self.actionsubmit_annotations_admin.triggered.connect(
            self.set_remote_annotation_session_as_audited
        )
        self.actionCompute_ROI_tracks_from_video.triggered.connect(
            self.store_locomotion_data
        )
        self.actionSign_Out.triggered.connect(lambda: self.sign_out())

        # Add BYUttons adds the buttonds assets
        # TODO: TEstint AddButtonHandler class REMOVE:
        from celer_sight_ai.core.image_button_handler import AddButtonHandler

        self.myButtonHandler = AddButtonHandler(self)

        config.global_signals.download_remote_image_signal.connect(
            self.download_remote_image
        )

        config.global_signals.create_annotation_object_signal.connect(
            self.MyInferenceHandler.create_annotation_object
        )
        config.global_signals.create_annotations_objects_signal.connect(
            self.MyInferenceHandler.create_annotations_objects
        )

        config.global_signals.deleteMaskFromMainWindow.connect(
            self.MyInferenceHandler.deleteMaskaFromImage
        )

        config.global_signals.deleteTrackFromMainWindow.connect(
            self.MyInferenceHandler.deleteTrackFromMainWindow
        )

        config.global_signals.delete_hole_from_mask_signal.connect(
            self.MyInferenceHandler.delete_hole_from_mask
        )
        from celer_sight_ai.io.image_reader import create_pyramidal_tiff

        config.global_signals.create_pyramidal_tiff_for_image_object_signal.connect(
            create_pyramidal_tiff_for_image_object
        )
        config.global_signals.update_scene_ultra_high_res_plane_signal.connect(
            self.viewer.update_scene_ultra_high_res_plane
        )
        config.global_signals.add_partial_slide_images_to_scene_signal.connect(
            self.viewer.add_partial_slide_images_to_scene
        )
        config.global_signals.check_and_update_high_res_slides_signal.connect(
            self.viewer.check_and_update_high_res_slides
        )

        self.actionRun_Test_Suite.triggered.connect(self.run_test_suite)
        config.global_signals.delete_all_masks_with_class_signal.connect(
            self.DH.BLobj.delete_all_masks_with_class
        )

        from celer_sight_ai.gui.custom_widgets.loading_dialog_widget import (
            LoadingDialog,
        )

        self.FrameRegionInfo.hide()

        self.loading_window = LoadingDialog(self.MainWindow)
        self.MainWindow.keyPressEvent = (
            self.keyPressEvent
        )  #!! need this if key events happen in the main winodw
        self.MainWindow.keyReleaseEvent = self.keyReleaseEvent
        self.MainWindow.changeEvent = self.changeEvent
        self.MainWindow.moveEvent = self.moveEvent
        self.installEventFilter(self)
        self.viewer.setAcceptDrops(True)
        self.setMouseTracking(True)

        # add model selection / ROI part selection
        from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
            FilterableIconTable,
            gather_cfgs,
        )

        category_map = gather_cfgs()

        self.category_selection_grid = FilterableIconTable(
            category_map=category_map, parent=self
        )

        self.category_selection_grid_layout.addWidget(self.category_selection_grid)

    @config.threaded
    def download_remote_image(self, image_object):
        image_object.download_remote_image()

    def toggle_mask_class_visibility(self, show=False, class_uuid=None):
        # hide all of the annotation on screen with that class_uuid
        # get all items in the scene
        from celer_sight_ai.gui.custom_widgets.scene import (
            BitMapAnnotation,
            PolygonAnnotation,
        )

        for item in self.viewer.scene().items():
            # get item class uuid:
            if hasattr(item, "class_id"):
                if class_uuid == item.class_id:
                    if isinstance(item, PolygonAnnotation):
                        # hide all items
                        item.set_visible_all(show)
                    elif isinstance(item, BitMapAnnotation):
                        item.setVisible(show)

    def spawn_patreon_widget(self):
        from celer_sight_ai.gui.custom_widgets.patreon_widget import PatreonWidget

        if config.user_cfg["OFFLINE_MODE"] == True:
            config.global_signals.errorSignal.emit(
                "Please sign in to connect your Patreon account."
            )
            return
        self.patreon_widget = PatreonWidget(self.MainWindow)
        self.patreon_widget.show()

    def set_remote_annotation_session_as_audited(self):
        """
        Sets the current active remote annotation session as audited
        """

        # get all images open
        all_images = [i for i in self.DH.BLobj.get_all_image_objects()]
        # get all image uuids
        all_image_uuids = [i.unique_id for i in all_images]
        # get all class names
        class_names = [i.text() for i in self.custom_class_list_widget.classes.values()]
        success, error_message = config.client.set_remote_annotation_session_as_audited(
            all_image_uuids, class_names
        )
        if not success:
            config.global_signals.errorSignal.emit(error_message)
            return
        # confirm with dialog
        config.global_signals.successSignal.emit("Images marked as audited")

    def create_new_label(self):
        # spawn dialog to create custom label
        # the label is create
        raise NotImplementedError

    def spawn_add_class_dialog(self):
        from celer_sight_ai.gui.custom_widgets.grid_button_image_selector import (
            FilterableClassList,
            gather_cfgs,
        )

        # get the image viewer
        # parent = self.viewer
        items = gather_cfgs(supercategory=config.supercategory)
        self.filterable_class_list = FilterableClassList(
            items=items, parent=self, with_model_type_selection=False
        )
        self.filterable_class_list.setParent(self.Images)
        self.filterable_class_list.show()

    def reload_config_user_settings(self):
        """
        Reloads the user settings from the config file, often usefull while testing
        """
        config.user_cfg, config.user_cfg_settings = config.load_user_settings()

    def Lunch_application_after_authenticationSettings(self):
        uiDialog = settingsMainClass(self.MainWindow)

    def sendLogsToServer(self):
        import celer_sight_ai.configHandle as configHandle
        from celer_sight_ai import config

        client = config.client
        client.crashLogsToServer()
        from celer_sight_ai.gui.designer_widgets_py_files.JobCompleteConfirmationDialog import (
            Ui_JobComplete as JobCompleteForm_UI,
        )

        self.JobCompleteForm = JobCompleteForm_UI()
        self.JobCompleteDialog = QtWidgets.QDialog()
        self.JobCompleteForm.setupUi(self.JobCompleteDialog)
        self.JobCompleteForm.retranslateUi(self.JobCompleteDialog)

        self.JobCompleteForm.ImportingLabel.setText(
            "Thank you for submitting the report"
        )

        self.JobCompleteForm.buttonBox.clicked.connect(
            lambda: self.JobCompleteDialog.close()
        )
        self.JobCompleteDialog.show()

    def ensure_not_particle_class_selected(self):
        """
        This method ensures that there is no particle class selected,
            usefull for when the user selects a ROI interactive tool.
        """
        logger.debug("Ensuring not particle selected")
        # get current class
        current_class_widget = self.custom_class_list_widget.currentItemWidget()
        if not current_class_widget:
            return
        if current_class_widget.is_particle:
            # if it has a parent
            if current_class_widget.parent_class_uuid:
                # select parent class
                self.custom_class_list_widget.click_on_widget_by_uuid(
                    current_class_widget.parent_class_uuid
                )

    def keyReleaseEvent(self, e):
        if e.type() == QtCore.QEvent.Type.KeyRelease:
            if self.during_drawing == False and e.modifiers() == QtCore.Qt.Modifier.ALT:
                self.polygon_remove_mode = False

        if self.viewer.hasPhoto():
            if e.isAutoRepeat():
                # return
                return super(Master_MainWindow, self).keyReleaseEvent(e)
            if e.type() == QtCore.QEvent.Type.MouseButtonRelease:
                if e.button() == QtCore.Qt.MouseButton.RightButton:
                    return False

            if (
                e.type() == QtCore.QEvent.Type.KeyRelease
                and e.key() == QtCore.Qt.Key.Key_Space
            ):
                self.viewer.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)

        return super(Master_MainWindow, self).keyReleaseEvent(e)

    def keyPressEvent(self, e):
        # Ignore standalone modifier key presses
        if e.key() in (
            QtCore.Qt.Key.Key_Control,  # 16777249
            QtCore.Qt.Key.Key_Shift,
            QtCore.Qt.Key.Key_Alt,
            QtCore.Qt.Key.Key_Meta,
        ):
            return super(Master_MainWindow, self).keyPressEvent(e)

        # self.modifiers = QtWidgets.QApplication.keyboardModifiers()
        # Move to next image with keys:
        if e.matches(QtGui.QKeySequence.StandardKey.Undo):
            self.undoAction.trigger()
            return
        if e.matches(QtGui.QKeySequence.StandardKey.Redo):
            self.redoAction.trigger()
            return
        # if e.key() == Qt.Key.Key_I and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
        # do single image inference
        if e.type() == QtCore.QEvent.Type.KeyPress:
            # selection shorcut
            if e.key() == QtCore.Qt.Key.Key_Q:
                self.actionSelectionTool.trigger()
            if e.key() == QtCore.Qt.Key.Key_3:
                self.MagicBrushMoveTool.trigger()
            if e.key() == QtCore.Qt.Key.Key_2:
                self.PolygonTool.trigger()
            if e.key() == QtCore.Qt.Key.Key_F:
                self.actionAutoTool.trigger()

            if e.key() == QtCore.Qt.Key.Key_D:
                image_object = self.DH.BLobj.get_current_image_object()
                if not image_object:
                    return
                if (
                    self.current_imagenumber
                    < len(
                        self.DH.BLobj.groups["default"]
                        .conds[self.DH.BLobj.get_current_condition()]
                        .images
                    )
                    - 1
                ):
                    config.global_signals.next_image_signal.emit()

                    # self.myButtonHandler.SetCheckToTrue(self.current_imagenumber)
            if e.key() == QtCore.Qt.Key.Key_A:
                if self.current_imagenumber > 0:
                    config.global_signals.previous_image_signal.emit()
        if e.modifiers() == QtCore.Qt.Modifier.ALT:
            self.polygon_remove_mode = True
        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.viewer.keyPressEvent(e)  # to cancel drawing
            return super(Master_MainWindow, self).keyPressEvent(e)
            # pass
        if e.type() == QtCore.QEvent.Type.MouseMove:
            pass

        if self.viewer.hasPhoto():
            if e.key() == QtCore.Qt.Key.Key_Space:
                if e.isAutoRepeat():
                    return super(Master_MainWindow, self).keyPressEvent(e)
                self.viewer.toggleDragMode()

            if e.key() == QtCore.Qt.MouseButton.RightButton:
                return super(Master_MainWindow, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key.Key_Left and self.imagenumber > 0:
            self.imagenumber = self.imagenumber - 1
            self.load_main_scene(self.imagenumber)

        if e.key() == QtCore.Qt.Key.Key_Escape:
            # self.close()
            return super(Master_MainWindow, self).keyReleaseEvent(e)

        if e.key() == QtCore.Qt.MouseButton.RightButton:
            pass

        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            # Ctrl+C
            if e.key() == Qt.Key.Key_C:
                self.copy_scene_items()
            # Ctrl+V
            elif e.key() == Qt.Key.Key_V:
                self.paste_scene_items()
            if e.key() == QtCore.Qt.Key.Key_Equal:
                self.viewer.zoom_in()
                return super(Master_MainWindow, self).keyPressEvent(e)
            elif e.key() == QtCore.Qt.Key.Key_Minus:
                self.viewer.zoom_out()
                return super(Master_MainWindow, self).keyPressEvent(e)

        return super(Master_MainWindow, self).keyPressEvent(e)

    # def moveEvent(self, event):
    #     return super(Master_MainWindow, self).moveEvent( event)

    def copy_scene_items(self):
        from celer_sight_ai import PolygonAnnotation

        items = self.viewer.scene().items()
        # So far only polygons are copied
        items = [i for i in items if isinstance(i, PolygonAnnotation)]
        self.copied_item = []
        if len(items) == 0:
            return
        items = [i for i in items if i.isSelected()]
        # Polygon object copied in memory will have this stracture:
        # [mask_type (polygon) , class_id , included_in_analysis , visibility]
        for item in items:
            # get mask by uuid of the item
            m = self.DH.BLobj.get_mask_object_by_uuid(item.unique_id)
            self.copied_item.append(
                {
                    "mask_type": m.mask_type,
                    "class_id": m.class_id,
                    "included_in_analysis": m.includedInAnalysis,
                    "visibility": m.visibilit,
                    "array": m.get_array(),
                }
            )

    def paste_scene_items(self):
        from celer_sight_ai import config

        for item in self.copied_items:
            config.global_signals.create_annotation_object.emit(
                [
                    self.MainWindow.DH.BLobj.get_current_condition(),
                    None,
                    [item["array"]],
                    self.MainWindow.current_imagenumber,
                    item["class_id"],
                    item["mask_type"],  # TODO: needs to be changed
                ]
            )

    def changeEvent(self, event):  # this is to catch window dchange events
        if hasattr(self, "aa_review_state"):
            self.MainWindow.FixTopFrameSignal.emit()

            if (
                event.type() == QtCore.QEvent.Type.WindowStateChange
                and self.aa_review_state == True
            ):
                if event.oldState() and QtCore.Qt.WindowState.WindowMinimized:
                    # self.auto_annotate_tool.show()
                    # self.auto_annotate_tool.raise_()
                    pass
                elif (
                    event.oldState() == QtCore.Qt.WindowState.WindowNoState
                    or self.windowState() == QtCore.Qt.WindowState.WindowMaximized
                ):
                    # self.auto_annotate_tool.hide()
                    pass
        return super(Master_MainWindow, self).changeEvent(event)

    ##########################################################################
    ################ Functions for Dialogue and windows 1,2,3 ################
    ##########################################################################

    @config.threaded
    def sendAnnotatedImagesToServer(
        self, force=False, with_dialog=False, state="corrected"
    ):
        """
        This function runs  when the user has annotated all of his data and he is ready to qunatify the results
        At that point, all of the images that have altered the annotation after the generated annotations that where computed
        from cloud inference, then this meants that these images generated inprecize annotations and need to bre retrained.
        """
        from celer_sight_ai import config
        from celer_sight_ai.core.threader import Threader

        config.contribing_data = True

        if config.user_cfg["SEND_CORRECTED_ANNOTATIONS"] == False and force == False:
            config.contribing_data = False
            return

        if with_dialog:

            config.global_signals.loading_dialog_show.emit()
            config.global_signals.loading_dialog_set_text.emit(
                "Uploading images for model retraining"
            )
            config.global_signals.loading_dialog_signal_update_progress_percent.emit(0)
            config.global_signals.loading_dialog_center.emit()
        client = config.client
        total_images_states = []
        # calculate the number of images that need to be sent
        total_images = len([i for i in self.DH.BLobj.get_all_image_objects()])
        current_image = 0
        logger.info("Started sending annotated images to server")
        # loop over all groups
        for group in self.DH.BLobj.groups:
            # loop over all conditions
            for cond in self.DH.BLobj.groups[group].conds:
                # loop over all images
                for imageID in range(
                    len(self.DH.BLobj.groups[group].conds[cond].images)
                ):
                    # if the annotation has been altered
                    if (
                        self.DH.BLobj.groups[group]
                        .conds[cond]
                        .images[imageID]
                        .userModifiedAnnotation
                    ) or force:
                        # send the image to the server
                        logger.info(
                            f"Sending image {imageID} to server at group {group} and condition {cond}"
                        )
                        # send threaded
                        try:
                            image_object = (
                                self.DH.BLobj.groups[group].conds[cond].images[imageID]
                            )
                            start_percentage = int((current_image / total_images) * 100)
                            end_percentage = int(
                                ((current_image + 1) / total_images) * 100
                            )

                            success, error_message = (
                                client.send_large_zipped_image_annotated(
                                    image_object,
                                    with_dialog=with_dialog,
                                    start_percentage=start_percentage,
                                    end_percentage=end_percentage,
                                    state=state,
                                )
                            )
                            if not success:
                                logger.error(f"Error : {error_message}")
                                config.global_signals.loading_dialog_signal_close.emit()
                                config.global_signals.errorSignal.emit(
                                    f"Error : {error_message}"
                                )
                                config.contribing_data = False
                                return
                            total_images_states.append([success, error_message])

                        except Exception:
                            import traceback

                            logger.error(f"Error : {error_message}")
                            logger.error(traceback.format_exc())
                            config.global_signals.errorSignal.emit(
                                "Failed to send data."
                            )
                            if with_dialog:
                                config.global_signals.loading_dialog_signal_close.emit()
                            config.contribing_data = False
                            return False
                        current_image += 1

                        if with_dialog:
                            # update percent
                            config.global_signals.loading_dialog_signal_update_progress_percent.emit(
                                int(round(current_image / total_images) * 100)
                            )
                        # If successfull mark it as completed, leaving outside of the try, except now so that we dont get
                        # any frozen interfaces.
                        self.DH.BLobj.groups[group].conds[cond].images[
                            imageID
                        ].setHasBeenUploaded(True)
        if with_dialog:
            config.global_signals.loading_dialog_signal_close.emit()
            if not all(total_images_states):
                logger.error(
                    f"Failed to send image {imageID} to server at group {group} and condition {cond}"
                )
                config.global_signals.loading_dialog_signal_close.emit()
                config.global_signals.warningSignal.emit(
                    "Failed to submit some of the data."
                )
            else:
                config.global_signals.successSignal.emit("Data submitted successfully")
        config.contribing_data = False

    def OnImportGetImagefromButtons(self, MODE=0):
        ChannelPickerWindow.MultiChannelImporterForm.close()
        QtWidgets.QApplication.processEvents()
        AllImages, resizedImages, sappliedNames = self.CollectImages(MODE)
        if AllImages == None or len(AllImages) == 0:
            return
        else:
            raise NotImplementedError("OnImportChannelPicker was here")
            # self.OnImportChannelPicker(AllImages, resizedImages, sappliedNames)
            self.load_main_scene(self.current_imagenumber)
            return

    def start_remote_annotation_session(self, without_prompt=False):
        """
        Starts a remote session for the user
        If the user is not in a session currently:
            1) Go to mainwindow.
            2) Get urls and add them to the scene
            3) Any adjustments to those are automatically updated with the server
        Otherwise:
            1) close the current session (prompt user to exit)
            2) start remote session
        """
        self.quit_project(without_prompt=without_prompt)
        # automatically log in, set supercategory and categroy and load some images.
        self.organism_selection.CelegansMainButton.click()
        # click on a default category
        self.CreateNewVButton_proceed.click()
        config.supercategory = config.user_cfg["REMOTE_ANNOTATION_SUPERCATEGORY"]
        # delete all classes
        self.custom_class_list_widget.delete_all_classes()
        # draw out the image urls and create a treatment
        client = config.client
        urls = client.remote_image_batch_for_annotation()
        # add images by drug and drop
        self.viewer.load_files_by_drag_and_drop(
            {"images": ["celer_sight_ai:" + i["image_uuid"] for i in urls]}
        )

    def sign_out(self):
        """
        Sign out the user from the application
        """
        from celer_sight_ai import config, configHandle

        logger.info("Signing out user")

        self.current_home_display_widget = None
        self.HomeButtonMain.click()

        self.images_preview_graphicsview.reset_state()
        # remove all treatments items in the list widget
        self.RNAi_list.clear()
        # delete all objects
        self.DH.reset_state()
        # delete all classes
        self.custom_class_list_widget.reset_state()
        # delete all analysis
        self.AnalysisSettings.reset_state()
        self.ai_model_combobox.setIndexAsSelected(0)
        # refresh scene
        self.images_preview_graphicsview.reset_state()
        self.clearViewerOnRefresh()
        # set the mainwindow to the login page
        self.stackedWidget.setCurrentWidget(self.MainInterface)
        self.viewer.setFocus()
        self.MainWindow.hide()

        # clear out log in state
        config.client.jwt = None

        # remove the jwt tokens from memory
        configHandle.clear_jwt_token_for_auto_login()

        # show log in dialog
        config.global_signals.show_log_in_dialog_signal.emit()
        config.categories_that_need_thumbnail = []
        # TODO: stop any ongoing processes such as inference sessions

    def quit_project(self, without_prompt=False):
        """
        Quit the project and bring the user back to the selection screen
        """
        if without_prompt is False:
            # ask the user if they want to quit
            reply = QtWidgets.QMessageBox.question(
                self.MainWindow,
                "Quit",
                "Are you sure you want to quit the project?\nAll unsaved data will be lost.",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply == QtWidgets.QMessageBox.StandardButton.No:
                return
        # click on the home button first
        self.current_home_display_widget = None
        self.HomeButtonMain.click()
        logger.info("Quiting project")
        self.images_preview_graphicsview.reset_state()
        # remove all treatments items in the list widget
        self.RNAi_list.clear()
        # delete all objects
        self.DH.reset_state()
        # delete all classes
        self.custom_class_list_widget.reset_state()
        # delete all analysis
        self.AnalysisSettings.reset_state()
        self.ai_model_combobox.setIndexAsSelected(0)
        # refresh scene
        self.images_preview_graphicsview.reset_state()
        self.clearViewerOnRefresh()
        self.stackedWidget.setCurrentWidget(self.orgSelectionSection)

    def CollectImages(self, MODE=0):
        """
        Depending on the modes we gother images
        0,0 = 0 None
        1,0 = 1 Combined only
        0,1 = 2 indi only
        1,1 = 3
        set up sapplied names also
        """
        import cv2

        allImages = []
        resizedImages = []
        sappliedNames = []
        iterator = 0
        if MODE == 0:
            return (None, None, None)
        elif MODE == 1:
            items = (
                ChannelPickerWindow.gridLayout_7.itemAt(i)
                for i in range(ChannelPickerWindow.gridLayout_7.count())
            )
            for w in items:
                iterator += 1
                fusedImage = w.widget().FuseImages(
                    w.widget().PushButton1.Image, w.widget().PushButton2.Image
                )
                fusedresizedImage = w.widget().FuseImages(
                    w.widget().PushButton1.resizedImage,
                    w.widget().PushButton2.resizedImage,
                )
                try:
                    allImages.append(fusedImage.copy())
                    resizedImages.append(fusedresizedImage.copy())
                    sappliedNames.append(None)
                except Exception:
                    pass
        elif MODE == 2:
            items = (
                ChannelPickerWindow.gridLayout.itemAt(i)
                for i in range(ChannelPickerWindow.gridLayout.count())
            )
            for w in items:
                iterator += 1
                allImages.append(w.widget().Image.copy())
                resizedImages.append(w.widget().resizedImage.copy())
                sappliedNames.append(w.widget().imgPath)

        elif MODE == 3:
            items = (
                ChannelPickerWindow.gridLayout_7.itemAt(i)
                for i in range(ChannelPickerWindow.gridLayout_7.count())
            )
            for w in items:
                iterator += 1
                fusedImage = w.widget().FuseImages(
                    w.widget().PushButton1.Image, w.widget().PushButton2.Image
                )
                fusedresizedImage = w.widget().FuseImages(
                    w.widget().PushButton1.resizedImage,
                    w.widget().PushButton2.resizedImage,
                )
                try:
                    allImages.append(fusedImage.copy())
                    resizedImages.append(fusedresizedImage.copy())
                    sappliedNames.append(None)
                except:
                    pass
            items = (
                ChannelPickerWindow.gridLayout.itemAt(i)
                for i in range(ChannelPickerWindow.gridLayout.count())
            )
            for w in items:
                iterator += 1
                allImages.append(w.widget().Image.copy())
                resizedImages.append(w.widget().resizedImage.copy())
                sappliedNames.append(w.widget().imgPath)
        # change rgb to bgr..
        for i in range(len(allImages)):
            allImages[i] = cv2.cvtColor(allImages[i], cv2.COLOR_BGR2RGB)
        return allImages, resizedImages, sappliedNames

    def get_current_treatment_widget(self):
        """
        Gets the currently selected treatment widget from the RNAi list.

        Returns:
            QListWidgetItem: The currently selected treatment widget item, or None if no item is selected.

        This method iterates through all items in the RNAi list and returns the first selected item.
        The RNAi list contains treatment widgets that represent different experimental conditions.
        """
        return self.RNAi_list.currentItem()

    def get_treatment_widget_by_name(self, treatment_name):
        for i in range(self.RNAi_list.count()):
            if self.RNAi_list.item(i).text() == treatment_name:
                return self.RNAi_list.item(i)
        return None

    def add_new_treatment_item(self, condition_name=None, condition_uuid=None):
        """
        Function to add a new Condition on the top right list.
        In addition all of the associated containers of arrays are updated, focus goes
        to the new condition list item
        """
        from celer_sight_ai.gui.custom_widgets.plot_handler import PlotViewerHandler

        logger.debug("add_new_treatment_item")
        if not condition_name:
            ConditionAdded = PlotViewerHandler.CheckDictionaryName(
                "Treatment", self.DH.BLobj.groups["default"].conds
            )
        else:
            ConditionAdded = condition_name
        # make sure that the treatment name is Unique
        if ConditionAdded in self.DH.BLobj.groups["default"].conds:
            ConditionAdded = PlotViewerHandler.CheckDictionaryName(
                "Treatment", self.DH.BLobj.groups["default"].conds
            )
        # if the item is already in the list with exactly the same name, do not add it
        if (
            ConditionAdded
            in self.RNAi_list.findItems(
                ConditionAdded, QtCore.Qt.MatchFlag.MatchExactly
            )
            or ConditionAdded in self.DH.BLobj.get_all_treatment_names()
        ):
            config.global_signals.notificationSignal(
                f"Treatment {ConditionAdded} already exists, skipping."
            )
            return ConditionAdded
        self.RNAi_list.setEnabled(False)
        # Clear any previous related variables
        if self.RNAi_list.count() != 0:
            if (
                self.RNAi_list.currentItem().text()
                == self.DH.BLobj.get_current_condition()
            ):
                self.previous_clicked_treatment_item = (
                    self.DH.BLobj.get_current_condition()
                )
            # self.previous_item_name_RNAi_list = self.RNAi_list.currentItem().text()
            # initializw everything again....
            self.temp_mask_to_use_Test_x = []
            self.temp_mask_to_use_Test_y = []
            self.counter_tmp = 0
            self.DH.unique_masks_tmp = []
            self.DH.masks_state_usr = []
            self.DH.masks_state = []
            # gui_main.main_viewer_state = False
            self.DH.predict_masks_state = False
            self.DH.pixon_list_opencv = []
            self.DH.all_masks = []
            self.DH.image_names = []
            self.DH.all_masks_usr = []
            self.selected_mask = -1
            self.DH.current_RNAi = 0
            dictionary_max_elements = 5
            self.DH.added_to_dictionary_state = True
            self.setCurrentImageNumber(-1)
            self.previous_imagenumber = -1
            self.selection_state = False  # weather or not we can aselect a mask
            ## lebel adds aggregates only
            self.DH.aggs_lables_all_RNAi = []
            self.DH.aggs_lables_RNAi = []
            self.DH.aggs_lables_worm = []
            self.DH.summary_counts_RNAi = []
            ## per count aggregates only
            self.DH.aggs_counts_all_RNAi = []  #
            self.DH.aggs_counts_RNAi = []
            self.DH.aggs_counts_worm = []
            self.DH.summary_counts_RNAi = []  #
            ## per volume aggregates only
            self.DH.aggs_volume_all_RNAi = []  #
            self.DH.aggs_volume_RNAi = []
            self.DH.aggs_volume_worm = []
            self.DH.summary_volume_RNAi = []  #
            self.imagenumber = 0
            self.all_stacked_images = []
            self.DH.view_field_list = []
            self.DH.AssetMaskListBool = []
            self.DH.AssetMaskListBoolSettings = []
            self.DH.AssetMaskListPolygon = []
            self.DH.AssetMaskListPolygonSettings = []

        self.name_of_added_listwidget = ConditionAdded
        # check again
        if (
            ConditionAdded
            in self.RNAi_list.findItems(
                ConditionAdded, QtCore.Qt.MatchFlag.MatchExactly
            )
            or ConditionAdded in self.DH.BLobj.get_all_treatment_names()
        ):
            config.global_signals.notificationSignal(
                f"Treatment {ConditionAdded} already exists, skipping."
            )
            self.RNAi_list.setEnabled(True)
            return ConditionAdded
        self.RNAi_list.addItem(self.name_of_added_listwidget)
        items = self.RNAi_list.findItems(
            self.name_of_added_listwidget, QtCore.Qt.MatchFlag.MatchExactly
        )  # get that particular item

        #
        # Update Dictionaries with new keys
        #
        import copy

        emptyList = []
        emptyList.append(copy.copy([]))
        self.DH.AssetMaskDictionary[str(self.name_of_added_listwidget)] = copy.deepcopy(
            emptyList
        )  # copy.copy(emptyList)
        self.DH.AssetMaskDictionaryBoolSettings[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList)
        self.DH.AnnotationRegions[str(self.name_of_added_listwidget)] = copy.deepcopy(
            emptyList
        )  # copy.copy(emptyList)
        self.DH.image_names_all_RNAi[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) # The name of the file
        self.DH.mask_RNAi_slots[str(self.name_of_added_listwidget)] = copy.deepcopy(
            emptyList
        )  # copy.copy(emptyList) # Dictionary for all_masks lists
        self.DH.usr_mask_RNAi_slots[str(self.name_of_added_listwidget)] = copy.deepcopy(
            emptyList
        )  # copy.copy(emptyList) #Dicitonary for all_masks_usr
        self.DH.dict_aggs_lables_all_RNAi[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList)# TODO: remove this its not used
        self.DH.dict_aggs_counts_all_RNAi[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) # Dictionary of all the aggregate counts, after the analysis
        self.DH.dict_aggs_volume_all_RNAi[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) # Dictionary of all the aggregate volume, after the analysis
        self.DH.dict_master_mask_list[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) # TODO: remove this its not used
        self.DH.dict_RNAi_attributes_all[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) # Dictionary for storing masks  state masks state usr, calculated dictionary state, added to dictionary state, predict masks state
        self.DH.all_worm_mask_points_x_slot[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList) #Dicionary for all_worm_mask_points_x
        self.DH.all_worm_mask_points_y_slot[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList)
        self.DH.stacked_images_slot[str(self.name_of_added_listwidget)] = copy.deepcopy(
            emptyList
        )  # copy.copy(emptyList) # Same as pixon_list_opencv dictionary? need to see whats going on here
        self.DH.mask_RNAi_slots_QPoints[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList)
        self.DH.mask_RNAi_slots_QPolygon[str(self.name_of_added_listwidget)] = (
            copy.deepcopy(emptyList)
        )  # copy.copy(emptyList)
        for index in items:
            index.setFlags(index.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
        if hasattr(self, "grid_layout_box1"):
            self.grid_layout_box1  # here we checklk to see if has been created or not,
            # its created on the  first addition and then when we dnd items its not needed to be added again
            self.myButtonHandler.UnparentLastCondition()

        self.DH.added_to_dictionary_state = False
        # if we just added an element select it
        self.RNAi_list.setCurrentRow(self.RNAi_list.count() - 1)
        self.get_roi_ai_button.setEnabled_(True)
        self.initialize_analysis_button.setEnabled_(True)
        self.viewer.LeftArrowChangeButton.show()
        self.viewer.RightArrowChangeButton.show()
        self.DH.BLobj.groups["default"].addCondition(
            self.name_of_added_listwidget, condition_uuid
        )
        self.DH.BLobj.set_current_condition(
            self.name_of_added_listwidget
        )  # Assign current Condition since we are changing the Listwidget items
        if condition_name:
            self.DH.BLobj.groups["default"].conds[
                self.name_of_added_listwidget
            ].condition_name_set = True

        clicked_treatment_widget = self.get_treatment_widget_by_name(
            self.name_of_added_listwidget
        )
        self.switch_treatment_onchange(
            clicked_treatment_widget=clicked_treatment_widget
        )

        self.RNAi_list.setEnabled(True)
        # return treatment name
        return self.name_of_added_listwidget

    def CreateProject(self):
        """
        Creates an object from the current configuration of th enew project dialog settings
        """
        from celer_sight_ai import config, configHandle
        from celer_sight_ai.MultiChannellImports import global_vars

        # to make sure that the widgets are pused to the right
        self.MainWindow.set_right_side_frame_images_geometry()
        selected_buttons = [
            i for i in self.category_selection_grid.items if i.isChecked()
        ]

        selected_configs = [i.cfg for i in selected_buttons]
        # get selected button and store settings to config
        # iterate over all buttons

        config.experiment_config = selected_configs
        self.stackedWidget.setCurrentWidget(self.MainInterface)
        self.viewer.setFocus()
        logger.info("creating project")
        if config.global_params:
            del config.global_params
        config.global_params = global_vars()
        self.new_analysis_object.Record_To_GlobalVars()
        config.global_params.hasBeenRecorded = False

        self.setUpAssaySettingsUi()
        config.global_signals.reCheckNeuralNets_magicBoxSignal.emit()
        config.client.download_assets()  # download any assets that need updating

    def run_test_suite(self):
        import subprocess

        from celer_sight_ai import config

        logger.info("Running test suite")
        config.client.download_test_fixtures()
        time.sleep(0.1)
        while config.client.downloading_test_fixtures:
            time.sleep(0.03)
            QtWidgets.QApplication.processEvents()
        # close the app and restart it with the --run-tests-short flag
        logger.info("Restarting the application to run tests")
        if config.is_executable:
            if sys.platform.startswith("win"):
                # get the exe path, which is on the parent path
                celer_sight_executable = os.path.join(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    ),
                    "Celer Sight AI.exe",
                )
                logger.info(
                    f"Starting new instance of the application: {celer_sight_executable}"
                )
                # Start a new instance of the current application
                subprocess.Popen([celer_sight_executable, "--run-tests-short"])
            else:
                raise NotImplementedError("Not implemented for this platform")
        else:
            celer_sight_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "Celer Sight AI.py"
            )
            # Start a new instance of the current application
            if not sys.platform.startswith("win"):
                # CREATE_NEW_CONSOLE not available on non windows
                subprocess.Popen([sys.executable, celer_sight_path], shell=True)
            else:
                subprocess.Popen(
                    [sys.executable, celer_sight_path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
        # Close the current instance
        sys.exit()

    def setUpAssaySettingsUi(self):
        # assign appropriate buttons and labels to analysis settings groupbox

        gl = config.global_params
        self.new_analysis_object
        if gl.analysis == self.new_analysis_object.analysis_map["mean_intensity"]:
            self.pg1_Analysis_a_label.setText("Intenisty")
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/meanIntensityAnalysis.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Analysis_btn.setIcon(icon)
            self.pg1_Analysis_btn.setIconSize(QtCore.QSize(30, 30))

        if gl.analysis == self.new_analysis_object.analysis_map["fragmentation"]:
            self.pg1_Analysis_a_label.setText("Fragmentation")
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/fragmentAnalysis.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Analysis_btn.setIcon(icon)
            self.pg1_Analysis_btn.setIconSize(QtCore.QSize(30, 30))

        if gl.analysis == self.new_analysis_object.analysis_map["particles"]:
            self.pg1_Analysis_a_label.setText("Particles")
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/particlesAnalysis.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Analysis_btn.setIcon(icon)
            self.pg1_Analysis_btn.setIconSize(QtCore.QSize(30, 30))
        if gl.analysis == self.new_analysis_object.analysis_map["colocalization"]:
            self.pg1_Analysis_a_label.setText("Colocalization")
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/colocalizationAnalysis.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Analysis_btn.setIcon(icon)
            self.pg1_Analysis_btn.setIconSize(QtCore.QSize(30, 30))
        if config.supercategory == "worm":
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/elegans_entity.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Entity_btn.setIcon(icon)
            self.pg1_Entity_btn.setIconSize(QtCore.QSize(50, 50))
        if config.supercategory == "cell":
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/cells_entity.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Entity_btn.setIcon(icon)
            self.pg1_Entity_btn.setIconSize(QtCore.QSize(50, 50))
        if config.supercategory == "tissue":
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("data/icons/tissue_entity.png"),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )
            self.pg1_Entity_btn.setIcon(icon)
            self.pg1_Entity_btn.setIconSize(QtCore.QSize(50, 50))

    def start_single_button_inference_loading(self, image_uuid):
        image_object = self.DH.BLobj.get_image_object_by_uuid(image_uuid)
        if image_object:
            image_object.myButton.button_instance.startInferenceAnimation()

    def assign_color_to_current_class(
        self,
    ):
        """
        This functions opens a color picker and assigns the button of interest the selected color
        """
        color = QtWidgets.QColorDialog.getColor()
        fg = color.name()  # Get hex
        self.pg1_settings_all_masks_color_button.setStyleSheet(
            "background-color:" + str(fg) + ";"
        )

        opSliderVal = self.pg1_settings_mask_opasity_slider.value()
        rgbVal = list(color.getRgb())
        rgbVal[3] = opSliderVal
        self.custom_class_list_widget.classes[
            self.custom_class_list_widget.currentItemWidget().unique_id
        ].set_color(rgbVal)

    def AssignColorDialogToButton(self, button, comboboxItem=None, index=None):
        """
        This functions opens a color picker and assigns the button of interest the selected color
        """
        color = QtWidgets.QColorDialog.getColor()
        fg = color.name()  # Get hex
        button.setStyleSheet("background-color:" + str(fg) + ";")
        if comboboxItem != None:
            comboboxItem.setItemData(index, color, QtCore.Qt.BackgroundRole)

    def GetPointsFromQPolygonF(self, polygonF):
        """
        Generates an (N,2) shaped array from a QPolygonF where N is the number of polygons
        """
        import numpy as np

        Startinglist = []
        for Point in polygonF:
            Startinglist.append([Point.y(), Point.x()])
        return np.asarray(Startinglist)

    def launch_dialog_to_send_for_training(self):
        """
        Launch window  to propt user for spefics regarding sending the images to the server for training
        The user is prompted to select if the images are partly or fully annotated.
        """
        from celer_sight_ai.gui.custom_widgets.contribute_images_widget import (
            ContributeImagesWidget,
        )

        # if there are not images, raise error
        if len([i for i in self.DH.BLobj.get_all_image_objects()]) == 0:
            config.global_signals.errorSignal.emit("No images to send for training")
            return
        if self.contribute_images_widget:
            self.contribute_images_widget.close()
            self.contribute_images_widget = None
        self.contribute_images_widget = ContributeImagesWidget(
            self, parent=self.MainInterface
        )
        self.contribute_images_widget.show()

    def loading_dialog_signal_update_progress_percentValue(self, value):
        self.MyLoadingAnimationDialogForm.progressBar.setValue(int(value))

    def ExportimagejROI(self, preset_dir=None):
        """
        Function that exports the masks in a imagejROI
        preset_dir : str path to the directory where the masks + images will be saved
        """

        import roifile
        from tifffile import imwrite

        ExportDict = {}
        if not preset_dir:
            my_dir = QtWidgets.QFileDialog.getExistingDirectory(
                None,
                "Select a folder:",
                os.path.expanduser("~"),
                QtWidgets.QFileDialog.Option.ShowDirsOnly,
            )
            my_dir = my_dir + "/"
        else:
            my_dir = preset_dir
        for treatment_name, treatment_object in self.DH.BLobj.groups[
            "default"
        ].conds.items():
            for image_object in treatment_object.images:

                for x in range(len(image_object.masks)):
                    AllCurrentPoints = image_object.masks[x].get_array()
                    for im, m in enumerate(AllCurrentPoints):
                        if im == 0:  # case of main annotation
                            preset = ""
                        else:
                            preset = "_HOLEID_" + str(im)

                        roi = roifile.ImagejRoi.frompoints(m)
                        out = roi.tobytes()
                        roi.tofile(
                            os.path.join(
                                my_dir,
                                "_"
                                + treatment_name
                                + "_"
                                + image_object.fileName.split(".")[0]
                                + "_"
                                + str(x + 1)
                                + preset
                                + ".roi",
                            )
                        )

    def coco_to_polygon(self, coco_annotation):
        # Unpack the list of coordinates into x, y pairs
        coords = [
            (coco_annotation[i], coco_annotation[i + 1])
            for i in range(0, len(coco_annotation), 2)
        ]
        return coords

    def is_continuous(self, nums):
        diffs = np.diff(nums)
        return np.all(diffs == diffs[0])

    def import_coco_tools(self):
        """
        Reads a coco annotation to the current project. The classes
        are added from the coco annotation file as is.
        The directory stracture needs to be as following:
        - root
            - annotations_cells.json
            - cells
            - annotations_cells2.json
            - cells2
            ...

        """
        import copy
        import json
        from glob import glob
        from itertools import groupby

        import skimage
        from tqdm import tqdm

        categories = []
        categories_set = False
        config.global_signals.lock_ui_signal.emit(["left_group", "image_viewer"])
        # scan for all possible json files
        my_dir = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Select a folder:",
            os.path.expanduser("~"),
            QtWidgets.QFileDialog.Option.ShowDirsOnly,
        )
        my_dir = my_dir + "/"
        annotation_files = glob(my_dir + "*.json")
        # for each annotation file, load all the images and annotations
        for annotation_file in annotation_files:
            # load json file
            with open(annotation_file) as f:
                annotation = json.load(f)

            root_dir = os.path.dirname(annotation_file)

            quick_categories = {}
            for i in annotation["categories"]:

                # check if the category exists, if not add it
                if i["name"] not in [
                    self.custom_class_list_widget.classes[i].text()
                    for i in self.custom_class_list_widget.classes
                ]:
                    # check to see if it exists in the categories section
                    class_uuid = (
                        self.custom_class_list_widget.get_class_uuid_by_class_name(
                            "cell"
                        )
                    )
                    if not class_uuid:
                        import uuid

                        # create a temp one
                        class_uuid = str(uuid.uuid4())
                        self.custom_class_list_widget.addClass(
                            class_name=i["name"],
                            class_uuid=class_uuid,
                            is_user_defined=True,
                        )
                else:
                    class_uuid = (
                        self.custom_class_list_widget.get_class_uuid_by_class_name(
                            i["name"]
                        )
                    )
                quick_categories[i["id"]] = {"name": i["name"], "uuid": class_uuid}

            # get the name of the annotation
            annotation_name = (
                os.path.basename(annotation_file)
                .replace("annotations_", "")
                .replace(".json", "")
            )
            self.add_new_treatment_item(annotation_name)
            images_urls = [
                os.path.join(root_dir, annotation_name, i["file_name"])
                for i in sorted(annotation["images"], key=lambda k: k["id"])
            ]  # glob(os.path.join(my_dir, annotation_name, "*.png"))
            # order the annotations by image id
            anno = sorted(annotation["annotations"], key=lambda k: k["image_id"])
            # group all annotation of the same image into one list
            # import groupby
            anno = [list(g) for k, g in groupby(anno, key=lambda x: x["image_id"])]
            # get total images range
            image_range = range(1, len(images_urls) + 1)
            if not self.is_continuous(image_range):
                logger.error("Corrupted COCO file : Image range is not continuous")
                continue
            image_ids = [i["id"] for i in annotation["images"]]
            image_ids_annotation = list(
                set([i["image_id"] for i in annotation["annotations"]])
            )
            # sort from smallest to largest
            image_ids = sorted(image_ids)
            anno_out = []

            for i, a in enumerate(anno):  # --> starts from 1
                if len(a) > 0:
                    img_id_in_annotation = a[0]["image_id"]
                    try:
                        anno_out.append(
                            [
                                {
                                    "polygon": [
                                        self.coco_to_polygon(x)
                                        for x in a["segmentation"]
                                    ],
                                    "class": quick_categories[a["category_id"]]["uuid"],
                                }
                                for a in anno[i]
                            ]
                        )
                    except Exception:
                        print()

            self.myButtonHandler.SetUpButtons(
                annotation_name,
                self,
                imagesUrls=images_urls,
                all_annotations=anno_out,
            )
            # wait until self.pg_2_widget_graph_visualizer_3 is enabled --> this is when the setupbuttons function is complete
            time.sleep(0.1)
            while not self.pg_2_widget_graph_visualizer_3.isEnabled():
                time.sleep(0.1)
                QtWidgets.QApplication.processEvents()

    def ExportCOCOTools(self):
        """
        Function that exports the masks in a json COCO format
        """
        import copy
        import json

        import skimage
        from shapely.geometry import Polygon
        from tqdm import tqdm

        all_categories = []

        license_template = {
            "url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "id": 1,
            "name": "Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)",
        }
        category_template = {"supercategory": "none", "id": 1, "name": "my_polygon"}

        annotation_template = {
            "segmentation": [[]],  #  [x1, y1, x2, y2, ...]
            "area": 5000,  # You should compute this accurately
            "iscrowd": 0,
            "image_id": 1,
            "bbox": [50, 50, 50, 50],  # You should compute this accurately
            "category_id": 1,  # class id
            "id": 1,  # annotation id (total)
        }
        image_template = {
            "license": 1,
            "file_name": "filepath",
            "height": 1280,
            "width": 1280,
            "id": 1,
        }
        current_class_ids = [
            self.custom_class_list_widget.getItemWidget(i).text()
            for i in range(self.custom_class_list_widget.count())
        ]
        categories = []
        for i, class_name in enumerate(current_class_ids):
            category_template = {
                "supercategory": config.supercategory,
                "id": i + 1,
                "name": class_name,
            }
            categories.append(category_template)
            dict_match = {class_name: i + 1}

        my_dir = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Select a folder:",
            os.path.expanduser("~"),
            QtWidgets.QFileDialog.Option.ShowDirsOnly,
        )

        # # create a category for every class
        # for class_name in self.DH.BLobj.classes:
        all_image_names = []
        for group_name in self.DH.BLobj.groups:
            for cond_name in tqdm(self.DH.BLobj.groups[group_name].conds):
                total_image_id = 1
                total_annotation_id = 1
                ExportDict = {}
                all_images = []
                all_annotations = []
                # replace space with underscore
                cond_name_space = cond_name.replace(" ", "_")
                # create a folder with the cond_name
                os.mkdir(os.path.join(my_dir, cond_name_space))
                image_dest_location = os.path.join(my_dir, cond_name_space)
                for i_im, image_obj in enumerate(
                    self.DH.BLobj.groups[group_name].conds[cond_name].images
                ):
                    if isinstance(image_obj, type(None)):
                        continue
                    # Convert the polygons to Bit mask and append everything to COmbined MAsk LIst:
                    for mask_obj in image_obj.masks:
                        polygon_array = mask_obj.polygon_array
                        coco_points_array = []
                        all_areas = []
                        total_area = 0
                        for im, m in enumerate(
                            polygon_array
                        ):  # iterate to handle main polygon and holes
                            coco_points_array_tmp = []
                            try:
                                pgon = Polygon(m)
                            except Exception as e:
                                print(e)
                                print("Skipping this polygon")
                                continue
                            if im == 0:
                                # get area of main polygon
                                total_area = pgon.area
                                # get bounding box
                                x, y, max_x, max_y = pgon.bounds
                            else:
                                # get area of the hole
                                total_area = total_area - pgon.area
                            for mm in m:
                                coco_points_array_tmp.append(int(mm[0]))
                                coco_points_array_tmp.append(int(mm[1]))
                            coco_points_array.append(coco_points_array_tmp)
                        annotation_dict = copy.deepcopy(annotation_template)
                        annotation_dict["segmentation"] = coco_points_array
                        # compute area after removing holes
                        # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
                        annotation_dict["area"] = int(total_area)
                        annotation_dict["iscrowd"] = 0
                        annotation_dict["image_id"] = int(total_image_id)
                        annotation_dict["bbox"] = [
                            int(x),
                            int(y),
                            int(float(max_x) - float(x)),
                            int(float(max_y) - float(y)),
                        ]
                        annotation_dict["category_id"] = dict_match[
                            mask_obj.class_id
                        ]  # class id
                        all_annotations.append(annotation_dict)
                        total_annotation_id += 1
                    image_dict = copy.deepcopy(image_template)
                    image_dict["license"] = 1
                    # read image
                    image = (
                        self.DH.BLobj.groups[group_name]
                        .conds[cond_name]
                        .getImage(i_im, to_uint8=True, to_rgb=True)
                    )
                    # make sure filename is unique:
                    if image_obj.fileName in all_image_names:
                        output_name = (
                            image_obj.fileName.split(".")[0]
                            + "_"
                            + str(i_im)
                            + "."
                            + "png"
                        )
                    else:
                        output_name = (
                            ".".join(image_obj.fileName.split(".")[:-1]) + "." + "png"
                        )
                    all_image_names.append(output_name)
                    # rgb to bgr
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    # save image to destination
                    cv2.imwrite(os.path.join(image_dest_location, output_name), image)
                    image_dict["file_name"] = output_name
                    if isinstance(image_obj.SizeY, type(None)):
                        image_dict["height"] = int(image.shape[0])
                    else:
                        image_dict["height"] = int(image_obj.SizeY)
                    if isinstance(image_obj.SizeX, type(None)):
                        image_dict["width"] = int(image.shape[1])
                    else:
                        image_dict["width"] = int(image_obj.SizeX)
                    image_dict["id"] = int(total_image_id)
                    all_images.append(image_dict)
                    total_image_id += 1
                ExportDict["images"] = all_images
                ExportDict["annotations"] = all_annotations
                # add licenses
                ExportDict["licenses"] = [license_template]
                ExportDict["categories"] = categories
                # write to .json file
                with open(
                    os.path.join(my_dir, f"annotations_{cond_name_space}.json"), "w"
                ) as f:
                    json.dump(ExportDict, f)
        print("Complete")

    def AppendToTextEditor(self, Text):
        return

    def ClearPlots(self):
        """
        Clear all of the plot instances that need to be updated
        """
        pass

    def AddNewPlot(self):
        """
        Adding an item to the list of all items names, the Qwidgetlist list
        and to our dictionary,names are all the generated from MyVisualPlotHandler.CheckDictionaryName
        """
        CurrentItem = str(self.pg2_graph_type_comboBox.currentText())
        CurrentItem = self.MyVisualPlotHandler.CheckDictionaryName(
            CurrentItem, self.MyVisualPlotHandler.WidgetDictionary
        )  # checking for repeated string name
        self.MyVisualPlotHandler.CurrentWidget = str(CurrentItem)
        self.MyVisualPlotHandler.WidgetDictionary[CurrentItem] = (
            self.MyVisualPlotHandler.DeterminePlotClass(
                str(self.pg2_graph_type_comboBox.currentText()), CurrentItem
            )
        )
        self.pg2_graphs_view.addItem(CurrentItem)
        self.pg2_graphs_view.setCurrentRow(0)
        self.setUpSpecificPlotWidget(CurrentItem)
        color_list = self.MyVisualPlotHandler.getInitSnsPallete()

        # add the PlotWidgets for current plot

    def collectImagesFromFolder(self, folder):
        import os

        # This method needs to be deprecated
        iterator = 0
        path = folder
        AllImages = []
        resizedImages = []
        sappliedNames = []
        from skimage.transform import resize

        ReduceBy = 3  # the ammount that we will divide the image resolution

        text_files = [
            f
            for f in os.listdir(path)
            if f.endswith(
                tuple(
                    [
                        ".png",
                        ".PNG",
                        ".jpg",
                        ".jpeg",
                        ".JPG",
                        ".JPEG",
                        ".bmp",
                        "BMP",
                        ".tif",
                        ".tiff",
                        ".TIF",
                    ]
                )
            )
        ]
        if len(text_files) == 0:
            return None, None, None, None
        for myfile in text_files:
            iterator += 1
            image1, result_dict = readImage(os.path.join(folder, myfile))
            channel_list = result_dict.get("channels", None)
            # if not isinstance(image1, (np.ndarray, np.generic)):
            #     continue
            # if image1.shape[0] >= 2000 or image1.shape[1] > 2000:
            #     text_files.pop(iterator - 1)
            #     continue
            # image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            AllImages.append([image1, channel_list])
            ResizedImage = resize(
                image1,
                (image1.shape[0] // ReduceBy, image1.shape[1] // ReduceBy),
                anti_aliasing=False,
                preserve_range=True,
            )
            resizedImages.append(ResizedImage)
            sappliedNames.append(os.path.join(folder, myfile))
        for i in range(len(text_files)):
            text_files[i] = os.path.basename(text_files[i])
        return AllImages, resizedImages, sappliedNames, text_files

    def OpenFolderTree(self):
        """
        When the user wants to open multiple conditions (subfolders in a folder)
        """
        import os

        my_dir = self.open_folder_explorer(MODE="FOLDER")
        # if not my_dir:
        #     return
        # if len(my_dir) == 0 :
        #     return
        # if len(my_dir) == 1:

        my_dir = self.fast_scandir(my_dir)
        self.setCurrentImageNumber(0)
        subfolders = my_dir
        for ConditionDirectory in subfolders:
            (
                AllImages,
                resizedImages,
                sappliedNames,
                filesList,
            ) = self.collectImagesFromFolder(ConditionDirectory)
            if not AllImages:
                continue
            (
                AllImages,
                resizedImages,
                sappliedNames,
                filesList,
            ) = self.excludeExactSameImages(
                AllImages, resizedImages, sappliedNames, filesList
            )
            self.name_of_added_listwidget = os.path.basename(ConditionDirectory)
            if AllImages == None or len(AllImages) == 0:
                continue
            else:
                raise NotImplementedError("OnImportChannelPicker was here")
                self.OnImportChannelPicker(
                    AllImages, resizedImages, None, sappliedNames
                )

            self.load_main_scene(0)
        self.MyInferenceHandler.onJobComplete("Finished importing tree!")
        return

    def excludeExactSameImages(
        self, AllImages, resizedImages, sappliedNames, filesList, removeBlack=True
    ):
        """
        checks if the resized images are exactly the same, if so it discards one
        """
        popList = []
        iterNum = 1
        for x in range(len(resizedImages)):
            for y in range(len(resizedImages) - iterNum):
                if np.array_equal(resizedImages[x], resizedImages[y + iterNum]):
                    popList.append(y + iterNum)
            iterNum += 1

        for i in reversed(range(len(resizedImages))):
            if i in popList:
                resizedImages.pop(i)
                AllImages.pop(i)
                sappliedNames.pop(i)
                filesList.pop(i)
        if removeBlack == True:
            for i in reversed(range(len(resizedImages))):
                if not np.any(resizedImages[i]):
                    resizedImages.pop(i)
                    AllImages.pop(i)
                    sappliedNames.pop(i)
                    filesList.pop(i)
        return AllImages, resizedImages, sappliedNames, filesList

    def fast_scandir(self, dirname):
        """
        Scans for subfolders
        """
        subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
        return subfolders

    def polygon_add_remove_selection(self, pos, mask, operation="add"):
        """

        an operation to add or remove to a mask with a polygon.
        """
        pass

    def Ui_control(self, lock_wdigets=True):
        """
        control mechanism to block and enable widgets
        """

        for widget in self.children():
            if lock_wdigets == True:
                if widget != self.viewer:
                    try:
                        widget.setEnabled(False)
                    except:
                        pass

            elif lock_wdigets == False:
                if widget != self.viewer:
                    try:
                        widget.setEnabled(True)
                    except:
                        pass
        return

    def lock_ui(self, lock_elements=["left_group", "image_viewer"]):
        # locks all widgets
        elements_mapping = {
            "workflow": self.frame_group_pg1_left_container_top,
            "left_group": self.group_pg1_left,
            "image_viewer": self.pg_2_widget_graph_visualizer_3,
            "treatment_image_buttons": self.images_preview_graphicsview,
            "get_roi_ai_button": self.get_roi_ai_button,
            "initialize_analysis_button": self.initialize_analysis_button,
            "condition_buttons": [
                self.addRNAi_button_list,
                self.delete_button_list,
                self.up_button_list,
                self.down_button_list,
            ],
            "classes": self.custom_class_list_widget,
            "interactive_tools": self.buttonToolList,
        }
        # What happens when we lock the ui twice? --> we need to keep track of the locked elements with extend()
        self._locked_ui_elements.extend([elements_mapping[i] for i in lock_elements])
        for element in self._locked_ui_elements:
            if isinstance(element, list):
                for e in element:
                    e.setEnabled(False)
            else:
                element.setEnabled(False)

    def unlock_ui(self):
        # locks all widgets
        for element in self._locked_ui_elements:
            if isinstance(element, list):
                for e in element:
                    e.setEnabled(True)
            else:
                element.setEnabled(True)
        self._locked_ui_elements = []

    def write_image_file(
        self, filename: str, images: list, thumbnail, metadata: dict, data_dict: dict
    ):
        import json
        import struct

        with open(filename, "wb") as f:
            # Write Header Metadata
            metadata_json = json.dumps(metadata).encode("utf-8")
            f.write(struct.pack("I", len(metadata_json)))
            f.write(metadata_json)

            # Write Dictionary Data
            dict_bytes = json.dumps(data_dict).encode("utf-8")
            f.write(struct.pack("I", len(dict_bytes)))
            f.write(dict_bytes)

            # Write Thumbnail
            thumbnail_bytes = thumbnail.tobytes()
            f.write(struct.pack("I", len(thumbnail_bytes)))
            f.write(thumbnail_bytes)

            # Write Number of Images
            f.write(struct.pack("I", len(images)))

            # Write Metadata and Individual Images
            for img in images:
                img_data = img.tobytes()

                # Write metadata
                f.write(struct.pack("I", img.width))
                f.write(struct.pack("I", img.height))
                f.write(struct.pack("I", len(img.getbands())))

                # Write image data
                f.write(struct.pack("I", len(img_data)))
                f.write(img_data)

    # def gather_data_for_celer_sight_image(self):
    #     return images, thumbnail, metadata, data_dict

    def numpy_to_python(self, data):
        if isinstance(data, np.ndarray):
            return self.numpy_to_python(data.tolist())
        elif isinstance(data, list):
            return [self.numpy_to_python(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(self.numpy_to_python(list(data)))
        elif isinstance(data, dict):
            return {key: self.numpy_to_python(value) for key, value in data.items()}
        elif isinstance(data, (int, float)):
            return data
        elif isinstance(data, str):
            return data
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")

    def handle_bytes(self, obj):
        import base64

        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode()
        raise TypeError("Object not serializable")

    def is_json_serializable(self, obj, parent_key=""):
        """
        Checks if a Python dictionary can be serialized into a JSON string.
        :param obj: The Python dictionary (or nested object) to check.
        :param parent_key: Used for nested dictionaries to show where the serialization fails.
        :return: True if the object is serializable, False otherwise.
        """

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                if not self.is_json_serializable(value, new_key):
                    return False
            return True

        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                new_key = f"{parent_key}[{i}]" if parent_key else f"[{i}]"
                if not self.is_json_serializable(value, new_key):
                    return False
            return True

        elif isinstance(obj, (str, int, float, bool, type(None))):
            return True

        else:
            print(
                f"The object at '{parent_key}' is not JSON serializable. It is of type {type(obj).__name__}."
            )
            return False

    def serialize_object(self, obj):
        if isinstance(obj, np.ndarray):
            # Convert numpy arrays to list
            return obj.tolist()
        # elif isinstance(obj, np.generic):
        #     # Convert numpy scalar types to native Python types
        #     return np.ndarray.item(obj)
        elif isinstance(obj, dict):
            # Recursive serialization for dictionary items
            return {key: self.serialize_object(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            # Recursive serialization for list or tuple items
            return [self.serialize_object(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool)):
            # Return the object as is if it is a basic data type
            return obj
        elif isinstance(obj, type(None)):
            return None
        else:
            # Convert any other type to string
            return str(obj)

    def save_celer_sight_file_decider(self):
        if config.CURRENT_SAVE_FILE:
            self.save_celer_sight_file(filename=config.CURRENT_SAVE_FILE)
        else:
            self.save_celer_sight_file()

    def save_celer_sight_file(self, filename=None):
        """
        Runs to save the plaba file (save as)
        """
        import base64
        import json
        import struct

        import zstandard as zstd
        from PIL import Image

        from celer_sight_ai import config

        # open a file save dialog
        if not filename:
            # check on qsettings, if there is a previous location saved, use that

            last_save = ""
            if config.settings.value("last_save_location"):
                last_save = config.settings.value("last_save_location")
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File as", last_save, "BMI Celer Sight File (*.bmics)"
            )
            # save the location of the parent dir
            config.settings.setValue("last_save_location", os.path.dirname(filename))
        if not filename:
            return
        try:
            image_arrays = []
            image_paths = []
            # with dialog get save location
            # filename = ...
            data_dict = {}
            # Get all classes
            all_classes_widgets = [
                self.custom_class_list_widget.getItemWidget(i)
                for i in range(self.custom_class_list_widget.count())
            ]
            data_dict["classes"] = []
            # calculate overall progress
            tot_images = 0
            for gk in self.DH.BLobj.groups:
                go = self.DH.BLobj.groups[gk]
                for ck in go.conds:
                    co = go.conds[ck]
                    for io in co.images:
                        tot_images += 1
            config.global_signals.start_progress_bar_signal.emit(
                {
                    "title": "Saving file...",
                    "window_title": "Saving in Progress",
                    "main_text": "",
                }
            )
            QtWidgets.QApplication.processEvents()
            iii = 0
            for cw in all_classes_widgets:
                cls_item = {}
                cls_item["name"] = cw.class_label.text()
                cls_item["unique_id"] = cw.unique_id
                cls_item["parent_class_uuid"] = cw.parent_class_uuid
                cls_item["is_particle"] = cw.is_particle
                cls_item["_is_class_visible"] = cw._is_class_visible
                cls_item["is_user_defined"] = cw.is_user_defined
                cls_item["color"] = cw.color
                data_dict["classes"].append(cls_item)

            # for every class widget, create an entry in classes
            # get all groups into metadata
            group_objects = []
            for gk in self.DH.BLobj.groups:
                group_item = {}
                go = self.DH.BLobj.groups[gk]
                group_item["groupName"] = gk
                group_item["unique_id"] = go.unique_id
                condition_objects = []
                for ck in go.conds:
                    condition_object = {}
                    co = go.conds[ck]
                    condition_object["condition_name"] = ck
                    condition_object["groupName"] = gk
                    condition_object["condition_name_set"] = co.condition_name_set
                    condition_object["unique_id"] = co.unique_id
                    image_objects = []
                    for io in co.images:  # id, not key.
                        out_image_object = {}
                        # full image path
                        complete_file_path = os.path.join(
                            str(io.fileRootFolder), io.fileName
                        )
                        image_paths.append(complete_file_path)
                        # if the image is remote, raise error and abort
                        if io.is_remote():
                            config.global_signals.errorSignal(
                                "Session contains remote images and can not be saved."
                            )
                        out_image_object["unique_id"] = io.unique_id
                        # get all relevant
                        # attributes for the image
                        out_image_object["AcquisitionDate"] = io.AcquisitionDate
                        out_image_object["DimensionOrder"] = io.DimensionOrder
                        out_image_object["ExperiementName"] = io.ExperiementName
                        out_image_object["ExposureTime"] = io.ExposureTime
                        out_image_object["ExposureTimeUnit"] = io.ExposureTimeUnit
                        out_image_object["ID"] = io.ID
                        out_image_object["_is_video"] = io._is_video
                        out_image_object["_is_ultra_high_res"] = io._is_ultra_high_res
                        out_image_object["PhotometricInterpretation"] = (
                            io.PhotometricInterpretation
                        )
                        out_image_object["PhysicalSizeX"] = io.PhysicalSizeX
                        out_image_object["PhysicalSizeXUnit"] = io.PhysicalSizeXUnit
                        out_image_object["PhysicalSizeY"] = io.PhysicalSizeY
                        out_image_object["PhysicalSizeYUnit"] = io.PhysicalSizeYUnit
                        out_image_object["SignificantBits"] = io.SignificantBits
                        out_image_object["SizeC"] = io.SizeC
                        out_image_object["SizeT"] = io.SizeT
                        out_image_object["SizeX"] = io.SizeX
                        out_image_object["SizeY"] = io.SizeY
                        out_image_object["SizeZ"] = io.SizeZ
                        out_image_object["Software"] = io.Software
                        out_image_object["bitDepth"] = io.bitDepth

                        out_image_object["channel_list"] = io.channel_list
                        out_image_object["computedInference"] = io.computedInference
                        out_image_object["treatment_uuid"] = io.treatment_uuid
                        out_image_object["fileName"] = str(io.fileName)
                        out_image_object["fileRootFolder"] = str(io.fileRootFolder)
                        out_image_object["group_uuid"] = io.group_uuid
                        out_image_object["hasBeenUploaded"] = io.hasBeenUploaded
                        out_image_object["imgID"] = io.imgID
                        out_image_object["is_stack"] = io.is_stack
                        # Get all current image objects
                        mask_objects = []
                        for mo in io.masks:
                            mask_object = {}
                            mask_object["class_id"] = mo.class_id
                            mask_object["class_group_id"] = mo.class_group_id
                            mask_object["spatial_id"] = mo.spatial_id
                            mask_object["score"] = mo.score
                            mask_object["image_uuid"] = mo.image_uuid
                            mask_object["includedInAnalysis"] = mo.includedInAnalysis
                            mask_object["mask_type"] = mo.mask_type
                            mask_object["is_suggested"] = mo.is_suggested
                            mask_object["_annotation_track_id"] = (
                                mo._annotation_track_id
                            )
                            mask_object["intensity_metrics"] = mo.intensity_metrics
                            if hasattr(mo, "particle_metrics"):
                                mask_object["particle_metrics"] = mo.particle_metrics
                            if hasattr(mo, "polygon_array"):
                                mask_object["polygon_array"] = []
                                arr = mo.get_array_for_storing()
                                arr = self.numpy_to_python(arr)
                                mask_object["polygon_array"].append(arr)
                            mask_object["unique_id"] = mo.unique_id
                            mask_object["visibility"] = mo.visibility
                            mask_objects.append(mask_object)
                        out_image_object["mask_objects"] = mask_objects
                        out_image_object["raw_image_extrema_set"] = (
                            io.raw_image_extrema_set
                        )
                        out_image_object["raw_image_max_value"] = io.raw_image_max_value
                        out_image_object["raw_image_min_value"] = io.raw_image_min_value
                        out_image_object["resolution"] = io.resolution
                        out_image_object["resolutionunit"] = io.resolutionunit
                        try:
                            out_image_object["thumbnail"] = io.thumbnail.hex()
                        except:
                            # in case an error is raised for the thumbnail, just set to none
                            # because it will get regenerated again when the file is loaded again
                            pass

                        out_image_object["_during_inference"] = io._during_inference
                        out_image_object["userModifiedAnnotation"] = (
                            io.userModifiedAnnotation
                        )
                        out_image_object["thumbnailGenerated"] = io.thumbnailGenerated
                        image_objects.append(out_image_object)
                        config.global_signals.update_progress_bar_progress_signal.emit(
                            {"percent": int((iii / tot_images) * 100)}
                        )
                        iii += 1

                        QtWidgets.QApplication.processEvents()
                    condition_object["image_objects"] = image_objects
                    condition_objects.append(condition_object)
                group_item["condition_objects"] = condition_objects
                group_objects.append(group_item)
            data_dict["grouped_data"] = group_objects
            config.global_signals.complete_progress_bar_signal.emit()
            from datetime import datetime

            data_dict = self.serialize_object(data_dict)
            now = datetime.now()
            metadata = {
                "version": "2",
                "user": config.user_attributes.username,
                "date": now.strftime("%B %d, %Y"),
            }
            with open(filename, "wb") as f:
                # Write Header Metadata
                metadata_json = json.dumps(metadata).encode("utf-8")
                f.write(struct.pack("I", len(metadata_json)))
                f.write(metadata_json)

                # record experiment settings
                analysis_type = None
                if (
                    config.global_params.analysis
                    == self.new_analysis_object.analysis_map["mean_intensity"]
                ):
                    analysis_type = "intensity"
                elif (
                    config.global_params.analysis
                    == self.new_analysis_object.analysis_map["particles"]
                ):
                    analysis_type = "particles"

                exp_settings = {
                    "supercategory": config.supercategory,
                    "analysis": analysis_type,
                }
                exp_settings = json.dumps(exp_settings).encode("utf-8")
                f.write(struct.pack("I", len(exp_settings)))
                f.write(exp_settings)

                # Write Dictionary Data
                dict_bytes = json.dumps(data_dict, default=self.handle_bytes).encode(
                    "utf-8"
                )
                f.write(struct.pack("I", len(dict_bytes)))
                f.write(dict_bytes)

                # # Write Thumbnail
                # thumbnail_bytes = out_image_object["thumbnail"]
                # f.write(struct.pack("I", len(thumbnail_bytes)))
                # f.write(thumbnail_bytes)
                # Write Number of Images
                f.write(struct.pack("I", len(image_paths)))
                cctx = zstd.ZstdCompressor()
                # Write Metadata and Individual Images
                for img_path in image_paths:
                    # Read and compress the image data
                    with open(img_path, "rb") as img_file:
                        image_data = img_file.read()
                        compressed_data = cctx.compress(image_data)
                    # get the size of the compressed data, if data is larger than 4GB use "Q" otherwise "I"
                    compressed_data_size = len(compressed_data)
                    if compressed_data_size > 4294967295:
                        # write stract type
                        mode = "Q"
                        struct.write(struct.pack("B", mode))
                        struct.write(struct.pack(mode, compressed_data_size))
                    else:
                        mode = "I"
                        f.write(struct.pack("c", mode.encode("utf-8")))
                        f.write(struct.pack(mode, compressed_data_size))

                    # Write the compressed image data
                    f.write(compressed_data)

            config.CURRENT_SAVE_FILE = filename
            config.global_signals.successSignal.emit("Saved successfully.")
            QtWidgets.QApplication.processEvents()
            return group_objects, filename
        except Exception as e:
            logger.error(e)
            config.global_signals.fatalErrorSignal.emit("Failed to save file")
            config.global_signals.complete_progress_bar_signal.emit()
            # remove the file if it was created
            if os.path.exists(filename):
                os.remove(filename)

    def get_array_from_storage(self, arr):
        from pycocotools import mask as coco_mask

        if isinstance(arr, dict):
            # Convert hex string to bytes and ensure correct RLE format
            rle = {
                "counts": bytes.fromhex(arr["counts"]),
                "size": tuple(arr["size"]),  # Convert to tuple for RLE format
            }
            return coco_mask.decode(rle)
        else:
            return arr

    def store_locomotion_data(self, file_location=None):

        # get file save location from user if not supplied
        if not file_location:
            file_location, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save csv", "", "CSV Files (*.csv)"
            )
        if not file_location:
            return
        # get all data
        self.MyInferenceHandler.track_all_masks_by_treatment(file_location)
        return

    def load_celer_sight_file(self, file_location=None):
        import base64
        import json
        import shutil
        import struct
        import uuid

        import zstandard as zstd
        from PIL import Image

        from celer_sight_ai import configHandle

        dctx = zstd.ZstdDecompressor()
        # open a file dialog
        if not file_location:
            # check on qsettings, if there is a previous location saved, use that

            last_save = ""
            if config.settings.value("last_save_location"):
                last_save = config.settings.value("last_save_location")
            file_location, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Select a Celer Sight file",
                last_save,
                "BMI Celer Sight File (*.bmics)",
            )
            # save the location of the parent dir
            config.settings.setValue(
                "last_save_location", os.path.dirname(file_location)
            )
        if not file_location:
            return
        if not os.path.exists(file_location):
            return
        prior_location = self.stackedWidget.currentWidget()
        if prior_location != self.MainInterface:
            # go to mainwindow
            self.create_new_enviroment_with_category()
            self.MainWindow.move_top_level_mainwindow_edge_widgets_to_position()
        try:
            # if we are at the supercategory selection page, move to main page
            self.stackedWidget.setCurrentWidget(self.MainInterface)
            # remove all classes
            self.custom_class_list_widget.delete_all_classes()

            # remove all
            self.DH.BLobj.delete_all_groups()

            from datetime import datetime

            now = datetime.now()
            # Format it into a string suitable for a folder name
            folder_name = now.strftime("%Y_%m_%d_%H_%M_%S")
            # get the local dir

            with open(file_location, "rb") as f:
                # Read metadata
                metadata_length = struct.unpack("I", f.read(4))[0]
                metadata = json.loads(f.read(metadata_length).decode("utf-8"))

                # if metadata["version"] == "2":, also read experiment settings
                if metadata["version"] == "2":
                    exp_settings_length = struct.unpack("I", f.read(4))[0]
                    exp_settings = json.loads(
                        f.read(exp_settings_length).decode("utf-8")
                    )
                    config.supercategory = exp_settings["supercategory"]
                    if exp_settings["analysis"] == "intensity":
                        config.global_params.analysis = (
                            self.new_analysis_object.analysis_map["mean_intensity"]
                        )
                    elif exp_settings["analysis"] == "particles":
                        config.global_params.analysis = (
                            self.new_analysis_object.analysis_map["particles"]
                        )

                # Read dictionary data
                dict_length = struct.unpack("I", f.read(4))[0]
                data_dict = json.loads(f.read(dict_length).decode("utf-8"))

                # # Skip thumbnail
                # thumbnail_length = struct.unpack("I", f.read(4))[0]
                # f.seek(thumbnail_length, 1)

                # # read thumbnails
                # thumbnails = f.read(thumbnail_length)

                # Read the number of images
                num_images = struct.unpack("I", f.read(4))[0]

                images = []

                # create classes
                for c in data_dict["classes"]:
                    # add single class first
                    self.custom_class_list_widget.addClass(
                        c["name"],
                        parent_class_uuid=c["parent_class_uuid"],
                        class_uuid=c["unique_id"],
                        is_user_defined=c["is_user_defined"],
                        color=tuple(c.get("color")),
                        is_particle=c["is_particle"],
                    )
                    # get that class item and patch it
                    class_item = self.custom_class_list_widget.getItemWidget(
                        self.custom_class_list_widget.count() - 1
                    )
                    class_item.is_particle = c["is_particle"]
                    class_item._is_class_visible = c["_is_class_visible"]
                    class_item.is_user_defined = c["is_user_defined"]
                    # TODO: patch extra variables manually

                # add groups (if not exists)
                for g in data_dict["grouped_data"]:
                    if not self.DH.BLobj.groups.get(g["groupName"]):
                        self.DH.BLobj.addGroup(g["groupName"], uuid=g.get("unique_id"))

                    for c in g["condition_objects"]:
                        if len(g["condition_objects"]) == 0:
                            continue
                        if not self.DH.BLobj.groups[g["groupName"]].conds.get(
                            c["condition_name"]
                        ):
                            self.add_new_treatment_item(
                                c["condition_name"], c.get("unique_id")
                            )
                        for i in c["image_objects"]:
                            # Read Metadata
                            # get strcut type
                            mode_type = struct.unpack("c", f.read(1))[0].decode("utf-8")
                            # Read Image Data
                            if mode_type == "I":
                                img_data_length = struct.unpack(mode_type, f.read(4))[0]
                            else:  # mode_type == "Q"
                                img_data_length = struct.unpack(mode_type, f.read(8))[0]

                            data_decompressed = dctx.decompress(f.read(img_data_length))
                            fileName = i["fileName"]
                            extension = fileName.split(".")[-1]
                            # generate a random name that does not exist so far
                            image_unique_id = i.get("unique_id")
                            if not image_unique_id:
                                image_unique_id = config.get_unique_id()
                            img_location = os.path.join(
                                config.cache_dir, image_unique_id
                            )
                            img_location = img_location + "." + extension
                            with open(img_location, "wb") as ff:
                                # write binary data_decompressed
                                ff.write(data_decompressed)
                            if "thumbnail" in i:
                                thumbnail = bytes.fromhex(i["thumbnail"])
                            else:
                                thumbnail = None

                            # add image
                            self.DH.BLobj.groups[g["groupName"]].conds[
                                c["condition_name"]
                            ].addImage_FROM_DISK(
                                imagePath=img_location,
                                group_uuid=g.get("unique_id"),
                                cond_uuid=c.get("unique_id"),
                                thumbnail=thumbnail,  # .encode("koi8_u"),
                                image_uuid=image_unique_id,
                            )
                            io = (
                                self.DH.BLobj.groups[g["groupName"]]
                                .conds[c["condition_name"]]
                                .images[i["imgID"]]
                            )
                            io.treatment_uuid = c.get("treatment_uuid")
                            io.group_uuid = g.get("group_uuid")
                            io._is_video = i.get("_is_video")
                            io._is_ultra_high_res = i.get("_is_ultra_high_res")
                            io.AcquisitionDate = i["AcquisitionDate"]
                            io.DimensionOrder = i["DimensionOrder"]
                            io.ExperiementName = i["ExperiementName"]
                            io.ExposureTime = i["ExposureTime"]
                            io.ExposureTimeUnit = i["ExposureTimeUnit"]
                            io.ID = i["ID"]
                            io.PhotometricInterpretation = i[
                                "PhotometricInterpretation"
                            ]
                            io.PhysicalSizeX = i["PhysicalSizeX"]
                            io.PhysicalSizeXUnit = i["PhysicalSizeXUnit"]
                            io.PhysicalSizeY = i["PhysicalSizeY"]
                            io.PhysicalSizeYUnit = i["PhysicalSizeYUnit"]
                            io.SignificantBits = i["SignificantBits"]
                            io.SizeC = i["SizeC"]
                            io.SizeT = i["SizeT"]
                            io.SizeX = i["SizeX"]
                            io.SizeY = i["SizeY"]
                            io.SizeZ = i["SizeZ"]
                            io.Software = i["Software"]
                            io.bitDepth = i["bitDepth"]

                            io.channel_list = i["channel_list"]
                            io.computedInference = i["computedInference"]

                            io.hasBeenUploaded = i["hasBeenUploaded"]
                            io.imgID = i["imgID"]
                            io.is_stack = i["is_stack"]
                            io.raw_image_extrema_set = i["raw_image_extrema_set"]
                            io.raw_image_max_value = i["raw_image_max_value"]
                            io.raw_image_min_value = i["raw_image_min_value"]
                            io.resolution = i["resolution"]
                            io.resolutionunit = i["resolutionunit"]
                            io._during_inference = i["_during_inference"]
                            io.userModifiedAnnotation = i["userModifiedAnnotation"]
                            io.thumbnailGenerated = i["thumbnailGenerated"]
                            # add masks
                            for m in i["mask_objects"]:
                                arr = m["polygon_array"]
                                if m["mask_type"] == "bitmap":
                                    arr = self.get_array_from_storage(arr)
                                else:
                                    # need to convert array within the list into numpy
                                    arr = [np.array(a) for a in arr[0]]
                                self.DH.BLobj.groups[g["groupName"]].conds[
                                    c["condition_name"]
                                ].images[-1].addMaskWithClass(
                                    arr,
                                    class_id=m["class_id"],
                                    mask_type=m["mask_type"],
                                    unique_id=m["unique_id"],
                                    visibility=m["visibility"],
                                    includedInAnalysis=m["includedInAnalysis"],
                                )
                                mo = (
                                    self.DH.BLobj.groups[g["groupName"]]
                                    .conds[c["condition_name"]]
                                    .images[-1]
                                    .masks[m["unique_id"]]
                                )
                                mo.class_group_id = m["class_group_id"]
                                mo.spatial_id = m["spatial_id"]
                                mo.score = m["score"]
                                mo.includedInAnalysis = m["includedInAnalysis"]
                                mo.mask_type = m["mask_type"]
                                mo.is_suggested = m["is_suggested"]
                                mo._annotation_track_id = m["_annotation_track_id"]
                                mo.intensity_metrics = m["intensity_metrics"]
                                if hasattr(m, "particle_metrics"):
                                    mo.particle_metrics = m["particle_metrics"]

            if self.custom_class_list_widget.count():
                # set the first class item as the active one
                self.custom_class_list_widget.setCurrentRow(0)
            if self.RNAi_list.count():
                QtWidgets.QApplication.processEvents()
                # Select the first item
                first_item = self.RNAi_list.item(0)
                self.RNAi_list.setCurrentItem(first_item)
                # Manually call the method that handles item selection
                # Trigger a scene refresh and image preview area refresh
                config.global_signals.refresh_image_preview_graphicsscene_signal.emit()
                config.global_signals.load_main_scene_signal.emit()
                self.switch_treatment_onchange(
                    first_item
                )  # update the image buttons to match the treatment
            return images
        except Exception as e:
            logger.error(e)

            self.stackedWidget.setCurrentWidget(prior_location)
            # quit session
            self.quit_project(without_prompt=True)

            config.global_signals.fatalErrorSignal.emit("Failed to read file.")

    from celer_sight_ai.gui.designer_widgets_py_files.scaledDialog import (
        Ui_ScaleDialog,
    )

    class scaleDialogClass(Ui_ScaleDialog):
        def __init__(self, MainWindow):
            self.MainWindow = MainWindow
            self.myDialog = QtWidgets.QDialog()
            self.setupUi(self.myDialog)
            self.buttonBox.button(
                QtWidgets.QDialogButtonBox.StandardButton.Ok
            ).clicked.connect(lambda: self.updatePixelScale())
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
                lambda: self.cancelAndClose()
            )
            if self.MainWindow.pixelSet:
                self.doubleSpinBox.setValue(self.MainWindow.pixelScalePerUnit)
            self.myDialog.show()
            # self.myDialog._raise()
            self.pushButton.clicked.connect(lambda: self.startScaleGetDistance())

        def updatePixelScale(self):
            self.MainWindow.pixelScalePerUnit = (
                self.doubleSpinBox.value() / self.doubleSpinBox_2.value()
            )
            self.MainWindow.pixelSet = True
            self.myDialog.close()

        def cancelAndClose(self):
            self.myDialog.close()

        def startScaleGetDistance(self):
            self.MainWindow.viewer.scaleBarDraw_STATE = True

    def execScaleDialog(self):
        config.global_signals.errorSignal.emit("Feature not supported yet.")
        return
        self.myScaleDialogClass = self.scaleDialogClass(self)

    def mask_dilution(self, mask, increase_mask_value):
        """
        Enlarge the mask
        """
        kernel = np.ones((5, 5), np.uint8)
        dilated_mask = cv2.dilate(
            mask.copy().astype(np.uint8), kernel, iterations=increase_mask_value
        )
        return dilated_mask

    def spawnAutoImportInstractions(self):
        from celer_sight_ai.gui.custom_widgets.instractionDialogues import (
            ExportNeuralSettingsDialog,
        )

        self.myAutoInportInstractions = ExportNeuralSettingsDialog(self)

    def spawnAutoAnalysisInstractions(self):
        from celer_sight_ai.gui.custom_widgets.instractionDialogues import (
            ExportNeuralSettingsDialog,
        )

        self.myAutoInportInstractions = ExportNeuralSettingsDialog(
            self, MODE="ANALYSIS"
        )

    def showEvent(self, event):
        """
        this gets trigured on first run after show() and everytime show is trigured
        """
        event.accept()

    def save_current_asset(self):
        current_item = self.RNAi_list.currentItem().text()

    def DeletePlotInstances(self):
        """
        Deletes the Plot instances and the dictionaries in the list pg2_graphs_view
        """
        try:
            currentItemIndex = self.pg2_graphs_view.currentRow()
            currentItem = self.pg2_graphs_view.currentItem().text()
            del self.MyVisualPlotHandler.WidgetDictionary[currentItem]
            self.pg2_graphs_view.takeItem(currentItemIndex)
        except Exception:
            logger.exception()

    def delete_canvas(self):
        """
        Deletes the canvas in the plots Dock
        """
        try:
            for widget in self.PlotCanvasFrame_Layout.children():
                try:
                    widget.deleteLater()
                    # sip.delete(widget)
                except:
                    pass
            QtWidgets.QApplication.processEvents()
        except Exception:
            pass
        return

    def autoPlotSeaborn_generic(self):
        from celer_sight_ai.gui.custom_widgets.plot_handler import plotStylesButton

        buttonForPlot = self.pg_2_plot_parameteres_scrollAreaWidgetContents.findChild(
            plotStylesButton, "pink_box_swarm_fade_simple1_NORMAL.png"
        )
        buttonForPlot.click()
        # pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2

    def plot_seaborn(self):
        """
        Plots our graph , main plot function
        """
        # TODO: add broken axis package: https://github.com/bendichter/brokenaxes
        import seaborn as sns

        from celer_sight_ai.gui.custom_widgets.plot_handler import MyPlotHandler

        return

        from matplotlib import pyplot as plt
        from matplotlib.figure import Figure

        sns.set()
        sns.set_style("whitegrid")
        """"
        for the lenfth in the the PlotViewerHandler self.CurrentWidget
        """
        # self it the Ui_Plot_tools_widget settings
        if not hasattr(self.DH, "final_df_counts_condition_global"):
            return
        dataframe_f = self.DH.plot_dataframe
        try:
            if hasattr(self, "figure"):
                del self.figure
        except:
            pass
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.canvas_data = FigureCanvas(self.figure)
        ax1 = self.figure.add_subplot(111)
        # Here we record the variables from the GUI intereface
        # MyPlotHandler_1 = MyPlotHandler(self,self.figure,dataframe_f,ax1
        # self.MyVisualPlotHandler = self.MyVisualPlotHandler.GatherPlotVariables(self,self.MyVisualPlotHandler)
        # Next we need to plot all of the plots in the combobox
        plt.xlabel(
            self.pg_2_x_axis_textedit.toPlainText(), fontsize=15
        )  # x-axis label with fontsize 15
        plt.ylabel(
            self.pg_2_x_axis_textedit.toPlainText(), fontsize=15
        )  # y-axis label with fontsize 15
        plt.title(self.pg_2_Title_textedit.toPlainText())
        ax1 = self.MyVisualPlotHandler.PlotSeaborn(
            self, self.MyVisualPlotHandler, ax1, dataframe_f
        )
        self.currentDataFrame = dataframe_f
        # Set the axes to be on the side:
        self.LastUsedAxis = ax1
        # Draw the ax1 to the canvas
        self.figure.tight_layout()
        self.currentAxis = ax1
        self.MyVisualPlotHandler.initInteractionSettings(ax1)
        self.canvas_data = FigureCanvas(self.figure)
        self.canvas.draw()
        self.canvas.update()
        import copy

        self.PlotCanvasFrame_Layout_2.addWidget(self.canvas_data, 0, 0, 1, 1)
        self.PlotCanvasFrame_Layout.addWidget(self.canvas, 0, 0, 1, 1)
        # add events
        QtWidgets.QApplication.processEvents()

    def convertQImageToMat(self, incomingImage):
        """Converts a QImage into an opencv MAT format"""

        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr

    def changeCondition(self, conditionToChangeTo=None):
        # changes the UI to the new condition
        if conditionToChangeTo:
            for i in range(self.RNAi_list.count()):
                if self.RNAi_list.item(i).text() == conditionToChangeTo:
                    self.RNAi_list.item(i).click()
                    break

    def compute_transform_and_display_analysis(self):
        """
        currently used to parse df to display in the qtable
        1) Extract all relevant channels and perform channel operations (blue over red , etc...)
        2) Extract all relevant ROIs and perform ROI operations (roi1 over roi2 , etc...)
        3) Display the result in the qtable

        There is currently no support for more than 2 channels or 2 ROIs per operation
        Instances in processed like so:
         - In the case where there are multiple instances as children to a parent mask, there will
           be a value in the final dataframe for each instance. If the mean of the child instance is
           4 and the mean of the parent mask is 10, then the value in the final dataframe will be 4/10 = 0.4
           if the operation is child over parent. If the child has multiple parent, which does happen,
           then each child will be processed for each parent as a separate value.
         - In the case that the child Roi is a binary mask and the parent is an instance segmentation mask, then for
           each instance in the parent mask, the mean of the child mask will be calculated and added to the final
           dataframe
        """
        # TODO: remove
        # initiaze all variables..
        import copy
        import itertools

        import pandas as pd

        from celer_sight_ai.gui.custom_widgets.analysis_handler import (
            SUPPORTED_CHANNEL_OPERATIONS,
            SUPPORTED_ROI_OPERATIONS,
            add,
            divide,
            multiply,
            subtract,
        )

        if self.all_condition_analysis_table.model():
            self.all_condition_analysis_table.setModel(None)

        Condition_names = []
        self.all_conditions_values = []
        self.all_conditions_values_averages = []
        self.all_conditions_values_SD = []
        self.all_conditions_values_SE = []
        self.per_condition_values = []
        self.final_df_counts_condition = []
        if hasattr(self, "all_RNAi_all_columns_pd"):
            del self.all_RNAi_all_columns_pd
        self.all_RNAi_all_columns_pd = []
        names = []

        # on async, it finishes faster than the data is loaded
        # TODO: fix this bug

        config.global_params.mean_fluorescent = True  #  for intensity analysis only
        if (
            config.global_params.analysis
            == self.new_analysis_object.analysis_map["mean_intensity"]
        ):
            names = []
            self.all_RNAi_all_columns_pd = []

            # for every channel compute the mean intensity for each condition for min max mean and all of the other values
            # if len(self.MainWindow.DH.BLobj. ) == 1:
            channel_used = self.channel_analysis_metrics_combobox.currentText()
            analysis_type = self.Results_pg2_AnalysisTypeComboBox.currentText()
            roi_selected = self.ROI_analysis_metrics_combobox.currentText()
            if channel_used == "":
                config.global_signals.notificationSignal.emit("Please select a channel")
                return
            if analysis_type == "":
                config.global_signals.notificationSignal.emit(
                    "Please select an analysis type"
                )
                return
            if roi_selected == "":
                config.global_signals.notificationSignal.emit("Please select an ROI")
                return
            final_dataframe = self.DH.allAnalysisDataContainer["Mean intensity"]

            # First, compute all channeloperations for each Roi individually (then we do Roi wise operations)

            # for every ROI do the channel opperations if needed and update the channel column

            # case for 1 channel
            channel_querry = self.AnalysisSettings.analysis_channels_named[channel_used]
            if len(channel_querry) == 1:
                df_channel = final_dataframe[final_dataframe["Channel"] == channel_used]
                pass
            else:
                # Perform channel operations for each ROI and store on the respective values
                # change the name of the channel to the channel x operation x channel name
                operation = channel_querry[1]
                channel1, channel2 = channel_querry[0], channel_querry[2]
                df1 = final_dataframe[final_dataframe["Channel"] == channel1]
                df2 = final_dataframe[final_dataframe["Channel"] == channel2]

                # Create a unique index within each Condition and ROI
                df1.loc[:, "index"] = df1.groupby(["Condition", "Roi"]).cumcount()
                df2.loc[:, "index"] = df2.groupby(["Condition", "Roi"]).cumcount()

                # Merge the dataframes
                df_merged = pd.merge(
                    df1, df2, on=["Condition", "Roi", "index"], suffixes=("_1", "_2")
                )

                # Perform the cell-wise operation
                df_channel = df_merged.copy()
                df_channel.loc[:, analysis_type] = pd.Series(
                    SUPPORTED_CHANNEL_OPERATIONS[operation](
                        df_merged[f"{analysis_type}_1"], df_merged[f"{analysis_type}_2"]
                    ),
                    index=df_channel.index,
                )
                # Keep only necessary columns
                df_channel = df_channel[["Condition", "Roi", "index", analysis_type]]

            # if there are roi operations, perform them with the channel adjusted data
            # do the same for Roi
            roi_querry = self.AnalysisSettings.analysis_roi_named[roi_selected]
            if len(roi_querry) == 1:
                df_roi = df_channel[final_dataframe["Roi"] == roi_selected]
            else:
                operation = roi_querry[
                    1
                ]  # extract the operation, roi_selected should be [roi1, operation, roi2]
                roi1, roi2 = roi_querry[0], roi_querry[2]
                df_roi_1 = df_channel[df_channel["Roi"] == roi1].copy()
                df_roi_2 = df_channel[df_channel["Roi"] == roi2].copy()

                # Create a unique index within each Condition
                df_roi_1.loc[:, "index"] = df_roi_1.groupby("Condition").cumcount()
                df_roi_2.loc[:, "index"] = df_roi_2.groupby("Condition").cumcount()

                # Merge the dataframes
                df_merged = pd.merge(
                    df_roi_1, df_roi_2, on=["Condition", "index"], suffixes=("_1", "_2")
                )

                # Perform the cell-wise operation
                df_roi = df_merged.copy()
                df_roi.loc[:, analysis_type] = pd.Series(
                    SUPPORTED_CHANNEL_OPERATIONS[operation](
                        df_merged[f"{analysis_type}_1"], df_merged[f"{analysis_type}_2"]
                    ),
                    index=df_roi.index,
                )

                # Keep only necessary columns
                df_roi = df_roi[["Condition", "index", analysis_type]]

            df_roi["index"] = df_roi.groupby("Condition").cumcount()

            df_displayed = df_roi.pivot(
                index="index", columns="Condition", values=analysis_type
            )
        elif (
            config.global_params.analysis
            == self.new_analysis_object.analysis_map["fragmentation"]
        ):
            raise NotImplementedError("Fragmentation not implemented")
            # Iterate over each element in our listwidget..
            self.all_RNAi_all_columns_pd = []
            names = []
            for i in range(self.RNAi_list.count()):
                current_item = self.RNAi_list.item(i).text()
                names.append(
                    current_item
                )  # get the names (in text) of all items in listview
                # gui_main.load_all_assets_listwidget_global(current_item) #load all the private assets from gui_main to global
                self.all_RNAi_all_columns_pd.append(
                    self.DH.dict_aggs_counts_all_RNAi[current_item]
                )
            # return

        elif (
            config.global_params.analysis
            == self.new_analysis_object.analysis_map["particles"]
        ):
            names = []
            self.all_RNAi_all_columns_pd = []

            # for every channel compute the mean intensity for each condition for min max mean and all of the other values
            # if len(self.MainWindow.DH.BLobj. ) == 1:
            channel_used = self.channel_analysis_metrics_combobox.currentText()
            analysis_type = self.Results_pg2_AnalysisTypeComboBox.currentText()

            final_dataframe = self.DH.allAnalysisDataContainer["Mean intensity"]
            final_dataframe = final_dataframe[
                final_dataframe["Channel"].str.fullmatch(channel_used)
            ].loc[:, ["Condition", analysis_type]]
            n_conditions = final_dataframe["Condition"].nunique()
            final_dataframe["index"] = final_dataframe.groupby("Condition").cumcount()

            final_dataframe = final_dataframe.pivot(
                index="index", columns="Condition", values=analysis_type
            )

        elif config.global_params.analysis == self.new_analysis_object.colocalization:
            self.all_RNAi_all_columns_pd = []
            raise NotImplementedError("Colocalization not implemented")
            names = []
            for i in range(self.RNAi_list.count()):
                current_item = self.RNAi_list.item(i).text()
                names.append(
                    current_item
                )  # get the names (in text) of all items in listview
                self.all_RNAi_all_columns_pd.append(
                    self.DH.allAnalysisDataContainer["colocalization"]["pearson"][
                        current_item
                    ]
                )

        self.DH.plot_dataframe = df_roi
        from celer_sight_ai.gui.custom_widgets.PDModel import pandasModel

        self.AnalysisSettings.update_channel_combobox_label(
            self.channel_analysis_metrics_combobox.currentIndex()
        )

        self.model_pandas = pandasModel(df_displayed, self.all_condition_analysis_table)
        self.all_condition_analysis_table.setModelCustom(self.model_pandas)
        self.removeEventFilter(self.all_condition_analysis_table)

    def updateResultsSpreadSheet(self):
        """
        During a new seleciton on the qcombobox
        """
        """
        Old function to make a copy of the variabels, this needs to get deleted
        """
        # TODO: remove
        # initiaze all variables..
        import itertools

        import pandas as pd

        self.all_condition_analysis_table.setModel(None)
        QtWidgets.QApplication.processEvents()
        Condition_names = []
        self.all_conditions_values = []
        self.all_conditions_values_averages = []
        self.all_conditions_values_SD = []
        self.all_conditions_values_SE = []
        self.per_condition_values = []
        self.final_df_counts_condition = []
        self.all_RNAi_all_columns_pd = []
        names = []

        AnalObject = self.new_analysis_object
        ProjectVars = config.global_params

        comboboxText1 = self.Results_pg2_AnalysisTypeComboBox.currentText()
        comboboxText2 = self.channel_analysis_metrics_combobox.currentText()
        DictionaryOfUse = []

        # # if current experiment is "Mean Intensity"
        if (
            config.global_params.analysis
            == self.new_analysis_object.analysis_map["mean_intensity"]
        ):
            return
            # DictionaryOfUse = self.DH.plot_dataframe["mean_intensity"]
            # self.channel_analysis_metrics_combobox.hide()
        elif comboboxText1 == "Aggregates":
            return
            # if ProjectVars.organism == AnalObject.cells:
            self.channel_analysis_metrics_combobox.show()
            if comboboxText2 == "Area":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif comboboxText2 == "R.IntDensity":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif comboboxText2 == "Particle area":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]

            elif comboboxText2 == "ROI per Image":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif comboboxText2 == "Mean intensity":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif comboboxText2 == "Area":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif comboboxText2 == "Count":
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    comboboxText2
                ]
            elif "Aggregates" in self.DH.allAnalysisDataContainer.keys():
                DictionaryOfUse = self.DH.allAnalysisDataContainer[comboboxText1][
                    "Count"
                ]

        elif comboboxText1 == "Colocalization":
            return
            if "colocalization" in self.DH.allAnalysisDataContainer.keys():
                if (
                    comboboxText2 == "pearson"
                    and "pearson"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"]["pearson"]
                    )
                if (
                    comboboxText2 == "kendalls tau"
                    and "kendalls tau"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"][
                            "kendalls tau"
                        ]
                    )
                if (
                    comboboxText2 == "manders"
                    and "manders"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"]["manders"]
                    )
                if (
                    comboboxText2 == "mandersM1"
                    and "mandersM1"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"]["mandersM1"]
                    )
                if (
                    comboboxText2 == "mandersM2"
                    and "mandersM2"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"]["mandersM2"]
                    )
                if (
                    comboboxText2 == "spearmans"
                    and "spearmans"
                    in self.DH.allAnalysisDataContainer["colocalization"].keys()
                ):
                    DictionaryOfUse = copy.deepcopy(
                        self.DH.allAnalysisDataContainer["colocalization"]["spearmans"]
                    )

        if isinstance(DictionaryOfUse, type(None)):
            return
        if len(DictionaryOfUse) == 0:
            return

        # for i in range(self.RNAi_list.count()):
        #     current_item = self.RNAi_list.item(i).text()
        #     names.append(
        #         current_item
        #     )  # get the names (in text) of all items in listview
        #     if current_item not in DictionaryOfUse.keys():
        #         return
        #     self.all_RNAi_all_columns_pd.append(DictionaryOfUse[current_item])
        # self.names = names
        # # for the first df and then we append after
        # try:
        #     dataframe = pd.DataFrame(
        #         self.all_RNAi_all_columns_pd[0], columns=["values"]
        #     )
        # except:
        #     return
        # dataframe["condition"] = names[0]
        # for the first vizible dataframe:
        vizible_df = DictionaryOfUse  # pd.DataFrame(self.all_RNAi_all_columns_pd[0], columns=[names[0]])
        # list that is used later to ctreate the vizible dataframe that we see, the otehr one is used for ploting
        # vizible_df_list = []
        # vizible_df_list.append(vizible_df)
        # for c in range(len(self.all_RNAi_all_columns_pd)):
        #     if c == 0:
        #         continue
        #     dataframe_tmp = pd.DataFrame(
        #         self.all_RNAi_all_columns_pd[c], columns=["values"]
        #     )
        #     dataframe_tmp["condition"] = names[c]
        #     dataframe = dataframe.append(dataframe_tmp, ignore_index=True)
        #     # for the vizible datafreame:

        #     vizible_df = pd.DataFrame(
        #         self.all_RNAi_all_columns_pd[c], columns=[names[c]]
        #     )
        #     # vizible_df = vizible_df.join(pd.DataFrame([self.all_RNAi_all_columns_pd[c]], columns = list(names[c])))
        #     vizible_df_list.append(vizible_df)
        # self.DH.plot_dataframe = dataframe

        from celer_sight_ai.gui.custom_widgets.PDModel import pandasModel

        # Convert list to DataFrame
        vizible_df = pd.DataFrame(DictionaryOfUse)
        self.model_pandas = pandasModel(vizible_df, self.all_condition_analysis_table)
        self.all_condition_analysis_table.setModelCustom(self.model_pandas)
        self.model_pandas = pandasModel(vizible_df, self.all_condition_analysis_table)
        # model_pandas = pandasModel(gui_main.plot_dataframe)
        self.all_condition_analysis_table.setModelCustom(self.model_pandas)
        self.removeEventFilter(self.all_condition_analysis_table)

    def get_average_list(self, lst):
        return sum(lst) / len(lst)

    def remove_values_from_list(self, the_list, val):
        return [value for value in the_list if value != val]

    def exclude_image(self, imagenumber, event):
        if event == QtCore.Qt.MouseButton.RightButton:
            pass

    def combine_usr_predicted(
        self, all_masks, user_pointsx, user_pointsy, withColor=False
    ):
        """
        This function combines the BOOL masks with the Polygon Masks
        """
        return []
        Final_masks = []
        AttributesList = []
        icon_eye = QtGui.QIcon()
        icon_eye.addPixmap(QtGui.QPixmap("data/icons/Eye.png"))
        for i in range(len(all_masks)):
            if self.DH.AssetMaskDictionary[self.DH.BLobj.get_current_condition()][
                self.current_imagenumber
            ][i].eyeIconReference.isChecked():
                Final_masks.append(
                    self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                        i
                    ].copy()
                )
                if (
                    withColor == True
                ):  # if we also care to forward a color information...
                    AttributesList.append(
                        self.DH.AssetMaskDictionary[
                            self.DH.BLobj.get_current_condition()
                        ][self.current_imagenumber][i].RegionAttribute
                    )
                self.DH.AssetMaskDictionary[self.DH.BLobj.get_current_condition()][
                    self.current_imagenumber
                ][i].eyeIconReference.setIcon(icon_eye)
            else:
                self.DH.AssetMaskDictionary[self.DH.BLobj.get_current_condition()][
                    self.current_imagenumber
                ][i].eyeIconReference.setIcon(QtGui.QIcon())

        if withColor == True:
            return Final_masks, AttributesList
        return Final_masks

    def make_master_mask(self, masks):
        """
        Makes a master mask so that its faster when the mouse is clicked over the image to determin whethere there is a mask under or not
        """

        iter = 0
        try:
            for i in range(len(masks)):
                if i == 0:
                    if type(masks[i]) == int:
                        prev_mask = []
                        continue
                    prev_mask = masks[i].copy()
                    iter += 1
                    continue
                else:
                    prev_mask = prev_mask.copy() + masks[i].copy()
                    iter += 1
            return prev_mask
        except:  # usualy when there is no masks
            return []

    def delete_mask_in_master(self, pos: QtCore.QPoint):
        """
        Deletes a mask through the viewer
        Parameters:
         - pos: QPoint
        """
        if self.DH.masks_state[self.current_imagenumber] == True:
            combined_mask = self.combine_usr_predicted(
                self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                    self.current_imagenumber
                ].copy(),
                self.DH.all_worm_mask_points_x_slot[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber].copy(),
                self.DH.all_worm_mask_points_y_slot[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber].copy(),
            )
        else:
            combined_mask = self.combine_usr_predicted(
                [],
                self.DH.all_worm_mask_points_x_slot[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber].copy(),
                self.DH.self.DH.all_worm_mask_points_y_slot[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber].copy(),
            )
        self.selected_mask = -1
        for i in range(len(combined_mask)):
            if (
                combined_mask[i][pos.y(), pos.x()] == True
            ):  # self.DH.all_worm_mask_points_x
                if i >= len(
                    self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                        self.current_imagenumber
                    ]
                ):
                    if (
                        len(
                            self.DH.all_worm_mask_points_x_slot[
                                self.DH.BLobj.get_current_condition()
                            ][self.current_imagenumber]
                        )
                        == 1
                    ):
                        self.DH.masks_state_usr[self.current_imagenumber] = False

                    try:
                        # We need to delete the Mask POLYGON points as well as the Mask ASset buttons
                        self.myButtonHandler.DeleteMaskAssetButton(
                            Number=i, MaskType="POLYGON"
                        )
                        del self.DH.all_worm_mask_points_x_slot[
                            self.DH.BLobj.get_current_condition()
                        ][self.current_imagenumber][
                            i
                            - len(
                                self.DH.mask_RNAi_slots[
                                    self.DH.BLobj.get_current_condition()
                                ][self.current_imagenumber]
                            )
                        ]
                        del self.DH.self.DH.all_worm_mask_points_y_slot[
                            self.DH.BLobj.get_current_condition()
                        ][self.current_imagenumber][
                            i
                            - len(
                                self.DH.mask_RNAi_slots[
                                    self.DH.BLobj.get_current_condition()
                                ][self.current_imagenumber]
                            )
                        ]
                    except Exception as e:
                        logger.exception(e)

                    return True
                else:
                    self.myButtonHandler.DeleteMaskAssetButton(
                        Number=i, MaskType="BOOL"
                    )

                    del self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                        self.current_imagenumber
                    ][i]
                    return False

    def MoveAndShowSelectedMaskDialog(self, mask):
        """
        Moves the dialog to the appropriete condition
        gathers all the masks and adds the annotation buttons (TODO: or are they already added
        from the button class)
        """
        raise NotImplementedError("This function is not used")
        # try:
        #     xmin, ymin, xmax, ymax = self.auto_tool_1.bbox2(mask)
        # except Exception as e:
        #     return
        # # Move the dialog to position
        # try:
        #     self.SelectionStateRegions = True
        #     self.SelectedMaskDialog.move(
        #         self.viewer.postoscene.position().x(),
        #         self.viewer.postoscene.position().y(),
        #     )
        #     self.myButtonHandler.SetUpButtonsAnnotationRegion(self.SelectedMaskDialog)
        #     self.SelectedMaskDialog.show()
        # except Exception as e:
        #     pass
        # # self.SelectedMaskDialog.setStyleSheet(self.OrangeStylesheet)
        # self.SelectedMaskDialog.show()

    def select_mask_in_master(self, pos, WithAnnotations=False):
        """
        Should select the mask under the mouse
        """
        raise NotImplementedError("This function is not used")
        # from celer_sight_ai.AA_cls import Grab_cut_tool

        # try:
        #     self.auto_tool_1
        # except:
        #     self.auto_tool_1 = Grab_cut_tool(
        #         self.DH.BLobj.groups["default"]
        #         .conds[self.DH.BLobj.get_current_condition()]
        #         .getImage(self.current_imagenumber)
        #         .copy()
        #     )
        # if self.DH.masks_state[self.current_imagenumber] == True:
        #     combined_mask = self.combine_usr_predicted(
        #         self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
        #             self.current_imagenumber
        #         ].copy(),
        #         self.DH.all_worm_mask_points_x_slot[
        #             self.DH.BLobj.get_current_condition()
        #         ][self.current_imagenumber].copy(),
        #         self.DH.self.DH.all_worm_mask_points_y_slot[
        #             self.DH.BLobj.get_current_condition()
        #         ][self.current_imagenumber].copy(),
        #     )
        # else:
        #     combined_mask = self.combine_usr_predicted(
        #         [],
        #         self.DH.all_worm_mask_points_x_slot[
        #             self.DH.BLobj.get_current_condition()
        #         ][self.current_imagenumber].copy(),
        #         self.DH.self.DH.all_worm_mask_points_y_slot[
        #             self.DH.BLobj.get_current_condition()
        #         ][self.current_imagenumber].copy(),
        #     )
        # for i in range(len(combined_mask)):
        #     if (
        #         combined_mask[i][pos.y(), pos.x()] == True
        #     ):  # self.DH.all_worm_mask_points_x
        #         if i >= len(
        #             self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
        #                 self.current_imagenumber
        #             ]
        #         ):
        #             self.selected_mask = i
        #             self.selected_mask_origin = (
        #                 "POLYGON"  # if the mask we are looking at is from polygon
        #             )
        #             if WithAnnotations == True:
        #                 self.MoveAndShowSelectedMaskDialog(combined_mask[i])

        #         else:
        #             self.selected_mask = i
        #             self.selected_mask_origin = "BOOL"  # if its a bitwise mask
        #             if WithAnnotations == True:
        #                 self.MoveAndShowSelectedMaskDialog(combined_mask[i])
        #         self.myButtonHandler.SelectMaskAssetButton()
        #         return

    def place_mask_locators_off(
        self,
        all_points_x,
        all_points_y,
        image_to_draw_on,
        small_image,
        offsetx=-3,
        offsety=-3,
    ):
        """
        When we draw with a polygon tool this places points (circles) at the edges
        """
        # locators:
        l_image = image_to_draw_on
        # Draws the
        try:
            for z in range(len(all_points_x)):
                x1 = all_points_x[z] + offsetx
                y1 = all_points_y[z] + offsety
                #
                x2 = x1 + small_image.shape[1]
                y2 = y1 + small_image.shape[0]
                alpha_s = small_image[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(0, 3):
                    l_image[y1:y2, x1:x2, c] = (
                        alpha_s * small_image[:, :, c]
                        + alpha_l * l_image[y1:y2, x1:x2, c].copy()
                    )
        except:
            return image_to_draw_on
        return l_image

    def place_mask_locators_off_short(
        self,
        all_points_x,
        all_points_y,
        image_to_draw_on,
        small_image,
        offsetx=-6,
        offsety=-6,
    ):
        """
        When we draw with a polygon tool this places points (circles) at the edges
        """
        # locators:
        l_image = image_to_draw_on

        x1 = all_points_x + offsetx
        y1 = all_points_y + offsety
        x2 = x1 + small_image.shape[0]
        y2 = y1 + small_image.shape[1]
        alpha_s = small_image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            l_image[y1:y2, x1:x2, c] = (
                alpha_s * small_image[:, :, c]
                + alpha_l * l_image[y1:y2, x1:x2, c].copy()
            )
        return l_image

    def onSubmit(self):
        self.submitted.emit()

    def reset_all_values(self):
        # if len(self.DH.view_field_dictionary_slots)!=0
        if self.RNAi_list.count() == 0:
            self.initialize_analysis_button.setEnabled_(False)
            self.get_roi_ai_button.setEnabled_(False)
            self.viewer.LeftArrowChangeButton.hide()
            self.viewer.RightArrowChangeButton.hide()

        self.DH.master_mask_list = []
        self.i_am_drawing_state = False
        self.worm_mask_points_x = []
        self.worm_mask_points_y = []
        self.selected_mask = 0
        self.temp_mask_to_use_Test_x = []
        self.temp_mask_to_use_Test_y = []
        self.DH.all_worm_mask_points_x = (
            []
        )  # need to make dictionaries of those for RNAi
        self.DH.all_worm_mask_points_y = []
        self.counter_tmp = 0
        self.DH.unique_masks_tmp = []
        self.DH.masks_state_usr = []
        self.DH.masks_state = []
        self.add_mask_btn_state = False
        # gui_main.main_viewer_state = False
        self.DH.predict_masks_state = False
        self.DH.pixon_list_opencv = []
        self.DH.all_masks = []
        self.DH.all_masks_usr = []
        self.selected_mask = -1
        self.DH.current_RNAi = 0
        # dictionary_max_elements = 5
        # self.DH.image_names_all_RNAi = {}
        self.DH.image_names = []
        self.DH.added_to_dictionary_state = True
        # self.DH.BLobj.groups['default'].conds = {}
        # self.DH.view_field_dictionary_slots = {}
        # self.DH.mask_RNAi_slots= {}
        # self.DH.usr_mask_RNAi_slots= {}
        self.DH.calculated_dictionary_state = False
        # self.DH.dict_aggs_lables_all_RNAi = {}
        # self.DH.dict_aggs_counts_all_RNAi= {}
        # self.DH.dict_aggs_volume_all_RNAi= {}
        # self.DH.dict_master_mask_list = {}
        # self.DH.dict_RNAi_attributes_all = {}
        # self.DH.dict_RNAi_attributes =  {'predict_masks_state':self.DH.predict_masks_state,
        #                                         'added_to_dictionary_state' : self.DH.added_to_dictionary_state,
        #                                         'calculated_dictionary_state':self.DH.calculated_dictionary_state,
        #                                         'masks_state_usr' : self.DH.masks_state_usr,
        #                                         'masks_state' : self.DH.masks_state}
        # self.DH.all_worm_mask_points_x_slot ={}
        # self.DH.all_worm_mask_points_y_slot ={}
        # self.DH.stacked_images_slot ={}
        self.delete_counter = 0  # a counter that helps with the delete paradox of deletelater that runs at the end of the eventloop
        self.setCurrentImageNumber(-1)
        self.previous_imagenumber = -1
        self.selection_state = False  # weather or not we can aselect a mask
        ## lebel adds aggregates only
        self.DH.aggs_lables_all_RNAi = []
        self.DH.aggs_lables_RNAi = []
        self.DH.aggs_lables_worm = []
        self.DH.summary_counts_RNAi = []
        ## per count aggregates only
        self.DH.aggs_counts_all_RNAi = []  #
        self.DH.aggs_counts_RNAi = []
        self.DH.aggs_counts_worm = []
        self.DH.summary_counts_RNAi = []  #
        ## per volume aggregates only
        self.DH.aggs_volume_all_RNAi = []  #
        self.DH.aggs_volume_RNAi = []
        self.DH.aggs_volume_worm = []
        self.DH.summary_volume_RNAi = []  #
        # self.list_grid_layout_box2 = []
        # self.list_grid_layout_box1 = []
        self.imagenumber = 0
        self.all_stacked_images = []
        # self.delete_assets

    def make_add_mask_button_state(self):
        if self.add_mask_btn_state == True:
            self.add_mask_btn_state = False
            self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        elif self.add_mask_btn_state == False:
            self.add_mask_btn_state = True
            self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))

    # def Threaded_on_button_clicked(self):
    #     worker = Worker(self.on_Button_clicked)
    #     self.threadpool.start(worker)

    def delete_treatment_item_by_name(self, treatment):
        # deletes item quickly and does not update ui, unless its the same as the displayed conditoin

        # Make sure that there is no active processes running
        if self.ai_model_settings_widget.is_generating:
            self.ai_model_settings_widget.cancel_generating()

        # if condition is the current condition, delete the preview images as well
        if treatment == self.RNAi_list.currentItem().text():
            self.delete_RNAi_list_item()
            return
        self.RNAi_list.takeItem(
            self.RNAi_list.findItems(treatment, QtCore.Qt.MatchFlag.MatchExactly)[
                0
            ].row()
        )

        # try and remove cache dirs
        try:
            import shutil

            # delete all images from cache of that treatment
            all_images = self.DH.BLobj.get_all_images_by_condition(treatment)
            for img in all_images:
                if img.is_cached:
                    try:
                        os.remove(img.cache_location)
                    except Exception as e:
                        logger.exception(e)

        except Exception as e:
            logger.exception(e)

        treatment_uuid = self.DH.BLobj.groups["default"].conds[treatment].unique_id
        self.DH.BLobj.object_mapping[treatment_uuid] = None
        del self.DH.BLobj.groups["default"].conds[
            treatment
        ]  # Dictionary for pixon_list_opencv lists

    def delete_image_preview_buttons(self):
        # remove all widgets on the images preview part of the graphics view
        for proxy_item in self.images_preview_graphicsview.scene().items():
            if proxy_item.widget() in self.DH.BLobj.get_all_buttons(
                self.DH.BLobj.get_current_group(), self.RNAi_list.currentItem().text()
            ):
                self.images_preview_graphicsview.scene().removeItem(proxy_item)
                proxy_item.widget().deleteLater()
        self.images_preview_graphicsview.clear_out_visible_buttons()

    def delete_RNAi_list_item(self):
        from celer_sight_ai.gui.custom_widgets.scene import BackgroundGraphicsItem

        self.channel_picker_widget.clear_channels()
        logger.debug("delete_RNAi_list_item")
        if self.RNAi_list.count() == 0:
            return
        if (
            self.RNAi_list.currentItem().text()
            not in self.DH.BLobj.groups["default"].conds.keys()
        ):
            return
        currentItem = self.RNAi_list.currentItem().text()
        self.DH.BLobj.set_current_condition(currentItem)

        self.delete_image_preview_buttons()

        if currentItem in self.DH.BLobj.groups["default"].conds:
            del self.DH.BLobj.groups["default"].conds[
                currentItem
            ]  # Dictionary for pixon_list_opencv lists

        self.reset_all_values()

        self.RNAi_list.takeItem(self.RNAi_list.currentRow())
        current_treatment_widget = self.get_treatment_widget_by_name(currentItem)
        self.previous_clicked_treatment_item = current_treatment_widget
        if current_treatment_widget:
            self.DH.BLobj.set_current_condition(current_treatment_widget.text())
        else:
            self.DH.BLobj.set_current_condition(None)

        if not (
            self.RNAi_list.count() == 0
            or self.RNAi_list.item(self.RNAi_list.currentRow()) == None
        ):
            #     self.viewer._photo = BackgroundGraphicsItem()
            #     self.viewer._photo.setZValue(-50)
            #     self.viewer._scene.addItem(self.viewer._photo)
            # else:
            self.myButtonHandler.ShowNewCondition(
                condition=self.RNAi_list.item(self.RNAi_list.currentRow()).text()
            )
            self.switch_treatment_onchange()

        self.load_main_scene(fit_in_view=True)
        return

    def up_button_list_item(self):
        logger.debug("up_button_list_item")
        currentRow = self.RNAi_list.currentRow()
        currentItem = self.RNAi_list.takeItem(currentRow)
        self.RNAi_list.insertItem(currentRow - 1, currentItem)
        self.RNAi_list.setCurrentItem(currentItem)

    def down_button_list_item(self):
        logger.debug("down_button_list_item")
        currentRow = self.RNAi_list.currentRow()
        currentItem = self.RNAi_list.takeItem(currentRow)
        self.RNAi_list.insertItem(currentRow + 1, currentItem)
        self.RNAi_list.setCurrentItem(currentItem)

    def mask_under_mouse(self, pos, mask):
        if mask is None:
            return False
        # mask = np.asarray(mask)
        if len(mask) == 1:
            if self.add_mask_btn_state == False:
                # try:
                if mask[0][pos.y(), pos.x()] == True:
                    self.delete_mask_in_master(pos)
                    self.load_main_scene(self.current_imagenumber)
                    return True
                else:
                    return False
        if len(mask) != 0:
            if self.add_mask_btn_state == False:
                # try:
                if mask[pos.y(), pos.x()] == True:
                    self.delete_mask_in_master(pos)
                    self.load_main_scene(self.current_imagenumber)
                    return True
                else:
                    return False
                # except:
                #     return
        else:
            return False

    def concatinate_masks(self, mask_list):
        for i in range(len(mask_list)):
            mask_tmp = mask_list[i].copy()  # convert to an unsigned byte
            if i == 0:
                final_mask_tmp = mask_tmp.copy()
            final_mask_tmp = cv2.bitwise_or(final_mask_tmp, mask_tmp)

        return final_mask_tmp

    def delete_assets(self, current_item):
        if current_item in self.DH.BLobj.groups["default"].conds:
            del self.DH.stacked_images_slot[current_item]
            del self.DH.view_field_dictionary_slots[current_item]
            del self.DH.BLobj.groups["default"].conds[current_item]
            del self.DH.mask_RNAi_slots[current_item]
            del self.DH.usr_mask_RNAi_slots[current_item]
            del self.DH.dict_aggs_counts_all_RNAi[current_item]
            del self.DH.dict_aggs_volume_all_RNAi[current_item]
            del self.DH.dict_RNAi_attributes
            del self.DH.dict_master_mask_list[current_item]
            del self.DH.dict_RNAi_attributes_all[current_item]
            del self.DH.all_worm_mask_points_x_slot[current_item]
            del self.DH.all_worm_mask_points_y_slot[current_item]
            del self.DH.image_names_all_RNAi[current_item]
        else:
            pass

    # Custom widgets only for windows
    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def load_all_assets_listwidget(self, current_item):
        """
        Loads up everything from dictionaries
        """
        if current_item in self.DH.dict_RNAi_attributes_all:
            self.DH.predict_masks_state = self.DH.dict_RNAi_attributes_all[
                current_item
            ]["predict_masks_state"]
            self.DH.added_to_dictionary_state = self.DH.dict_RNAi_attributes_all[
                current_item
            ]["added_to_dictionary_state"]
            self.DH.calculated_dictionary_state = self.DH.dict_RNAi_attributes_all[
                current_item
            ]["calculated_dictionary_state"]
            self.DH.masks_state_usr = self.DH.dict_RNAi_attributes_all[current_item][
                "masks_state_usr"
            ].copy()
            self.DH.masks_state = self.DH.dict_RNAi_attributes_all[current_item][
                "masks_state"
            ].copy()
        # all all assets
        # self.DH.image_names = self.DH.image_names_all_RNAi[current_item].copy()
        self.all_stacked_images = self.DH.stacked_images_slot[current_item].copy()
        # self.DH.view_field_list =   self.DH.view_field_dictionary_slots[current_item].copy()
        self.DH.pixon_list_opencv = self.DH.stacked_images_slot[
            current_item
        ].copy()  # self.DH.BLobj.groups['default'].conds[current_item].copy()
        self.DH.all_masks = self.DH.mask_RNAi_slots[current_item].copy()
        self.DH.all_masks_usr = self.DH.usr_mask_RNAi_slots[current_item].copy()
        # self.DH.master_mask_list = self.DH.dict_master_mask_list[current_item].copy()

        if current_item in self.DH.dict_aggs_counts_all_RNAi.keys():
            self.DH.aggs_counts_all_RNAi = self.DH.dict_aggs_counts_all_RNAi[
                current_item
            ].copy()
            self.DH.aggs_volume_all_RNAi = self.DH.dict_aggs_volume_all_RNAi[
                current_item
            ].copy()

        if current_item in self.DH.all_worm_mask_points_x_slot.keys():
            self.DH.all_worm_mask_points_x = self.DH.all_worm_mask_points_x_slot[
                current_item
            ].copy()
            self.DH.all_worm_mask_points_y = self.DH.all_worm_mask_points_y_slot[
                current_item
            ].copy()

        # AssetMasks maybe movet his to button handler
        if current_item in self.DH.AssetMaskDictionary.keys():
            self.DH.AssetMaskListBool = self.DH.AssetMaskDictionary[current_item].copy()
        else:
            self.DH.AssetMaskDictionary[current_item] = {}
            self.DH.AssetMaskListBool = {}
        # self.DH.AssetMaskListPolygon = self.DH.AssetMaskDictionaryPolygon[current_item].copy()
        # try:
        #     self.DH.AssetMaskListBoolSettings = self.DH.AssetMaskDictionaryBoolSettings[current_item].copy()
        #     self.DH.AssetMaskListPolygonSettings = self.DH.AssetMaskDictionaryPolygonSettings[current_item].copy()
        # except Exception as e:

    def load_all_assets_listwidget_after_load(self, current_item):
        try:
            for i in range(self.MasterMaskLabelcomboBox.count()):
                self.DH.AnnotationRegions[str(i)] = (
                    self.MasterMaskLabelcomboBox.itemText(i)
                )
        except Exception as e:
            logger.exception(e)
        try:
            if current_item in self.DH.AssetMaskDictionary.keys():
                self.DH.AssetMaskListBool = self.DH.AssetMaskDictionary[
                    current_item
                ].copy()
            else:
                self.DH.AssetMaskDictionary[current_item] = {}
                self.DH.AssetMaskListBool = {}
            # self.DH.AssetMaskListPolygon = self.DH.AssetMaskDictionaryPolygon[current_item].copy()
        except Exception as e:
            logger.exception(e)

    # def show_predict_masks(self):
    #     """
    #     TODO: delete
    #     i dont think this is used anymopre
    #     """
    #     if all( self.DH.masks_state_usr) ==False or all(self.DH.masks_state) == False:
    #         # TODO whats the point of this?
    #         #self.switch_RNAi_Ui(tab_index = 0)
    #         self.switch_RNAi_Ui(tab_index = 1)
    #         return
    #     mask_icon = QtGui.QIcon()
    #     positions =[(i,j) for i in range(100) for j in range(self.num_elem_width)]
    #     values = np.array([i for i in range(len(self.DH.pixon_list_opencv))])
    #     iter_buttons_2 =0
    #     buttonz_list_2 =[]
    #     self.masked_pixon_list = []

    #     for position,value in zip(positions,values):
    #         iter_buttons_2+=1
    #         buttonz_list_2.append(QtWidgets.QPushButton(str(iter_buttons_2-1)))
    #         #logger(self.buttonz_list_2[iter_buttons_2-1].text())
    #         buttonz_list_2[iter_buttons_2-1].setSizePolicy(self.sizePolicy)
    #         buttonz_list_2[iter_buttons_2-1].setMinimumSize(QtCore.QSize(0, 80))
    #         buttonz_list_2[iter_buttons_2-1].setMaximumSize(QtCore.QSize(90, 130))
    #         buttonz_list_2[iter_buttons_2-1].setCheckable(True)
    #         masked_imgon =self.apply_all_masks(self.DH.BLobj.groups['default'].conds[self.DH.BLobj.get_current_condition()][iter_buttons_2-1], self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][iter_buttons_2-1], points = False)
    #         # need to reize image to be able to handle large images:
    #         width1 = masked_imgon.shape[0]
    #         hight1 = masked_imgon.shape[1]
    #         width2 = 90
    #         ration_w = width1 / float(width2)
    #         dim = (int(hight1 * ration_w), width1)
    #         masked_imgon = cv2.resize(masked_imgon, dim, interpolation = cv2.INTER_AREA)

    #         self.pixon = QtGui.QPixmap.fromImage(QtGui.QImage(masked_imgon,masked_imgon.shape[1], masked_imgon.shape[0], QtGui.QImage.Format.FORMAT_RGB32))
    #         self.masked_pixon_list.append(self.pixon)
    #         mask_icon.addPixmap(self.pixon, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    #         buttonz_list_2[iter_buttons_2-1].setIcon(mask_icon)
    #         buttonz_list_2[iter_buttons_2-1].setIconSize(QtCore.QSize(85,85))
    #         buttonz_list_2[iter_buttons_2-1].installEventFilter(self)
    #         # self.grid_layout_box2.addWidget(buttonz_list_2[iter_buttons_2-1], *position)
    #         buttonz_list_2[iter_buttons_2-1].clicked.connect((lambda _, b=(iter_buttons_2-1): self.set_curent_button(imagenumber=b)))
    #         buttonz_list_2[iter_buttons_2-1].clicked.connect((lambda _, b=(iter_buttons_2-1): self.load_main_scene(image_number=b)))
    #         #self.buttonz_list_2[iter_buttons_2-1].clicked.connect((lambda _, b=(iter_buttons_2-1): self.load_main_scene(image_number=b)))
    #         if iter_buttons_2 == 1: # only should be created once

    #             self.grid_layout_box2 = QtWidgets.QGridLayout(self.mask_preview_scrollArea_Contents)
    #             self.grid_layout_box2.setObjectName("grid_layout_box2")
    #         self.grid_layout_box2.addWidget(buttonz_list_2[iter_buttons_2-1], *position)

    #     self.update_scroll_preview(0)

    def GenerateQPolygonFromMasks(self):
        tmpList = []
        import copy

        #
        # Points that are drawn
        #
        self.DH.mask_RNAi_slots_QPoints = {}
        for Condition, data in self.DH.all_worm_mask_points_x_slot.items():
            LenOfImages = len(self.DH.all_worm_mask_points_x_slot[Condition])
            emptyList = []
            for i in range(LenOfImages):
                emptyList.append(copy.copy([]))
            self.DH.mask_RNAi_slots_QPoints[Condition] = copy.deepcopy(emptyList)

        # Masks
        #
        for Condition, data in self.DH.all_worm_mask_points_x_slot.items():
            for image in range(len(self.DH.all_worm_mask_points_x_slot[Condition])):
                for mask in range(
                    len(self.DH.all_worm_mask_points_x_slot[Condition][image])
                ):
                    tmpList1 = []
                    for p in range(
                        len(self.DH.all_worm_mask_points_x_slot[Condition][image][mask])
                    ):
                        tmpList1.append(
                            QtCore.QPointF(
                                self.DH.all_worm_mask_points_x_slot[Condition][image][
                                    mask
                                ][p],
                                self.DH.all_worm_mask_points_y_slot[Condition][image][
                                    mask
                                ][p],
                            )
                        )
                    self.DH.mask_RNAi_slots_QPoints[Condition][image].append(
                        QtGui.QPolygonF(tmpList1)
                    )
        # import skimage
        # for Condition, data in self.DH.mask_RNAi_slots.items():
        #     for image in range(len(self.DH.mask_RNAi_slots[Condition])):
        #         tmpList1= []
        #         for mask in range(len(self.DH.mask_RNAi_slots[Condition][image])):
        #             contours = skimage.measure.find_contours(self.DH.mask_RNAi_slots[Condition][image][mask].copy(), 0.8)
        #             appr_hand = skimage.measure.approximate_polygon(np.asarray(contours[0]), tolerance=0.5)
        #             QpointPolygonMC = QtGui.QPolygonF( [ QtCore.QPointF(p[1], p[0]) for p in appr_hand])
        #             self.DH.mask_RNAi_slots_QPoints[Condition][image].append(QpointPolygonMC)
        # tmpPolygon = QtGui.QPolygonF(tmpList1)

    def draw_polygon_mask(self, pointsy, pointsx, with_off_set=False):
        """
        Converts a polygon mask to Bitwise mask
        """
        import skimage

        image_object = (
            self.DH.BLobj.groups["default"]
            .conds[self.DH.BLobj.get_current_condition()]
            .images[self.current_imagenumber]
        )
        if not with_off_set:
            mask = np.zeros(
                [image_object.SizeX, image_object.SizeY],
                dtype=bool,
            )
            rr, cc = skimage.draw.polygon(pointsy, pointsx, shape=mask.shape)
            mask[rr, cc] = True
            return mask
        else:
            start_x = min(pointsx)
            start_y = min(pointsy)
            end_x = max(pointsx)
            end_y = max(pointsy)
            mask = np.zeros(
                [end_x - start_x, end_y - start_y],
                dtype=bool,
            )
            adjusted_points_x = [x - start_x for x in pointsx]
            adjusted_points_y = [y - start_y for y in pointsy]
            rr, cc = skimage.draw.polygon(
                adjusted_points_y, adjusted_points_x, shape=mask.shape
            )
            mask[rr, cc] = True
            return mask, start_x, start_y

    def draw_polygon_mask_simple(self, pointsy, pointsx):
        """
        Converts a polygon mask list to Bitwise mask list
        """
        import skimage

        mask_list = []
        for i in range(len(pointsx)):
            mask = np.zeros(
                self.DH.BLobj.groups["default"]
                .conds[self.DH.BLobj.get_current_condition()]
                .getImage(self.current_imagenumber)
                .shape,
                dtype=bool,
            )
            rr, cc = skimage.draw.polygon(pointsy[i], pointsx[i], shape=mask.shape)
            mask[rr, cc] = True
        mask_list.append(mask)
        return mask_list

    def apply_mask(self, image, mask1, pointsx, pointsy):
        """
        Draws mask on image
        """
        mask2 = np.zeros(image.shape, image.dtype)

        image[mask1 == 1] = (0, 0, 255)

        # .Set(mask1,cv2.Scalar(0,0,255))
        image2 = self.place_mask_locators_off(
            pointsx, pointsy, image.copy(), self.DH.circle_selection_image
        )
        return image2

    def apply_mask_old(self, image, mask1, pointsx, pointsy):
        """
        Draws mask on image
        """
        redImg = np.zeros(image.shape, image.dtype)
        # a candom choice would be np.random.choice(range(125,255), size=3)
        color = [0, 255, 255]
        redImg[:, :] = color
        mask2 = np.zeros(image.shape, image.dtype)
        # copy your image_mask to all dimensions (i.e. colors) of your image
        for i in range(3):
            mask2[:, :, i] = mask1.copy()

        redMask = cv2.bitwise_and(redImg, redImg, mask=mask2)

        redMask = cv2.addWeighted(redMask, 0.2, image, 1, 0, image)
        redMask = self.place_mask_locators_off(
            pointsx, pointsy, redMask, self.DH.circle_selection_image
        )
        return redMask

    def apply_mask_simple(self, image, mask):
        """
        Draws mask on image
        """
        redImg = np.zeros(image.shape, image.dtype)
        color = [0, 255, 255]
        redImg[:, :] = color
        redMask = cv2.bitwise_and(redImg, redImg, mask=mask)

        redMask = cv2.addWeighted(redMask, 0.2, image, 1, 0, image)

        return redMask

    def apply_all_masks_and_contours(self, image, all_masks_list, AttributeList=None):
        """
        After all the masks have been converted to BOOL then we apply them to the image
        This is for after the second mask as been applied
        """
        import time

        start = time.time()
        from PIL import ImageColor

        x = 0

        if AttributeList != None:
            AttributeColorDict = {}
            for i in range(self.MasterMaskLabelcomboBox.count()):
                AttributeColorDict[str(self.MasterMaskLabelcomboBox.itemText(i))] = (
                    np.asarray(
                        ImageColor.getcolor(
                            str(
                                self.MasterMaskLabelcomboBox.itemData(
                                    i, QtCore.Qt.BackgroundRole
                                ).name()
                            ),
                            "RGB",
                        )
                    )
                )
        if AttributeList == None:
            for mask in all_masks_list:
                if type(mask) == int:
                    continue
                all_masks_list_tmp = mask.astype(
                    np.uint8
                ).copy()  # convert to an unsigned byte

                contours = cv2.Canny(all_masks_list_tmp * 255, 100, 200)
                kernelNumber = 2
                kernel = np.ones((kernelNumber, kernelNumber), np.uint8)
                contours = cv2.dilate(contours.astype(np.uint8), kernel, iterations=1)
                contours = contours.astype(bool)

                try:
                    if self.parent().selected_mask_origin == "BOOL":
                        Attribute = self.DH.AssetMaskDictionaryBool[
                            self.DH.BLobj.get_current_condition()
                        ][self.current_imagenumber][
                            self.selected_mask
                        ].BBWidget.MaskPropertiesWidgetLabelcomboBox.text()
                        indexRegion = self.MasterMaskLabelcomboBox.findText(Attribute)
                        hexColor = self.MasterMaskLabelcomboBox.itemData(
                            indexRegion, QtCore.Qt.BackgroundRole
                        ).name()
                        color = np.asarray(ImageColor.getcolor(str(hexColor), "RGB"))
                        # color = self.DH.AssetMaskListBool[self.current_imagenumber][x].MaskColor
                    else:
                        Attribute = self.DH.AssetMaskDictionaryBool[
                            self.DH.BLobj.get_current_condition()
                        ][self.current_imagenumber][
                            self.selected_mask
                        ].BBWidget.MaskPropertiesWidgetLabelcomboBox.text()
                        indexRegion = self.MasterMaskLabelcomboBox.findText(Attribute)
                        hexColor = self.MasterMaskLabelcomboBox.itemData(
                            indexRegion, QtCore.Qt.BackgroundRole
                        ).name()
                        color = np.asarray(ImageColor.getcolor(str(hexColor), "RGB"))
                        # color = self.DH.AssetMaskListPolygon[self.current_imagenumber][x-len(self.DH.all_masks[self.current_imagenumber])].MaskColor
                except Exception:
                    color = np.array([255, 255, 255])
            # if self.selected_mask != x:
            color = color / 2  # not selected is half the opacity
            image[contours] = color
            x += 1
        else:
            for mask in all_masks_list:
                all_masks_list_tmp = mask.astype(
                    np.uint8
                ).copy()  # convert to an unsigned byte

                contours = cv2.Canny(all_masks_list_tmp * 255, 100, 200)
                kernelNumber = 2
                kernel = np.ones((kernelNumber, kernelNumber), np.uint8)
                contours = cv2.dilate(contours.astype(np.uint8), kernel, iterations=1)
                contours = contours.astype(bool)

                # not selected is half the opacity
                try:
                    color = AttributeColorDict[AttributeList[x]]
                except:
                    color = np.array([255, 255, 255])
                color = color / 2
                image[contours] = color
                x += 1
        end = time.time()
        self.ConstractedImage = (
            image.copy()
        )  # an image that contains all of the masks upplied to image
        return image

    def apply_all_masks_and_contours_new(self, image, all_masks_list):
        """
        After all the masks have been converted to BOOL then we apply them to the image
        This is for after the second mask as been applied
        """
        image_tmp = image.copy()

        all_masks_list_tmp = all_masks_list.astype(
            np.uint8
        ).copy()  # convert to an unsigned byte
        contours, hierarchy = cv2.findContours(
            all_masks_list_tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_None
        )
        redImg = np.zeros(image.shape, image.dtype)
        color = [0, 0, 255]
        redImg[:, :] = color
        redMask = cv2.bitwise_and(redImg, redImg, mask=all_masks_list_tmp * 255)

        cv2.addWeighted(redMask, 0.1, image, 1, 0, image)
        # for i in range(len(contours)):
        #     cv2.drawContours(image, contours, i, (0,0,0), 3)
        for i in range(len(contours)):
            cv2.drawContours(image, contours, i, (0, 0, 255), 2)
        return image

    def loadMaskSelectionOnly(self, AddedAnnotation=False):
        """
        Assumes tthat self.ConstractedImage has already been computed
        """
        import MCCocoTools
        from PIL import ImageColor

        try:
            TempConstractedImage = self.ConstractedImage.copy()
            if self.selected_mask_origin == "BOOL":
                mask = self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                    self.current_imagenumber
                ][self.selected_mask]
                # color = self.DH.AssetMaskListBool[self.current_imagenumber][self.selected_mask].MaskColor
                # Get Color form MAster combobox
                Attribute = self.DH.AssetMaskDictionaryBool[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber][
                    self.selected_mask
                ].BBWidget.MaskPropertiesWidgetLabelcomboBox.text()
                if Attribute == None:
                    indexRegion = self.MasterMaskLabelcomboBox.currentIndex()
                else:
                    indexRegion = self.MasterMaskLabelcomboBox.findText(Attribute)
                try:
                    hexColor = self.MasterMaskLabelcomboBox.itemData(
                        indexRegion, QtCore.Qt.BackgroundRole
                    ).name()
                    color = ImageColor.getcolor(str(hexColor), "RGB")
                except:
                    color = [255, 255, 255]

            elif self.selected_mask_origin == "POLYGON":
                # color = self.DH.AssetMaskListPolygon[self.current_imagenumber][self.selected_mask].MaskColor
                mask = MCCocoTools.PolyToBit(
                    self.DH.all_worm_mask_points_y_slot[
                        self.DH.BLobj.get_current_condition()
                    ][self.current_imagenumber][self.selected_mask].copy(),
                    self.DH.all_worm_mask_points_x_slot[
                        self.DH.BLobj.get_current_condition()
                    ][self.current_imagenumber][self.selected_mask].copy(),
                    self.DH.BLobj.groups["default"]
                    .conds[self.DH.BLobj.get_current_condition()]
                    .getImage(self.current_imagenumber),
                )
                Attribute = self.DH.AssetMaskDictionaryPolygon[
                    self.DH.BLobj.get_current_condition()
                ][self.current_imagenumber][
                    self.selected_mask
                ].BBWidget.MaskPropertiesWidgetLabelcomboBox.text()
                indexRegion = self.MasterMaskLabelcomboBox.findText(Attribute)
                hexColor = self.MasterMaskLabelcomboBox.itemData(
                    indexRegion, QtCore.Qt.BackgroundRole
                ).name()
                color = ImageColor.getcolor(str(hexColor), "RGB")

            all_masks_list_tmp = mask.astype(np.uint8).copy()
            contours = cv2.Canny(all_masks_list_tmp * 255, 100, 200)
            kernel = np.ones((2, 2), np.uint8)
            contours = cv2.dilate(contours.astype(np.uint8), kernel, iterations=1)
            contours = contours.astype(bool)
            if AddedAnnotation == True:
                self.ConstractedImage[contours] = color
            TempConstractedImage[contours] = color

            pixon = QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    TempConstractedImage,
                    TempConstractedImage.shape[1],
                    TempConstractedImage.shape[0],
                    QtGui.QImage.Format.Format_RGB888,
                )
            )

            self.viewer.setPhoto(pixon, fit_in_view_state=False)

        except Exception as e:
            logger.exception(e)

    def GetActiveChannels(self, image):
        """
        False is the value that is currently active
        """
        import numpy as np

        from celer_sight_ai.gui.custom_widgets.channel_picker_widget import (
            ChannelPickerWidget,
        )

        # list all widgets in the channel picker widget
        checked_channels = self.channel_picker_widget.get_checked_channels()

        return checked_channels

    def appendMaskToScene(self, object_dict):
        """Creates the graphics item from the mask object that will
        be added to the scene. Runs after the create_annotation_object() method and
        when we switch images.

        Args:
            object_dict (dict): _description_
        """
        from celer_sight_ai.gui.custom_widgets.scene import (
            BitMapAnnotation,
            PolygonAnnotation,
        )

        image_uuid = object_dict["image_uuid"]
        mask_uuid = object_dict["mask_uuid"]
        mask_type = object_dict["mask_type"]

        image_object = self.DH.BLobj.get_image_object_by_uuid(image_uuid)
        if not image_object:
            return
        mask_object = image_object.masks[mask_uuid]
        mask_annotation = mask_object.get_array()

        class_id = mask_object.class_id
        unique_id = mask_object.unique_id
        if mask_type == "polygon":
            tmp_item = PolygonAnnotation(
                self,
                image_object.unique_id,
                mask_annotation,
                class_id,
                unique_id,
                track_unique_id=mask_object._annotation_track_id,
                is_suggested=mask_object.is_suggested,
                score=mask_object.score,
                _disable_spawn_extra_items=image_object._disable_overlay_annotation_items,
            )
            scene_items_to_add = tmp_item.get_graphic_scene_items()
            tmp_item.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False
            )
            tmp_item.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
            [self.viewer._scene.addItem(i) for i in scene_items_to_add if i]
            tmp_item.canDetectChange = True
        elif mask_type == "bitmap":
            tmp_item = BitMapAnnotation(
                self, mask_object, mask_annotation, class_id, unique_id
            )
            scene_items_to_add = [
                tmp_item
            ]  # maybe add more here later like in -> get_graphic_scene_items()
            tmp_item.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False
            )
            [self.viewer._scene.addItem(i) for i in scene_items_to_add]
            tmp_item.canDetectChange = True

    def clearViewerOnRefresh(self, with_masks=True):
        """
        The function `clearViewerOnRefresh` clears the items in a QGraphicsScene object and performs
        additional actions related to a viewer object.

        Returns:
          None
        """
        from celer_sight_ai.gui.custom_widgets.scene import (
            BackgroundGraphicsItem,
            BitMapAnnotation,
        )

        self.loading_tile_inference_graphic_items = []
        if with_masks:
            for item in self.viewer._scene.items():
                # remove the previous image from the scene
                self.viewer._photo.setPixmap(QtGui.QPixmap())
                if not isinstance(item, BackgroundGraphicsItem):
                    self.viewer._scene.removeItem(item)
                elif isinstance(item, BitMapAnnotation):
                    self.viewer._scene.removeItem(item)
        if self.viewer.magic_brush_cursor:
            if self.viewer.magic_brush_cursor in self.viewer._scene.items():
                self.viewer._scene.removeItem(self.viewer.magic_brush_cursor)
        if hasattr(self.viewer, "h_guide_magic_tool"):
            if self.viewer.h_guide_magic_tool in self.viewer._scene.items():
                self.viewer._scene.removeItem(self.viewer.h_guide_magic_tool)
        if hasattr(self.viewer, "v_guide_magic_tool"):
            if self.viewer.v_guide_magic_tool in self.viewer._scene.items():
                self.viewer._scene.removeItem(self.viewer.v_guide_magic_tool)
        if self.viewer.i_am_drawing_state == True:
            self.viewer.completeDrawingPolygon()
        if self.viewer.SkGb_during_drawing == True:
            self.viewer.placeSkGbFinish(pos=None, COMPLETE=False)
        if self.viewer.aa_tool_draw and self.viewer.during_drawing_bbox:
            self.viewer.completeDrawing_Bounding_Box()
        return

    def get_mask_color_from_class(self, class_id=None):
        """
        If the class_id is in the dictionary of classes, then use the color from the dictionary, otherwise
        use the color from the button

        Args:
          class_id: the class id of the object you want to get the color for.

        Returns:
          The color of the mask.
        """
        return self.custom_class_list_widget.classes[class_id].color

    def set_mask_color_from_class(self, graphics_view_object, class_id=None):
        """
        It takes a polygon object and a class id, and sets the color of the polygon object to the color of
        the class id

        Args:
          polygon_object: the polygon object to be modified
          class_id: the class id of the object

        Returns:
          The polygon_object is being returned.
        """

        colorToUseNow = self.get_mask_color_from_class(class_id)
        somepen = QtGui.QPen(
            QtGui.QColor(colorToUseNow[0], colorToUseNow[1], colorToUseNow[2])
        )
        somepen.setWidth(
            self.viewer.QuickTools.lineWidthSpinBoxPolygonTool.value()
        )  # self.MaskWidth)
        somepen.setCapStyle(
            self.ColorPrefsViewer.MyStyles[self.ColorPrefsViewer.CurrentPenCapStyle]
        )
        somepen.setStyle(
            self.ColorPrefsViewer.MyStyles[self.ColorPrefsViewer.CurrentPenStyle]
        )
        somepen.setCosmetic(True)  # so that stroke is always constant
        graphics_view_object.setPen(somepen)
        return graphics_view_object

    def delete_image_with_button(self, object):
        """
        Deletes an image from the data
        object = {
            "group_name" : str,
            "treatment_name : str,
            "image_uuid" : int
        }
        """
        logger.info(f"Deleting image with button {object}")
        treatment_object = self.DH.BLobj.get_condition_by_uuid(object["treatment_uuid"])
        if not treatment_object:
            treatment_object = self.DH.BLobj.get_treatment_object_from_image_uuid(
                object["image_uuid"]
            )
        if not treatment_object:
            return
        image_object = treatment_object.images[object["image_uuid"]]
        # delete the image and the button
        try:
            image_object.myButton.button_instance.deleteCurrentImage(reload_image=True)
        except:
            logger.exception("Error deleting image with button")

    def load_all_current_image_annotations(self, img_uuid):
        from celer_sight_ai.gui.custom_widgets.scene import (
            BitMapAnnotation,
            PolygonAnnotation,
        )

        # get image object
        io = self.DH.BLobj.get_image_object_by_uuid(image_uuid=img_uuid)
        if not io or io._masks_spawned:
            return
        io._masks_spawned = True
        # load mask objects to scene
        masks_to_remove = []
        for mask_idx in range(len(io.masks)):

            mask_obj = io.masks[mask_idx]
            if mask_obj.mask_type == "polygon":
                try:
                    tmpItem = PolygonAnnotation(
                        self,  # parent
                        io.unique_id,  # image uuid
                        mask_obj.polygon_array,  # array
                        mask_obj.class_id,  # class name
                        mask_obj.unique_id,  # unique id
                        track_unique_id=mask_obj._annotation_track_id,
                        is_suggested=mask_obj.is_suggested,
                        score=mask_obj.score,
                        _disable_spawn_extra_items=io._disable_overlay_annotation_items,
                    )
                except Exception:
                    logger.error(
                        f"Error loading polygon annotation {mask_obj.unique_id}"
                    )
                    config.global_signals.notify_error_signal.emit(
                        f"Error loading polygon annotation {mask_obj.unique_id}"
                    )
                    # delete mask object
                    masks_to_remove.append(mask_obj.unique_id)
                scene_items_to_add = tmpItem.get_graphic_scene_items()

            elif mask_obj.mask_type == "bitmap":
                tmpItem = BitMapAnnotation(
                    self,  # parent
                    mask_obj,
                    mask_obj.get_array(),  # array
                    mask_obj.class_id,  # class name
                    mask_obj.unique_id,  # unique id
                )
                scene_items_to_add = [tmpItem]
            tmpItem.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            # tmpItem.removeAllPoints()
            tmpItem.pointsCreated = False
            if (
                self.viewer.MoveTool is True
            ):  # we only want to be able ot move when the MOve tool is active
                tmpItem.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            if not self.viewer.ML_brush_tool_object_state:
                tmpItem.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
                )
            if self.viewer.aa_tool_draw:
                tmpItem.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
                )
            # # required for focusItemChanged signal to work:
            [
                self.viewer._scene.addItem(i)
                for i in scene_items_to_add
                if i not in self.viewer.scene().items()
            ]
            tmpItem.canDetectChange = True
        # delete the masks that were not loaded
        for mask_obj in masks_to_remove:
            del self.io.masks[mask_obj]

    def change_image_hook_method(self, object):
        logger.debug("Image change hook running")
        # A hook that runs everytime the image in the viewport changes updates to a different image
        pass

    def load_main_scene_and_fit_in_view(self):
        self.load_main_scene(fit_in_view=True)

    def load_main_scene(
        self,
        image_number: int = 0,
        from_spot: bool = True,
        fit_in_view: bool = False,
        fast_load_ram: bool = False,  # to quickly apply brightness updates
    ):
        bbox_rect = self.viewer.mapToScene(
            self.viewer.viewport().geometry()
        ).boundingRect()
        config.viewport_bounding_box = [
            bbox_rect.x(),
            bbox_rect.y(),
            bbox_rect.width(),
            bbox_rect.height(),
        ]
        self.clearViewerOnRefresh()

        # remove all deep zoom items
        while config._deepzoom_pixmaps:
            self.viewer._scene.removeItem(config._deepzoom_pixmaps.pop()[0])
        # self.viewer._photo.setPixmap(QtGui.QPixmap())
        current_condition = self.DH.BLobj.get_current_condition()
        if not current_condition:
            # set the _photo object to empty
            self.viewer._photo.setPixmap(QtGui.QPixmap())
            # update background
            self.viewer.update()
            return
        current_condition_object = self.DH.BLobj.groups["default"].conds[
            current_condition
        ]
        #  Case where We have an empty scene --> Drag and Drop images is shown
        if (
            len(self.DH.BLobj.groups["default"].conds) == 0
            and len(current_condition_object.images) == 0
        ):
            self.no_image_displayed = True
            DisplayedImage = cv2.imread("data/icons/Drag-Drop-icon-viewer.png")
            DisplayedImage = cv2.cvtColor(DisplayedImage, cv2.COLOR_BGR2RGB)
            self.currentUsedPixmap = self.DH.BLobj.get_image_pixmap(DisplayedImage)
            self._zoom = 0
            self.channel_picker_widget.clear_channels()
            if self.currentUsedPixmap and not self.currentUsedPixmap == 0:
                self._empty = False
                self.viewer.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
                # Convert to QPixmap if it's a tuple of QImages
                if isinstance(self.currentUsedPixmap, tuple):
                    pixmap = QtGui.QPixmap.fromImage(self.currentUsedPixmap[0])
                else:
                    pixmap = self.currentUsedPixmap
                self.viewer._photo.setPixmap(pixmap)
                self.viewer._photo.setZValue(
                    -50
                )  # -49 is interactive deep zoom previous elements and  - 48 is current element on the deep zzom
                # set pixmap size to the actual size of the image
            else:
                return
            self.viewer.centerOn(
                self.viewer._photo.boundingRect().x()
                + (self.viewer._photo.boundingRect().width() // 2),
                self.viewer._photo.boundingRect().y()
                + (self.viewer._photo.boundingRect().height() // 2),
            )

            return

        io = self.DH.BLobj.get_current_image_object()

        if isinstance(io, type(None)):
            return

        if not io:
            logger.warning("No image object found, skipping load main scene.")
            return

        if (
            io._is_ultra_high_res
            and self.viewer.particle_analysis_settings_widget._is_ui_spawned
        ):
            # do not allow for particle analysis on ultra high res images
            self.viewer.particle_analysis_settings_widget.despawn()

        # set flag to off, to make sure that masks are spawned later
        io._masks_spawned = False

        # set the config.viewport_bounding_box to fit the whole image
        # this will help aviod some bugs with high res images that generate
        # unessecary deep zoom items

        config.viewport_bounding_box = [0, 0, io.SizeX, io.SizeY]

        condition_uuid = self.DH.BLobj.get_current_condition_uuid()

        # start the process of getting the image data and update the scene widget
        config.global_signals.load_main_scene_gather_image_threaded_signal.emit(
            {
                "group_id": self.DH.BLobj.get_current_group(),
                "cond_uuid": condition_uuid,
                "img_uuid": io.unique_id,
                "fast_load_ram": fast_load_ram,
                "fit_in_view": fit_in_view,
            }
        )

    def get_current_thumbnail(self):
        if (
            len(self.DH.BLobj.groups["default"].conds) == 0
            or len(
                self.DH.BLobj.groups["default"]
                .conds[self.DH.BLobj.get_current_condition()]
                .images
            )
            == 0
        ):
            return
        DisplayedImage = (
            self.DH.BLobj.groups["default"]
            .conds[self.DH.BLobj.get_current_condition()]
            .getImage(self.current_imagenumber, to_uint8=True, for_viewport=True)
        )
        DisplayedImage = cv2.cvtColor(DisplayedImage, cv2.COLOR_BGR2RGB)
        self.currentUsedPixmap = self.DH.BLobj.get_image_pixmap(DisplayedImage)
        # get the bounding box of the viewport in the scene coordinates
        bbox_rect = self.viewer.mapToScene(
            self.viewer.viewport().geometry()
        ).boundingRect()
        config.viewport_bounding_box = [
            bbox_rect.x(),
            bbox_rect.y(),
            bbox_rect.width(),
            bbox_rect.height(),
        ]
        return self.currentUsedPixmap

    @config.threaded
    def load_main_scene_gather_image(self, signal_object={}):
        # create a thread with threader

        from celer_sight_ai import config
        from celer_sight_ai.core.threader import RacerThread

        logger.info("Reading image for scene progressively (threaded)")
        group_id = signal_object["group_id"]
        cond_uuid = signal_object["cond_uuid"]
        img_uuid = signal_object["img_uuid"]
        fast_load_ram = signal_object["fast_load_ram"]
        fit_in_view = signal_object["fit_in_view"]

        #  case where we have a preview image ready
        #  In this case we need to load both the preview
        #  and the original in a threaded race

        condition_object = self.DH.BLobj.get_condition_by_uuid(cond_uuid)
        if not condition_object:
            logger.warning("Condition object not found.")
            config.global_signals.load_main_scene_signal.emit()
            return

        image_idx = condition_object.images.get_index(img_uuid)
        if isinstance(image_idx, type(None)) or image_idx >= len(
            condition_object.images
        ):
            # load image 0 by clicking on it
            image_idx = 0
            if len(self.images_preview_graphicsview.visible_buttons) > 0:
                self.images_preview_graphicsview.visible_buttons[
                    0
                ].button_instance.click()
                return
        if len(condition_object.images) <= image_idx:
            logger.warning("Image number out of bounds.")
            config.global_signals.load_main_scene_signal.emit()
            return
        io = condition_object.images[img_uuid]
        if io._is_ultra_high_res:
            # load once first required for ultra high res
            try:
                # case of ultra high res, read image normally for viewport
                # which will read form the deepview object
                self.load_main_scene_read_image(
                    {
                        "group_id": group_id,
                        "cond_uuid": cond_uuid,
                        "img_uuid": img_uuid,
                        "fast_load_ram": fast_load_ram,
                        "fit_in_view": fit_in_view,
                    }
                )
            except Exception:
                logger.debug("Loading image normally.")
                self.load_main_scene_read_image(
                    {
                        "group_id": group_id,
                        "cond_uuid": cond_uuid,
                        "img_uuid": img_uuid,
                        "fast_load_ram": fast_load_ram,
                        "fit_in_view": fit_in_view,
                    }
                )
                return

        self.no_image_displayed = False  # mark as image loaded

        if io.thumbnailGenerated:
            # if image is ultra high res, just read it as low resolution once to fill the background
            if io._is_ultra_high_res:
                # check if tiles have been generated
                if io._is_pyramidal:
                    logger.debug(
                        "Ultra high res image is pyramidal, thus we dont have to display anything further."
                    )

                    return
                logger.debug("Reloading with Ultra high res image's thumbnail.")
                self.load_main_scene_display_image(signal_object)
                return
            logger.debug("Reading image through racing thread.")
            RacerThread(
                func1=self.load_main_scene_display_image,  # this does a quick update from thumbnail
                func2=self.load_main_scene_read_image,  # this reads the full update
                func1_kwargs={"signal_object": signal_object},
                func2_kwargs={"signal_object": signal_object},
            ).run()
            return
        else:
            # load image normally and then send the signal to display it
            # also, store the thumbnail
            logger.debug("Loading image normally.")
            self.load_main_scene_read_image(
                {
                    "group_id": group_id,
                    "cond_uuid": cond_uuid,
                    "img_uuid": img_uuid,
                    "fast_load_ram": fast_load_ram,
                    "fit_in_view": fit_in_view,
                }
            )
            return

    def refresh_main_scene_image_only(self):
        raise NotImplementedError("Not implemented")

    def refresh_main_scene_pixmap_only(self, new_image, tile=None):
        logger.info("Refreshing image only")
        # quick refresh on just the main image
        pixmap = self.DH.BLobj.get_image_pixmap(new_image)
        self.viewer.setPhoto(pixmap, fit_in_view_state=False)

    def load_main_scene_read_image(self, signal_object={}):
        logger.info("Loading Scene")
        group_id = signal_object["group_id"]
        cond_uuid = signal_object["cond_uuid"]
        img_uuid = signal_object["img_uuid"]
        fast_load_ram = signal_object["fast_load_ram"]
        fit_in_view = signal_object["fit_in_view"]
        condition_object = self.DH.BLobj.get_condition_by_uuid(cond_uuid)
        if not condition_object:
            logger.warning("Condition object not found.")
            config.global_signals.load_main_scene_signal.emit()
            return
        if self.current_imagenumber >= len(condition_object.images):
            logger.warning("Attempted to read image number out of bounds")
            config.global_signals.load_main_scene_signal.emit()
            return
        img_idx = condition_object.images.get_index(img_uuid)
        if isinstance(img_idx, type(None)) or len(condition_object.images) <= img_idx:
            logger.warning("Image number out of bounds.")
            config.global_signals.load_main_scene_signal.emit()
            return

        do_channel_filter = False
        checked_channels = self.channel_picker_widget.get_checked_channels()
        io = self.DH.BLobj.get_image_object_by_uuid(img_uuid)
        refresh_channels = False
        # if the current available channels are different from the previous ones, clear the channel picker
        if io.channel_list:
            if [config.ch_as_str(i).lower() for i in io.channel_list] != [
                config.ch_as_str(i).lower() for i in self.channel_picker_widget.channels
            ]:
                refresh_channels = True

        if not condition_object.images[img_uuid].channel_list or refresh_channels:

            do_channel_filter = False
            channel_names_to_filter = None
            # check with cached channels
            if refresh_channels:
                checked_channels = [
                    i
                    for i in io.channel_list
                    if config.get_visible_channel_cache(i, True)
                ]
        else:

            # remove any changes that are not being used
            image_channels_lower = [
                config.ch_as_str(i).lower()
                for i in condition_object.images[img_uuid].channel_list
            ]
            checked_channels = [
                i for i in checked_channels if str(i).lower() in image_channels_lower
            ]
            do_channel_filter = True
            channel_names_to_filter = checked_channels

        DisplayedImage = condition_object.getImage(
            img_uuid,
            to_uint8=False,
            do_channel_filter=do_channel_filter,
            channel_names_to_filter=channel_names_to_filter,
            fast_load_ram=fast_load_ram,
            for_interactive_zoom=True,
            for_thumbnail=True,
            avoid_loading_ultra_high_res_arrays_normaly=True,
        )
        config.global_signals.spawn_channels_signal.emit(
            io.get_channel_name_and_colors()
        )
        if isinstance(DisplayedImage, type(None)):
            logger.error("Displayed image is nan!")
            return

        DisplayedImage = self.handle_adjustment_to_image(
            DisplayedImage, to_uint8=True
        )  # brightness equalization
        # set image as thumbnail
        if not io.thumbnailGenerated:
            condition_object.set_thumbnail(img_uuid, DisplayedImage)
        config.load_main_scene_read_image = False
        config.global_signals.load_main_scene_display_image_signal.emit(
            {
                "image": DisplayedImage,
                "group_id": group_id,
                "cond_uuid": cond_uuid,
                "img_uuid": img_uuid,
                "fast_load_ram": fast_load_ram,
                "fit_in_view": fit_in_view,
            }
        )
        config.global_signals.load_all_current_image_annotations_signal.emit(img_uuid)

    def load_main_scene_display_image(self, signal_object={}):
        # Handle concurent loading IF it happends
        DisplayedImage = signal_object.get("image")
        group_id = signal_object["group_id"]
        cond_uuid = signal_object["cond_uuid"]
        img_uuid = signal_object["img_uuid"]
        fit_in_view = signal_object["fit_in_view"]
        fast_load_ram = signal_object["fast_load_ram"]

        condition_object = self.DH.BLobj.get_condition_by_uuid(cond_uuid)
        if not condition_object:
            logger.warning("Condition object not found.")
            # reload the scene
            config.global_signals.load_main_scene_signal.emit()
            return
        img_id = condition_object.images.get_index(img_uuid)

        if isinstance(img_id, type(None)) or img_id >= len(condition_object.images):
            logger.warning("Image number out of bounds.")
            config.global_signals.load_main_scene_signal.emit()
            return
        image_object = condition_object.images[img_uuid]
        if isinstance(DisplayedImage, type(None)):
            # get from thumbnail
            try:
                DisplayedImage = condition_object.get_thumbnail(img_uuid)
                # apply brightness and contrast
                DisplayedImage = self.handle_adjustment_to_image(
                    DisplayedImage, to_uint8=True
                )

            except Exception as e:
                logger.error(e)
                return
        while self.during_load_main_scene_display is True:
            time.sleep(0.0001)
        self.during_load_main_scene_display = True

        try:

            # DisplayedImage is the result of this block << Qt >>
            self.viewer.LabelNumberViewer.setText("Image: " + str(img_id + 1))
            self.viewer.updateMaskCountLabel()
            if self.viewer.i_am_drawing_state == True:
                self.viewer.completeDrawingPolygon()

            # magic box graphic item << Qt >>
            if self.viewer.i_am_drawing_state_bbox == True:
                try:
                    self.croppedItem = CropItem(
                        self.currentUsedPixmap,
                        QtCore.QRectF(
                            self.viewer.aa_tool_bb_first_x,
                            self.viewer.aa_tool_bb_first_y,
                            self.viewer.last_bbox_x - self.viewer.aa_tool_bb_first_x,
                            self.viewer.last_bbox_y - self.viewer.aa_tool_bb_first_y,
                        ),
                        QtCore.QRectF(
                            0, 0, DisplayedImage.shape[1], DisplayedImage.shape[0]
                        ),
                    )
                    self.viewer._scene.addItem(self.croppedItem)
                except Exception as e:
                    # print traceback
                    logger.error(e.__traceback__)
                    self.viewer.i_am_drawing_state_bbox = False

            # get pixmap from image  << Qt >>
            self.currentUsedPixmap = self.DH.BLobj.get_image_pixmap(DisplayedImage)
            # get current image object size x size y

            size_x = image_object.SizeX

            self.viewer.ensureVisible(self.viewer._photo)
            self.viewer.sceneItemsListUndo = []
            self.undoStack.clear()
            # add by pixmap item

            self.viewer.setPhoto(
                self.currentUsedPixmap,
                fit_in_view_state=False,
                rescaled_width=size_x if DisplayedImage.shape[1] != size_x else None,
            )

            if (
                self.viewer.rm_Masks_STATE is True
                or self.viewer.ML_brush_tool_object_state is True
            ):
                self.viewer.makeAllGraphicItemsNonSelectable()
            self.viewer.polyPreviousSelectedItems = []

            if fit_in_view:
                self.viewer.fitImageInView()
            self.during_load_main_scene_display = False

            # force update tiles
            self.viewer.check_and_remove_deepzoom_tiles_that_dont_belong()

            self.viewer.check_and_update_high_res_slides(force_update=True)
            config.global_signals.load_all_current_image_annotations_signal.emit(
                img_uuid
            )

        except Exception as e:
            self.during_load_main_scene_display = False
            tb_str = traceback.format_exception(e)
            tb_str = "".join(tb_str)
            logger.error("An error occurred: %s\nTraceback:\n%s", e, tb_str)
        self.during_load_main_scene_display = False
        self.during_scene_refresh = False
        # now load inference tiles if needed
        config.global_signals.spawn_inference_tile_graphics_items_signal.emit()
        QtWidgets.QApplication.processEvents()

    def addClassItem(
        self,
        class_name=None,
        class_uuid=None,
        parent_uuid=None,
        is_user_defined=True,
        is_particle=False,
        parent_class_name=None,  # if set, when we add the class in the future
        # this class will become the child of the matching parent class
        children_classes_uuids=[],
    ):
        import random

        from celer_sight_ai import config

        # if not class name provided, generate a class name
        if not class_name:
            classes_without_children = self.DH.BLobj.get_all_top_level_classes()
            if len(classes_without_children):
                lastItem = self.custom_class_list_widget.classes[
                    classes_without_children[-1]
                ].text()
                lastItem = lastItem.split("_")

                lastPart = lastItem[-1]
                if lastPart.isnumeric():
                    lastNumeric = int(lastPart)
                    AllExceptLast = lastItem[:-1]
                    class_name = "_".join(AllExceptLast) + "_" + str(lastNumeric + 1)
                else:
                    class_name = "_".join(lastItem) + "_1"
            else:
                class_name = "Class_1"

        # item count

        c = self.custom_class_list_widget.count()
        while True:
            if len(config.bright_colors) > c:
                if not self.DH.BLobj.is_color_in_any_class(config.bright_colors[c]):
                    color = config.bright_colors[c]
                    break
                else:
                    c += 1
                    continue
            else:
                # generate a random rgb color:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )

                break
        return self.custom_class_list_widget.addClass(
            class_name,
            class_uuid=class_uuid,
            parent_class_uuid=parent_uuid,
            color=color,
            is_user_defined=is_user_defined,
            is_particle=is_particle,
            parent_class_name=parent_class_name,
            children_classes_uuids=children_classes_uuids,
        )

    def get_current_class(self) -> str:
        """
        It returns the text of the currently selected item in the list widget.

        Returns:
          The current class in the left list widget (str).
        """
        return self.custom_class_list_widget.currentItemWidget().text()

    def remove_class_item(self, class_uuid=None):
        # removes the current or specified selected class, and should also remove the masks
        if not class_uuid:
            class_uuid = self.custom_class_list_widget.getItemWidget(
                self.custom_class_list_widget.currentRow()
            ).unique_id

        # remove all child items
        child_items = self.custom_class_list_widget.get_all_clild_classes_items(
            class_uuid
        )
        child_items = child_items[::-1]
        parent_uuid = self.custom_class_list_widget.classes[
            class_uuid
        ].parent_class_uuid
        if parent_uuid:
            self.custom_class_list_widget.classes[
                parent_uuid
            ].children_class_uuids.remove(class_uuid)
        for cu in child_items:
            self.remove_class_item(cu.unique_id)

        # find the row of the item with the class_uuid
        row = self.custom_class_list_widget.get_row_from_uuid(class_uuid)
        if row is not None:  # Add null check
            del self.custom_class_list_widget.classes[class_uuid]
            self.custom_class_list_widget.takeItem(row)

        # get all masks with that class_uuid
        all_masks = [
            i for i in self.DH.BLobj.get_all_mask_objects() if i.class_id == class_uuid
        ]
        for mask in all_masks:
            config.global_signals.deleteMaskFromMainWindow.emit(
                {"mask_uuid": mask.unique_id}
            )

        # triget a scene refresh
        config.global_signals.load_main_scene_signal.emit()

    def handle_adjustment_to_image(self, image, brightness=None, to_uint8=True):
        """
        Adds brightness and contrast
        TODO: this needs fixing,
        """
        original_type = image.dtype
        # convert data type
        original_dtype = image.dtype
        if original_dtype == np.uint8:
            max_value = 255
            min_value = 0
            image = image.astype(np.int32)
        elif original_dtype == np.uint16:
            max_value = 65535
            min_value = 0
        elif original_dtype == np.uint32:
            max_value = 4294967295
            min_value = 0
        else:
            max_value = 4294967295
            min_value = -4294967295
        if to_uint8 and original_dtype != np.uint8:
            image = cv2.normalize(
                image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
            ).astype(np.uint8)
            max_value = 255
            min_value = 0
        brightent_img = self.Brightness_adjast(image, brightness)
        brightent_img = np.clip(brightent_img, min_value, max_value)
        contrasted_image = np.clip(brightent_img, min_value, max_value)
        if to_uint8 and original_dtype != np.uint8:
            contrasted_image = contrasted_image.astype(np.uint8)
        return contrasted_image.astype(original_type)

    def Brightness_adjast(self, image_in, brightness=None):
        if brightness:
            theta = brightness / 10
        else:
            theta = self.pg1_settings_contras_slider.value() / 10
        if theta == 0:
            return image_in
        image_in = image_in * theta
        return image_in

    def contrast_adjast(self, image_in, phi=1, theta=1, maxIntensity=255.0):
        return image_in
        # Parameters for manipulating image data
        # depends on dtype of image data

        theta = self.pg1_settings_contras_slider.value()
        phi = 100  # self.Phi.value()/10
        if theta == 0 or phi == 0:
            return image_in
        x = np.arange(maxIntensity)
        y = (maxIntensity / phi) * (x / (maxIntensity / theta)) ** 0.5
        # Decrease intensity such that
        # dark pixels become much darker,
        # bright pixels become slightly dark
        newImage1 = (maxIntensity / phi) * (image_in / (maxIntensity / theta)) ** 2
        # image_out = np.array(newImage1,dtype=np.uint8)
        return newImage1

    def loadSceneSignalMethod(self, obj_list):
        """Wrapper for loadImage function after the loadSingal is triggered"""
        # if current group is not the same as the group provided, change
        from celer_sight_ai import config

        if obj_list[0] != None:
            # check if we need to change condition
            if obj_list[1] != config.user_attributes.current_condition:
                # change to current condition
                self.changeCondition(obj_list[1])
                QtWidgets.QApplication.processEvents()

            self.load_main_scene(obj_list[2])

    def loadImage(self, imagenumber=0, fit_in_view_state_image=True):
        # if imagenumber >= len() TODO:fix this
        # convert data type
        try:
            image = (
                self.DH.BLobj.groups["default"]
                .conds[self.DH.BLobj.get_current_condition()]
                .getImage(imagenumber)
            )
        except:
            image = (
                self.DH.BLobj.groups["default"]
                .conds[self.DH.BLobj.get_current_condition()]
                .getImage(0)
            )
        # if self.pg1_settings_brightness_slider.value() != 1:
        #     brightent_img= self.Brightness_adjast(image)
        if self.pg1_settings_contras_slider.value() != 0:
            brightent_img = self.Brightness_adjast(image)
            brightent_img = np.clip(brightent_img, 0, 255)
            contrasted_image = self.contrast_adjast(brightent_img)
            contrasted_image = np.clip(contrasted_image, 0, 255)
            image = contrasted_image
        # convert to pixmap
        contrasted_image = image.astype(np.uint8)
        qimage_contrast = QtGui.QImage(
            contrasted_image,
            contrasted_image.shape[1],
            contrasted_image.shape[0],
            QtGui.QImage.Format.Format_RGB888,
        )
        self.currentPixmap = QtGui.QPixmap.fromImage(qimage_contrast)
        self.viewer.setPhoto(
            self.currentPixmap, fit_in_view_state=fit_in_view_state_image
        )

    def loadImage_old(self, imagenumber=0):
        self.viewer.setPhoto(
            self.DH.BLobj.groups["default"].conds[
                self.DH.BLobj.get_current_condition()
            ][imagenumber]
        )

    def load_main_scene_if_photo(self):
        # if self.viewer.hasPhoto() == False:
        #     return
        if self.during_scene_refresh is True:
            return
        self.during_scene_refresh = True
        self.load_main_scene(self.current_imagenumber, fast_load_ram=True)

    def delete_mask(self):
        if self.selected_mask >= 0:
            del self.DH.mask_RNAi_slots[self.DH.BLobj.get_current_condition()][
                self.current_imagenumber
            ][self.selected_mask]
            self.selected_mask = -1

    def delete_all_buttons_in_tabs(self, tab_index):
        """
        Delete all of the properties that are tied to this particular condition
        Including the buttons on th emain window and MY button class
        """
        logger.debug("Deleting all buttons in tabs")

        Item = self.RNAi_list.currentItem().text()

        del self.myButtonHandler.DictThumbnail[Item]  # dictionary for all tumbnails
        del self.myButtonHandler.DictVisibility[
            Item
        ]  # Dictionary that "Hides" unsused images
        del self.myButtonHandler.DictIncludeInAnalysis[
            Item
        ]  # Dictionary that shows if an image is included in our analys
        del self.myButtonHandler.DictMaskThumbnails[Item]
        del self.myButtonHandler.DictMaskButtons[Item]

        if tab_index == 0:
            for button in self.image_preview_scrollArea_Contents.children():
                if type(button) == QtWidgets.QPushButton:
                    button.clicked.disconnect()
                button.deleteLater()
        elif tab_index == 1:
            for button in self.MaskScrollAreaWidgetContents.children():
                if type(button) == QtWidgets.QPushButton:
                    button.clicked.disconnect()

                button.deleteLater()

    def ImportDecider(self, prefolder=""):
        """
        Decides iof we are usign two channels and we need the special importer to fuse our images or not
        special importer is,..
        """
        from celer_sight_ai.MultiChannellImports import MultiChannelImporterUi

        global ChannelPickerWindow
        ChannelPickerWindow = MultiChannelImporterUi(self)
        """
        open special importer window
        """
        self.OpenFolderAsCondition()
        return

    def OpenIndiImagesForCondition(self, Prefolder=""):
        """
        Open a folder, import Only the selected Images if we have current COndiion, if not, Make a New Condition.
        """

        if Prefolder == "":
            my_dir = self.open_folder_explorer(MODE="FILE")
            if not my_dir or not my_dir[0]:  # Check if my_dir is None or empty
                return
            my_files_list = my_dir[0]
            self.PreviousNamesForFilesList = my_files_list.copy()
            if my_dir == None or my_dir == ".":
                # self.reset_all_values()
                return False
        else:
            my_dir = Prefolder
        config.global_signals.OpenIndiImagesForConditionFINISHED.emit(my_files_list)
        return

    def OpenFolderAsCondition(self, Prefolder=""):
        """
        Open a folder, import all of the images within and add the Asset buttons on the Overview tabs
        """

        # If a folder is supplied then  we open# If a folder is supplied then  we open# If a folder is supplied then  we open thatIf a folder is supplied then  we open that, otherwise we open explorer
        my_dir = ""
        if Prefolder == "":
            my_dir = self.open_folder_explorer()
            if my_dir == None or my_dir == ".":
                # self.reset_asll_values()
                return False
        else:
            my_dir = Prefolder
        my_files_list = self.list_files(my_dir)
        if len(my_files_list) == 0 or my_files_list == None:
            return False

        config.global_signals.OpenIndiImagesForConditionFINISHED.emit(my_files_list)
        # Convert my_dir to string if it's a list/tuple
        if not my_dir:
            return False
        if isinstance(my_dir, (list, tuple)):
            condition_name = os.path.basename(str(my_dir[0]))
        else:
            condition_name = os.path.basename(my_dir)
        ChannelPickerWindow.ConditionName.setText(condition_name)

    def AppendEmptyLists(self, ObjectDictionary, ListNumber):
        emptyList = []
        for i in range(ListNumber):
            emptyList.append(copy.copy([]))
        ObjectDictionary[str(self.name_of_added_listwidget)] = emptyList
        return ObjectDictionary

    def open_folder_explorer(self, MODE="FOLDER"):  # or FILE
        """
        Opens the Dialog to choose the folder to import, returns path
        """
        import os

        settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        my_dir = None
        if MODE == "FOLDER":
            DirToLoad = settings.value("LastImportImages")
            my_dir = QtWidgets.QFileDialog.getExistingDirectory(
                None, "Select a folder:", DirToLoad[0]
            )
            if isinstance(my_dir, str):
                my_dir = [my_dir]
                settings.setValue("LastImportImages", my_dir)
            else:
                settings.setValue("LastImportImages", my_dir[0])
        elif MODE == "FILE":
            DirToLoad = settings.value("LastImportImages")
            my_dir = QtWidgets.QFileDialog.getOpenFileNames(
                None, "Select a folder:", DirToLoad
            )
            if len(my_dir[0]) != 0:
                settings.setValue("LastImportImages", os.path.dirname(my_dir[0][0]))
            return my_dir
        elif MODE == "TREE":
            _f_dlg = QtWidgets.QFileDialog()
            _f_dlg.setFileMode(QtWidgets.QFileDialog.Directory)
            _f_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
            # Try to select multiple files and directories at the same time in QFileDialog
            myListView = _f_dlg.findChild(QtWidgets.QListView, "listView")
            if myListView:
                myListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

            myTreeView = _f_dlg.findChild(QtWidgets.QTreeView)
            if myTreeView:
                myTreeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

            _f_dlg.exec()
            paths = _f_dlg.selectedFiles()
            for i in reversed(range(len(paths))):
                if i == 0:
                    continue
                if str(paths[0] + "/") in paths[i]:
                    paths.pop(0)
                    break
            return [paths[-1]]

        if self.label_update(my_dir) == False:
            return None

        self.name_of_added_listwidget = ""
        # Handle case where my_dir is a list
        dir_path = my_dir[0] if isinstance(my_dir, list) else my_dir
        if dir_path is None:
            return None
        self.name_of_added_listwidget = str(
            os.path.basename(os.path.normpath(dir_path))
        )
        return my_dir

    def initialize_dictionaries(self):
        pass

    def updateDictionariesWithNewKeys(self, obj):
        """
        The function updates dictionaries with new keys based on the current item in a list, and handles
        cases where the new key already exists or is the same as the previous key.
        """
        previous_item_name = obj[0]
        new_item_name = obj[1]
        logger.debug("updateDictionariesWithNewKeys")
        if self.RNAi_list.currentItem():
            if (
                new_item_name
                not in self.DH.BLobj.groups[
                    self.DH.BLobj.get_current_group()
                ].conds.keys()
            ):
                self.DH.BLobj.groups["default"].conds[new_item_name] = (
                    self.DH.BLobj.groups["default"].conds.pop(previous_item_name)
                )

                self.DH.BLobj.set_current_condition(new_item_name)

    def previous_name_RNAi_list(self):
        logger.debug("previous_name_RNAi_list")
        # when i click on the list item i record my current and my next item
        self.prev_item_name = self.RNAi_list.currentItem()
        self.previous_item_name_RNAi_list = self.prev_item_name.text()
        self.previous_item_RNAi_list = self.RNAi_list.currentItem()
        logger.debug(f"prev_item_name {self.prev_item_name}")
        logger.debug(
            f"previous_item_name_RNAi_list {self.previous_item_name_RNAi_list}"
        )
        self.double_clicked_item = self.RNAi_list.currentItem().text()

    def current_name_RNAi_list(self):
        """
        This saves all the assets to a dictionary when we change RNAi list item NAME,
        so for example, when we renaim worms to worms1234
        """
        import copy

        logger.debug("current_name_RNAi_list")
        if self.RNAi_list.currentItem():
            self.new_item_name = self.RNAi_list.currentItem().text()
            if self.previous_item_name_RNAi_list == None:
                return
            if self.new_item_name == None:
                return
            if self.new_item_name != self.previous_item_name_RNAi_list:
                # add new keys with values witht he new name
                self.DH.image_names_all_RNAi[self.new_item_name] = self.DH.image_names
                self.DH.stacked_images_slot[self.new_item_name] = (
                    self.DH.stacked_images_slot[
                        self.previous_item_name_RNAi_list
                    ].copy()
                )
                # self.DH.view_field_dictionary_slots[ self.new_item_name] = self.DH.view_field_dictionary_slots[ self.previous_item_name_RNAi_list].copy()
                self.DH.BLobj.groups["default"].conds[self.new_item_name] = (
                    copy.deepcopy(
                        self.DH.BLobj.groups["default"].conds[
                            self.previous_item_name_RNAi_list
                        ]
                    )
                )
                self.DH.mask_RNAi_slots[self.new_item_name] = copy.deepcopy(
                    self.DH.mask_RNAi_slots[self.previous_item_name_RNAi_list]
                )
                # self.DH.dict_RNAi_attributes_all[self.new_item_name] = copy.deepcopy(self.DH.dict_RNAi_attributes_all[self.previous_item_name_RNAi_list])
                self.DH.usr_mask_RNAi_slots[self.new_item_name] = copy.deepcopy(
                    self.DH.usr_mask_RNAi_slots[self.previous_item_name_RNAi_list]
                )
                self.DH.dict_aggs_counts_all_RNAi[self.new_item_name] = copy.deepcopy(
                    self.DH.dict_aggs_counts_all_RNAi[self.previous_item_name_RNAi_list]
                )
                self.DH.dict_aggs_volume_all_RNAi[self.new_item_name] = copy.deepcopy(
                    self.DH.dict_aggs_volume_all_RNAi[self.previous_item_name_RNAi_list]
                )
                # self.DH.dict_master_mask_list[self.new_item_name] = copy.deepcopy(self.DH.dict_master_mask_list[self.previous_item_name_RNAi_list])
                self.DH.all_worm_mask_points_x_slot[self.new_item_name] = copy.deepcopy(
                    self.DH.all_worm_mask_points_x_slot[
                        self.previous_item_name_RNAi_list
                    ]
                )
                self.DH.all_worm_mask_points_y_slot[self.new_item_name] = copy.deepcopy(
                    self.DH.all_worm_mask_points_y_slot[
                        self.previous_item_name_RNAi_list
                    ]
                )
                self.DH.mask_RNAi_slots_QPoints[self.new_item_name] = copy.copy(
                    self.DH.mask_RNAi_slots_QPoints[self.previous_item_name_RNAi_list]
                )
                self.DH.dict_RNAi_attributes = {
                    "predict_masks_state": self.DH.predict_masks_state,
                    "added_to_dictionary_state": self.DH.added_to_dictionary_state,
                    "calculated_dictionary_state": self.DH.calculated_dictionary_state,
                    "masks_state_usr": self.DH.masks_state_usr.copy(),
                    "masks_state": self.DH.masks_state.copy(),
                }
                self.DH.dict_RNAi_attributes_all[self.new_item_name] = copy.deepcopy(
                    self.DH.dict_RNAi_attributes
                )
                self.DH.AssetMaskDictionary[self.new_item_name] = copy.copy(
                    self.DH.AssetMaskDictionary[self.previous_item_name_RNAi_list]
                )
                # self.DH.AssetMaskDictionaryPolygon[self.new_item_name] = copy.copy(AssetMaskDictionaryPolygon[self.previous_item_name_RNAi_list])
                self.DH.AssetMaskDictionaryBoolSettings[self.new_item_name] = copy.copy(
                    self.DH.AssetMaskDictionaryBoolSettings[
                        self.previous_item_name_RNAi_list
                    ]
                )
                # self.DH.AssetMaskDictionaryPolygonSettings[self.new_item_name] = copy.copy(self.DH.AssetMaskDictionaryPolygonSettings[self.previous_item_name_RNAi_list])

                # delete old keys with values
                del self.DH.image_names_all_RNAi[self.previous_item_name_RNAi_list]
                del self.DH.stacked_images_slot[self.previous_item_name_RNAi_list]
                del self.DH.BLobj.groups["default"].conds[
                    self.previous_item_name_RNAi_list
                ]
                del self.DH.mask_RNAi_slots[self.previous_item_name_RNAi_list]
                del self.DH.dict_RNAi_attributes_all[self.previous_item_name_RNAi_list]
                del self.DH.usr_mask_RNAi_slots[self.previous_item_name_RNAi_list]
                del self.DH.dict_aggs_counts_all_RNAi[self.previous_item_name_RNAi_list]
                del self.DH.dict_aggs_volume_all_RNAi[self.previous_item_name_RNAi_list]
                # del self.DH.dict_master_mask_list[self.previous_item_name_RNAi_list]
                del self.DH.all_worm_mask_points_x_slot[
                    self.previous_item_name_RNAi_list
                ]
                del self.DH.all_worm_mask_points_y_slot[
                    self.previous_item_name_RNAi_list
                ]
                del self.DH.mask_RNAi_slots_QPoints[self.previous_item_name_RNAi_list]
                del self.DH.AssetMaskDictionaryBoolSettings[
                    self.previous_item_name_RNAi_list
                ]
                # del self.DH.AssetMaskDictionaryPolygonSettings[self.previous_item_name_RNAi_list]
                self.DH.BLobj.set_current_condition(self.new_item_name)
                # AddButtonHandler classes also need to be updated...
                self.myButtonHandler.UpdateDicts(
                    self.previous_item_name_RNAi_list, self.new_item_name
                )
        else:
            return

    def switch_treatment_onchange(self, clicked_treatment_widget=None):
        """
        When we change condition from The self.RNAi_list remove last condition
        """
        logger.debug("delete_both_tabs_onchange")
        if not clicked_treatment_widget:
            return
        self.double_clicked_item = None
        logger.debug("switch_treatment_onchange")
        reload_view = False
        current_treatment_widget = self.get_current_treatment_widget()
        new_treatment_name = clicked_treatment_widget.text()
        if not new_treatment_name:
            logger.error(f"Treatment {new_treatment_name} not found in RNAi list")
            return
        if self.previous_clicked_treatment_item == clicked_treatment_widget:
            logger.debug(
                f"Treatment {new_treatment_name} is already the current treatment"
            )
            return
        # clear any selected buttons
        self.images_preview_graphicsview.selected_buttons.clear()
        self.images_preview_graphicsview.selected_buttons.append(0)
        self.DH.BLobj.set_current_condition(new_treatment_name)

        self.myButtonHandler.ShowNewCondition(Mode="IMAGE")
        reload_view = True
        self.setCurrentImageNumber(0)
        self.previous_imagenumber = 0

        self.images_preview_graphicsview.update_visible_buttons(
            clicked_treatment_widget, force_update=True
        )

        self.previous_clicked_treatment_item = clicked_treatment_widget
        if reload_view:
            self.load_main_scene(self.current_imagenumber, fit_in_view=True)

    def switch_RNAi_Ui(self, tab_index=0, element_width=2):
        """
        Old function,needs to change
        """
        # try:
        #     if len(self.RNAi_list.count())==1:
        #         return
        # except:
        #     return

        self.all_stacked_images = []
        if (
            len(
                self.DH.BLobj.groups["default"].conds[
                    self.DH.BLobj.get_current_condition()
                ]
            )
            == 0
        ):
            return

        # QtWidgets.QApplication.processEvents()

        # load all states from the current item that has just been clicked
        current_item = self.RNAi_list.currentItem().text()
        # self.previous_item_name_RNAi_list = self.RNAi_list.currentItem().text()
        self.DH.predict_masks_state = self.DH.dict_RNAi_attributes_all[current_item][
            "predict_masks_state"
        ]
        self.DH.added_to_dictionary_state = self.DH.dict_RNAi_attributes_all[
            current_item
        ]["added_to_dictionary_state"]
        self.DH.calculated_dictionary_state = self.DH.dict_RNAi_attributes_all[
            current_item
        ]["calculated_dictionary_state"]
        self.DH.masks_state_usr = self.DH.dict_RNAi_attributes_all[current_item][
            "masks_state_usr"
        ].copy()
        self.DH.masks_state = self.DH.dict_RNAi_attributes_all[current_item][
            "masks_state"
        ].copy()

        # all all assets
        # self.DH.image_names = self.DH.image_names_all_RNAi[current_item].copy()

        self.all_stacked_images = self.DH.stacked_images_slot[current_item]
        # self.DH.view_field_list = self.DH.view_field_dictionary_slots[current_item].copy()
        # self.DH.pixon_list_opencv = self.DH.BLobj.groups['default'].conds[current_item].copy()
        self.DH.all_masks = self.DH.mask_RNAi_slots[current_item].copy()
        self.DH.all_masks_usr = self.DH.usr_mask_RNAi_slots[current_item].copy()
        # self.DH.master_mask_list = self.DH.dict_master_mask_list[current_item].copy()
        self.DH.all_worm_mask_points_x = self.DH.all_worm_mask_points_x_slot[
            current_item
        ].copy()
        self.DH.all_worm_mask_points_y = self.DH.all_worm_mask_points_y_slot[
            current_item
        ].copy()

        iter_buttons = 0
        icon = QtGui.QIcon()
        buttonz_list = []
        self.num_elem_width = element_width
        # def add_buttons(self, MainWindow, stack_images):
        # self.image_preview_scrollArea.setWidget(self.image_preview_scrollArea_Contents)
        positions = [(i, j) for i in range(100) for j in range(self.num_elem_width)]
        self.values = np.array(
            [
                i
                for i in range(
                    len(
                        self.DH.BLobj.groups["default"].conds[
                            self.DH.BLobj.get_current_condition()
                        ]
                    )
                )
            ]
        )
        self.sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)

        for position, value in zip(positions, self.values):
            iter_buttons += 1
            buttonz_list.append(QtWidgets.QPushButton(str(iter_buttons)))
            buttonz_list[iter_buttons - 1].setSizePolicy(self.sizePolicy)
            buttonz_list[iter_buttons - 1].setMinimumSize(QtCore.QSize(0, 80))
            buttonz_list[iter_buttons - 1].setMaximumSize(QtCore.QSize(180, 180))
            buttonz_list[iter_buttons - 1].setCheckable(True)
            buttonz_list[iter_buttons - 1].setText("")
            self.imgon = self.DH.BLobj.groups["default"].conds[
                self.DH.BLobj.get_current_condition()
            ][iter_buttons - 1]
            self.imgoff = self.imgon.astype(np.uint8)
            self.imgon = cv2.cvtColor(self.imgon, cv2.COLOR_BGR2RGB)
            self.imgon = QtGui.QImage(
                self.imgon,
                self.imgon.shape[1],
                self.imgon.shape[0],
                QtGui.QImage.Format.Format_RGB888,
            )
            self.pixon = QtGui.QPixmap.fromImage(self.imgon)
            self.pixon_list.append(self.pixon)
            icon.addPixmap(self.pixon, QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            buttonz_list[iter_buttons - 1].setIcon(icon)
            buttonz_list[iter_buttons - 1].setIconSize(QtCore.QSize(160, 160))
            # buttonz_list[iter_buttons-1].installEventFilter(self)

            if tab_index == 0:
                if iter_buttons == 1:
                    # try:
                    #     self.grid_layout_box1
                    # except:
                    self.grid_layout_box1 = QtWidgets.QGridLayout(
                        self.image_preview_scrollArea_Contents
                    )
                    self.grid_layout_box1.setObjectName("grid_layout_box1")
                    # else:
                    #     pass
                self.grid_layout_box1.addWidget(
                    buttonz_list[iter_buttons - 1], *position
                )
                # self.update_scroll_preview(0)
                self.included_image_list.append(True)
                # self.DH.view_field_list = self.pixon_list
                # self.buttonz_list[iter_buttons-1].clicked.connect((lambda _, b=(iter_buttons-1): self.exclude_image(imagenumber=b)))
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.set_curent_button(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.load_main_scene(
                            imagenumber=b
                        )
                    )
                )
                # self.buttonz_list[iter_buttons-1].clicked.connect((lambda _, b=(iter_buttons-1): self.is_pressed_image_handler(imagenumber=b)))

            if tab_index == 1:  # mask
                if iter_buttons == 1:  # only should be created once
                    # need to pu this here because it gets deleted from delete_all_buttons()
                    # try:
                    #     self.grid_layout_box1
                    # except:
                    self.grid_layout_box2 = QtWidgets.QGridLayout(
                        self.mask_preview_scrollArea_Contents
                    )
                    self.grid_layout_box2.setObjectName("grid_layout_box2")
                    # else:
                    #     pass
                self.grid_layout_box2.addWidget(
                    buttonz_list[iter_buttons - 1], *position
                )
                self.update_scroll_preview(1)
                # gui_main.included_image_list.append(True)
                self.DH.view_field_list = self.pixon_list
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.set_curent_button(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.load_main_scene(
                            imagenumber=b
                        )
                    )
                )

    def label_update(self, my_dir):
        if my_dir == None or my_dir == "." or my_dir == "":
            return False
        else:
            return True

    def natural_keys(self, text):
        import re

        return [self.atoi(c) for c in re.split(r"(\d+)", text)]

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def list_files(self, path):
        files = [
            f
            for f in os.listdir(path)
            if not f.startswith(".")
            and os.path.splitext(f)[1].lower()
            in (".jpg", ".jpeg", ".TIF", ".tiff", ".tif", ".png", ".PNG")
        ]
        files.sort(key=self.natural_keys)
        return files

    def update_image_list(self, MainWindow, image_up, image_id):
        self.label.setPixmap(image_up)

    def update_scroll_preview(self, tab_index=1):
        height = int(len(self.values) / self.num_elem_width) * 100
        if tab_index == 0:
            self.image_preview_scrollArea_Contents.setMinimumSize(
                QtCore.QSize(200, height)
            )
        elif tab_index == 1:
            self.mask_preview_scrollArea_Contents.setMinimumSize(
                QtCore.QSize(200, height)
            )

    # def on_Button_clicked(self, checked=None):
    #     # transfer assets that are local to global:
    #     self.RNAi_list_global = self.RNAi_list
    #     ####continue
    #     dialog = QtWidgets.QDialog()
    #     dialog.ui = Ui_Dialog()
    #     dialog.ui.setupUi2(dialog)
    #     dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
    #     dialog.show()
    #     dialog.exec()
    #     #dialog.show()
    #     #self.showMinimized()

    def downscale_image(self, original_image, max_resolution_h, max_resolution_w):
        """
        Figure out the scale change for y and x
        """
        scale_width = original_image.shape[1] / max_resolution_w
        scale_hight = original_image.shape[0] / max_resolution_h
        if scale_hight > scale_width:
            scale_percent = scale_width
        else:
            scale_percent = scale_hight
            # percent of original size
        width = int(original_image.shape[1] * scale_percent)
        height = int(original_image.shape[0] * scale_percent)
        dim = (width, height)
        # resize image
        resized = cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)
        return resized

    def load_images(
        self, list_files_1, outfolder_1="C:\\asap__imaging_temp", path_files=""
    ):
        all_max = []
        path_final = []
        final = []

        for a in range(len(list_files_1)):
            images_proc = []
            path_tmp = ""
            path_tmp = path_files + "/" + list_files_1[a]
            path_final.append(path_tmp)
            images_proc1 = np.asarray(cv2.imread(path_final[a]))
            images_proc1 = cv2.cvtColor(images_proc1, cv2.COLOR_BGR2RGB)
            final.append(images_proc1)
        return final

    # needs to be called with signal
    def add_buttons_drop(self, urls):
        """
        Function that runs when we already have a condition added and we want to drop new images to
        that condition
        """

        self.delete_all_buttons_in_tabs(0)
        self.delete_all_buttons_in_tabs(1)
        QtWidgets.QApplication.processEvents
        self.add_buttons(
            self.MainWindow, tab_index=0, from_url_drop=True, added_urls=urls
        )
        self.add_buttons(
            self.MainWindow, tab_index=1, from_url_drop=True, added_urls=urls
        )
        self.save_current_asset()
        self.urls_droped = []

    def add_buttons(
        self,
        MainWindow,
        tab_index,
        element_width=2,
        from_url_drop=False,
        added_urls=[],
        precompute_mask=False,
    ):
        if tab_index == 0:
            return
        if from_url_drop == False:
            icon = QtGui.QIcon()
            self.num_elem_width = element_width
            positions = [(i, j) for i in range(100) for j in range(self.num_elem_width)]
            self.values = np.array([i for i in range(len(self.all_stacked_images))])
            iter_buttons = 0
            buttonz_list = []
            self.pixon_list = []
            if precompute_mask == False:
                self.DH.masks_state = []
                self.DH.all_worm_mask_points_x = []
                self.DH.all_worm_mask_points_y = []
                self.DH.all_masks = []
                self.DH.all_masks_usr = []
                self.DH.master_mask_list = []
            elif precompute_mask == True:
                current_item = self.current_item_rnai
                self.DH.masks_state_usr = self.DH.dict_RNAi_attributes_all[
                    current_item
                ]["masks_state_usr"].copy()
                self.DH.masks_state = self.DH.dict_RNAi_attributes_all[current_item][
                    "masks_state"
                ].copy()
                self.DH.all_worm_mask_points_x = self.DH.all_worm_mask_points_x_slot[
                    current_item
                ].copy()
                self.DH.all_worm_mask_points_y = self.DH.all_worm_mask_points_y_slot[
                    current_item
                ].copy()
                self.DH.all_masks = self.DH.mask_RNAi_slots[current_item].copy()
                self.DH.all_masks_usr = self.DH.usr_mask_RNAi_slots[current_item].copy()
                # self.DH.master_mask_list =[]
            self.DH.pixon_list_opencv = []
            self.included_image_list = []

            self.temp_mask_to_use_Test_x = []
            self.temp_mask_to_use_Test_y = []
            self.worm_mask_points_x = []
            self.worm_mask_points_y = []
            self.i_am_drawing_state = False
            self.list_px = []
            self.list_py = []
            self.add_mask_btn_state = False
            self.DH.predict_masks_state = False
            self.selection_state = False  # weather or not we can aselect a mask
            # add null masks
            tmp_list = []
            for i in range(len(self.all_stacked_images)):
                self.DH.all_masks.append(tmp_list.copy())
                self.DH.master_mask_list = []
                self.DH.all_worm_mask_points_y.append(tmp_list.copy())
                self.DH.all_worm_mask_points_x.append(tmp_list.copy())
            self.sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum
            )
            self.sizePolicy.setHorizontalStretch(0)
            self.sizePolicy.setVerticalStretch(0)
            for d in range(len(self.all_stacked_images)):
                self.DH.masks_state.append(False)
                self.DH.masks_state_usr.append(False)
        else:
            icon = QtGui.QIcon()
            self.DH.pixon_list_opencv = []
            iter_buttons = 0
            buttonz_list = []
            self.pixon_list = []
            self.selection_state = False
            for url in added_urls:
                self.all_stacked_images.append(cv2.imread(url))
            tmp_list = []
            for i in range(len(added_urls)):
                self.DH.all_masks.append(tmp_list.copy())
                self.DH.master_mask_list.append(tmp_list.copy())
                self.DH.all_worm_mask_points_y.append(tmp_list.copy())
                self.DH.all_worm_mask_points_x.append(tmp_list.copy())
                self.sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Fixed,
                    QtWidgets.QSizePolicy.Policy.Minimum,
                )
                self.sizePolicy.setHorizontalStretch(0)
                self.sizePolicy.setVerticalStretch(0)
            for d in range(len(added_urls)):
                self.DH.masks_state.append(False)
                self.DH.masks_state_usr.append(False)
            positions = [(i, j) for i in range(100) for j in range(self.num_elem_width)]
            self.values = np.array([i for i in range(len(self.all_stacked_images))])

        for position, value in zip(positions, self.values):
            iter_buttons += 1
            buttonz_list.append(QtWidgets.QPushButton(str(iter_buttons)))
            buttonz_list[iter_buttons - 1].setSizePolicy(self.sizePolicy)
            buttonz_list[iter_buttons - 1].setMinimumSize(QtCore.QSize(0, 80))
            buttonz_list[iter_buttons - 1].setMaximumSize(QtCore.QSize(180, 180))
            buttonz_list[iter_buttons - 1].setCheckable(True)
            buttonz_list[iter_buttons - 1].setText("")
            # cv2.imshow("test widnow",self.all_stacked_images[iter_buttons-1] )
            self.imgon = self.all_stacked_images[iter_buttons - 1]
            QtWidgets.QApplication.processEvents()
            # self.DH.pixon_list_opencv.append(self.imgon)
            if self.imgon.shape[0] > 6500 or self.imgon.shape[1] > 6500:
                imgon_sm = self.downscale_image(self.imgon.copy(), 6500, 6500)
            else:
                imgon_sm = self.imgon.copy()
            imgon_sm_pix = QtGui.QImage(
                imgon_sm,
                imgon_sm.shape[1],
                imgon_sm.shape[0],
                QtGui.QImage.Format.Format_RGB888,
            )
            QtWidgets.QApplication.processEvents()
            self.pixon = QtGui.QPixmap.fromImage(imgon_sm_pix).copy()
            self.pixon_list.append(self.pixon)
            # TODO fix the active image appearencem wuh pixoff...
            icon.addPixmap(
                self.pixon.copy(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
            )
            buttonz_list[iter_buttons - 1].setIcon(icon)
            buttonz_list[iter_buttons - 1].setIconSize(QtCore.QSize(160, 160))
            # buttonz_list[iter_buttons-1]
            # buttonz_list[iter_buttons-1].installEventFilter(self)
            if tab_index == 0:
                if iter_buttons == 1:
                    self.grid_layout_box1 = QtWidgets.QGridLayout(
                        self.image_preview_scrollArea_Contents
                    )
                    self.grid_layout_box1.setObjectName("grid_layout_box1")

                    # image_tab_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
                    # self.verticalLayout_4.addItem(image_tab_spacer)
                if iter_buttons == len(self.all_stacked_images):
                    self.DH.view_field_list = self.pixon_list
                self.grid_layout_box1.addWidget(
                    buttonz_list[iter_buttons - 1], *position
                )
                # self.update_scroll_preview(0)
                self.included_image_list.append(True)

                # self.buttonz_list[iter_buttons-1].clicked.connect((lambda _, b=(iter_buttons-1): self.exclude_image(imagenumber=b)))

                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.set_curent_button(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.load_main_scene(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    lambda: self.viewer.setDragMode(
                        QtWidgets.QGraphicsView.DragMode.NoDrag
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    lambda _: setattr(
                        config.global_params, "is_mask_button_selected", False
                    )
                )
                # lambda _ : setattr(config.global_params, 'is_mask_button_selected', False)
                # buttonz_list[iter_buttons-1].clicked.connect((lambda _, b=(iter_buttons-1): self.is_pressed_image_handler(imagenumber=b)))
                # self.image_preview_scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

            if tab_index == 1:  # mask
                if iter_buttons == 1:  # only should be created once
                    # need to pu this here because it gets deleted from delete_all_buttons()
                    self.grid_layout_box2 = QtWidgets.QGridLayout(
                        self.mask_preview_scrollArea_Contents
                    )
                    self.grid_layout_box2.setObjectName("grid_layout_box2")
                    # mask_tab_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
                    # self.verticalLayout_5.addItem(mask_tab_spacer)
                if iter_buttons == len(self.all_stacked_images):
                    self.DH.view_field_list = self.pixon_list

                self.grid_layout_box2.addWidget(
                    buttonz_list[iter_buttons - 1], *position
                )

                self.included_image_list.append(True)
                # self.view_field_list = self.pixon_list
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.set_curent_button(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    (
                        lambda _, b=(iter_buttons - 1): self.load_main_scene(
                            imagenumber=b
                        )
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    lambda: self.viewer.setDragMode(
                        QtWidgets.QGraphicsView.DragMode.NoDrag
                    )
                )
                buttonz_list[iter_buttons - 1].clicked.connect(
                    lambda _: setattr(
                        config.global_params, "is_mask_button_selected", True
                    )
                )
                # self.buttonz_list[iter_buttons-1].clicked.connect((lambda _, b=(iter_buttons-1): self.is_pressed_image_handler(imagenumber=b)))

            # self.is_pressed_image_handler
        if tab_index == 0:
            self.load_main_scene(0)
        else:
            self.load_main_scene(0)

    def setCurrentImageNumber(self, imagenumber):
        """Setter for the current image number, by using config we are able to obtain the variable globaly"""
        self.current_imagenumber = imagenumber
        from celer_sight_ai import config

        config.user_attributes.current_image_number = imagenumber

    def set_curent_button(self, imagenumber):
        self.previous_imagenumber = self.current_imagenumber
        self.current_imagenumber = imagenumber


class settingsMainClass(settingsDialog1):
    def __init__(self, MainWindow=None):
        super(settingsMainClass, self).__init__()
        self.MainWindow = MainWindow
        self.myDialog = QtWidgets.QDialog()
        self.setupUi(self.myDialog)
        self.setupToggles()

        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self.myDialog)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.myDialog.setGraphicsEffect(self.shadow)

        self.myDialog.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.myDialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.myDialog.show()

    def setupToggles(self):
        from celer_sight_ai.gui.toggle_cs import ButtonToggle

        self.placeholder_btn_anim = ButtonToggle()
        self.placeholder_btn_anim.setObjectName("placeholder_btn_anim")
        self.placeholder_btn_anim.stateChanged.connect(
            lambda: self.onBtnStateChecked(
                "maxImageResImport_Toggle", self.placeholder_btn
            )
        )
        self.gridLayout_12.replaceWidget(
            self.placeholder_btn, self.placeholder_btn_anim
        )
        self.placeholder_btn.hide()

        self.placeholder_btn_2_anim = ButtonToggle()
        self.placeholder_btn_2_anim.setObjectName("placeholder_btn_2_anim")
        self.placeholder_btn_2_anim.stateChanged.connect(
            lambda: self.onBtnStateChecked(
                "maxImageResResize_Toggle", self.placeholder_btn
            )
        )
        self.gridLayout_13.replaceWidget(
            self.placeholder_btn_2, self.placeholder_btn_2_anim
        )
        self.placeholder_btn_2.hide()


class WorkerSignals(QtCore.QObject):
    """
    Used as mysignals in mainwidnow
    """

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)  # can be anything
    progress = QtCore.pyqtSignal(int)
    createNew = QtCore.pyqtSignal()


if __name__ == "__main__":
    pass
