import logging
import os

import cv2
import numpy as np
import skimage
from PyQt6 import QtCore, QtGui, QtWidgets
from skimage.draw import circle_perimeter as circle

import celer_sight_ai.gui.custom_widgets.viewer as viewer
from celer_sight_ai import config

# import (
#     ArrowChangeImageButton,
#     BitMapAnnotation,
#     PolygonAnnotation,
# )
from celer_sight_ai.gui.custom_widgets.viewer.scene import SceneViewer, readImage
from celer_sight_ai.io.image_reader import read_specialized_image
from celer_sight_ai.models.viewer import DragEventType

logger = logging.getLogger(__name__)


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
        super().__init__()
        # super(Ui_MainWindow, self).__init__()
        from PyQt6.QtOpenGLWidgets import QOpenGLWidget

        from celer_sight_ai import config
        from celer_sight_ai.gui.custom_widgets.viewer.scene import (
            BackgroundGraphicsItem,
        )

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

        # Magic click that adjusts magic box mask
        self.active_adjustment_annotation_uuid = None

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
        self._photo.setZValue(config.Z_VALUE_BACKGROUND_IMAGE)
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

        self.LeftArrowChangeButton = viewer.ArrowChangeImageButton(
            MODE="left",
            imageLocation="data\\NeedsAttribution\\LeftPageArrow.png",
            Viewer=self,
            StartingPositionXMOD=-45,
            StartingPositionYMOD=0,
        )
        self.RightArrowChangeButton = viewer.ArrowChangeImageButton(
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

        # High-res update debouncing
        self._high_res_update_timer = QtCore.QTimer()
        self._high_res_update_timer.setSingleShot(True)
        self._high_res_update_timer.timeout.connect(
            self._perform_debounced_high_res_update
        )

        # Store the last update parameters to avoid redundant calls
        self._last_update_params = {
            "viewport_bbox": None,
            "zoom_level": None,
            "force_update": False,
        }

        # Debounce settings
        self._debounce_delay_ms = 250  # 150ms delay
        self._min_movement_threshold = 50  # minimum pixels moved before update
        self._min_zoom_threshold = 0.1  # minimum zoom change before update

    def request_debounced_high_res_update(self, force_update=False):
        """
        Public method to request a debounced high-res update.
        This replaces direct signal emissions.
        """
        if not self.hasPhoto():
            return

        # Get current viewport and zoom information
        bbox_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        viewport_bbox = [
            bbox_rect.x(),
            bbox_rect.y(),
            bbox_rect.width(),
            bbox_rect.height(),
        ]
        zoom_level = self.transform().m11()

        # Check if significant change occurred
        if not force_update and self._should_skip_update(viewport_bbox, zoom_level):
            return

        # Store parameters for the actual update
        self._last_update_params = {
            "viewport_bbox": viewport_bbox,
            "zoom_level": zoom_level,
            "force_update": force_update,
        }

        # Start/restart the debounce timer
        self._high_res_update_timer.start(self._debounce_delay_ms)

    def _should_skip_update(self, viewport_bbox, zoom_level):
        """
        Check if update should be skipped based on movement/zoom thresholds.
        """
        last_params = self._last_update_params

        if not last_params["viewport_bbox"]:
            return False

        # Calculate movement distance (center points)
        current_center_x = viewport_bbox[0] + viewport_bbox[2] / 2
        current_center_y = viewport_bbox[1] + viewport_bbox[3] / 2

        last_center_x = (
            last_params["viewport_bbox"][0] + last_params["viewport_bbox"][2] / 2
        )
        last_center_y = (
            last_params["viewport_bbox"][1] + last_params["viewport_bbox"][3] / 2
        )

        movement_distance = (
            (current_center_x - last_center_x) ** 2
            + (current_center_y - last_center_y) ** 2
        ) ** 0.5

        # Calculate zoom difference
        zoom_difference = abs(zoom_level - last_params["zoom_level"])

        # Skip if movement and zoom change are below thresholds
        return (
            movement_distance < self._min_movement_threshold
            and zoom_difference < self._min_zoom_threshold
        )

    def _perform_debounced_high_res_update(self):
        """
        Internal method that performs the actual high-res update.
        Called by the debounce timer.
        """
        params = self._last_update_params
        if not params["viewport_bbox"]:
            return

        # Update config with the latest viewport info
        config.viewport_bounding_box = params["viewport_bbox"]

        # Emit the actual signal
        config.global_signals.check_and_update_high_res_slides_signal.emit()
        # if hasattr(config, "current_photo_viewer") and config.current_photo_viewer:
        #     config.current_photo_viewer.request_debounced_high_res_update(
        #         force_update=True
        #     )

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
            if isinstance(item, (viewer.PolygonAnnotation, viewer.BitMapAnnotation)):
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
            i for i in self.scene().items() if isinstance(i, (viewer.PolygonAnnotation))
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
                get_deep_zoom_by_openslide,
                get_deep_zoom_by_tiffslide,
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
        import heapq

        from celer_sight_ai.io.image_reader import DEEPZOOM_TILE_SIZE

        items_added = []
        idx = 1
        logger.info("Adding deepview images to scene")
        image_objects = object.get("image_data", None)
        bbox_objects = object.get("image_bounding_box", None)
        image_name = object.get("image_name", None)
        downsample = object.get("downsample", None)

        scale = downsample

        # Get current zoom level to determine if this tile is appropriate
        current_zoom = self.transform().m11()
        optimal_downsample = self.calculate_optimal_downsample_for_zoom()
        min_downsample, max_downsample = self.get_downsample_range_for_zoom(
            optimal_downsample
        )

        image_object = image_objects[0]
        bbox = bbox_objects[0]

        photo = QtWidgets.QGraphicsPixmapItem()

        # Set cache mode based on zoom level
        if current_zoom > 1.0:
            # High zoom - use ItemCoordinateCache for better performance
            photo.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache)
        else:
            # Low zoom - use DeviceCoordinateCache
            photo.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache)

        photo.setPos(bbox[0], bbox[1])
        photo.setScale(scale)
        photo.setPixmap(image_object)
        photo.setCacheMode(
            QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache
        )  # DeviceCoordinateCache

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
            # Larger downsample means that the image needs to have a lower Z value
            # because we want the lower downsampled images to be on top (as they are higher resolution).
            photo.setZValue(config.Z_VALUE_BACKGROUND_IMAGE + (240 - int(downsample)))
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

        except Exception as e:
            logger.error(e)
            return

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
        from celer_sight_ai.io.image_reader import write_ome_tiff

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

                    images_data = []
                    all_channels_list = []
                    for j in range(
                        len(image_channel_list_arr[i][ii])
                    ):  # for every channel / sub-image
                        # TODO: adjust for pyramidal????
                        img, result_dict = readImage(image_channel_list_arr[i][ii][j])
                        channels_list = result_dict.get("channels", None)
                        if len(channels_list) != 1 or (
                            len(img.shape) != 2 and img.shape[2] > 1
                        ):
                            config.global_signal.errorSignal(
                                "The images to be combined are not grayscale, please provide grayscale images"
                            )
                            logger.warning(
                                "Images provided are not grayscale, aborting"
                            )
                            return
                        all_channels_list.extend(channels_list)
                        if len(img.shape) == 3:
                            img = img.squeeze()
                            if len(img.shape) == 3:
                                config.global_signal.errorSignal(
                                    "The images to be combined are not grayscale, please provide grayscale images"
                                )
                        images_data.append(img)  # raw image

                    # Prepare ImageJ style metadata with channel names
                    # channel_names_arr[i] = list(channel_names_arr[i][j])

                    combined_image = np.stack(images_data, axis=-1)
                    # save the image as a tiff with the channels included
                    import os

                    # generate a uuid that does not exist in config.cache_dir
                    import uuid

                    import tifffile

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

                    # save image to disk at a temp location
                    import uuid

                    import bioformats

                    dtype = combined_image.dtype
                    if dtype == np.uint16:
                        dtype = bioformats.PT_UINT16
                    elif dtype == np.uint8:
                        dtype = bioformats.PT_UINT8

                    # Ensure channel names are properly formatted strings
                    formatted_channel_names = [str(name) for name in all_channels_list]

                    write_ome_tiff(
                        arr=combined_image,
                        channels=formatted_channel_names,
                        tif_path=output_path,
                        physical_pixel_size_x=result_dict.get(
                            "physical_pixel_size_x", None
                        ),
                        physical_pixel_size_y=result_dict.get(
                            "physical_pixel_size_y", None
                        ),
                        physical_pixel_unit_x=result_dict.get(
                            "physical_pixel_unit_x", None
                        ),
                        physical_pixel_unit_y=result_dict.get(
                            "physical_pixel_unit_y", None
                        ),
                    )
                    out_urls.append(output_path)
                if treatmetns:
                    self.MainWindow.add_new_treatment_item(treatmetns[i])
                self.load_files_by_drag_and_drop(out_urls)

    def combine_image_channels_and_save_to_disk(
        self, image_channel_list, channel_names, multi_treatment=False, treatmetns=None
    ):
        # Reads the grayscale images, combines them and saves them to disk. If images are not grayscale raise error
        import copy

        from celer_sight_ai.io.image_reader import write_ome_tiff

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
                        if len(chn) != 1 or (len(img.shape) != 2 and img.shape[2] > 1):
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

                    # Prepare ImageJ style metadata with channel names
                    channel_names_arr[i] = list(channel_names_arr[i])
                    metadata = {"cs_channels": channel_names_arr[i], "axes": "YXC"}

                    # generate a uuid that does not exist in config.cache_dir
                    import os
                    import uuid

                    file_name = os.path.basename(image_channel_list_arr[i][0][ii])
                    indx_channel = file_name.lower().index(
                        channel_names_arr[i][0].lower()
                    )
                    # delete channel from the original filename
                    file_name = (
                        file_name[:indx_channel]
                        + file_name[indx_channel + len(channel_names_arr[i][0]) :]
                    )
                    output_path = os.path.join(str(config.cache_dir), file_name)
                    iii = 0
                    while os.path.exists(output_path + ".tif"):
                        import random

                        if iii > 1000:
                            break
                        output_path = os.path.join(
                            config.cache_dir,
                            file_name + str(random.randint(0, 1000)),
                        )
                        iii += 1

                    output_path = os.path.join(output_path + ".tif")
                    # Save the combined image as a TIFF file with metadata

                    write_ome_tiff(
                        arr=combined_image,
                        channels=channel_names_arr[i],
                        tif_path=output_path,
                    )

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
        import glob
        import re
        from collections import defaultdict
        from functools import partial

        from natsort import natsorted

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

                # Discard potential similar / almost identical patterns
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
        self,
        urls=[],
        channel_pattern=True,
        treatment_pattern=True,
        auto_accept=False,
        channel_pattern_auto_accept=False,
        treatment_pattern_auto_accept=False,
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

        import glob
        from functools import partial

        from celer_sight_ai.gui.custom_widgets.viewer.scene import (
            find_treatment_patterns_within_filepaths,
        )

        # case of urls as dict --> already determined treatments names and paths
        if isinstance(urls, dict):
            for k, v in urls.items():
                self.MainWindow.add_new_treatment_item(k)
                QtWidgets.QApplication.processEvents()  # needed to prevent errors from uuids missmatch
                self.add_new_images_by_drag_and_drop(v)
            return

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

                if channel_pattern and len(img_file_list) > 1:
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
                    # get all subfolders
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

        return super().dragEnterEvent(event)

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
                    logger.warning("Could not fit image in view, image size is null")
                    return
                x_padding = image_object.SizeX * 0.25
                y_padding = image_object.SizeY * 0.25
                self.scene().setSceneRect(
                    -image_object.SizeX - x_padding,
                    -image_object.SizeY
                    - y_padding,  # BUG: This was using SizeX instead of SizeY
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

    def setPhoto_and_mask(self, pixmap: QtGui.QPixmap | None = None):
        if pixmap is None:
            return
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
            # update graphicsview
            self.update()
        else:
            return
        if fit_in_view_state is True:
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
        if (
            self.MainWindow.current_imagenumber is None
            or self.MainWindow.current_imagenumber == -1
        ):
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
        if zoom_factor is None:
            zoom_factor = 1.2

        # Get current zoom level
        current_matrix = self.transform()
        current_zoom = abs(current_matrix.m11())

        # Define maximum zoom (adjust as needed)
        max_zoom = 50.0

        # Check if we're already at maximum zoom
        if current_zoom >= max_zoom:
            logger.debug(f"Already at maximum zoom level: {current_zoom}")
            return

        mod = 5
        scale_factor = 1 + (zoom_factor / mod)

        # Calculate what the new zoom would be
        new_zoom = current_zoom * scale_factor

        # If new zoom would exceed maximum, scale to exactly the maximum
        if new_zoom > max_zoom:
            scale_factor = max_zoom / current_zoom
            logger.debug(f"Limiting zoom in to maximum: {max_zoom}")

        self.scale(scale_factor, scale_factor)

        if hasattr(config, "current_photo_viewer") and config.current_photo_viewer:
            config.current_photo_viewer.request_debounced_high_res_update(
                force_update=True
            )

    def zoom_out(self, zoom_factor=None):
        if zoom_factor is None:
            zoom_factor = 1.2

        # Validate current transform before proceeding
        current_matrix = self.transform()
        if current_matrix.determinant() <= 0:
            logger.warning("Invalid transformation matrix detected, resetting")
            self.resetTransform()
            return

        # Get current total zoom level
        current_zoom = abs(current_matrix.m11())

        # Define minimum zoom based on image content
        min_zoom = self.calculate_minimum_zoom()

        # Check if we're already at minimum zoom
        if current_zoom <= min_zoom:
            logger.debug(f"Already at minimum zoom level: {current_zoom}")
            return

        mod = 5
        scale_factor = 1 - (zoom_factor / mod)

        # Calculate what the new zoom would be
        new_zoom = current_zoom * scale_factor

        # If new zoom would be below minimum, scale to exactly the minimum
        if new_zoom < min_zoom:
            scale_factor = min_zoom / current_zoom
            logger.debug(f"Limiting zoom out to minimum: {min_zoom}")

        # Ensure scale factor doesn't go negative or too small
        scale_factor = max(0.1, scale_factor)

        self.scale(scale_factor, scale_factor)

        # Instead of direct matrix manipulation, use centerOn for repositioning
        if hasattr(self, "_last_center_point"):
            self.centerOn(self._last_center_point)

        # Ensure content stays visible
        self.ensure_content_visible()

        if hasattr(config, "current_photo_viewer") and config.current_photo_viewer:
            config.current_photo_viewer.request_debounced_high_res_update(
                force_update=True
            )

    def calculate_minimum_zoom(self):
        """
        Calculate the minimum zoom level based on image content and viewport size.
        Returns a zoom level that ensures content remains visible.
        """
        if not self.hasPhoto():
            return 0.01  # Fallback minimum

        # Get image object and its dimensions
        image_object = self.MainWindow.DH.BLobj.get_current_image_object()
        if not image_object or not image_object.SizeX or not image_object.SizeY:
            return 0.01

        # Get viewport dimensions
        viewport_rect = self.viewport().rect()
        viewport_width = viewport_rect.width()
        viewport_height = viewport_rect.height()

        if viewport_width <= 0 or viewport_height <= 0:
            return 0.01

        # Calculate scale needed to fit image in viewport with some margin
        scale_x = viewport_width / (image_object.SizeX * 4)  # 4x margin for zoom out
        scale_y = viewport_height / (image_object.SizeY * 4)

        # Use the smaller scale to ensure content fits
        min_scale = min(scale_x, scale_y)

        # Ensure minimum is not too small
        return max(0.01, min_scale)

    def ensure_content_visible(self):
        """
        Ensures that image content remains visible in the viewport after zoom operations.
        """
        if not self.hasPhoto():
            return

        # Get current scene rect and viewport
        scene_rect = self._photo.sceneBoundingRect()
        if scene_rect.isNull():
            return

        viewport_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        # Check if image is completely outside viewport
        if not scene_rect.intersects(viewport_rect):
            # Center the view on the image
            self.centerOn(scene_rect.center())
            logger.debug("Recentered view on image content")

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
            return super().wheelEvent(event)

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
        return (-(value / radius) + 1) * dt

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
        from celer_sight_ai.gui.custom_widgets.viewer.scene import bbox_drawing_cls

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
        from celer_sight_ai import config
        from celer_sight_ai.core.Workers import Worker

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
        # if there are no treatments available, throw an error

        if not self.MainWindow.DH.BLobj.get_current_condition_uuid():
            config.global_signals.errorSignal.emit(
                "No treatments available, please add a treatment to continue"
            )
            return
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

    def calculate_optimal_downsample_for_zoom(self):
        """
        Calculate the optimal downsample level based on current zoom level.
        Higher zoom (transform().m11()) needs lower downsample (higher resolution).
        Lower zoom needs higher downsample (lower resolution).
        """
        current_zoom = self.transform().m11()

        # Get baseline zoom
        if hasattr(self, "_fit_view_zoom") and self._fit_view_zoom > 0:
            relative_zoom = current_zoom / self._fit_view_zoom
        else:
            # Fallback calculation
            image_object = self.MainWindow.DH.BLobj.get_current_image_object()
            if image_object and image_object.SizeX:
                viewport_rect = self.viewport().rect()
                scale_x = viewport_rect.width() / image_object.SizeX
                scale_y = viewport_rect.height() / image_object.SizeY
                fit_scale = min(scale_x, scale_y) * 0.9
                relative_zoom = current_zoom / fit_scale
            else:
                relative_zoom = 1.0

        # Traditional downsample: higher value = lower resolution
        if relative_zoom >= 8.0:
            optimal_downsample = 1.0  # Highest resolution
        elif relative_zoom >= 4.0:
            optimal_downsample = 2.0  # High resolution
        elif relative_zoom >= 2.0:
            optimal_downsample = 4.0  # Medium resolution
        elif relative_zoom >= 1.0:
            optimal_downsample = 8.0  # Lower resolution
        elif relative_zoom >= 0.5:
            optimal_downsample = 16.0  # Low resolution
        else:
            optimal_downsample = 32.0  # Lowest resolution

        return optimal_downsample

    def get_downsample_range_for_zoom(self, optimal_downsample):
        """
        Get the acceptable downsample range for smooth transitions.
        We keep tiles within a certain range to avoid abrupt changes.
        """
        # Allow some tolerance around the optimal downsample
        tolerance_factor = 1.5

        min_downsample = optimal_downsample / tolerance_factor
        max_downsample = optimal_downsample * tolerance_factor

        return min_downsample, max_downsample

    def cull_inappropriate_zoom_tiles(self):
        """
        Remove tiles that are inappropriate for the current zoom level.
        This is the core optimization for zoom-aware tile management.
        """
        if not config._deepzoom_pixmaps:
            return

        optimal_downsample = self.calculate_optimal_downsample_for_zoom()
        min_downsample, max_downsample = self.get_downsample_range_for_zoom(
            optimal_downsample
        )

        # Get current viewport for additional culling
        viewport_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        viewport_padding = 500  # Keep some tiles outside viewport for smooth panning
        viewport_rect.adjust(
            -viewport_padding, -viewport_padding, viewport_padding, viewport_padding
        )

        tiles_to_remove = []
        tiles_by_downsample = {}

        if len(config._deepzoom_pixmaps) > config.MAX_DEEPZOOM_OBJECTS:
            # Group tiles by downsample level and check if they should be kept
            for item_data in config._deepzoom_pixmaps:
                pixmap_item, bbox, downsample, order, image_name = item_data

                # Check if tile is outside acceptable downsample range
                if downsample < min_downsample or downsample > max_downsample:
                    tiles_to_remove.append(item_data)
                    continue

                # Check if tile is outside viewport (with padding)
                item_rect = QtCore.QRectF(bbox[0], bbox[1], bbox[2], bbox[3])
                if not viewport_rect.intersects(item_rect):
                    tiles_to_remove.append(item_data)
                    continue

                # Group remaining tiles by downsample for further optimization
                downsample_key = round(downsample, 3)
                if downsample_key not in tiles_by_downsample:
                    tiles_by_downsample[downsample_key] = []
                tiles_by_downsample[downsample_key].append(item_data)

        # If we have too many tiles at the optimal level, keep only the closest ones
        optimal_key = round(optimal_downsample, 3)
        if (
            optimal_key in tiles_by_downsample
            and len(tiles_by_downsample[optimal_key]) > 15
        ):
            # Sort by distance from viewport center and keep only the closest ones
            viewport_center = viewport_rect.center()
            tiles_by_downsample[optimal_key].sort(
                key=lambda item: (
                    (item[1][0] + item[1][2] / 2 - viewport_center.x()) ** 2
                    + (item[1][1] + item[1][3] / 2 - viewport_center.y()) ** 2
                )
                ** 0.5
            )
            # Keep only the 15 closest tiles, mark the rest for removal
            tiles_to_remove.extend(tiles_by_downsample[optimal_key][15:])

        # Remove inappropriate tiles
        for item_data in tiles_to_remove:
            pixmap_item = item_data[0]
            if pixmap_item in self.scene().items():
                self.scene().removeItem(pixmap_item)
            if item_data in config._deepzoom_pixmaps:
                config._deepzoom_pixmaps.remove(item_data)

        logger.debug(
            f"Removed {len(tiles_to_remove)} inappropriate tiles. "
            f"Optimal downsample: {optimal_downsample}, "
            f"Range: {min_downsample:.2f}-{max_downsample:.2f}"
        )

    def update_tiles_for_zoom_change(self):
        """
        Called when zoom level changes significantly.
        Triggers tile updates if needed.
        """
        current_zoom = self.transform().m11()

        # Check if zoom changed significantly since last update
        if hasattr(self, "_last_zoom_level"):
            zoom_change = abs(current_zoom - self._last_zoom_level) / max(
                current_zoom, 0.1
            )
            if zoom_change < 0.1:  # Less than 10% change
                return

        self._last_zoom_level = current_zoom

        # Cull inappropriate tiles
        self.cull_inappropriate_zoom_tiles()

        # Update config to track current zoom-appropriate downsample
        optimal_downsample = self.calculate_optimal_downsample_for_zoom()
        config._current_deep_zoom_downsample_level = optimal_downsample

        # Request new tiles if we don't have enough at the current zoom level
        if hasattr(config, "current_photo_viewer") and config.current_photo_viewer:
            config.current_photo_viewer.request_debounced_high_res_update(
                force_update=True
            )

    def process_bounding_box(
        self,
        image_uuid,
        bbox,
        class_id=None,
        current_group="default",
        ideal_annotation_to_image_ratio=None,
        retain_object_ratio_from_previous_inference=False,
    ):
        """
        Process a bounding box for a given image, handling bounds checking and adjustment.

        Args:
            image_uuid: UUID of the image to process
            bbox: Bounding box coordinates [x1, y1, x2, y2] or None
            class_id: Optional class ID for the bounding box
            current_group: Group UUID (defaults to "default")

        Returns:
            Dictionary containing processed results or None if processing failed
        """
        from celer_sight_ai import config
        from celer_sight_ai.io.image_reader import (
            get_optimal_crop_bbox,
        )

        # Get current treatment UUID
        treatment_uuid = self.MainWindow.DH.BLobj.get_current_condition_uuid()

        # Check if bbox is None and use stored coordinates if needed
        if isinstance(bbox, type(None)):
            x1 = min(self.aa_tool_bb_first_x, self.last_bbox_x)
            x2 = max(self.aa_tool_bb_first_x, self.last_bbox_x)
            y1 = min(self.aa_tool_bb_first_y, self.last_bbox_y)
            y2 = max(self.aa_tool_bb_first_y, self.last_bbox_y)
        else:
            x1, y1, x2, y2 = bbox
        bbox_object = [x1, y1, x2, y2]
        # Get image object
        image_object = (
            self.MainWindow.DH.BLobj.groups[current_group]
            .conds[self.MainWindow.DH.BLobj.get_current_condition()]
            .images[image_uuid]
        )

        # Ensure bbox is within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image_object.SizeX, x2)
        y2 = min(image_object.SizeY, y2)

        if not image_object.SizeX or not image_object.SizeY:
            logger.warning("Image size not found, skipping")
            return None

        # Get optimal crop bbox
        if class_id is None:
            class_id = self.MainWindow.DH.BLobj.get_current_class_uuid()

        bbox_tile = get_optimal_crop_bbox(
            image_object.SizeX,
            image_object.SizeY,
            [round(x1), round(y1), round(x2), round(y2)],
            class_id,
            ideal_annotation_to_image_ratio=ideal_annotation_to_image_ratio,
            retain_object_ratio_from_previous_inference=retain_object_ratio_from_previous_inference,
        )
        bbox_tile = list(bbox_tile)

        # Adjust if bbox extends beyond right edge
        if bbox_tile[0] + bbox_tile[2] > image_object.SizeX:
            difference = (bbox_tile[0] + bbox_tile[2]) - image_object.SizeX
            bbox_tile[2] = int(bbox_tile[2] - difference)
            bbox_tile[0] = int(max(0, bbox_tile[0] - difference))

        # Adjust if bbox extends beyond bottom edge  
        if bbox_tile[1] + bbox_tile[3] > image_object.SizeY:
            difference = (bbox_tile[1] + bbox_tile[3]) - image_object.SizeY
            bbox_tile[3] = int(bbox_tile[3] - difference)
            bbox_tile[1] = int(max(0, bbox_tile[1] - difference))

        # Make bbox square using largest dimension
        bbox_tile[2] = bbox_tile[3] = max(bbox_tile[2], bbox_tile[3])

        # Get image for the tile
        seg_image_prior = image_object.getImage(
            to_uint8=True,
            to_rgb=True,
            fast_load_ram=True,
            for_interactive_zoom=True,
            for_thumbnail=False,
            bbox=bbox_tile,
            avoid_loading_ultra_high_res_arrays_normaly=True,
        )
        config.dbg_image(seg_image_prior)
        if isinstance(seg_image_prior, type(None)):
            return None

        # Apply adjustments
        seg_image_prior = self.MainWindow.handle_adjustment_to_image(seg_image_prior)

        bbox_width = max(x2 - x1, y2 - y1)

        # Skip if bbox is too small
        if (y2 - y1) * (x2 - x1) < 30:
            return None

        # Calculate padding
        padding_top = bbox_tile[1] if bbox_tile[1] < 0 else 0
        padding_left = bbox_tile[0] if bbox_tile[0] < 0 else 0

        # Calculate bbox in the segmentation image coordinates
        bbox_in_seg = [
            bbox_object[0] - bbox_tile[0],
            bbox_object[1] - bbox_tile[1],
            (bbox_object[2] - bbox_tile[0]),
            (bbox_object[3] - bbox_tile[1]),
        ]

        resize_to_processed_image = [
            bbox_in_seg[2] / seg_image_prior.shape[1],  # resize on X
            bbox_in_seg[3] / seg_image_prior.shape[0],  # resize on Y
        ]

        return {
            "image_uuid": image_uuid,
            "treatment_uuid": treatment_uuid,
            "group_uuid": current_group,
            "class_id": class_id,
            "bbox": [x1, y1, x2, y2],
            "bbox_tile": bbox_tile,
            "bbox_in_seg": bbox_in_seg,
            "seg_image": seg_image_prior,
            "padding_top": padding_top,
            "padding_left": padding_left,
            "image_object": image_object,
            "width": bbox_width,
            "resize_factor_processed_image": resize_to_processed_image,
        }

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
        from celer_sight_ai.core.magic_box_tools import mask_to_polygon
        from celer_sight_ai.io.image_reader import (
            generate_complete_spiral_tiles,
            get_optimal_crop_bbox,
        )

        logger.debug("draw_bounding_box_stop")

        # get current image
        while config.load_main_scene_read_image is True:
            import time

            time.sleep(0.001)
        ideal_annotation_to_image_ratio = None
        retain_object_ratio_from_previous_inference = False
        if self.is_magic_mask_generator_mode():
            ideal_annotation_to_image_ratio = None
            retain_object_ratio_from_previous_inference = True
        else:
            ideal_annotation_to_image_ratio = 0.40

        result = self.process_bounding_box(
            current_image_uuid,
            bbox,
            class_id,
            current_group,
            ideal_annotation_to_image_ratio,
            retain_object_ratio_from_previous_inference,
        )

        if result is None:
            self.threadedBoundingBoxStopWorkerResultFunction()
            return

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
            "image_uuid": result["image_uuid"],
            "condition_uuid": result["treatment_uuid"],
            "group_uuid": result["group_uuid"],
            "class_uuid": self.MainWindow.DH.BLobj.get_current_class_uuid(),
            "mask_uuid": mask_uuid,
            "SizeX": result["image_object"].SizeX,
            "SizeY": result["image_object"].SizeY,
        }

        try:
            finalmask, offset_x, offset_y = (
                self.MainWindow.sdknn_tool.get_bounding_box_mask(
                    result["seg_image"],
                    celer_sight_object,
                    bounding_box=result["bbox_in_seg"],
                    tile_bbox=result["bbox_tile"],
                )
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

        # Extract values from result
        x1, y1, x2, y2 = result["bbox"]
        bbox_formatted = [x1, y1, x2 - x1, y2 - y1]  # [x,y,w,h]

        self.aa_review_state = False

        resize_factor_x = result["seg_image"].shape[1] / result["bbox_tile"][2]
        resize_factor_y = result["seg_image"].shape[0] / result["bbox_tile"][3]

        try:
            all_arrays = mask_to_polygon(
                finalmask,
                image_shape=result["seg_image"].shape,
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
                "treatment_uuid": result["treatment_uuid"],
                "group_uuid": result["group_uuid"],
                "array": all_arrays,
                "image_uuid": result["image_uuid"],
                "class_id": result["class_id"],
                "mask_type": "polygon",
            }
        )

        ##### calculate the typical mask width in pixels for that class ####
        from celer_sight_ai.inference_handler import calculate_polygon_width

        annotation_width = calculate_polygon_width(
            all_arrays[0].astype(np.uint32)
        )  # in diameter
        config.CLASS_REGISTRY_WIDTH[class_id] = annotation_width

        image_object = self.MainWindow.DH.BLobj.get_image_object_by_uuid(
            result["image_uuid"]
        )
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
                bbox_formatted,  # [x,y,w,h]
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
                if isinstance(io, type(None)):
                    return
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

        for item in self._scene.items():
            if type(item) == viewer.PolygonAnnotation:
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
            from celer_sight_ai.gui.custom_widgets.viewer.transitionAnim import (
                labelAnimation,
            )

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

    def add_point_as_magic_click(self, point: QtCore.QPoint):
        # check if there is an annotation polygon below the point
        print(f"adding point as magic click {point}")
        from shapely.geometry import Point
        from shapely.geometry.polygon import Polygon

        if not self.active_adjustment_annotation_uuid:
            return
        target_annotation = (
            self.MainWindow.DH.BLobj.get_current_image_object().get_by_uuid(
                self.active_adjustment_annotation_uuid
            )
        )
        # Determine if this is a positive or negative point
        if not target_annotation:
            return
        polygon_data = target_annotation.get_array()
        if isinstance(polygon_data, list) and len(polygon_data) > 0:
            # Get the outer polygon and any holes
            outer_polygon = polygon_data[0]
            holes = polygon_data[1:] if len(polygon_data) > 1 else []

            try:
                # Create a Shapely polygon with holes
                shapely_polygon = Polygon(outer_polygon, holes)

                # Ensure the geometry is valid
                if not shapely_polygon.is_valid:
                    # Use make_valid to repair the geometry
                    from shapely import make_valid

                    shapely_polygon = make_valid(shapely_polygon)

                shapely_point = Point(point.x(), point.y())
                is_within_polygon = shapely_polygon.contains(shapely_point)
            except Exception as e:
                print(f"Error creating polygon: {e}")
                is_within_polygon = False
        else:
            is_within_polygon = False
        if is_within_polygon:
            # Point is inside a polygon - add as negative point
            print(f"Adding negative point at {point}")
            target_annotation.magic_click_negative_points.append(point)

            # Visual feedback for negative point (red)
            feedback_item = QtWidgets.QGraphicsEllipseItem(
                point.x() - 5, point.y() - 5, 10, 10
            )
            feedback_item.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 150)))
            feedback_item.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2))
            self._scene.addItem(feedback_item)
        else:
            # Point is outside all polygons - add as positive point
            print(f"Adding positive point at {point}")
            target_annotation.magic_click_positive_points.append(point)

            # Visual feedback for positive point (green)
            feedback_item = QtWidgets.QGraphicsEllipseItem(
                point.x() - 5, point.y() - 5, 10, 10
            )
            feedback_item.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 150)))
            feedback_item.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 2))
            self._scene.addItem(feedback_item)

        # Update the mask using SAM with the adjustment points
        self.update_mask_with_adjustment_points(mask_object=target_annotation)

    def update_mask_with_adjustment_points(self, mask_object):
        """Apply the adjustment points to update the current mask"""

        if not hasattr(self, "active_adjustment_annotation_uuid"):
            return

        image_object = self.MainWindow.DH.BLobj.get_current_image_object()
        bbox = mask_object.get_bounding_box()
        x1, y1, w, h = bbox
        x2 = x1 + w
        y2 = y1 + h

        # Convert points to format expected by the model
        positive_points = (
            np.array([(p.x(), p.y()) for p in mask_object.magic_click_positive_points])
            if len(mask_object.magic_click_positive_points) > 0
            else np.array([])
        )

        negative_points = (
            np.array([(p.x(), p.y()) for p in mask_object.magic_click_negative_points])
            if len(mask_object.magic_click_negative_points) > 0
            else np.array([])
        )

        if len(positive_points) == 0 and len(negative_points) == 0:
            return

        # For positive points, get MIN bounding box of all points
        pos_min_x = (
            positive_points[:, 0].min() if len(positive_points) > 0 else float("inf")
        )
        pos_min_y = (
            positive_points[:, 1].min() if len(positive_points) > 0 else float("inf")
        )
        pos_max_x = (
            positive_points[:, 0].max() if len(positive_points) > 0 else float("-inf")
        )
        pos_max_y = (
            positive_points[:, 1].max() if len(positive_points) > 0 else float("-inf")
        )

        # For negative points, get MAX bounding box of all points
        neg_min_x = (
            negative_points[:, 0].min() if len(negative_points) > 0 else float("inf")
        )
        neg_min_y = (
            negative_points[:, 1].min() if len(negative_points) > 0 else float("inf")
        )
        neg_max_x = (
            negative_points[:, 0].max() if len(negative_points) > 0 else float("-inf")
        )
        neg_max_y = (
            negative_points[:, 1].max() if len(negative_points) > 0 else float("-inf")
        )

        # Get overall min/max
        min_x = min(pos_min_x, neg_min_x)
        min_y = min(pos_min_y, neg_min_y)
        max_x = max(pos_max_x, neg_max_x)
        max_y = max(pos_max_y, neg_max_y)

        # adjust bounding box to contain the edges of the points (so points + bbox)
        x1 = min(x1, min_x)
        y1 = min(y1, min_y)
        x2 = max(x2, max_x)
        y2 = max(y2, max_y)

        result = self.process_bounding_box(
            image_object.unique_id,
            [round(x1), round(y1), round(x2), round(y2)],
            mask_object.class_id,
            ideal_annotation_to_image_ratio=0.40,
        )
        if result is None:
            self.threadedBoundingBoxStopWorkerResultFunction()
            return

        mask_object = image_object.get_by_uuid(self.active_adjustment_annotation_uuid)

        if not mask_object:
            return

        celer_sight_object = {
            "image_uuid": result["image_uuid"],
            "condition_uuid": result["treatment_uuid"],
            "group_uuid": result["group_uuid"],
            "class_uuid": self.MainWindow.DH.BLobj.get_current_class_uuid(),
            "mask_uuid": mask_object,
            "SizeX": result["image_object"].SizeX,
            "SizeY": result["image_object"].SizeY,
        }

        print()
        # store original polygon array for undo
        # original_polygon_array = mask_object.get_array().copy()

        if not (len(positive_points) > 0 or len(negative_points) > 0):
            return

        # Get image data
        image_data = result["seg_image"]

        # Apply brightness/contrast adjustments as in draw_bounding_box_stop
        image_data = self.MainWindow.handle_adjustment_to_image(image_data)

        extra_point_prompts = []
        for p in mask_object.magic_click_positive_points:
            extra_point_prompts.append(
                (
                    (p.x() - result["bbox_tile"][0]),
                    (p.y() - result["bbox_tile"][1]),
                    1,
                )
            )
        for p in mask_object.magic_click_negative_points:
            extra_point_prompts.append(
                (
                    (p.x() - result["bbox_tile"][0]),
                    (p.y() - result["bbox_tile"][1]),
                    0,
                )
            )

        updated_mask, offset_x, offset_y = (
            self.MainWindow.sdknn_tool.magic_box_2.magic_box_predict(
                image=image_data,
                celer_sight_object=celer_sight_object,
                prompt_bbox=result["bbox_in_seg"],
                extra_point_prompts=extra_point_prompts,
                post_process=True,
                tile_bbox=result["bbox_tile"],
            )
        )
        # Convert mask to polygon and create new annotation
        from celer_sight_ai.core.magic_box_tools import mask_to_polygon

        resize_factor_x = result["seg_image"].shape[1] / result["bbox_tile"][2]
        resize_factor_y = result["seg_image"].shape[0] / result["bbox_tile"][3]
        new_polygon_array = mask_to_polygon(
            updated_mask,
            image_shape=result["seg_image"].shape,
            offset_x=offset_x,
            offset_y=offset_y,
            resize_factor_x=resize_factor_x,
            resize_factor_y=resize_factor_y,
        )
        # Create new annotation with same class_id
        from celer_sight_ai.historyStack import AdjustPolygonCommand

        # Create the command and add to history stack
        adjust_command = AdjustPolygonCommand(
            polygon_item=mask_object,
            old_polygon_array=mask_object.get_array(),
            new_polygon_array=new_polygon_array,
            mask_uuid=self.active_adjustment_annotation_uuid,
            image_uuid=image_object.unique_id,
            MainWindow=self.MainWindow,
        )
        # Add to undo stack
        self.MainWindow.undoStack.push(adjust_command)

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
        logger.info(f"im drawing state is {self.i_am_drawing_state}")
        logger.info(f"im drawing state is {self.MainWindow.counter_tmp}")
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

            # get the current image uuid
            image_uuid = self.MainWindow.DH.BLobj.get_current_image_object().unique_id
            selected_items = self._scene.selectedItems()
            # get only grip items
            selected_items = [i for i in selected_items if type(i) == GripItem]
            if len(selected_items):
                self.MainWindow.undoStack.push(
                    GripItemMoveCommand(
                        image_uuid=image_uuid,
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
            f"On release function states are {self.ML_brush_tool_object_state} and {self.ML_brush_tool_draw_is_active}"
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

        if self.pop_up_tool_choosing_state == True:
            # self.ui_tool_selection.MyDialog.hide()
            self.pop_up_tool_choosing_state = False
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            self.update_tool()
            return super().mouseReleaseEvent(event)

        return super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.leftMouseBtn_autoRepeat = True
                if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                    if self.aa_tool_draw is True:  # if we are drawing a magic bbox
                        # special case that we adjust the precious bbox
                        self.add_point_as_magic_click(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        return super().mousePressEvent(event)

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
        return super().mousePressEvent(event)

    def keyReleaseEvent(self, ev):
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Shift or key == QtCore.Qt.Key.Key_Alt:
            self.POLYGON_MODIFY_MODE = None
        return super().keyReleaseEvent(ev)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key.Key_Escape:
            if self.i_am_drawing_state is True:
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
        scene_pos = self.mapToScene(event.position().toPoint())
        scene_pos_point = scene_pos.toPoint()

        # Update status text less frequently
        if hasattr(self, "_status_update_timer"):
            self._status_update_timer.stop()
        else:
            self._status_update_timer = QtCore.QTimer()
            self._status_update_timer.setSingleShot(True)
            self._status_update_timer.timeout.connect(
                lambda: self.MainWindow.under_window_comments.setText(
                    f"Scene pos: {int(scene_pos.x())} {int(scene_pos.y())}"
                )
            )
        self._status_update_timer.start(50)
        # Zoom-aware tile culling (debounced)
        if hasattr(self, "_zoom_cull_timer"):
            self._zoom_cull_timer.stop()
        else:
            self._zoom_cull_timer = QtCore.QTimer()
            self._zoom_cull_timer.setSingleShot(True)
            self._zoom_cull_timer.timeout.connect(self.cull_inappropriate_zoom_tiles)
        self._zoom_cull_timer.start(100)

        # rubber band mode:
        if self.scaleBarDraw_duringDraw_STATE is True:
            self.scaleBarWhile(scene_pos_point)

        if self.ui_tool_selection.selected_button == "skeleton grabcut":
            if self.SkGb_during_drawing is True:
                self.SkGbWhileDrawing(scene_pos_point)

        if self.MAGIC_BRUSH_DURING_DRAWING is True:
            self.movePointsBrushToolMagic1(
                self.magic_brush_pos_a.x() - scene_pos.x(),
                self.magic_brush_pos_a.y() - scene_pos.y(),
                self.magic_brush_points_set_A,
            )
            self.magic_brush_pos_a = scene_pos

        # FIX RUBBER BAND HERE
        """
        Draw FG or BG at CELL Random Forrest
        """
        if self.rm_Masks_tool_draw is True:
            self.DeleteAllMasksUnderMouse(scene_pos_point)
            return super().mouseMoveEvent(event)
        if self.i_am_drawing_state is True:
            self.CurrentPosOnScene = scene_pos_point
        if self.aa_review_state is True:
            return super().mouseMoveEvent(event)
        if self.aa_tool_draw is True:
            if self.i_am_drawing_state_bbox is True:
                # starts the drawing process
                self.auto_annotate_tool_while_draw(scene_pos_point)
            self.global_pos = self.mapToGlobal(
                QtCore.QPoint(int(scene_pos.x()), int(scene_pos.y()))
            )
            # if magic tool is active

            # update the position of the guides
            pos = self.mapToScene(event.position().toPoint())
            topLeft = self.mapToScene(0, 0)
            bottomRight = self.mapToScene(
                self.viewport().width(), self.viewport().height()
            )
            if self.h_guide_magic_tool not in self.scene().items():
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

            if self._photo.isUnderMouse() and self.add_mask_btn_state is True:
                if self.MainWindow.counter_tmp > 0 and self.i_am_drawing_state is True:
                    self.draw_while_mouse_move(scene_pos_point)
                    return super().mouseMoveEvent(event)

        if self.ML_brush_tool_draw_is_active is True and self.brushMask_STATE is True:
            if self.ML_brush_tool_draw_foreground_add is True:
                # get pos on scene
                evPos = scene_pos

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
                return super().mouseMoveEvent(event)

            elif self.ML_brush_tool_draw_background_add is True:
                evPos = scene_pos
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
                return super().mouseMoveEvent(event)

        if self.pop_up_tool_choosing_state is True:
            if event.type() == QtCore.QEvent.Type.MouseMove:
                self.ui_tool_selection.MyDialog.mouseMoveEvent(event)
                # return True
        return super().mouseMoveEvent(event)

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

                # Improved gesture handling with matrix validation
                current_matrix = self.transform()

                # Check if matrix is valid (determinant should be positive)
                determinant = current_matrix.determinant()

                if (
                    determinant <= 0
                    or abs(current_matrix.m11()) < 0.001
                    or abs(current_matrix.m22()) < 0.001
                ):
                    # Matrix is corrupted, reset to identity and reapply current zoom
                    logger.warning(
                        "Detected corrupted transformation matrix, resetting"
                    )
                    self.resetTransform()
                    # Restore to a reasonable zoom level
                    if hasattr(self, "_last_valid_zoom"):
                        zoom_level = max(0.1, min(10.0, self._last_valid_zoom))
                        self.scale(zoom_level, zoom_level)
                    return True

                # Store last valid zoom for recovery
                self._last_valid_zoom = abs(current_matrix.m11())

                # Apply zoom with safer bounds
                zoom_delta = np.clip(
                    event.value(), -0.5, 0.5
                )  # Reduced range for stability
                zoom_factor = 1.0 + zoom_delta

                # Ensure zoom factor is reasonable
                zoom_factor = max(0.5, min(2.0, zoom_factor))

                self.scale(zoom_factor, zoom_factor)

                if (
                    hasattr(config, "current_photo_viewer")
                    and config.current_photo_viewer
                ):
                    config.current_photo_viewer.request_debounced_high_res_update(
                        force_update=True
                    )
                return True

            elif typ == QtCore.Qt.NativeGestureType.SwipeNativeGesture:
                print(f"other gesture type: {typ}")
            if typ == QtCore.Qt.NativeGestureType.EndNativeGesture:
                print(f"ending gesture {-1 if self.zoomValue < 0 else 1}")
            return True

        if isinstance(event, QtWidgets.QWidgetItem):
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
                            return super().eventFilter(source, event)
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                if self.ML_brush_tool_object_state is True:
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
            if self.mgcClick_STATE is True or self.mgcBrushT is True:
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
                if self.magic_brush_cursor not in self._scene.items():
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
                        return super().eventFilter(source, event)

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
                    if self.during_drawing_bbox is True:
                        if len(self._scene.selectedItems()) == 0:
                            self.draw_bounding_box_stop_THREADED(
                                self.mapToScene(event.position().toPoint()).toPoint()
                            )
                            self.completeDrawing_Bounding_Box()
                    elif len(self._scene.selectedItems()) == 0:
                        # if control modifier is pressed, ignore, as we are adjusting
                        # the prompt with points
                        if (
                            event.modifiers()
                            & QtCore.Qt.KeyboardModifier.ControlModifier
                        ):
                            return super().eventFilter(source, event)
                        # bounding box beggins process by setting init points x,y and allows for while to start
                        self.auto_annotate_tool_start(
                            self.mapToScene(event.position().toPoint()).toPoint()
                        )
                        self.MainWindow.selected_mask -= 1
        return super().eventFilter(source, event)

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
        import cv2
        import skimage

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
            if type(item) is viewer.PolygonAnnotation:
                if item.isUnderMouse():
                    item.DeleteMask()
                    return

    def clearAllMasksUnderMouse(self, pos):
        # clear masks in current image in the self._scene
        for item in self._scene.items():
            if type(item) is viewer.PolygonAnnotation:
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
            if supplied_mask_bool is False:
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
                self.MainWindow.current_imagenumber,
                self.MainWindow.DH.BLobj.get_current_condition(),
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
                if type(item) is QtWidgets.QGraphicsPixmapItem:
                    if cursor != None:
                        item.setCursor(cursor)
                    continue
                if type(item) is viewer.PolygonAnnotation:
                    item.removeAllPoints()
                    item.canDetectChange = False
                item.setFlag(
                    QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False
                )
        else:
            for item in self._scene.items():
                if type(item) is QtWidgets.QGraphicsPixmapItem:
                    continue
                if type(item) is viewer.PolygonAnnotation:
                    if not item.pointsInited:
                        item.canDetectChange = False
                        item.setFlag(
                            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
                            False,
                        )
                    elif pointsOnly is True:
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
            if type(item) is QtWidgets.QGraphicsPixmapItem:
                continue
            if type(item) is viewer.PolygonAnnotation or type(item) is viewer.GripItem:
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
        if (distanceActual * (self._zoom / 10 + 1)) <= (
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
        from celer_sight_ai.gui.custom_widgets.viewer.scene_annotations.gripItem import GripItem
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
                        if type(item) is viewer.PolygonAnnotation:
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

