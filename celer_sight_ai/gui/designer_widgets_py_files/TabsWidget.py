# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\backup_work_old - Copy\EasyFluo\UiAssets\TabsWidget.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1073, 768)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainwindow_tabs = QtWidgets.QTabWidget(Form)
        self.mainwindow_tabs.setAutoFillBackground(False)
        self.mainwindow_tabs.setStyleSheet("")
        self.mainwindow_tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.mainwindow_tabs.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.mainwindow_tabs.setTabBarAutoHide(False)
        self.mainwindow_tabs.setObjectName("mainwindow_tabs")
        self.analysis_workspace = QtWidgets.QWidget()
        self.analysis_workspace.setMinimumSize(QtCore.QSize(0, 0))
        self.analysis_workspace.setStyleSheet("")
        self.analysis_workspace.setObjectName("analysis_workspace")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.analysis_workspace)
        self.horizontalLayout_6.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.mainwindow_tabs.addTab(self.analysis_workspace, "")
        self.results_inspector = QtWidgets.QWidget()
        self.results_inspector.setObjectName("results_inspector")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.results_inspector)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mainwindow_tabs.addTab(self.results_inspector, "")
        self.horizontalLayout.addWidget(self.mainwindow_tabs)

        self.retranslateUi(Form)
        self.mainwindow_tabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.mainwindow_tabs.setTabText(
            self.mainwindow_tabs.indexOf(self.analysis_workspace),
            _translate("Form", "             Analysis Workspace              "),
        )
        self.mainwindow_tabs.setTabText(
            self.mainwindow_tabs.indexOf(self.results_inspector),
            _translate("Form", "             Results inspector             "),
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
