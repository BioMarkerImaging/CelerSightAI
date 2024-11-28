from PyQt6 import QtGui, QtCore, QtWidgets
import os
import logging

logger = logging.getLogger(__name__)


class burger_settings_button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)

        self.normal_icon_path = os.path.join(
            os.environ["CELER_SIGHT_AI_HOME"], "data/icons/burger_config_normal.png"
        )
        self.cross_icon_path = os.path.join(
            os.environ["CELER_SIGHT_AI_HOME"], "data/icons/burger_config_cross.png"
        )
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.burger_state = "on"
        self.set_burger_state("off")
        self.setFixedWidth(20)
        self.setFixedHeight(20)
        # on click switch button state
        self.clicked.connect(lambda: self.switch_button_state())
        # add drop shadow
        self.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=10, xOffset=0, yOffset=0)
        )
        # set hand cursor
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            """
            QPushButton{ 
                border-radius: 10px;
                background-color: rgb(240, 240, 240);
                border: 0px solid rgb(200, 200, 200);
                }
            QPushButton:hover{
                border: 0px solid rgb(200, 200, 200);
            }
            QPushButton:pressed {
                background-color: rgb(200, 200, 200);
            }
            """
        )

    def set_burger_state(self, state="off"):
        self.burger_state = state
        if state == "off":
            self.setIcon(QtGui.QIcon(self.cross_icon_path))
            self.setIconSize(QtCore.QSize(13, 13))
        elif state == "on":
            self.setIcon(QtGui.QIcon(self.normal_icon_path))
            self.setIconSize(QtCore.QSize(13, 13))
        else:
            raise ValueError("burger_state must be either 'on' or 'off'")

    def switch_button_state(self):
        if self.burger_state == "on":
            self.set_burger_state("off")
        elif self.burger_state == "off":
            self.set_burger_state("on")

    def is_on(self):
        return self.burger_state == "on"
