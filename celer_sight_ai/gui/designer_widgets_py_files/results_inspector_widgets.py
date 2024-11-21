# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\results_inspector_widgets.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(862, 648)
        Form.setMinimumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.results_inspector_frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.results_inspector_frame.sizePolicy().hasHeightForWidth()
        )
        self.results_inspector_frame.setSizePolicy(sizePolicy)
        self.results_inspector_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.results_inspector_frame.setMaximumSize(QtCore.QSize(1500, 16777215))
        self.results_inspector_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.results_inspector_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.results_inspector_frame.setObjectName("results_inspector_frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.results_inspector_frame)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.all_condition_analysistable = QtWidgets.QTabWidget(
            self.results_inspector_frame
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.all_condition_analysistable.setFont(font)
        self.all_condition_analysistable.setStyleSheet(
            "\n"
            "QTabBar::tab {\n"
            "    color: #b1b1b1;\n"
            "    border: 1px solid #444;\n"
            "    border-bottom-style: none;\n"
            "    background-color: #323232;\n"
            "    padding-left: 10px;\n"
            "    padding-right: 10px;\n"
            "    padding-top: 3px;\n"
            "    padding-bottom: 2px;\n"
            "    margin-right: -1px;\n"
            "    border-radius: 3px;\n"
            "    height: 100px;\n"
            "    width: 30px;\n"
            "    \n"
            "}\n"
            "\n"
            "QTabWidget::pane {\n"
            "    border: 1px solid #444;\n"
            "    top: 1px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:last\n"
            "{\n"
            "    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
            "    border-top-right-radius: 3px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:first:!selected\n"
            "{\n"
            " margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
            "\n"
            "\n"
            "    border-top-left-radius: 3px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected\n"
            "{\n"
            "    color: #b1b1b1;\n"
            "    border-bottom-style: solid;\n"
            "    margin-top: 3px;\n"
            "    background-color: QLinearGradient(x1:0, y1:0, x2:1, y2:0, stop:1 #212121, stop:.4 #343434);\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected\n"
            "{\n"
            "    border-top-left-radius: 3px;\n"
            "    border-top-right-radius: 3px;\n"
            "    margin-bottom: 0px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected:hover\n"
            "{\n"
            "    /*border-top: 2px solid #ffaa00;\n"
            "    padding-bottom: 3px;*/\n"
            "    border-top-left-radius: 3px;\n"
            "    border-top-right-radius: 3px;\n"
            "    background-color: QLinearGradient(x1:0, y1:0, x2:1, y2:0, stop:1 #212121, stop:0.4 #0084c4);\n"
            "}\n"
            ""
        )
        self.all_condition_analysistable.setTabPosition(
            QtWidgets.QTabWidget.TabPosition.West
        )
        self.all_condition_analysistable.setObjectName("all_condition_analysistable")
        self.all_conditions = QtWidgets.QWidget()
        self.all_conditions.setObjectName("all_conditions")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.all_conditions)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.all_condition_analysistable.addTab(self.all_conditions, "")
        self.per_condition = QtWidgets.QWidget()
        self.per_condition.setObjectName("per_condition")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.per_condition)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.per_condition_analysis_table = QtWidgets.QTableView(self.per_condition)
        self.per_condition_analysis_table.setObjectName("per_condition_analysis_table")
        self.verticalLayout_7.addWidget(self.per_condition_analysis_table)
        self.all_condition_analysistable.addTab(self.per_condition, "")
        self.per_worm = QtWidgets.QWidget()
        self.per_worm.setObjectName("per_worm")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.per_worm)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.worm_check_analysis_splitter = QtWidgets.QSplitter(self.per_worm)
        self.worm_check_analysis_splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.worm_check_analysis_splitter.setObjectName("worm_check_analysis_splitter")
        self.worm_analysis_check = QtWidgets.QGraphicsView(
            self.worm_check_analysis_splitter
        )
        self.worm_analysis_check.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.worm_analysis_check.setObjectName("worm_analysis_check")
        self.per_worm_analysistable = QtWidgets.QTableView(
            self.worm_check_analysis_splitter
        )
        self.per_worm_analysistable.setObjectName("per_worm_analysistable")
        self.verticalLayout_8.addWidget(self.worm_check_analysis_splitter)
        self.frame_per_conditions = QtWidgets.QFrame(self.per_worm)
        self.frame_per_conditions.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_per_conditions.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_per_conditions.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_per_conditions.setObjectName("frame_per_conditions")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_per_conditions)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.display_condtions_btn = QtWidgets.QPushButton(self.frame_per_conditions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.display_condtions_btn.sizePolicy().hasHeightForWidth()
        )
        self.display_condtions_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.display_condtions_btn.setFont(font)
        self.display_condtions_btn.setObjectName("display_condtions_btn")
        self.horizontalLayout_5.addWidget(self.display_condtions_btn)
        self.pushBdisplay_worms_btn = QtWidgets.QPushButton(self.frame_per_conditions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushBdisplay_worms_btn.sizePolicy().hasHeightForWidth()
        )
        self.pushBdisplay_worms_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.pushBdisplay_worms_btn.setFont(font)
        self.pushBdisplay_worms_btn.setObjectName("pushBdisplay_worms_btn")
        self.horizontalLayout_5.addWidget(self.pushBdisplay_worms_btn)
        self.open_pop_up_btn = QtWidgets.QPushButton(self.frame_per_conditions)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.open_pop_up_btn.sizePolicy().hasHeightForWidth()
        )
        self.open_pop_up_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.open_pop_up_btn.setFont(font)
        self.open_pop_up_btn.setObjectName("open_pop_up_btn")
        self.horizontalLayout_5.addWidget(self.open_pop_up_btn)
        self.verticalLayout_8.addWidget(self.frame_per_conditions)
        self.all_condition_analysistable.addTab(self.per_worm, "")
        self.gridLayout_6.addWidget(self.all_condition_analysistable, 1, 0, 1, 1)
        self.ResultsInspaceterToolsFrame = QtWidgets.QFrame(
            self.results_inspector_frame
        )
        self.ResultsInspaceterToolsFrame.setMinimumSize(QtCore.QSize(0, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ResultsInspaceterToolsFrame.setFont(font)
        self.ResultsInspaceterToolsFrame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.ResultsInspaceterToolsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ResultsInspaceterToolsFrame.setObjectName("ResultsInspaceterToolsFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ResultsInspaceterToolsFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CopyDecimalDot = QtWidgets.QPushButton(self.ResultsInspaceterToolsFrame)
        self.CopyDecimalDot.setObjectName("CopyDecimalDot")
        self.horizontalLayout.addWidget(self.CopyDecimalDot)
        self.CopyDecimalComma = QtWidgets.QPushButton(self.ResultsInspaceterToolsFrame)
        self.CopyDecimalComma.setObjectName("CopyDecimalComma")
        self.horizontalLayout.addWidget(self.CopyDecimalComma)
        self.line = QtWidgets.QFrame(self.ResultsInspaceterToolsFrame)
        self.line.setMinimumSize(QtCore.QSize(18, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.ResultsInspaceterToolsFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Results_pg2_AnalysisTypeComboBox = QtWidgets.QComboBox(
            self.ResultsInspaceterToolsFrame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Results_pg2_AnalysisTypeComboBox.sizePolicy().hasHeightForWidth()
        )
        self.Results_pg2_AnalysisTypeComboBox.setSizePolicy(sizePolicy)
        self.Results_pg2_AnalysisTypeComboBox.setMinimumSize(QtCore.QSize(124, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Results_pg2_AnalysisTypeComboBox.setFont(font)
        self.Results_pg2_AnalysisTypeComboBox.setObjectName(
            "Results_pg2_AnalysisTypeComboBox"
        )
        self.Results_pg2_AnalysisTypeComboBox.addItem("")
        self.Results_pg2_AnalysisTypeComboBox.addItem("")
        self.Results_pg2_AnalysisTypeComboBox.addItem("")
        self.horizontalLayout.addWidget(self.Results_pg2_AnalysisTypeComboBox)
        self.channel_analysis_metrics_combobox = QtWidgets.QComboBox(
            self.ResultsInspaceterToolsFrame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.channel_analysis_metrics_combobox.sizePolicy().hasHeightForWidth()
        )
        self.channel_analysis_metrics_combobox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.channel_analysis_metrics_combobox.setFont(font)
        self.channel_analysis_metrics_combobox.setObjectName(
            "channel_analysis_metrics_combobox"
        )
        self.channel_analysis_metrics_combobox.addItem("")
        self.channel_analysis_metrics_combobox.addItem("")
        self.channel_analysis_metrics_combobox.addItem("")
        self.channel_analysis_metrics_combobox.addItem("")
        self.horizontalLayout.addWidget(self.channel_analysis_metrics_combobox)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem)
        self.SpreadSheetState = QtWidgets.QPushButton(self.ResultsInspaceterToolsFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SpreadSheetState.sizePolicy().hasHeightForWidth()
        )
        self.SpreadSheetState.setSizePolicy(sizePolicy)
        self.SpreadSheetState.setStyleSheet(
            "QPushButton{\n"
            "background-color: rgba(255, 255, 255,0);\n"
            "border-width: 0px;  \n"
            "border-style: solid;  \n"
            "border-radius: 6;  \n"
            "padding: 3px;  \n"
            "font-size: 12px;  \n"
            "padding-left: 5px;  \n"
            "padding-right: 5px;\n"
            "}\n"
            "QPushButton:hover{\n"
            "background-color: rgba(255, 255, 255,0);\n"
            "border-width: 0px;  \n"
            "border-style: solid;  \n"
            "border-radius: 6;  \n"
            "padding: 3px;  \n"
            "font-size: 12px;  \n"
            "padding-left: 5px;  \n"
            "padding-right: 5px;\n"
            "}\n"
            ""
        )
        self.SpreadSheetState.setText("")
        self.SpreadSheetState.setObjectName("SpreadSheetState")
        self.horizontalLayout.addWidget(self.SpreadSheetState)
        self.gridLayout_6.addWidget(self.ResultsInspaceterToolsFrame, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.results_inspector_frame)

        self.retranslateUi(Form)
        self.all_condition_analysistable.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.all_condition_analysistable.setTabText(
            self.all_condition_analysistable.indexOf(self.all_conditions),
            _translate("Form", "All conditions"),
        )
        self.all_condition_analysistable.setTabText(
            self.all_condition_analysistable.indexOf(self.per_condition),
            _translate("Form", "Per Condition"),
        )
        self.display_condtions_btn.setText(_translate("Form", "Display\n" "Conditions"))
        self.pushBdisplay_worms_btn.setText(_translate("Form", "Display\n" "Worms"))
        self.open_pop_up_btn.setText(_translate("Form", "Open\n" "Pop-up"))
        self.all_condition_analysistable.setTabText(
            self.all_condition_analysistable.indexOf(self.per_worm),
            _translate("Form", "Per worm"),
        )
        self.CopyDecimalDot.setText(
            _translate("Form", "Copy with \n" " decima as  '.'")
        )
        self.CopyDecimalComma.setText(
            _translate("Form", "Copy with\n" " decimal as ','")
        )
        self.label.setText(_translate("Form", "Analysis type: "))
        self.Results_pg2_AnalysisTypeComboBox.setItemText(
            0, _translate("Form", "Colocalization")
        )
        self.Results_pg2_AnalysisTypeComboBox.setItemText(
            1, _translate("Form", "Mean intensity")
        )
        self.Results_pg2_AnalysisTypeComboBox.setItemText(
            2, _translate("Form", "Aggregates")
        )
        self.channel_analysis_metrics_combobox.setItemText(
            0, _translate("Form", "Count")
        )
        self.channel_analysis_metrics_combobox.setItemText(
            1, _translate("Form", "pearson")
        )
        self.channel_analysis_metrics_combobox.setItemText(
            2, _translate("Form", "Area")
        )
        self.channel_analysis_metrics_combobox.setItemText(
            3, _translate("Form", "R.IntDensity")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())