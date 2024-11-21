# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\simplePalleteWidgetSpecific.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(280, 80)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.palleteLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.palleteLabel.setFont(font)
        self.palleteLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.palleteLabel.setObjectName("palleteLabel")
        self.gridLayout.addWidget(self.palleteLabel, 0, 0, 1, 1)
        self.PushButtonPalleteColors = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PushButtonPalleteColors.sizePolicy().hasHeightForWidth()
        )
        self.PushButtonPalleteColors.setSizePolicy(sizePolicy)
        self.PushButtonPalleteColors.setMaximumSize(QtCore.QSize(230, 20))
        self.PushButtonPalleteColors.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.PushButtonPalleteColors.setStyleSheet(
            "QPushButton{\n" "background-color: rgba(0, 0, 0,0);\n" "}"
        )
        self.PushButtonPalleteColors.setText("")
        self.PushButtonPalleteColors.setObjectName("PushButtonPalleteColors")
        self.gridLayout.addWidget(self.PushButtonPalleteColors, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.palleteLabel.setText(_translate("Form", "PalletLabel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
