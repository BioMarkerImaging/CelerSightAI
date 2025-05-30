from PyQt6 import QtCore, QtGui, QtWidgets


class HoleAnnotationItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, annotation_item, hole_array, array_index=None, color=None):
        super().__init__()
        self.array_index = array_index
        self.hole_array = hole_array
        self.annotation_item = annotation_item
        # set brush to dark gray
        self.setAcceptHoverEvents(True)
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
        self.my_brush.setColor(self.color)
        self.setBrush(self.my_brush)

    def hoverEnterEvent(self, event):
        # make sure current class exists (sometimes due to asyncronus deletion
        # it might no exist anymore)
        if self.my_brush:
            self.color = self.my_brush.color()
            self.color.setAlpha(125)
            self.my_brush.setColor(self.color)
            self.setFocus()
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.color = self.my_brush.color()
        self.color.setAlpha(255)
        self.my_brush.setColor(self.color)
        return super().hoverLeaveEvent(event)

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
