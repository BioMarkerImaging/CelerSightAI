import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets


class BitMapAnnotation(QtWidgets.QGraphicsPixmapItem):
    def __init__(
        self,
        MyParent=None,
        mask_object=None,
        bitmap_array=None,  # np.array
        class_id=None,
        unique_id=None,
    ):
        super().__init__()

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
        from celer_sight_ai.gui.custom_widgets.viewer.scene_annotations.polygonAnnotation import (
            PolygonAnnotation,
        )

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
        return super().paint(painter, option, widget)
