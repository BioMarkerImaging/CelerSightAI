# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov1\UiAssets\SelectedSettintgsDialog.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(209, 202)
        self.ExpandAnnotationScrollAreaButton = QtWidgets.QPushButton(Dialog)
        self.ExpandAnnotationScrollAreaButton.setGeometry(QtCore.QRect(0, 0, 25, 25))
        self.ExpandAnnotationScrollAreaButton.setText("")
        self.ExpandAnnotationScrollAreaButton.setObjectName(
            "ExpandAnnotationScrollAreaButton"
        )
        self.ExpandAnnotationscrollArea = QtWidgets.QScrollArea(Dialog)
        self.ExpandAnnotationscrollArea.setGeometry(QtCore.QRect(26, 0, 181, 201))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ExpandAnnotationscrollArea.sizePolicy().hasHeightForWidth()
        )
        self.ExpandAnnotationscrollArea.setSizePolicy(sizePolicy)
        self.ExpandAnnotationscrollArea.setWidgetResizable(True)
        self.ExpandAnnotationscrollArea.setObjectName("ExpandAnnotationscrollArea")
        self.ExpandAnnotationscrollAreaWidgetContents = QtWidgets.QWidget()
        self.ExpandAnnotationscrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, 179, 199)
        )
        self.ExpandAnnotationscrollAreaWidgetContents.setObjectName(
            "ExpandAnnotationscrollAreaWidgetContents"
        )
        self.ExpandAnnotationscrollArea.setWidget(
            self.ExpandAnnotationscrollAreaWidgetContents
        )

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
