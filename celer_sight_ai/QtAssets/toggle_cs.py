# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# ///////////////////////////////////////////////////////////////

from PyQt6 import QtCore, QtGui, QtWidgets


class ButtonToggle(QtWidgets.QCheckBox):
    def __init__(
        self,
        width=60,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCff",
        textColor="#FF0000",
        animation_curve=QtCore.QEasingCurve.Type.OutBounce,
    ):
        QtWidgets.QCheckBox.__init__(self)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, 28)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        self.textColor = textColor

        self.myFont = QtGui.QFont("Lato Black,helvetica", 8)

        # CREATE ANIMATION
        self._circle_position = 3
        self.animation = QtCore.QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)  # Time in milisseconds

        # CONNECT STATE CHANGED
        self.stateChanged.connect(self.start_transition)

    # CREATE NEW SETTER AND GET PROPERTIE
    @QtCore.pyqtProperty(float)  # Get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter  # Setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    # START ANIMATION
    def start_transition(self, value):
        self.animation.stop()  # Stop animation if running
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)

        # START ANIMATION
        self.animation.start()

    # SET NEW HIT AREA
    def hitButton(self, pos: QtCore.QPoint):
        return self.contentsRect().contains(pos)

    # DRAW NEW ITEMS
    def paintEvent(self, e):
        # SET PAINTER
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # SET AS NO PEN
        p.setPen(QtCore.Qt.PenStyle.NoPen)

        # DRAW RECTANGLE
        rect = QtCore.QRect(0, 0, self.width(), self.height())

        # CHECK IF IS CHECKED
        if not self.isChecked():
            # DRAW BG
            p.setBrush(QtGui.QColor(self._bg_color))
            p.drawRoundedRect(
                0,
                0,
                rect.width(),
                rect.height(),
                rect.height() // 2,
                rect.height() // 2,
            )
            p.setBrush(QtGui.QColor(self.textColor))

            # DRAW CIRCLE
            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)
            # #ADD TEXT
            # p.setPen(QtGui.QColor(self._bg_color))
            # p.setFont(self.myFont)
            # p.drawText(QtCore.QPoint(self._circle_position+2,18), "OFF")

        else:
            # DRAW BG
            p.setBrush(QtGui.QColor(self._active_color))
            p.drawRoundedRect(
                0,
                0,
                rect.width(),
                rect.height(),
                rect.height() // 2,
                rect.height() // 2,
            )

            # DRAW CIRCLE
            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

            # #ADD TEXT
            # p.setPen(QtGui.QColor(self._circle_color))
            # p.setFont(self.myFont)
            # p.drawText(QtCore.QPoint(self._circle_position+2,18), "ON")
        # END DRAW
        p.end()
