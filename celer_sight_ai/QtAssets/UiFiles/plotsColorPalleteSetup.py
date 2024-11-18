# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\plotsColorPalleteSetup.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 2)
        self.acceptCancelDialog = QtWidgets.QDialogButtonBox(Dialog)
        self.acceptCancelDialog.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply
            | QtWidgets.QDialogButtonBox.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.acceptCancelDialog.setCenterButtons(False)
        self.acceptCancelDialog.setObjectName("acceptCancelDialog")
        self.gridLayout.addWidget(self.acceptCancelDialog, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Filter"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "All"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "ColorBlind"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "Red shade"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "Green shade"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "Blue shade"))
        self.comboBox_2.setItemText(5, _translate("Dialog", "Bright pallete"))
        self.comboBox_2.setItemText(6, _translate("Dialog", "Dark pallete"))
        self.label_2.setText(_translate("Dialog", "Pallete :"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
