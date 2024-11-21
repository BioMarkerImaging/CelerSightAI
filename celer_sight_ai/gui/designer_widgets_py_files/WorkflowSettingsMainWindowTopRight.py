# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\WorkflowSettingsMainWindowTopRight.ui'
#
# Created by: PyQt6 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WorkflowSettingsTopRightMainWidget(object):
    def setupUi(self, WorkflowSettingsTopRightMainWidget):
        WorkflowSettingsTopRightMainWidget.setObjectName(
            "WorkflowSettingsTopRightMainWidget"
        )
        WorkflowSettingsTopRightMainWidget.resize(341, 76)
        WorkflowSettingsTopRightMainWidget.setMaximumSize(QtCore.QSize(374, 76))
        WorkflowSettingsTopRightMainWidget.setStyleSheet(
            "QWidget#WorkflowSettingsTopRightMainWidget{\n"
            "background-color: rgba(59, 59, 59,0);\n"
            "\n"
            "}\n"
            "QPushButton{\n"
            "background-color: rgba(0, 0, 0,100);\n"
            "border-radius:15px;\n"
            "border-style:solid;\n"
            "border-width:2px;\n"
            "\n"
            "color:rgba(255,255,255,255);\n"
            "}\n"
            "QLabel{\n"
            "background-color:rgba(0,0,0,0);\n"
            "}"
        )
        self.gridLayout = QtWidgets.QGridLayout(WorkflowSettingsTopRightMainWidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.organismSettingBtn = QtWidgets.QPushButton(
            WorkflowSettingsTopRightMainWidget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.organismSettingBtn.sizePolicy().hasHeightForWidth()
        )
        self.organismSettingBtn.setSizePolicy(sizePolicy)
        self.organismSettingBtn.setMinimumSize(QtCore.QSize(95, 0))
        self.organismSettingBtn.setMaximumSize(QtCore.QSize(83, 16777215))
        font = QtGui.QFont()
        font.setFamily("qtquickcontrols")
        font.setPointSize(11)
        self.organismSettingBtn.setFont(font)
        self.organismSettingBtn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.organismSettingBtn.setStyleSheet("")
        self.organismSettingBtn.setObjectName("organismSettingBtn")
        self.gridLayout.addWidget(self.organismSettingBtn, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.area_usedSettingsBnt = QtWidgets.QPushButton(
            WorkflowSettingsTopRightMainWidget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.area_usedSettingsBnt.sizePolicy().hasHeightForWidth()
        )
        self.area_usedSettingsBnt.setSizePolicy(sizePolicy)
        self.area_usedSettingsBnt.setMinimumSize(QtCore.QSize(95, 0))
        self.area_usedSettingsBnt.setMaximumSize(QtCore.QSize(83, 16777215))
        font = QtGui.QFont()
        font.setFamily("qtquickcontrols")
        font.setPointSize(11)
        self.area_usedSettingsBnt.setFont(font)
        self.area_usedSettingsBnt.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.area_usedSettingsBnt.setStyleSheet("")
        self.area_usedSettingsBnt.setObjectName("area_usedSettingsBnt")
        self.gridLayout.addWidget(self.area_usedSettingsBnt, 1, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.AnalysisSettingsBtn = QtWidgets.QPushButton(
            WorkflowSettingsTopRightMainWidget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.AnalysisSettingsBtn.sizePolicy().hasHeightForWidth()
        )
        self.AnalysisSettingsBtn.setSizePolicy(sizePolicy)
        self.AnalysisSettingsBtn.setMinimumSize(QtCore.QSize(95, 0))
        self.AnalysisSettingsBtn.setMaximumSize(QtCore.QSize(83, 16777215))
        font = QtGui.QFont()
        font.setFamily("qtquickcontrols")
        font.setPointSize(11)
        self.AnalysisSettingsBtn.setFont(font)
        self.AnalysisSettingsBtn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.AnalysisSettingsBtn.setStyleSheet("")
        self.AnalysisSettingsBtn.setObjectName("AnalysisSettingsBtn")
        self.gridLayout.addWidget(self.AnalysisSettingsBtn, 1, 3, 1, 1)
        self.WorkflowSettingsTopRightMainWidgetStractureLabel = QtWidgets.QLabel(
            WorkflowSettingsTopRightMainWidget
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.WorkflowSettingsTopRightMainWidgetStractureLabel.setFont(font)
        self.WorkflowSettingsTopRightMainWidgetStractureLabel.setStyleSheet("")
        self.WorkflowSettingsTopRightMainWidgetStractureLabel.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.WorkflowSettingsTopRightMainWidgetStractureLabel.setObjectName(
            "WorkflowSettingsTopRightMainWidgetStractureLabel"
        )
        self.gridLayout.addWidget(
            self.WorkflowSettingsTopRightMainWidgetStractureLabel, 0, 1, 1, 1
        )
        self.WorkflowSettingsTopRightMainWidgetWorkflowLabel = QtWidgets.QLabel(
            WorkflowSettingsTopRightMainWidget
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.WorkflowSettingsTopRightMainWidgetWorkflowLabel.setFont(font)
        self.WorkflowSettingsTopRightMainWidgetWorkflowLabel.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.WorkflowSettingsTopRightMainWidgetWorkflowLabel.setObjectName(
            "WorkflowSettingsTopRightMainWidgetWorkflowLabel"
        )
        self.gridLayout.addWidget(
            self.WorkflowSettingsTopRightMainWidgetWorkflowLabel, 0, 2, 1, 1
        )
        self.WorkflowSettingsTopRightMainWidgetAnalysisLabel = QtWidgets.QLabel(
            WorkflowSettingsTopRightMainWidget
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.WorkflowSettingsTopRightMainWidgetAnalysisLabel.setFont(font)
        self.WorkflowSettingsTopRightMainWidgetAnalysisLabel.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.WorkflowSettingsTopRightMainWidgetAnalysisLabel.setObjectName(
            "WorkflowSettingsTopRightMainWidgetAnalysisLabel"
        )
        self.gridLayout.addWidget(
            self.WorkflowSettingsTopRightMainWidgetAnalysisLabel, 0, 3, 1, 1
        )

        self.retranslateUi(WorkflowSettingsTopRightMainWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkflowSettingsTopRightMainWidget)

    def retranslateUi(self, WorkflowSettingsTopRightMainWidget):
        _translate = QtCore.QCoreApplication.translate
        WorkflowSettingsTopRightMainWidget.setWindowTitle(
            _translate("WorkflowSettingsTopRightMainWidget", "Form")
        )
        self.organismSettingBtn.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Cell")
        )
        self.area_usedSettingsBnt.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Scratch\n" "Assay")
        )
        self.AnalysisSettingsBtn.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Generic\n" "Analysis")
        )
        self.WorkflowSettingsTopRightMainWidgetStractureLabel.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Stracture")
        )
        self.WorkflowSettingsTopRightMainWidgetWorkflowLabel.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Workflow")
        )
        self.WorkflowSettingsTopRightMainWidgetAnalysisLabel.setText(
            _translate("WorkflowSettingsTopRightMainWidget", "Analysis type")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    WorkflowSettingsTopRightMainWidget = QtWidgets.QWidget()
    ui = Ui_WorkflowSettingsTopRightMainWidget()
    ui.setupUi(WorkflowSettingsTopRightMainWidget)
    WorkflowSettingsTopRightMainWidget.show()
    sys.exit(app.exec())
