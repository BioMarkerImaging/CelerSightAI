# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\Ntopfluov1\UiAssets\ImportSettings.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        Dialog.resize(203, 125)
        Dialog.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        Dialog.setStyleSheet(
            "background-color: rgba(50,50,50,225);\n"
            "border-radius: 8;\n"
            "color: rgba(255,255,255 225)"
        )
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.buttonBox.setStyleSheet(
            "         QPushButton  \n"
            "         {  \n"
            "             color: #b1b1b1;  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);  \n"
            "             border-width: 1px;  \n"
            "             border-color: #1e1e1e;  \n"
            "             border-style: solid;  \n"
            "             border-radius: 6;  \n"
            "             padding: 3px;  \n"
            "             font-size: 12px;  \n"
            "             padding-left: 5px;  \n"
            "             padding-right: 5px;  \n"
            "         }  \n"
            "           \n"
            "         QPushButton:pressed  \n"
            "         {  \n"
            "             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);  \n"
            "         }  "
        )
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setText("")
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 2, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkBox.setFont(font)
        self.checkBox.setText("")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Import Settings"))
        self.label_3.setText(_translate("Dialog", "Individual Channels"))
        self.label_2.setText(_translate("Dialog", "CombinedChannels"))
        self.label.setText(_translate("Dialog", "Import the Following:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
