# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\aa_toolbar_2.ui'
#
# Created by: PyQt6 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets


class auto_annotate_tool_ui(QtWidgets.QDialog):
    """
    signals to get the ui back to mainwindow
    """

    signal_ok = QtCore.pyqtSignal()
    signal_reset = QtCore.pyqtSignal()

    signal_add_FG = QtCore.pyqtSignal(bool)
    signal_add_BG = QtCore.pyqtSignal(bool)

    # reset_clicked = QtCore.pyqtSignal()
    def __init__(self):
        super(auto_annotate_tool_ui, self).__init__()
        auto_annotate_tool_ui.ok_clicked = self.signal_ok
        auto_annotate_tool_ui.reset_clicked = self.signal_reset
        auto_annotate_tool_ui.signal_add_FG = self.signal_add_FG
        auto_annotate_tool_ui.signal_add_BG = self.signal_add_BG
        pass

    def setupUi(self, auto_annotate_tool):
        auto_annotate_tool.setObjectName("auto_annotate_tool")
        auto_annotate_tool.resize(249, 178)
        # Aded tp be transparent
        auto_annotate_tool.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        auto_annotate_tool.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.AA_widget = QtWidgets.QWidget(auto_annotate_tool)
        self.AA_widget.setGeometry(QtCore.QRect(0, 0, 31, 171))
        self.AA_widget.setStyleSheet(
            "\n"
            "QWidget{\n"
            " color: #b1b1b1;\n"
            "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
            "border-width: 0px;\n"
            " border-color: #1e1e1e;\n"
            "border-style: solid;\n"
            "border-radius: 5;\n"
            "padding: 0px;\n"
            "font-size: 12px;\n"
            "padding-left: 0px;\n"
            "padding-right: 0px;\n"
            "}\n"
            "\n"
            "QToolButton{\n"
            "background-color: rgba(255, 255, 255,0);\n"
            "}"
        )
        self.AA_widget.setObjectName("AA_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.AA_widget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_FB_area = QtWidgets.QToolButton(self.AA_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_FB_area.sizePolicy().hasHeightForWidth())
        self.add_FB_area.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//icon_plus_AA.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.add_FB_area.setIcon(icon)
        self.add_FB_area.setIconSize(QtCore.QSize(50, 50))
        self.add_FB_area.setObjectName("add_FB_area")
        self.verticalLayout.addWidget(self.add_FB_area)
        self.add_BG_area = QtWidgets.QToolButton(self.AA_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_BG_area.sizePolicy().hasHeightForWidth())
        self.add_BG_area.setSizePolicy(sizePolicy)
        self.add_BG_area.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//icon_minus_AA.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon1.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//icon_minus_AA_on.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        self.add_BG_area.setIcon(icon1)
        self.add_BG_area.setIconSize(QtCore.QSize(50, 50))
        self.add_BG_area.setObjectName("add_BG_area")
        self.verticalLayout.addWidget(self.add_BG_area)
        self.more_tools_btn = QtWidgets.QToolButton(self.AA_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.more_tools_btn.sizePolicy().hasHeightForWidth()
        )
        self.more_tools_btn.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//Assisted_Neural_off.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.more_tools_btn.setIcon(icon2)
        self.more_tools_btn.setIconSize(QtCore.QSize(30, 45))
        self.more_tools_btn.setObjectName("more_tools_btn")
        self.verticalLayout.addWidget(self.more_tools_btn)
        self.more_tools_btn_3 = QtWidgets.QToolButton(self.AA_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.more_tools_btn_3.sizePolicy().hasHeightForWidth()
        )
        self.more_tools_btn_3.setSizePolicy(sizePolicy)
        self.more_tools_btn_3.setWhatsThis("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//Assisted_line_off.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.more_tools_btn_3.setIcon(icon3)
        self.more_tools_btn_3.setIconSize(QtCore.QSize(30, 45))
        self.more_tools_btn_3.setObjectName("more_tools_btn_3")
        self.verticalLayout.addWidget(self.more_tools_btn_3)
        self.more_tools_btn_2 = QtWidgets.QToolButton(self.AA_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.more_tools_btn_2.sizePolicy().hasHeightForWidth()
        )
        self.more_tools_btn_2.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap("data//icons//icons_aa_tool//settings_off.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.more_tools_btn_2.setIcon(icon4)
        self.more_tools_btn_2.setIconSize(QtCore.QSize(30, 45))
        self.more_tools_btn_2.setObjectName("more_tools_btn_2")
        self.verticalLayout.addWidget(self.more_tools_btn_2)
        self.widget = QtWidgets.QWidget(auto_annotate_tool)
        self.widget.setGeometry(QtCore.QRect(41, 0, 201, 171))
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.widget.setStyleSheet(
            "\n"
            "QWidget{\n"
            " color: #b1b1b1;\n"
            "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
            "border-width: 0px;\n"
            " border-color: #1e1e1e;\n"
            "border-style: solid;\n"
            "border-radius: 5;\n"
            "padding: 0px;\n"
            "font-size: 12px;\n"
            "padding-left: 0px;\n"
            "padding-right: 0px;\n"
            "}\n"
            "QSlider{\n"
            "background-color: rgba(0,0,0,0);\n"
            "}\n"
            "QSlider::groove:horizontal {\n"
            "\n"
            "background-color: white;\n"
            "border: 0px solid black;\n"
            " height: 2px;\n"
            "border-radius: 1px;\n"
            "}\n"
            "QSlider::handle:horizontal {\n"
            "\n"
            "background-color: white;\n"
            "border: 2px solid black;\n"
            " width: 3px;\n"
            "height:20px;\n"
            "line-height: 10px;\n"
            "margin-top: -6px;\n"
            "margin-bottom: -6px;\n"
            " border-radius: 10px;\n"
            "\n"
            "}\n"
            "\n"
            "QSpinBox{\n"
            "color: white;\n"
            "background-color: rgba(0,0,0,0);\n"
            "}\n"
            "\n"
            "QLabel{\n"
            "color : white;\n"
            "background-color: rgba(0,0,0,0);\n"
            "}\n"
            "QFrame{\n"
            "background-color: rgba(0,0,0,0);\n"
            "\n"
            "}\n"
            "QPushButton{\n"
            "color: white;\n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(142, 142, 142, 255), stop:1 rgba(133, 133, 133, 255));\n"
            "border-style: solid;\n"
            "border-color: rgb(20, 20, 20);\n"
            "border-width:1px;\n"
            "border-radius: 5;\n"
            "}\n"
            "QPushButton:hover{\n"
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(102, 102, 102, 255), stop:1 rgba(90, 90, 90, 255));\n"
            "}"
        )
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(11, 9, 9, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBox_4 = QtWidgets.QSpinBox(self.widget)
        self.spinBox_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.spinBox_4.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox_4.setProperty("value", 15)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout.addWidget(self.spinBox_4, 4, 2, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.widget)
        self.spinBox_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.spinBox_3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox_3.setProperty("value", 21)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setWrapping(False)
        self.spinBox.setFrame(True)
        self.spinBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.spinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(4)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 0, 2, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget)
        self.spinBox_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.spinBox_2.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox_2.setProperty("value", 4)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 2, 2, 1, 1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_2.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(10)
        self.horizontalSlider_2.setPageStep(2)
        self.horizontalSlider_2.setProperty("value", 4)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.gridLayout.addWidget(self.horizontalSlider_2, 2, 1, 1, 1)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_3.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.horizontalSlider_3.setMinimum(3)
        self.horizontalSlider_3.setMaximum(51)
        self.horizontalSlider_3.setSingleStep(2)
        self.horizontalSlider_3.setPageStep(6)
        self.horizontalSlider_3.setProperty("value", 21)
        self.horizontalSlider_3.setSliderPosition(21)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.gridLayout.addWidget(self.horizontalSlider_3, 3, 1, 1, 1)
        self.horizontalSlider_4 = QtWidgets.QSlider(self.widget)
        self.horizontalSlider_4.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.horizontalSlider_4.setMinimum(1)
        self.horizontalSlider_4.setMaximum(30)
        self.horizontalSlider_4.setPageStep(4)
        self.horizontalSlider_4.setProperty("value", 15)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.gridLayout.addWidget(self.horizontalSlider_4, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.widget)
        self.horizontalSlider.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.horizontalSlider.setStyleSheet("")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(5)
        self.horizontalSlider.setPageStep(2)
        self.horizontalSlider.setProperty("value", 2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(85, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(85, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addWidget(self.frame, 5, 0, 1, 3)
        self.label_4.setBuddy(self.horizontalSlider_4)
        self.label_3.setBuddy(self.horizontalSlider_3)
        self.label_2.setBuddy(self.horizontalSlider_2)
        self.label.setBuddy(self.horizontalSlider)

        self.retranslateUi(auto_annotate_tool)

        self.horizontalSlider.valueChanged["int"].connect(self.spinBox.setValue)
        self.horizontalSlider_2.valueChanged["int"].connect(self.spinBox_2.setValue)
        self.horizontalSlider_3.valueChanged["int"].connect(self.spinBox_3.setValue)
        self.horizontalSlider_4.valueChanged["int"].connect(self.spinBox_4.setValue)

        self.horizontalSlider.valueChanged["int"].connect(self.spinBox.setValue)
        self.horizontalSlider_2.valueChanged["int"].connect(self.spinBox_2.setValue)
        self.horizontalSlider_3.valueChanged["int"].connect(self.spinBox_3.setValue)
        self.horizontalSlider_4.valueChanged["int"].connect(self.spinBox_4.setValue)

        self.horizontalSlider  # detail
        self.horizontalSlider_2  # closing
        self.horizontalSlider_3  # C. adjast
        self.horizontalSlider_4  # Normalize

        self.add_FB_area.clicked.connect(lambda: self.emit_add_FB_area())
        self.add_BG_area.clicked.connect(lambda: self.emit_add_BG_area())

        self.detail_value = self.horizontalSlider.value()
        self.closing_value = self.horizontalSlider_2.value()
        self.c_adjast = self.horizontalSlider_3.value()
        self.normalize = self.horizontalSlider_4.value()

        self.horizontalSlider.valueChanged["int"].connect(lambda: self.assign_value())
        self.horizontalSlider_2.valueChanged["int"].connect(lambda: self.assign_value())
        self.horizontalSlider_3.valueChanged["int"].connect(lambda: self.assign_value())
        self.horizontalSlider_4.valueChanged["int"].connect(lambda: self.assign_value())

        self.pushButton.clicked.connect(lambda: self.emit_OK())  # OK
        self.pushButton_2.clicked.connect(lambda: self.emit_RESET())  # reset

        self.horizontalSlider_4.setValue(2)

        self.more_tools_btn_2.pressed.connect(self.widget.show)
        QtCore.QMetaObject.connectSlotsByName(auto_annotate_tool)

    def assign_value(self):
        self.detail_value = self.horizontalSlider.value()
        self.closing_value = self.horizontalSlider_2.value()
        self.c_adjast = self.horizontalSlider_3.value()
        self.normalize = self.horizontalSlider_4.value()

    def emit_add_FB_area(self):
        auto_annotate_tool_ui.signal_add_FG.emit(True)

    def emit_add_BG_area(self):
        auto_annotate_tool_ui.signal_add_BG.emit(True)

    def emit_OK(self):
        auto_annotate_tool_ui.ok_clicked.emit()

    def emit_RESET(self):
        auto_annotate_tool_ui.reset_clicked.emit()

    def retranslateUi(self, auto_annotate_tool):
        _translate = QtCore.QCoreApplication.translate
        auto_annotate_tool.setWindowTitle(_translate("auto_annotate_tool", "Form"))
        self.add_FB_area.setText(_translate("auto_annotate_tool", ""))
        self.more_tools_btn.setText(_translate("auto_annotate_tool", ""))
        self.more_tools_btn_3.setText(_translate("auto_annotate_tool", ""))
        self.more_tools_btn_2.setText(_translate("auto_annotate_tool", ""))
        self.label_4.setText(_translate("auto_annotate_tool", "Normalize"))
        self.label_3.setText(_translate("auto_annotate_tool", "C. adjust"))
        self.label_2.setText(_translate("auto_annotate_tool", "Closing"))
        self.label.setText(_translate("auto_annotate_tool", "Detail"))
        self.pushButton.setText(_translate("auto_annotate_tool", "OK"))
        self.pushButton_2.setText(_translate("auto_annotate_tool", "RESET"))

    def assign_values(self, source, value):
        source = value


if __name__ == "__main__":
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    # auto_annotate_tool = QtWidgets.QWidget()
    # ui = auto_annotate_tool_ui()
    # ui.setupUi(auto_annotate_tool)
    # auto_annotate_tool.hide()
    # sys.exit(app.exec())
