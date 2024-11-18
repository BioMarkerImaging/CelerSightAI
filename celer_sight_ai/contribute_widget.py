import typing
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QButtonGroup,
)
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from celer_sight_ai import config


class ContributeButton(QtWidgets.QPushButton):
    def __init__(self, icon_normal, icon_checked, icon_hover, parent=None):
        super().__init__(parent)
        self.color = (255, 214, 0)
        self.icon_normal = QtGui.QIcon(icon_normal)
        self.icon_checked = QtGui.QIcon(icon_checked)
        self.icon_hover = QtGui.QIcon(icon_hover)
        self.installEventFilter(self)
        # Initial state
        self.setCheckable(True)
        self.setIcon(self.icon_normal)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setAutoExclusive(True)
        if self.isChecked():
            self.setIcon(self.icon_checked)
        else:
            self.setIcon(self.icon_normal)
        # Connect signal to slot
        self.toggled.connect(self.updateIcon)

    def updateIcon(self, checked: bool):
        if checked:
            self.setIcon(self.icon_checked)
        else:
            self.setIcon(self.icon_normal)

    # def eventEventFilter(self, event: QEvent) -> bool:
    #     # if event is hover enter
    #     if event.type() == QEvent.Type.HoverEnter:
    #         if not self.is_checked():
    #             self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    #             # set hover_background
    #             # check if its not checked
    #             if not self.is_checked():
    #                 self.setIcon(self.icon_hover)
    #     if event.type() == QEvent.Type.HoverLeave:
    #         if not self.is_checked():
    #             self.setIcon(self.icon_normal)

    #     return super().event(event)

    def event(self, event: QEvent) -> bool:
        # if event is hover enter
        if event.type() == QEvent.Type.HoverEnter:
            if not self.isChecked():
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
                # set hover_background
                # check if its not checked
                if not self.isChecked():
                    self.setIcon(self.icon_hover)
        if event.type() == QEvent.Type.HoverLeave:
            if not self.isChecked():
                self.setIcon(self.icon_normal)

        return super().event(event)

    # def event(self, event: QEvent):
    #     if event.type() == QEvent.Type.HoverEnter:
    #         print("Hovered over the button!")
    #         # Handle hover enter logic here
    #         # For example, you can change the cursor to a hand pointer:
    #         self.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
    #     elif event.type() == QEvent.Type.HoverLeave:
    #         print("Left the hover over the button!")
    #         # Handle hover leave logic here
    #         # Revert the cursor back to arrow:
    #         self.setCursor(QtGui.QCursor(Qt.CursorShape.ArrowCursor))
    #     return super().event(event)


