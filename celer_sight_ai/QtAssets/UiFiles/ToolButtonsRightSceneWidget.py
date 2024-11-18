# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\ToolButtonsRightSceneWidget.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WidgetSceneTools(object):
    def setupUi(self, WidgetSceneTools):
        WidgetSceneTools.setObjectName("WidgetSceneTools")
        WidgetSceneTools.resize(94, 179)
        WidgetSceneTools.setWindowTitle("SideMenu")
        WidgetSceneTools.setWindowOpacity(0.9)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetSceneTools)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ZoomInButtonTool = QtWidgets.QPushButton(WidgetSceneTools)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ZoomInButtonTool.sizePolicy().hasHeightForWidth()
        )
        self.ZoomInButtonTool.setSizePolicy(sizePolicy)
        self.ZoomInButtonTool.setText("")
        self.ZoomInButtonTool.setObjectName("ZoomInButtonTool")
        self.verticalLayout.addWidget(self.ZoomInButtonTool)
        self.ZoomOutButtonTool = QtWidgets.QPushButton(WidgetSceneTools)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ZoomOutButtonTool.sizePolicy().hasHeightForWidth()
        )
        self.ZoomOutButtonTool.setSizePolicy(sizePolicy)
        self.ZoomOutButtonTool.setText("")
        self.ZoomOutButtonTool.setObjectName("ZoomOutButtonTool")
        self.verticalLayout.addWidget(self.ZoomOutButtonTool)
        self.FitbuttonTool = QtWidgets.QPushButton(WidgetSceneTools)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FitbuttonTool.sizePolicy().hasHeightForWidth()
        )
        self.FitbuttonTool.setSizePolicy(sizePolicy)
        self.FitbuttonTool.setText("")
        self.FitbuttonTool.setObjectName("FitbuttonTool")
        self.verticalLayout.addWidget(self.FitbuttonTool)

        self.retranslateUi(WidgetSceneTools)
        QtCore.QMetaObject.connectSlotsByName(WidgetSceneTools)

    def retranslateUi(self, WidgetSceneTools):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    WidgetSceneTools = QtWidgets.QWidget()
    ui = Ui_WidgetSceneTools()
    ui.setupUi(WidgetSceneTools)
    WidgetSceneTools.show()
    sys.exit(app.exec())
