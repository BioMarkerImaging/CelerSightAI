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
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from celer_sight_ai import config
import json

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QIcon, QPixmap


class AnimatedToggleButton(QPushButton):
    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None, available_modes : list[str , str] =None, *args, **kwargs):
        super().__init__(parent)
        # if available modes are None, then the buttons is UnAvailable else it has lite and pro modes,
        # pro mode is prefered than lite mode
        self.available_modes = available_modes # Should be ["Pro" , "List"]

        self.initUI()
        self.pro_position = QtCore.QRect(
            self.width() - self.button.width() - 5,
            5,
            self.button.width(),
            self.button.height(),
        )
        self.lite_position = QtCore.QRect(
            5, 5, self.button.width(), self.button.height()
        )
        self.halfway_positions = QtCore.QRect(
            (self.width() // 2) - self.button.width() - 5,
            5,
            self.button.width(),
            self.button.height(),
        )
        self.animateButton()

        # # Center the widget horizontally and position it at 80% vertically
        # self.move(
        #     parent.width() // 2 - self.width() // 2,
        #     int(parent.height() * 0.8) - self.height() // 2,
        # )

    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.button = QPushButton("", self)
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(lambda: self.onToggle())

        self.setStyleSheet(
            """
            QPushButton {
                border-radius: 6px;
                background-color: rgb(13,12,0);
            }
            QPushButton:hover{
                border: 0px solid;
            }
            QLabel{
                background-color:rgba(0,0,0,0);
            }
            """
        )

        WIDTH = 115
        HEIGHT = 40

        self.border = 5

        self.setFixedSize(WIDTH, HEIGHT)
        self.button.setFixedSize(
            (WIDTH // 2) - (self.border), HEIGHT - (self.border * 2)
        )

        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.setStyleSheet("background-color: rgb(45,45,0);")

        # Pro label
        self.text_on = QtWidgets.QLabel("Pro", self)
        self.text_on.setStyleSheet(
            """
            #text_on_pro{
                font-family: "Arial";
                font-size: 20px;
                color: rgb(255,231,0);
                background-color: rgba(0,0,0,0);
            
            """
        )
        self.text_on.setObjectName("text_on_pro")
        font = self.text_on.font()
        font.setPointSize(20)
        # set bolt
        font.setBold(True)

        print("Before:", self.text_on.font().toString())

        self.text_on.setFont(font)
        print("After:", self.text_on.font().toString())

        self.text_on.update()  # or label.repaint()

        text_height = (
            self.text_on.fontMetrics().boundingRect(self.text_on.text()).height()
        )
        # plase on the right side of the image
        self.text_on.move(
            (WIDTH // 2) + (self.border * 2) + 8,
            (text_height // 2)
            - (self.border)
            - 2,  # 2 is the boarder of the innder button
        )
        self.text_off = QtWidgets.QLabel("Lite", self)
        # self.text_off.setFont(font)

        text_height = (
            self.text_on.fontMetrics().boundingRect(self.text_off.text()).height()
        )
        text_width = (
            self.text_on.fontMetrics().boundingRect(self.text_off.text()).width()
        )
        self.text_on.setParent(self)

        # Lite label

        # plase on the right side of the image
        self.text_off.move(
            (self.border * 2) + 8,
            (text_height // 2)
            # - (self.border)
            # - 2,  # 2 is the boarder of the innder button
        )
        self.text_off.setStyleSheet("""
                                    color: rgb(255,255,255);
                                    background-color: rgba(0,0,0,0);
                                    """)
        # make text bold
        font = self.text_on.font()
        # font.setPointSize(20)
        # set bolt
        # font.setBold(True)
        self.text_off.setFont(font)
        self.text_off.setParent(self)

        self.text_disabled = QtWidgets.QLabel("UNAVAILABLE", self)

        self.text_disabled.setParent(self)
        # should expand on the whole widget
        self.text_disabled.setGeometry(0, 0, WIDTH, HEIGHT)
        text_width = (
            self.text_on.fontMetrics().boundingRect(self.text_disabled.text()).width()
        )
        text_height = (
            self.text_on.fontMetrics().boundingRect(self.text_disabled.text()).height()
        )
        # plase on middle of the widget
        self.text_disabled.move((WIDTH // 2) - (text_width // 2), 0)

        self.text_disabled.setStyleSheet("color: rgb(255,255,255);")
        # make text bold
        font = self.text_disabled.font()
        font.setBold(True)
        self.text_disabled.setFont(font)
        self.text_disabled.setParent(self)
        self.text_disabled.setStyleSheet("color: rgb(215,50,50);")

        self.update_checked()
        if "Pro" in self.available_modes:
            self.setChecked(True)
        else:
            self.setChecked(False)
        if len(self.available_modes) > 0:  # lite and/ or pro are available
            self.set_model_enabled()
        else:
            self.set_model_disabled()

    def set_model_disabled(self):
        self.button.hide()
        self.text_disabled.setVisible(True)
        self.text_on.setVisible(False)
        self.text_off.setVisible(False)

    def set_model_enabled(self):
        self.button.setEnabled(True)
        self.text_disabled.setVisible(False)
        self.text_on.setVisible(True)
        self.text_off.setVisible(True)

    def update_checked(self):
        if self.isChecked():
            self.text_on.setStyleSheet(
                """
                font-size: 20px;
                font-weight: bold;
                color: rgb(255,231,0);
                
                """
            )
            self.text_off.setStyleSheet(
                """
                color: rgb(75,75,75);
                font-weight: bold;
                font-size: 20px;
                """
            )
        else:
            self.text_on.setStyleSheet(
                """

                    font-size: 20px;
                    font-weight: bold;
                    color: rgb(255,231,0);
                
                """
            )
            self.text_off.setStyleSheet(
                """
                color: rgb(225,225,225);
                font-weight: bold;
                font-size: 20px;

                """
            )

    def onToggle(self):
        # self.button.setText("Pro" if self.button.isChecked() else "Lite")
        self.toggled.emit(self.isChecked())
        self.update_checked()
        self.animateButton()

    def animateButton(self):
        self.animation = QPropertyAnimation(self.button, b"geometry")
        # make it bounce
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.setDuration(400)

        if self.isChecked() and "Pro" in self.available_modes:
            # case were pro is available
            # From Lite to Pro toggle
            end_geometry = self.pro_position
        elif not self.isChecked() and "Lite" in self.available_modes:
            # Case Pro and Lite are available
            # From Pro to Lite
            end_geometry = self.lite_position
        elif self.isChecked() and "Pro" not in self.available_modes:
            # Case Lite is available
            # From Lite to Lite (from halfway to Lite as Pro is not available)
            end_geometry = self.lite_position
            self.animation.setStartValue(self.pro_position)
            QtWidgets.QToolTip.setFont(QtGui.QFont("SansSerif", 10))
            QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), "Pro model not available")
            self.setChecked(False)
            self.update_checked()
        elif not self.isChecked() and "Lite" not in self.available_modes:
            # Case Lite is available
            # From Lite to Lite (from halfway to Lite as Pro is not available)
            self.animation.setStartValue(self.lite_position)
            end_geometry = self.pro_position
            QtWidgets.QToolTip.setFont(QtGui.QFont("SansSerif", 10))
            QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), "Lite model not available")
            self.setChecked(True)
            self.update_checked()

        else:
            # Case Pro and Lite are not available
            # From halfway to halfway (no animation)
            start_geometry = self.halfway_positions
            self.animation.setStartValue(start_geometry)
            end_geometry = self.halfway_positions
            QtWidgets.QToolTip.setFont(QtGui.QFont("SansSerif", 10))
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), "No model available for this task"
            )
            self.setChecked(False)
            self.update_checked()
            self.set_model_disabled()
        self.animation.setEndValue(end_geometry)
        self.animation.start()


if "__main__" == __name__:
    # create a widget and add the button
    app = QApplication([])
    widget = QWidget()
    layout = QVBoxLayout(widget)
    widget.setLayout(layout)
    widget.resize(300, 200)
    widget.setWindowTitle("Animated Toggle Button")
    widget.setWindowIcon(QIcon("icon.png"))
    widget.show()
    # create the animated button
    button = AnimatedToggleButton(widget, available_modes=["Pro", "Lite"])
    layout.addWidget(button)
    # start application
    app.exec()
