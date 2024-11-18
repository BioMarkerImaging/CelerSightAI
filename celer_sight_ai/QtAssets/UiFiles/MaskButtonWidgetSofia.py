# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\user\Documents\topfluov1\UiAssets\MaskButtonWidgetSofia.ui'
#
# Created by: PyQt6 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 58)
        Form.setMaximumSize(QtCore.QSize(16777215, 58))
        Form.setStyleSheet(
            "QFrame#MaskWidgetFrame\n"
            "{\n"
            "    \n"
            "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #636a7c, stop: 0.1 #636a7c, stop: 0.5 #636a7c, stop: 0.9 #636a7c, stop: 1 #636a7c);\n"
            "    border-width: 1px;\n"
            "    border-color: #5f6678;\n"
            "    border-style: solid;\n"
            "    border-radius: 3;\n"
            "    padding: 4px;\n"
            "    font-size: 12px;\n"
            "    padding-left: 5px;\n"
            "    padding-right: 5px;\n"
            "}\n"
            "\n"
            "QFrame:pressed#MaskWidgetFrame\n"
            "{\n"
            "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2f384c, stop: 0.1 #2f384c, stop: 0.5 #2f384c, stop: 0.9 #2f384c, stop: 1 #2f384c);\n"
            "    border-width:10px;\n"
            "    border-color: #2f384c;\n"
            "    border-style: solid;\n"
            "    border-radius: 3;\n"
            "}\n"
            "\n"
            "QFrame:hover#MaskWidgetFrame\n"
            "{\n"
            "    border-width:1px;\n"
            "    border-color: #2f384c;\n"
            "    border-style: solid;\n"
            "    border-radius: 3;\n"
            "   background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2f384c, stop: 0.1 #2f384c, stop: 0.5 #2f384c, stop: 0.9 #2f384c, stop: 1 #2f384c);\n"
            "}\n"
            "\n"
            "QPushButton:pressed#MaskPropertiesWidgetLabelcomboBox\n"
            "{\n"
            " border-width:10px;\n"
            " border-color: rgb(255, 255, 255);\n"
            " border-style: solid;\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "QFrame#EyeWidgetFrame\n"
            "{\n"
            "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #636a7c, stop: 0.1 #636a7c, stop: 0.5 #636a7c, stop: 0.9 #636a7c, stop: 1 #636a7c);\n"
            "    border-width: 0px;\n"
            "    border-color: #5f6678;\n"
            "    border-style: solid;\n"
            "    border-radius: 3;\n"
            "    padding: 4px;\n"
            "    font-size: 12px;\n"
            "    padding-left: 5px;\n"
            "    padding-right: 5px;\n"
            "}\n"
            "\n"
            "\n"
            "QPushButton#EyeIcon\n"
            "{\n"
            "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #636a7c, stop: 0.1 #636a7c, stop: 0.5 #636a7c, stop: 0.9 #636a7c, stop: 1 #636a7c);\n"
            "    border-width: 0px;\n"
            "    border-color: #5f6678;\n"
            "    border-style: solid;\n"
            "    border-radius: 3;\n"
            "    padding: 4px;\n"
            "    font-size: 12px;\n"
            "    padding-left: 5px;\n"
            "    padding-right: 5px;\n"
            "}\n"
            ""
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.EyeWidgetFrame = QtWidgets.QFrame(Form)
        self.EyeWidgetFrame.setMinimumSize(QtCore.QSize(40, 0))
        self.EyeWidgetFrame.setMaximumSize(QtCore.QSize(40, 16777215))
        self.EyeWidgetFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.EyeWidgetFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.EyeWidgetFrame.setObjectName("EyeWidgetFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.EyeWidgetFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.EyeIcon = QtWidgets.QPushButton(self.EyeWidgetFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EyeIcon.sizePolicy().hasHeightForWidth())
        self.EyeIcon.setSizePolicy(sizePolicy)
        self.EyeIcon.setMinimumSize(QtCore.QSize(0, 10))
        self.EyeIcon.setStyleSheet("")
        self.EyeIcon.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(
                "C:\\Users\\user\\Documents\\topfluov1\\UiAssets\\../../../.designer/data/icons/Eye.png"
            ),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.EyeIcon.setIcon(icon)
        self.EyeIcon.setIconSize(QtCore.QSize(50, 50))
        self.EyeIcon.setObjectName("EyeIcon")
        self.horizontalLayout_3.addWidget(self.EyeIcon)
        self.horizontalLayout.addWidget(self.EyeWidgetFrame)
        self.MaskWidgetFrame = QtWidgets.QFrame(Form)
        self.MaskWidgetFrame.setStyleSheet(
            "selection-background-color: rgb(182, 182, 182);"
        )
        self.MaskWidgetFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.MaskWidgetFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.MaskWidgetFrame.setObjectName("MaskWidgetFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.MaskWidgetFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ArrayPropertiesWidgetbtn = QtWidgets.QPushButton(self.MaskWidgetFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ArrayPropertiesWidgetbtn.sizePolicy().hasHeightForWidth()
        )
        self.ArrayPropertiesWidgetbtn.setSizePolicy(sizePolicy)
        self.ArrayPropertiesWidgetbtn.setMinimumSize(QtCore.QSize(33, 30))
        self.ArrayPropertiesWidgetbtn.setMaximumSize(QtCore.QSize(33, 30))
        self.ArrayPropertiesWidgetbtn.setText("")
        self.ArrayPropertiesWidgetbtn.setAutoDefault(False)
        self.ArrayPropertiesWidgetbtn.setDefault(False)
        self.ArrayPropertiesWidgetbtn.setFlat(False)
        self.ArrayPropertiesWidgetbtn.setObjectName("ArrayPropertiesWidgetbtn")
        self.horizontalLayout_2.addWidget(self.ArrayPropertiesWidgetbtn)
        self.MaskPropertiesWidgetbtn = QtWidgets.QPushButton(self.MaskWidgetFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MaskPropertiesWidgetbtn.sizePolicy().hasHeightForWidth()
        )
        self.MaskPropertiesWidgetbtn.setSizePolicy(sizePolicy)
        self.MaskPropertiesWidgetbtn.setMaximumSize(QtCore.QSize(70, 70))
        self.MaskPropertiesWidgetbtn.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.MaskPropertiesWidgetbtn.setText("")
        self.MaskPropertiesWidgetbtn.setObjectName("MaskPropertiesWidgetbtn")
        self.horizontalLayout_2.addWidget(self.MaskPropertiesWidgetbtn)
        self.MaskPropertiesWidgetLabelcomboBox = QtWidgets.QLabel(self.MaskWidgetFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MaskPropertiesWidgetLabelcomboBox.sizePolicy().hasHeightForWidth()
        )
        self.MaskPropertiesWidgetLabelcomboBox.setSizePolicy(sizePolicy)
        self.MaskPropertiesWidgetLabelcomboBox.setObjectName(
            "MaskPropertiesWidgetLabelcomboBox"
        )
        self.horizontalLayout_2.addWidget(self.MaskPropertiesWidgetLabelcomboBox)
        self.horizontalLayout.addWidget(self.MaskWidgetFrame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.MaskPropertiesWidgetLabelcomboBox.setText(_translate("Form", "Curves1"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
