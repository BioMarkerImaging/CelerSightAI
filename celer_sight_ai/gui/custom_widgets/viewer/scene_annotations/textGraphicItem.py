from PyQt6 import QtCore, QtGui, QtWidgets


class ClassGraphicsTextItem(QtWidgets.QGraphicsItem):
    def __init__(self, text, x, y, box_color):
        super().__init__()
        self.text = text
        self.color = QtGui.QColor(
            int(box_color[0] * 0.75), int(box_color[1] * 0.75), int(box_color[2] * 0.75)
        )
        self.x = x
        self.y = y
        self.setZValue(15)
        self.my_pen = QtGui.QPen(self.color)
        self.my_brush = QtGui.QBrush(self.color)
        self.font = QtGui.QFont()

    def boundingRect(self):
        scale = self.scene().views()[0].transform().m11()
        self.font.setPixelSize(int(13.5 / scale))
        fm = QtGui.QFontMetricsF(self.font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()

        return QtCore.QRectF(
            0,
            0,
            text_width * 1.3,
            text_height * 1.3,
        )

    def update_annotations_color(self, color):
        self.color = QtGui.QColor(color[0], color[1], color[2])
        self.my_pen.setColor(self.color)
        self.my_brush.setColor(self.color)
        self.update()

    def paint(self, painter, option, widget=None):
        scale = self.scene().views()[0].transform().m11()
        self.setPos(QtCore.QPointF(self.x + (16 / scale), self.y - (9 / scale)))

        self.my_pen.setWidthF(1 / scale)
        painter.setPen(self.my_pen)
        # get brush

        painter.setBrush(self.my_brush)

        self.font = painter.font()
        self.font.setPixelSize(int(13.5 / scale))
        painter.setFont(self.font)

        fm = QtGui.QFontMetricsF(self.font)
        text_width = fm.horizontalAdvance(self.text)
        text_height = fm.height()
        # Draw the bounding rectangle with rounded corners
        rect = QtCore.QRectF(
            0,
            0,
            (text_width * 1.3),
            (text_height * 1.3),
        )

        painter.drawRoundedRect(rect, 5 / scale, 5 / scale)

        painter.setPen(QtGui.QColor("white"))  # Set text color
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.text)
