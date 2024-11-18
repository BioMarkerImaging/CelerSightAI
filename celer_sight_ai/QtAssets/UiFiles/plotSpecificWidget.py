# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\plotSpecificWidget.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(376, 44)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PlotVisibility = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PlotVisibility.sizePolicy().hasHeightForWidth()
        )
        self.PlotVisibility.setSizePolicy(sizePolicy)
        self.PlotVisibility.setMaximumSize(QtCore.QSize(30, 16777215))
        self.PlotVisibility.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.PlotVisibility.setText("")
        self.PlotVisibility.setObjectName("PlotVisibility")
        self.horizontalLayout.addWidget(self.PlotVisibility)
        self.ConditionLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ConditionLabel.setFont(font)
        self.ConditionLabel.setObjectName("ConditionLabel")
        self.horizontalLayout.addWidget(self.ConditionLabel)
        self.PrimaryColor = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryColor.sizePolicy().hasHeightForWidth())
        self.PrimaryColor.setSizePolicy(sizePolicy)
        self.PrimaryColor.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.PrimaryColor.setText("")
        self.PrimaryColor.setObjectName("PrimaryColor")
        self.horizontalLayout.addWidget(self.PrimaryColor)
        self.EdgeColor = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EdgeColor.sizePolicy().hasHeightForWidth())
        self.EdgeColor.setSizePolicy(sizePolicy)
        self.EdgeColor.setMaximumSize(QtCore.QSize(15, 16777215))
        self.EdgeColor.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.EdgeColor.setText("")
        self.EdgeColor.setObjectName("EdgeColor")
        self.horizontalLayout.addWidget(self.EdgeColor)
        self.line = QtWidgets.QFrame(Form)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(15, 16777215))
        self.pushButton.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ConditionLabel.setText(_translate("Form", "Control"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
