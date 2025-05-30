from PyQt6 import QtCore, QtGui, QtWidgets


class CenterCircleGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self, radius, x, y, color):
        super().__init__()
        self.radius = radius
        self.setPos(QtCore.QPointF(x, y))
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.setZValue(15)
        self.my_pen = QtGui.QPen(self.color)
        self.my_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))

    def boundingRect(self):
        scale = self.scene().views()[0].transform().m11()
        # The bounding rectangle will be a square with sides of length 2*radius
        return QtCore.QRectF(
            -self.radius / scale,  # x
            -self.radius / scale,  # y
            2 * self.radius / scale,  # width
            2 * self.radius / scale,  # height
        )

    def paint(self, painter, option, widget=None):
        scale = self.scene().views()[0].transform().m11()

        self.my_pen.setWidthF(1.6 / scale)

        # set brush
        painter.setBrush(self.my_brush)
        painter.setPen(self.my_pen)
        painter.drawEllipse(
            QtCore.QPointF(0, 0), self.radius / scale, self.radius / scale
        )

    def update_annotations_color(self, color):
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.my_pen = QtGui.QPen(self.color)
        self.update()
