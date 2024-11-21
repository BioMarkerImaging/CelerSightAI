# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\backup_work_old - Copy\EasyFluo\UiAssets\PerMaskPropertiesWidget.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(358, 68)
        Form.setStyleSheet(
            "\n"
            "\n"
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
            ""
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MaskWidgetFrame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MaskWidgetFrame.sizePolicy().hasHeightForWidth()
        )
        self.MaskWidgetFrame.setSizePolicy(sizePolicy)
        self.MaskWidgetFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.MaskWidgetFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.MaskWidgetFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.MaskWidgetFrame.setObjectName("MaskWidgetFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.MaskWidgetFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.MaskPropertiesWidgetbtn = QtWidgets.QPushButton(self.MaskWidgetFrame)
        self.MaskPropertiesWidgetbtn.setMaximumSize(QtCore.QSize(70, 70))
        self.MaskPropertiesWidgetbtn.setText("")
        self.MaskPropertiesWidgetbtn.setObjectName("MaskPropertiesWidgetbtn")
        self.horizontalLayout_2.addWidget(self.MaskPropertiesWidgetbtn)
        spacerItem = QtWidgets.QSpacerItem(
            90,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.MaskPropertiesWidgetLabelcomboBox = QtWidgets.QComboBox(
            self.MaskWidgetFrame
        )
        self.MaskPropertiesWidgetLabelcomboBox.setMinimumSize(QtCore.QSize(100, 0))
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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
