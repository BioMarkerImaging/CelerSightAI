import logging

import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from shapely.geometry import Polygon

from celer_sight_ai import config

logger = logging.getLogger(__name__)


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
        super().__init__()
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

        self.set_polygon_array(polygon_array)
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

    def get_hover_opacity(self):
        """
        Maps slider value (0-100) to opacity values:
        - At slider=0: both opacities near zero
        - At slider=50: current values (30, 80)
        - At slider=100: both opacities near 100
        """
        slider_value = self.MyParent.pg1_settings_mask_opasity_slider.value()
        # For hover_opacity: 10 -> 80 -> 100
        if slider_value <= 50:
            hover = 10 + slider_value * (70 / 50)  # Linear from 10 to 80
        else:
            hover = 80 + (slider_value - 50) * (20 / 50)  # Linear from 80 to 100

        return int(hover)

    def get_non_hover_opacity(self):
        # For non_hover_opacity: 0 -> 30 -> 90

        slider_value = self.MyParent.pg1_settings_mask_opasity_slider.value()
        if slider_value <= 50:
            non_hover = slider_value * (30 / 50)  # Linear from 0 to 30
        else:
            non_hover = 30 + (slider_value - 50) * (60 / 50)  # Linear from 30 to 90
        return int(non_hover)

    def set_polygon_array(self, polygon_array):
        self.polygon_array = [
            i.squeeze() for i in polygon_array
        ]  # reference to DH Qpoints polygon

    def set_fast_cache_mode(self, mode=True):
        """
        Sets the cache mode for the polygon annotation item
        If there are a lot of annotation items, high caching is prefered.
        """
        if mode == self.fast_cache_mode:
            return

        # For very large polygons, always use ItemCoordinateCache regardless of mode
        polygon_area = 0
        if self.bbox:
            polygon_area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])

        # If polygon covers more than 1M pixels, force ItemCoordinateCache
        if polygon_area > 1_000_000:
            self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache)
            self.fast_cache_mode = True
        elif mode is True:
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

        opacity_value = self.get_non_hover_opacity()

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
        # Calculate polygon complexity before processing
        total_points = sum(len(arr) for arr in polygon)
        polygon_area = 0

        if len(polygon) > 0:
            np_polygon_0 = np.array(polygon[0])
            self.bbox = [
                int(np.min(np_polygon_0[:, 0])),
                int(np.min(np_polygon_0[:, 1])),
                int(np.max(np_polygon_0[:, 0])),
                int(np.max(np_polygon_0[:, 1])),
            ]
            polygon_area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])
        else:
            return

        # For very large polygons, use ultra-fast rendering mode
        if total_points > 2000 or polygon_area > 10_000_000:
            self._use_ultra_fast_mode(polygon)
        elif total_points > 1000 or polygon_area > 1_000_000:
            path = self._create_optimized_painter_path(polygon)
            if path:
                self.setPath(path)
                self._apply_polygon_styling()
        else:
            path = self._create_standard_painter_path(polygon)
            if path:
                self.setPath(path)
                self._apply_polygon_styling()

    def _use_ultra_fast_mode(self, polygon):
        """Ultra-fast mode for very large polygons - skips expensive operations"""

        # For ultra-large polygons, create a simplified rectangular representation
        # or a heavily decimated polygon
        np_polygon_0 = np.array(polygon[0])

        # Drastically reduce points for performance
        if len(np_polygon_0) > 100:
            # Take every nth point to reduce to ~50-100 points max
            step = max(1, len(np_polygon_0) // 50)
            simplified_polygon = np_polygon_0[::step]
        else:
            simplified_polygon = np_polygon_0

        # Create path with simplified polygon only (ignore holes completely)
        path = QtGui.QPainterPath()
        p_arr = self.array2d_to_qpolygonf(simplified_polygon)
        if p_arr:
            path.addPolygon(p_arr)
            path.closeSubpath()

        self.setPath(path)

        # Use simplified styling for performance
        self._apply_ultra_fast_styling()

        # Disable extra items completely
        self._disable_spawn_extra_items = True

        # Set aggressive performance flags
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemUsesExtendedStyleOption, True
        )
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemClipsToShape, False
        )  # Disable for speed
        self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.ItemCoordinateCache)

        # Disable hover events completely
        self.setAcceptHoverEvents(False)

    def _apply_ultra_fast_styling(self):
        """Simplified styling for ultra-large polygons"""
        colorToUseNow = self.get_mask_color()

        # Simplified pen - no cosmetic, minimal width
        pen = QtGui.QPen(
            QtGui.QColor(colorToUseNow[0], colorToUseNow[1], colorToUseNow[2], 100)
        )
        pen.setWidth(1)  # Fixed minimal width
        pen.setCosmetic(False)  # Faster than cosmetic
        self.setPen(pen)

        # Simplified brush
        brush = QtGui.QBrush(
            QtGui.QColor(colorToUseNow[0], colorToUseNow[1], colorToUseNow[2], 30)
        )
        self.setBrush(brush)

    def _create_optimized_painter_path(self, polygon):
        """Optimized path creation - skip holes for large polygons"""
        path = QtGui.QPainterPath()

        np_polygon_0 = np.array(polygon[0])

        # Reduce precision for very large polygons
        if len(np_polygon_0) > 5000:
            np_polygon_0 = np.round(np_polygon_0, 1)

        p_arr = self.array2d_to_qpolygonf(np_polygon_0)
        if p_arr:
            path.addPolygon(p_arr)
            path.closeSubpath()

            # CRITICAL: Skip hole processing for large polygons - this is the main bottleneck
            polygon_area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])
            if (
                len(polygon) > 1 and polygon_area < 5_000_000
            ):  # Only process holes for smaller polygons
                for h in range(1, len(polygon)):
                    hole_arr = np.array(polygon[h])
                    if len(hole_arr) > 1000:  # Skip very complex holes
                        continue

                    p_arr_hole = self.array2d_to_qpolygonf(hole_arr)
                    if p_arr_hole:
                        sub_path = QtGui.QPainterPath()
                        sub_path.addPolygon(p_arr_hole)
                        sub_path.closeSubpath()
                        path = path.subtracted(sub_path)

        return path

    def _create_standard_painter_path(self, polygon):
        """Standard path creation for normal-sized polygons"""
        path = QtGui.QPainterPath()
        np_polygon_0 = np.array(polygon[0])

        p_arr = self.array2d_to_qpolygonf(np_polygon_0)
        if p_arr:
            path.addPolygon(p_arr)
            path.closeSubpath()
        else:
            return None

        if len(polygon) > 1:
            for h in range(1, len(polygon)):
                p_arr = self.array2d_to_qpolygonf(polygon[h])
                if p_arr:
                    sub_path = QtGui.QPainterPath()
                    sub_path.addPolygon(p_arr)
                    sub_path.closeSubpath()
                    path = path.subtracted(sub_path)

        return path

    def _apply_polygon_styling(self):
        """Separated styling logic for cleaner code"""
        colorToUseNow = self.get_mask_color()

        # Create pen
        somepen = QtGui.QPen(
            QtGui.QColor(
                colorToUseNow[0],
                colorToUseNow[1],
                colorToUseNow[2],
                int(
                    self.get_hover_opacity()
                    * (
                        self.MyParent.pg1_settings_mask_line_opasity_slider.value()
                        / 100
                    )
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
        somepen.setCosmetic(True)
        self.setPen(somepen)

        # Create brush
        brush = QtGui.QBrush(
            QtGui.QColor(
                colorToUseNow[0],
                colorToUseNow[1],
                colorToUseNow[2],
                int(
                    self.get_non_hover_opacity()
                    * (self.MyParent.pg1_settings_mask_opasity_slider.value() / 100)
                ),
            )
        )
        self.setBrush(brush)

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

    # def paint(self, painter, option, widget):
    #     option.state &= ~QtWidgets.QStyle.StateFlag.State_Selected
    #     super().paint(painter, option, widget)

    def paint(self, painter, option, widget):
        """Optimized paint method with viewport awareness"""

        # Early exit if polygon is completely outside viewport
        if self.bbox and hasattr(self, "MyParent") and self.MyParent:
            try:
                viewer = self.MyParent.viewer
                if viewer.hasPhoto():
                    # Get viewport in scene coordinates
                    viewport_rect = viewer.mapToScene(
                        viewer.viewport().rect()
                    ).boundingRect()

                    # Check if polygon intersects with viewport
                    polygon_rect = QtCore.QRectF(
                        self.bbox[0],
                        self.bbox[1],
                        self.bbox[2] - self.bbox[0],
                        self.bbox[3] - self.bbox[1],
                    )

                    if not viewport_rect.intersects(polygon_rect):
                        return  # Don't paint if not visible

                    # For very large polygons, set fast rendering hints
                    polygon_area = (self.bbox[2] - self.bbox[0]) * (
                        self.bbox[3] - self.bbox[1]
                    )
                    if polygon_area > 5_000_000:
                        painter.setRenderHint(
                            QtGui.QPainter.RenderHint.Antialiasing, False
                        )
                        painter.setRenderHint(
                            QtGui.QPainter.RenderHint.SmoothPixmapTransform, False
                        )

            except Exception as e:
                logger.error(f"PolygonAnnotation paint error: {e}")
                pass

        # Remove selection state for performance
        option.state &= ~QtWidgets.QStyle.StateFlag.State_Selected

        # Call parent paint
        super().paint(painter, option, widget)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            event.ignore()
        return super().eventFilter(source, event)

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
        from celer_sight_ai.gui.custom_widgets.scene_objects.holeAnnotation import (
            HoleAnnotationItem,
        )
        if len(self.polygon_array) > 0:
            color = self.get_mask_color()
            for h in range(1, len(self.polygon_array)):
                self.poly_hole_scene_items.append(
                    HoleAnnotationItem(self, self.polygon_array[h], h, color)
                )
                # add it to the viewer scene
                self.MyParent.viewer.scene().addItem(self.poly_hole_scene_items[-1])

    def update_polygon_holes_indexes(self, index: int, amount: int = 1):
        for i, item in enumerate(self.poly_hole_scene_items):
            if i < index:
                continue
            item.array_index += amount

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
            logger.error(f"PolygonAnnotation itemChange error: {e}")
            # log traceback
            import traceback

            logger.error(traceback.format_exc())
        return super().itemChange(change, value)

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
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.endingPosX = self.pos().x()
        self.endingPosY = self.pos().y()
        return super().mouseReleaseEvent(event)

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

        return super().hoverEnterEvent(event)

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
        return super().hoverLeaveEvent(event)
