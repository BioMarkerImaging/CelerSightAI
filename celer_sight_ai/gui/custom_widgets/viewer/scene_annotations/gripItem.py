from PyQt6 import QtCore, QtGui, QtWidgets


class GripItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, annotation_item=None, index=None, color=[0,0,0]):
        super().__init__()
        self.is_being_created = True
        self.circle = QtGui.QPainterPath()
        self.circle.addEllipse(QtCore.QRectF(-3, -3, 7, 7))
        self.square = QtGui.QPainterPath()
        self.square.addEllipse(QtCore.QRectF(-4, -4, 9, 9))
        self.m_annotation_item = annotation_item
        self.m_index = index
        if annotation_item:
            self.setParentItem(annotation_item)
        self.setPath(self.circle)
        my_color = QtGui.QColor(color[0], color[1], color[2], 255)

        self.my_brush = QtGui.QBrush(QtGui.QColor(my_color.lighter(150)))

        self.setBrush(self.my_brush)
        self.my_pen = QtGui.QPen(QtGui.QColor(my_color.lighter(250)), 1)
        self.my_pen.setCosmetic(True)

        self.setPen(self.my_pen)
        self.setAcceptHoverEvents(True)
        self.setZValue(11)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, False)
        self.magicMove = False  # indicates if its moved by magic brush
        self.is_being_created = False

    def mousePressEvent(self, event):
        if self.m_annotation_item:
            if self.m_annotation_item.MyParent.viewer.MAGIC_BRUSH_STATE:
                # propagate event to parent
                if self.m_annotation_item:
                    return self.m_annotation_item.mousePressEvent(event)
                # self.m_annotation_item.MyParent.viewer.mousePressEvent(event)

    def update_annotations_color(self, color=None):
        if not color:
            return
        my_color = QtGui.QColor(color[0], color[1], color[2], 255)
        self.my_brush = QtGui.QBrush(QtGui.QColor(my_color.lighter(150)))
        self.setBrush(self.my_brush)
        self.my_pen = QtGui.QPen(QtGui.QColor(my_color.lighter(250)), 1)
        self.my_pen.setCosmetic(True)
        self.setPen(self.my_pen)

    def itemChange(self, change, value):
        if self.m_annotation_item:
            if self.m_annotation_item.canDetectChange is True:
                if (
                    change
                    == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemSelectedChange
                ):
                    pass
                elif (
                    change
                    == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
                    and self.isEnabled()
                ):
                    if (
                        self.m_annotation_item.MyParent.viewer.sceneRubberband.isVisible()
                        is True
                    ):
                        self.m_annotation_item.MyParent.viewer.sceneRubberband.hide()
                        self.m_annotation_item.MyParent.viewer.firstRubberBandDrag = (
                            False
                        )
                    if value.isNull():
                        return super().itemChange(change, value)
                    self.m_annotation_item.movePoint(self.m_index, value)
                    self.m_annotation_item.update_annotation()
        return super().itemChange(change, value)