class ContributeWidget(QtWidgets.QWidget):
    """
    This widget is an interface for the user to provide partially and fully annotated data for model training.
    This interface can be used for 'contribute' data , which goes straight to the community models
    or 'private' data for custom personal models of the paid users.
    """

    def __init__(self, parent=None, mode="contribute"):
        super().__init__(parent)
        self.mode = mode
        font_id = QtGui.QFontDatabase.addApplicationFont(
            os.path.join(os.environ.get("CELER_SIGHT_AI_HOME"), "data/fonts/Inter/Static/Inter-ExtraLight.ttf")
        )
        # # Load font from a file into a QByteArray
        # font_file_path = "celer_sight_ai/data/fonts/Roboto/Roboto-Regular.ttf"
        # font_data = QtCore.QByteArray()
        # f = QtCore.QFile(font_file_path)
        # font_data = f.readAll()

        # # Add font from QByteArray to the application
        # font_id = QtGui.QFontDatabase.addApplicationFontFromData(font_data)
        # QtGui.QFontDatabase.addApplicationFont("

        print(font_id)
        self.custom_font_title = QtGui.QFont(
            "Inter", 25
        )  # Replace with the actual name of the font family
        self.custom_font_mini_title = QtGui.QFont(
            "Inter", 20
        )  # Replace with the actual name of the font family
        # self.custom_font_mini_title.setPointSize(18)

    def setupUi(self, w):
        w.setObjectName("ContributeWidget")
        w.resize(530, 440)
        # add background shadow
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        w.setGraphicsEffect(shadow)

        w.setStyleSheet(
            """
            background-color: rgb(45,45,45);
            border: 0px solid rgb(0,0,0);
            border-radius: 15px;
            """
        )

        # set content margins to zero
        w.setContentsMargins(0, 0, 0, 0)

        # remove window handle
        w.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # w.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        w.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, False)
        w.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        w.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoMousePropagation)
        # if there is a parent, center the window to the center of the parent
        if w.parent():
            w.move(
                w.parent().frameGeometry().topLeft()
                + w.parent().rect().center()
                - w.rect().center()
            )

        self.gridLayout = QtWidgets.QGridLayout(w)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 10)
        self.gridLayout.setSpacing(0)
        self.title_label = QtWidgets.QLabel(w)
        self.title_label.setObjectName("title_label")
        self.title_label.setText("Contribute")
        self.gridLayout.setObjectName("gridLayout")
        self.title_label.setFont(self.custom_font_title)
        s = """
            background-color: rgb(25,25,25);
            color: rgb(255,255,255);
            border-top-right-radius: 15px;
            border-top-left-radius: 15px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
            border: 0px solid rgb(25,25,25);
            padding-left: 10px;
            """
        self.title_label.setStyleSheet(s)
        self.title_label.setMaximumHeight(40)
        self.title_label.setMinimumHeight(40)

        self.gridLayout.addWidget(
            self.title_label, 0, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.mini_title = QtWidgets.QLabel(w)
        self.mini_title.setObjectName("mini_title")
        self.mini_title.setText("My experiment is:")
        self.mini_title.setFont(self.custom_font_mini_title)
        self.mini_title.setStyleSheet("padding-left: 10px;")
        self.mini_title.setMaximumHeight(30)
        self.mini_title.setMinimumHeight(30)
        self.gridLayout.addWidget(
            self.mini_title, 1, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        # add images partial annotated and fully annotated
        # add buttons for each
        self.partially_annotated_button = ContributeButton(
            icon_normal="celer_sight_ai/data/icons/partially_annotated_infograph_off.png",
            icon_checked="celer_sight_ai/data/icons/partially_annotated_infograph_on.png",
            icon_hover="celer_sight_ai/data/icons/partially_annotated_infograph.png",
            parent=w,
        )
        self.partially_annotated_button.setObjectName("partially_annotated_button")
        self.partially_annotated_button.setText("")
        # add image
        self.partially_annotated_button.setIcon(
            QtGui.QIcon("celer_sight_ai/data/icons/partially_annotated_infograph.png")
        )
        width = 274
        height = 275
        self.partially_annotated_button.setIconSize(QtCore.QSize(width, height))
        self.partially_annotated_button.setFlat(True)
        self.partially_annotated_button.setMaximumHeight(height)
        self.partially_annotated_button.setMaximumWidth(width)
        self.gridLayout.addWidget(
            self.partially_annotated_button,
            2,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.fully_annotated_button = ContributeButton(
            icon_normal="celer_sight_ai/data/icons/fully_annotated_infograph_off.png",
            icon_checked="celer_sight_ai/data/icons/fully_annotated_infograph_on.png",
            icon_hover="celer_sight_ai/data/icons/fully_annotated_infograph.png",
            parent=w,
        )
        self.fully_annotated_button.setObjectName("fully_annotated_button")
        self.fully_annotated_button.setText("")
        self.fully_annotated_button.setIconSize(QtCore.QSize(width, height))
        self.fully_annotated_button.setFlat(True)
        self.fully_annotated_button.setMaximumHeight(height)
        self.fully_annotated_button.setMaximumWidth(width)
        self.gridLayout.addWidget(
            self.fully_annotated_button,
            2,
            1,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.partially_annotated_button.setChecked(True)

        # add next and prev buttons
        self.next_button = QtWidgets.QPushButton(w)
        self.next_button.setObjectName("next_button")
        self.next_button.setText("Next")
        self.next_button.setMaximumWidth(100)
        self.next_button.setMinimumWidth(100)
        self.next_button.setStyleSheet(
            """
            

            QPushButton{
                margin-left: 10px;
                background-color: rgb(50,100,50);
                border-radius: 5px;
                color: rgb(0,180,0);
                padding: 5px;
            }
            QPushButton:hover{
                background-color: rgb(50,155,50);
                color: rgb(0,255,0);
                }

            """
        )
        self.gridLayout.addWidget(
            self.next_button, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.cancel_button = QtWidgets.QPushButton(w)
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("Cancel")
        self.cancel_button.setMaximumWidth(100)
        self.cancel_button.setMinimumWidth(100)

        self.cancel_button.setStyleSheet(
            """
            
            QPushButton{
                margin-right: 10px;
                background-color: rgb(100,50,50);
                border-radius: 5px;
                color: rgb(180,0,0);
                padding: 5px;
            }
            QPushButton:hover{
                background-color: rgb(155,50,50);
                color: rgb(255,0,0);
                }

            """
        )
        self.gridLayout.addWidget(
            self.cancel_button, 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    ui = ContributeWidget(w)
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec())
