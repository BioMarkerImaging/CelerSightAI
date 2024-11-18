# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\pg1_widget_mask_settings.ui'
#
# Created by: PyQt6 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_pg1_settings_widget(object):
    def setupUi(self, pg1_settings_widget):
        pg1_settings_widget.setObjectName("pg1_settings_widget")
        pg1_settings_widget.resize(393, 771)
        self.horizontalLayout = QtWidgets.QHBoxLayout(pg1_settings_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea_analysis_tools = QtWidgets.QScrollArea(pg1_settings_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scrollArea_analysis_tools.sizePolicy().hasHeightForWidth()
        )
        self.scrollArea_analysis_tools.setSizePolicy(sizePolicy)
        self.scrollArea_analysis_tools.setMinimumSize(QtCore.QSize(384, 0))
        self.scrollArea_analysis_tools.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scrollArea_analysis_tools.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scrollArea_analysis_tools.setWidgetResizable(True)
        self.scrollArea_analysis_tools.setObjectName("scrollArea_analysis_tools")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 374, 769))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mask_contrast_brightness_btn_widget = QtWidgets.QWidget(
            self.scrollAreaWidgetContents_2
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mask_contrast_brightness_btn_widget.sizePolicy().hasHeightForWidth()
        )
        self.mask_contrast_brightness_btn_widget.setSizePolicy(sizePolicy)
        self.mask_contrast_brightness_btn_widget.setMinimumSize(QtCore.QSize(369, 700))
        self.mask_contrast_brightness_btn_widget.setMaximumSize(
            QtCore.QSize(200, 16777215)
        )
        self.mask_contrast_brightness_btn_widget.setStyleSheet(
            "QLabel{\n"
            "color: rgba(255, 255, 255,200);\n"
            "}\n"
            "\n"
            "QCheckBox{\n"
            "border: 0px solid;\n"
            "border-color: rgba(255, 255, 255,0);\n"
            "border-radius: 3px;\n"
            "   background-color: rgba(30, 30, 30,0);\n"
            "}\n"
            "\n"
            "QSpinBox{\n"
            "border: 0px solid;\n"
            "border-color: rgba(255, 255, 255,0);\n"
            "border-radius: 3px;\n"
            "    background-color: rgba(30, 30, 30,120);\n"
            "}\n"
            "\n"
            "\n"
            "QGroupBox {\n"
            "\n"
            "\n"
            "    border: 1px solid;\n"
            "    border-color: rgb(20, 20, 20);\n"
            "    margin-top: 20px;\n"
            "\n"
            "    border-top-left-radius: 15px;\n"
            "    border-top-right-radius:15px;\n"
            "    border-bottom-left-radius: 15px;\n"
            "    border-bottom-right-radius: 15px;\n"
            "    background-color: rgb(90, 90, 90);\n"
            "\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    font-size: 12px;\n"
            "    border-top-color: rgb(255, 255, 255);\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top left;\n"
            "\n"
            "    border-top-left-radius: 15px;\n"
            "    border-top-right-radius:15px;\n"
            "    padding: 2px 10px;\n"
            "    background-color: rgba(255, 255, 255,0);\n"
            "    color:rgba(255, 255, 255,220);\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "\n"
            "    font-size: 12px;\n"
            "    border-radius: 5px;\n"
            "    background-color: rgb(40, 40, 40);\n"
            "}\n"
            "QFrame{\n"
            "    background-color: rgba(40, 40, 40,0);\n"
            "\n"
            "}\n"
            "\n"
            "QSlider{\n"
            "background-color: rgba(0, 0, 0,0);\n"
            "}\n"
            "\n"
            "QSlider::groove:horizontal {\n"
            "background-color: white;\n"
            "border: 0px solid black; \n"
            "height: 2px; \n"
            "border-radius: 1px;\n"
            "}\n"
            "QSlider::handle:horizontal {\n"
            "background-color: white;\n"
            " border: 2px solid black;\n"
            "width: 5px;\n"
            " height: 10px;\n"
            " line-height: 10px;\n"
            " margin-top: -8px;\n"
            "margin-bottom: -8px;\n"
            "border-radius: 10px;\n"
            "}"
        )
        self.mask_contrast_brightness_btn_widget.setObjectName(
            "mask_contrast_brightness_btn_widget"
        )
        self.gridLayout_12 = QtWidgets.QGridLayout(
            self.mask_contrast_brightness_btn_widget
        )
        self.gridLayout_12.setContentsMargins(9, 0, 9, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.pg1_MaskAttributes_groupBox_ToolBox = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_MaskAttributes_groupBox_ToolBox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_MaskAttributes_groupBox_ToolBox.setSizePolicy(sizePolicy)
        self.pg1_MaskAttributes_groupBox_ToolBox.setMinimumSize(QtCore.QSize(108, 99))
        self.pg1_MaskAttributes_groupBox_ToolBox.setMaximumSize(
            QtCore.QSize(16777215, 99)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_MaskAttributes_groupBox_ToolBox.setFont(font)
        self.pg1_MaskAttributes_groupBox_ToolBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_MaskAttributes_groupBox_ToolBox.setFlat(False)
        self.pg1_MaskAttributes_groupBox_ToolBox.setCheckable(False)
        self.pg1_MaskAttributes_groupBox_ToolBox.setObjectName(
            "pg1_MaskAttributes_groupBox_ToolBox"
        )
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4 = QtWidgets.QGridLayout(
            self.pg1_MaskAttributes_groupBox_ToolBox
        )
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.setContentsMargins(9, 6, 9, 7)
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.setHorizontalSpacing(9)
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.setVerticalSpacing(7)
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.setObjectName(
            "MaskAttributesgridLayout_GrouBox_ToolBox_4"
        )
        self.pg1_MaskAttributes_ApplyToEmpty = QtWidgets.QPushButton(
            self.pg1_MaskAttributes_groupBox_ToolBox
        )
        self.pg1_MaskAttributes_ApplyToEmpty.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_MaskAttributes_ApplyToEmpty.sizePolicy().hasHeightForWidth()
        )
        self.pg1_MaskAttributes_ApplyToEmpty.setSizePolicy(sizePolicy)
        self.pg1_MaskAttributes_ApplyToEmpty.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_MaskAttributes_ApplyToEmpty.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pg1_MaskAttributes_ApplyToEmpty.setFont(font)
        self.pg1_MaskAttributes_ApplyToEmpty.setStyleSheet(
            "QPushButton:{\n"
            "color: rgb(255, 255, 255);\n"
            "    background-color: rgb(0, 85, 255);\n"
            "}"
        )
        self.pg1_MaskAttributes_ApplyToEmpty.setObjectName(
            "pg1_MaskAttributes_ApplyToEmpty"
        )
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_MaskAttributes_ApplyToEmpty, 0, 1, 1, 1
        )
        self.pg1_MaskAttributes_ApplyToAllImages = QtWidgets.QPushButton(
            self.pg1_MaskAttributes_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_MaskAttributes_ApplyToAllImages.sizePolicy().hasHeightForWidth()
        )
        self.pg1_MaskAttributes_ApplyToAllImages.setSizePolicy(sizePolicy)
        self.pg1_MaskAttributes_ApplyToAllImages.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_MaskAttributes_ApplyToAllImages.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_MaskAttributes_ApplyToAllImages.setFont(font)
        self.pg1_MaskAttributes_ApplyToAllImages.setObjectName(
            "pg1_MaskAttributes_ApplyToAllImages"
        )
        self.MaskAttributesgridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_MaskAttributes_ApplyToAllImages, 0, 2, 1, 1
        )
        self.gridLayout_12.addWidget(
            self.pg1_MaskAttributes_groupBox_ToolBox, 6, 0, 1, 2
        )
        self.pg1_Maskshandler_groupBox_ToolBox = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_Maskshandler_groupBox_ToolBox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_Maskshandler_groupBox_ToolBox.setSizePolicy(sizePolicy)
        self.pg1_Maskshandler_groupBox_ToolBox.setMinimumSize(QtCore.QSize(108, 99))
        self.pg1_Maskshandler_groupBox_ToolBox.setMaximumSize(
            QtCore.QSize(16777215, 99)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_Maskshandler_groupBox_ToolBox.setFont(font)
        self.pg1_Maskshandler_groupBox_ToolBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_Maskshandler_groupBox_ToolBox.setFlat(False)
        self.pg1_Maskshandler_groupBox_ToolBox.setCheckable(False)
        self.pg1_Maskshandler_groupBox_ToolBox.setObjectName(
            "pg1_Maskshandler_groupBox_ToolBox"
        )
        self.gridLayout_GrouBox_ToolBox_4 = QtWidgets.QGridLayout(
            self.pg1_Maskshandler_groupBox_ToolBox
        )
        self.gridLayout_GrouBox_ToolBox_4.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.gridLayout_GrouBox_ToolBox_4.setContentsMargins(9, 6, 9, 7)
        self.gridLayout_GrouBox_ToolBox_4.setHorizontalSpacing(9)
        self.gridLayout_GrouBox_ToolBox_4.setVerticalSpacing(7)
        self.gridLayout_GrouBox_ToolBox_4.setObjectName("gridLayout_GrouBox_ToolBox_4")
        self.pg1_Maskshandler_DeleteAll_button = QtWidgets.QPushButton(
            self.pg1_Maskshandler_groupBox_ToolBox
        )
        self.pg1_Maskshandler_DeleteAll_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_Maskshandler_DeleteAll_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_Maskshandler_DeleteAll_button.setSizePolicy(sizePolicy)
        self.pg1_Maskshandler_DeleteAll_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_Maskshandler_DeleteAll_button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_Maskshandler_DeleteAll_button.setFont(font)
        self.pg1_Maskshandler_DeleteAll_button.setStyleSheet(
            "QPushButton:{\n"
            "color: rgb(255, 255, 255);\n"
            "    background-color: rgb(0, 85, 255);\n"
            "}"
        )
        self.pg1_Maskshandler_DeleteAll_button.setObjectName(
            "pg1_Maskshandler_DeleteAll_button"
        )
        self.gridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_Maskshandler_DeleteAll_button, 0, 1, 1, 1
        )
        self.pg1_Maskshandler_DeleteAllPolygon_button = QtWidgets.QPushButton(
            self.pg1_Maskshandler_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_Maskshandler_DeleteAllPolygon_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_Maskshandler_DeleteAllPolygon_button.setSizePolicy(sizePolicy)
        self.pg1_Maskshandler_DeleteAllPolygon_button.setMinimumSize(
            QtCore.QSize(80, 20)
        )
        self.pg1_Maskshandler_DeleteAllPolygon_button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_Maskshandler_DeleteAllPolygon_button.setFont(font)
        self.pg1_Maskshandler_DeleteAllPolygon_button.setObjectName(
            "pg1_Maskshandler_DeleteAllPolygon_button"
        )
        self.gridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_Maskshandler_DeleteAllPolygon_button, 0, 2, 1, 1
        )
        self.pg1_Maskshandler_DeleteAllBit_button = QtWidgets.QPushButton(
            self.pg1_Maskshandler_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_Maskshandler_DeleteAllBit_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_Maskshandler_DeleteAllBit_button.setSizePolicy(sizePolicy)
        self.pg1_Maskshandler_DeleteAllBit_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_Maskshandler_DeleteAllBit_button.setObjectName(
            "pg1_Maskshandler_DeleteAllBit_button"
        )
        self.gridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_Maskshandler_DeleteAllBit_button, 1, 1, 1, 1
        )
        self.pg1_settings_lasso_Render = QtWidgets.QPushButton(
            self.pg1_Maskshandler_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_lasso_Render.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_lasso_Render.setSizePolicy(sizePolicy)
        self.pg1_settings_lasso_Render.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_settings_lasso_Render.setObjectName("pg1_settings_lasso_Render")
        self.gridLayout_GrouBox_ToolBox_4.addWidget(
            self.pg1_settings_lasso_Render, 1, 2, 1, 1
        )
        self.gridLayout_12.addWidget(self.pg1_Maskshandler_groupBox_ToolBox, 4, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_12.addItem(spacerItem, 11, 1, 1, 1)
        self.pg1_channels_groupBox_ToolBox = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_channels_groupBox_ToolBox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_channels_groupBox_ToolBox.setSizePolicy(sizePolicy)
        self.pg1_channels_groupBox_ToolBox.setMinimumSize(QtCore.QSize(108, 60))
        self.pg1_channels_groupBox_ToolBox.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_channels_groupBox_ToolBox.setFont(font)
        self.pg1_channels_groupBox_ToolBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_channels_groupBox_ToolBox.setFlat(False)
        self.pg1_channels_groupBox_ToolBox.setCheckable(False)
        self.pg1_channels_groupBox_ToolBox.setObjectName(
            "pg1_channels_groupBox_ToolBox"
        )
        self.gridLayout_GrouBox_ToolBox_5 = QtWidgets.QGridLayout(
            self.pg1_channels_groupBox_ToolBox
        )
        self.gridLayout_GrouBox_ToolBox_5.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.gridLayout_GrouBox_ToolBox_5.setContentsMargins(10, 5, 26, 5)
        self.gridLayout_GrouBox_ToolBox_5.setHorizontalSpacing(0)
        self.gridLayout_GrouBox_ToolBox_5.setVerticalSpacing(7)
        self.gridLayout_GrouBox_ToolBox_5.setObjectName("gridLayout_GrouBox_ToolBox_5")
        self.pg1_green_channel_button_visual = QtWidgets.QPushButton(
            self.pg1_channels_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_green_channel_button_visual.sizePolicy().hasHeightForWidth()
        )
        self.pg1_green_channel_button_visual.setSizePolicy(sizePolicy)
        self.pg1_green_channel_button_visual.setMinimumSize(QtCore.QSize(50, 20))
        self.pg1_green_channel_button_visual.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_green_channel_button_visual.setFont(font)
        self.pg1_green_channel_button_visual.setStyleSheet(
            "\n"
            "QPushButton{\n"
            "            color: rgb(255, 255, 255);\n"
            "\n"
            "             border-width: 2px;  \n"
            "             border-style: solid;  \n"
            "             border-radius: 0;  \n"
            "             padding: 3px;  \n"
            "\n"
            "             padding-left: 5px;  \n"
            "             padding-right: 5px;  \n"
            "            background-color: rgb(5, 255, 5);\n"
            "            border-color: rgb(0, 20, 0);\n"
            "            font-size: 19px;\n"
            "}\n"
            "\n"
            "QPushButton:hover{\n"
            "    border-width: 2px;  \n"
            "    border-color: rgb(0, 100, 0);\n"
            "    border-style: solid;  \n"
            "}\n"
            "\n"
            "QPushButton:checked{\n"
            "    border-width: 2px;  \n"
            "    background-color:rgb(40,80,40);\n"
            "    border-style: solid;  \n"
            "}\n"
            ""
        )
        self.pg1_green_channel_button_visual.setCheckable(True)
        self.pg1_green_channel_button_visual.setChecked(True)
        self.pg1_green_channel_button_visual.setObjectName(
            "pg1_green_channel_button_visual"
        )
        self.gridLayout_GrouBox_ToolBox_5.addWidget(
            self.pg1_green_channel_button_visual, 0, 3, 1, 1
        )
        self.pg1_red_channel_button_visual = QtWidgets.QPushButton(
            self.pg1_channels_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_red_channel_button_visual.sizePolicy().hasHeightForWidth()
        )
        self.pg1_red_channel_button_visual.setSizePolicy(sizePolicy)
        self.pg1_red_channel_button_visual.setMinimumSize(QtCore.QSize(44, 20))
        self.pg1_red_channel_button_visual.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_red_channel_button_visual.setFont(font)
        self.pg1_red_channel_button_visual.setStyleSheet(
            "\n"
            "QPushButton{\n"
            "    color: rgb(255, 255, 255);\n"
            "    border-width: 2px;  \n"
            "    border-right-width: 0 px;\n"
            "    border-style: solid;  \n"
            "    border-radius: 10;  \n"
            "    padding: 3px;  \n"
            "    border-top-right-radius: 0;\n"
            "    border-bottom-right-radius: 0;\n"
            "    padding-left: 5px;  \n"
            "    padding-right: 5px;  \n"
            "    background-color: rgb(225, 0, 4);\n"
            "    border-color: rgb(20, 0, 0);\n"
            "    font-size: 19px;\n"
            "}\n"
            "\n"
            "QPushButton:hover{\n"
            "    border-width: 2px;  \n"
            "    border-color: rgb(100, 0, 0);\n"
            "    border-right-width: 0 px;\n"
            "    border-style: solid;  \n"
            "}\n"
            "\n"
            "QPushButton:checked{\n"
            "    border-width: 2px;  \n"
            "    background-color:rgb(80,40,40);\n"
            "    border-right-width: 0 px;\n"
            "    border-style: solid;  \n"
            "}\n"
            ""
        )
        self.pg1_red_channel_button_visual.setCheckable(True)
        self.pg1_red_channel_button_visual.setChecked(True)
        self.pg1_red_channel_button_visual.setObjectName(
            "pg1_red_channel_button_visual"
        )
        self.gridLayout_GrouBox_ToolBox_5.addWidget(
            self.pg1_red_channel_button_visual, 0, 2, 1, 1
        )
        self.pg1_blue_channel_button_visual = QtWidgets.QPushButton(
            self.pg1_channels_groupBox_ToolBox
        )
        self.pg1_blue_channel_button_visual.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_blue_channel_button_visual.sizePolicy().hasHeightForWidth()
        )
        self.pg1_blue_channel_button_visual.setSizePolicy(sizePolicy)
        self.pg1_blue_channel_button_visual.setMinimumSize(QtCore.QSize(50, 20))
        self.pg1_blue_channel_button_visual.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pg1_blue_channel_button_visual.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_blue_channel_button_visual.setFont(font)
        self.pg1_blue_channel_button_visual.setStyleSheet(
            "\n"
            "QPushButton{\n"
            "        color: rgb(255, 255, 255);\n"
            "\n"
            "             border-width: 2px;  \n"
            "            border-left-width: 0px;\n"
            "             border-style: solid;  \n"
            "             border-radius: 10;  \n"
            "             padding: 3px;  \n"
            "                border-top-left-radius: 0;\n"
            "                border-bottom-left-radius: 0;\n"
            "             padding-left: 5px;  \n"
            "             padding-right: 5px;  \n"
            "        background-color: rgb(5,5 , 255);\n"
            "        border-color: rgb(5, 5, 20);\n"
            "        font-size: 19px;\n"
            "}\n"
            "\n"
            "\n"
            "QPushButton:hover{\n"
            "    border-width: 2px;  \n"
            "    border-color: rgb(0, 0, 200);\n"
            "    border-left-width: 0 px;\n"
            "    border-style: solid;  \n"
            "}\n"
            "\n"
            "QPushButton:checked{\n"
            "    border-width: 2px;  \n"
            "    background-color:rgb(40,40,80);\n"
            "    border-left-width: 0 px;\n"
            "    border-style: solid;  \n"
            "}\n"
            ""
        )
        self.pg1_blue_channel_button_visual.setCheckable(True)
        self.pg1_blue_channel_button_visual.setChecked(True)
        self.pg1_blue_channel_button_visual.setObjectName(
            "pg1_blue_channel_button_visual"
        )
        self.gridLayout_GrouBox_ToolBox_5.addWidget(
            self.pg1_blue_channel_button_visual, 0, 4, 1, 1
        )
        self.labeActiveChannelsLabel = QtWidgets.QLabel(
            self.pg1_channels_groupBox_ToolBox
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labeActiveChannelsLabel.setFont(font)
        self.labeActiveChannelsLabel.setObjectName("labeActiveChannelsLabel")
        self.gridLayout_GrouBox_ToolBox_5.addWidget(
            self.labeActiveChannelsLabel, 0, 0, 1, 1
        )
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_GrouBox_ToolBox_5.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_12.addWidget(self.pg1_channels_groupBox_ToolBox, 1, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_12.addItem(spacerItem2, 11, 0, 1, 1)
        self.pg1_settings_groupBox_ToolBox = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_groupBox_ToolBox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_groupBox_ToolBox.setSizePolicy(sizePolicy)
        self.pg1_settings_groupBox_ToolBox.setMinimumSize(QtCore.QSize(108, 99))
        self.pg1_settings_groupBox_ToolBox.setMaximumSize(QtCore.QSize(16777215, 99))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_groupBox_ToolBox.setFont(font)
        self.pg1_settings_groupBox_ToolBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignCenter
            | QtCore.Qt.AlignmentFlag.AlignTop
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_settings_groupBox_ToolBox.setFlat(False)
        self.pg1_settings_groupBox_ToolBox.setCheckable(False)
        self.pg1_settings_groupBox_ToolBox.setObjectName(
            "pg1_settings_groupBox_ToolBox"
        )
        self.gridLayout_GrouBox_ToolBox_2 = QtWidgets.QGridLayout(
            self.pg1_settings_groupBox_ToolBox
        )
        self.gridLayout_GrouBox_ToolBox_2.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.gridLayout_GrouBox_ToolBox_2.setContentsMargins(9, 6, 9, 7)
        self.gridLayout_GrouBox_ToolBox_2.setHorizontalSpacing(9)
        self.gridLayout_GrouBox_ToolBox_2.setVerticalSpacing(7)
        self.gridLayout_GrouBox_ToolBox_2.setObjectName("gridLayout_GrouBox_ToolBox_2")
        self.pg1_settings_lasso_remove_button = QtWidgets.QPushButton(
            self.pg1_settings_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_lasso_remove_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_lasso_remove_button.setSizePolicy(sizePolicy)
        self.pg1_settings_lasso_remove_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_settings_lasso_remove_button.setObjectName(
            "pg1_settings_lasso_remove_button"
        )
        self.gridLayout_GrouBox_ToolBox_2.addWidget(
            self.pg1_settings_lasso_remove_button, 1, 2, 1, 1
        )
        self.pg1_settings_lasso_plus_button = QtWidgets.QPushButton(
            self.pg1_settings_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_lasso_plus_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_lasso_plus_button.setSizePolicy(sizePolicy)
        self.pg1_settings_lasso_plus_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_settings_lasso_plus_button.setObjectName(
            "pg1_settings_lasso_plus_button"
        )
        self.gridLayout_GrouBox_ToolBox_2.addWidget(
            self.pg1_settings_lasso_plus_button, 1, 1, 1, 1
        )
        self.pg1_settings_poly_add_button = QtWidgets.QPushButton(
            self.pg1_settings_groupBox_ToolBox
        )
        self.pg1_settings_poly_add_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_poly_add_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_poly_add_button.setSizePolicy(sizePolicy)
        self.pg1_settings_poly_add_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_settings_poly_add_button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_settings_poly_add_button.setFont(font)
        self.pg1_settings_poly_add_button.setStyleSheet(
            "QPushButton:{\n"
            "color: rgb(255, 255, 255);\n"
            "    background-color: rgb(0, 85, 255);\n"
            "}"
        )
        self.pg1_settings_poly_add_button.setObjectName("pg1_settings_poly_add_button")
        self.gridLayout_GrouBox_ToolBox_2.addWidget(
            self.pg1_settings_poly_add_button, 0, 1, 1, 1
        )
        self.pg1_settings_poly_remove_button = QtWidgets.QPushButton(
            self.pg1_settings_groupBox_ToolBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_poly_remove_button.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_poly_remove_button.setSizePolicy(sizePolicy)
        self.pg1_settings_poly_remove_button.setMinimumSize(QtCore.QSize(80, 20))
        self.pg1_settings_poly_remove_button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg1_settings_poly_remove_button.setFont(font)
        self.pg1_settings_poly_remove_button.setObjectName(
            "pg1_settings_poly_remove_button"
        )
        self.gridLayout_GrouBox_ToolBox_2.addWidget(
            self.pg1_settings_poly_remove_button, 0, 2, 1, 1
        )
        self.gridLayout_12.addWidget(self.pg1_settings_groupBox_ToolBox, 5, 0, 1, 2)
        self.pg1_settings_groupBox_brightness_contrast = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_groupBox_brightness_contrast.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_groupBox_brightness_contrast.setSizePolicy(sizePolicy)
        self.pg1_settings_groupBox_brightness_contrast.setMinimumSize(
            QtCore.QSize(0, 0)
        )
        self.pg1_settings_groupBox_brightness_contrast.setMaximumSize(
            QtCore.QSize(16777215, 250)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_groupBox_brightness_contrast.setFont(font)
        self.pg1_settings_groupBox_brightness_contrast.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_settings_groupBox_brightness_contrast.setObjectName(
            "pg1_settings_groupBox_brightness_contrast"
        )
        self.gridLayout_18 = QtWidgets.QGridLayout(
            self.pg1_settings_groupBox_brightness_contrast
        )
        self.gridLayout_18.setContentsMargins(9, 5, 9, 6)
        self.gridLayout_18.setHorizontalSpacing(10)
        self.gridLayout_18.setVerticalSpacing(11)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.pg1_settings_ContrastAffectsNN_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_ContrastAffectsNN_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_ContrastAffectsNN_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_ContrastAffectsNN_label.setFont(font)
        self.pg1_settings_ContrastAffectsNN_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.pg1_settings_ContrastAffectsNN_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg1_settings_ContrastAffectsNN_label.setObjectName(
            "pg1_settings_ContrastAffectsNN_label"
        )
        self.gridLayout_18.addWidget(
            self.pg1_settings_ContrastAffectsNN_label, 1, 0, 1, 1
        )
        self.spinBox_Theta_3 = QtWidgets.QSpinBox(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinBox_Theta_3.sizePolicy().hasHeightForWidth()
        )
        self.spinBox_Theta_3.setSizePolicy(sizePolicy)
        self.spinBox_Theta_3.setFrame(True)
        self.spinBox_Theta_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_Theta_3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox_Theta_3.setKeyboardTracking(False)
        self.spinBox_Theta_3.setObjectName("spinBox_Theta_3")
        self.gridLayout_18.addWidget(self.spinBox_Theta_3, 5, 2, 1, 1)
        self.pg1_settings_brightness_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_brightness_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_brightness_label.setSizePolicy(sizePolicy)
        self.pg1_settings_brightness_label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_brightness_label.setFont(font)
        self.pg1_settings_brightness_label.setObjectName(
            "pg1_settings_brightness_label"
        )
        self.gridLayout_18.addWidget(self.pg1_settings_brightness_label, 2, 0, 1, 1)
        self.pg1_settings_brightness_slider = QtWidgets.QSlider(
            self.pg1_settings_groupBox_brightness_contrast
        )
        self.pg1_settings_brightness_slider.setStyleSheet("")
        self.pg1_settings_brightness_slider.setMinimum(-255)
        self.pg1_settings_brightness_slider.setMaximum(255)
        self.pg1_settings_brightness_slider.setPageStep(1)
        self.pg1_settings_brightness_slider.setProperty("value", 0)
        self.pg1_settings_brightness_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.pg1_settings_brightness_slider.setInvertedAppearance(False)
        self.pg1_settings_brightness_slider.setObjectName(
            "pg1_settings_brightness_slider"
        )
        self.gridLayout_18.addWidget(self.pg1_settings_brightness_slider, 2, 1, 1, 1)
        self.pg1_settings_contras_slider = QtWidgets.QSlider(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_contras_slider.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_contras_slider.setSizePolicy(sizePolicy)
        self.pg1_settings_contras_slider.setStyleSheet("")
        self.pg1_settings_contras_slider.setMinimum(-100)
        self.pg1_settings_contras_slider.setMaximum(100)
        self.pg1_settings_contras_slider.setPageStep(1)
        self.pg1_settings_contras_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.pg1_settings_contras_slider.setObjectName("pg1_settings_contras_slider")
        self.gridLayout_18.addWidget(self.pg1_settings_contras_slider, 5, 1, 1, 1)
        self.pg1_settings_contras_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_contras_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_contras_label.setSizePolicy(sizePolicy)
        self.pg1_settings_contras_label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_contras_label.setFont(font)
        self.pg1_settings_contras_label.setObjectName("pg1_settings_contras_label")
        self.gridLayout_18.addWidget(self.pg1_settings_contras_label, 5, 0, 1, 1)
        self.spinBox_Phi_3 = QtWidgets.QSpinBox(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinBox_Phi_3.sizePolicy().hasHeightForWidth()
        )
        self.spinBox_Phi_3.setSizePolicy(sizePolicy)
        self.spinBox_Phi_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.spinBox_Phi_3.setWrapping(False)
        self.spinBox_Phi_3.setFrame(True)
        self.spinBox_Phi_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_Phi_3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.spinBox_Phi_3.setAccelerated(False)
        self.spinBox_Phi_3.setKeyboardTracking(False)
        self.spinBox_Phi_3.setObjectName("spinBox_Phi_3")
        self.gridLayout_18.addWidget(self.spinBox_Phi_3, 2, 2, 1, 1)
        self.pg1_settings_ContrastAffectsNN_checkbox = QtWidgets.QCheckBox(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_ContrastAffectsNN_checkbox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_ContrastAffectsNN_checkbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pg1_settings_ContrastAffectsNN_checkbox.setFont(font)
        self.pg1_settings_ContrastAffectsNN_checkbox.setStyleSheet("")
        self.pg1_settings_ContrastAffectsNN_checkbox.setText("")
        self.pg1_settings_ContrastAffectsNN_checkbox.setIconSize(QtCore.QSize(16, 16))
        self.pg1_settings_ContrastAffectsNN_checkbox.setCheckable(True)
        self.pg1_settings_ContrastAffectsNN_checkbox.setChecked(False)
        self.pg1_settings_ContrastAffectsNN_checkbox.setObjectName(
            "pg1_settings_ContrastAffectsNN_checkbox"
        )
        self.gridLayout_18.addWidget(
            self.pg1_settings_ContrastAffectsNN_checkbox, 1, 1, 1, 1
        )
        self.gridLayout_12.addWidget(
            self.pg1_settings_groupBox_brightness_contrast, 2, 0, 1, 2
        )
        self.pg1_settings_groupBox_mask_appearance = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_groupBox_mask_appearance.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_groupBox_mask_appearance.setSizePolicy(sizePolicy)
        self.pg1_settings_groupBox_mask_appearance.setMinimumSize(QtCore.QSize(0, 104))
        self.pg1_settings_groupBox_mask_appearance.setMaximumSize(
            QtCore.QSize(16777215, 250)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_groupBox_mask_appearance.setFont(font)
        self.pg1_settings_groupBox_mask_appearance.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg1_settings_groupBox_mask_appearance.setObjectName(
            "pg1_settings_groupBox_mask_appearance"
        )
        self.gridLayout_21 = QtWidgets.QGridLayout(
            self.pg1_settings_groupBox_mask_appearance
        )
        self.gridLayout_21.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_21.setHorizontalSpacing(10)
        self.gridLayout_21.setVerticalSpacing(11)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.pg1_settings_mask_opasity_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_mask_opasity_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_mask_opasity_label.setSizePolicy(sizePolicy)
        self.pg1_settings_mask_opasity_label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_mask_opasity_label.setFont(font)
        self.pg1_settings_mask_opasity_label.setObjectName(
            "pg1_settings_mask_opasity_label"
        )
        self.gridLayout_21.addWidget(self.pg1_settings_mask_opasity_label, 2, 0, 1, 1)
        self.pg1_settings_mask_visibility_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_mask_visibility_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_mask_visibility_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_mask_visibility_label.setFont(font)
        self.pg1_settings_mask_visibility_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.pg1_settings_mask_visibility_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg1_settings_mask_visibility_label.setObjectName(
            "pg1_settings_mask_visibility_label"
        )
        self.gridLayout_21.addWidget(
            self.pg1_settings_mask_visibility_label, 1, 0, 1, 1
        )
        self.pg1_settings_mask_opasity_slider = QtWidgets.QSlider(
            self.pg1_settings_groupBox_mask_appearance
        )
        self.pg1_settings_mask_opasity_slider.setStyleSheet("")
        self.pg1_settings_mask_opasity_slider.setMinimum(0)
        self.pg1_settings_mask_opasity_slider.setMaximum(100)
        self.pg1_settings_mask_opasity_slider.setPageStep(5)
        self.pg1_settings_mask_opasity_slider.setProperty("value", 75)
        self.pg1_settings_mask_opasity_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.pg1_settings_mask_opasity_slider.setInvertedAppearance(False)
        self.pg1_settings_mask_opasity_slider.setObjectName(
            "pg1_settings_mask_opasity_slider"
        )
        self.gridLayout_21.addWidget(self.pg1_settings_mask_opasity_slider, 2, 1, 1, 1)
        self.pg1_settings_mask_visibility_checkbox = QtWidgets.QCheckBox(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_mask_visibility_checkbox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_mask_visibility_checkbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pg1_settings_mask_visibility_checkbox.setFont(font)
        self.pg1_settings_mask_visibility_checkbox.setStyleSheet("")
        self.pg1_settings_mask_visibility_checkbox.setText("")
        self.pg1_settings_mask_visibility_checkbox.setIconSize(QtCore.QSize(16, 16))
        self.pg1_settings_mask_visibility_checkbox.setCheckable(True)
        self.pg1_settings_mask_visibility_checkbox.setChecked(False)
        self.pg1_settings_mask_visibility_checkbox.setObjectName(
            "pg1_settings_mask_visibility_checkbox"
        )
        self.gridLayout_21.addWidget(
            self.pg1_settings_mask_visibility_checkbox, 1, 1, 1, 1
        )
        self.pg1_settings_all_masks_color_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_all_masks_color_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_all_masks_color_label.setSizePolicy(sizePolicy)
        self.pg1_settings_all_masks_color_label.setMaximumSize(
            QtCore.QSize(16777215, 40)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_all_masks_color_label.setFont(font)
        self.pg1_settings_all_masks_color_label.setObjectName(
            "pg1_settings_all_masks_color_label"
        )
        self.gridLayout_21.addWidget(
            self.pg1_settings_all_masks_color_label, 3, 0, 1, 1
        )
        self.pg1_settings_selected_mask_color_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_selected_mask_color_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_selected_mask_color_label.setSizePolicy(sizePolicy)
        self.pg1_settings_selected_mask_color_label.setMinimumSize(QtCore.QSize(0, 35))
        self.pg1_settings_selected_mask_color_label.setMaximumSize(
            QtCore.QSize(16777215, 40)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_selected_mask_color_label.setFont(font)
        self.pg1_settings_selected_mask_color_label.setObjectName(
            "pg1_settings_selected_mask_color_label"
        )
        self.gridLayout_21.addWidget(
            self.pg1_settings_selected_mask_color_label, 6, 0, 1, 1
        )
        self.frame_2 = QtWidgets.QFrame(self.pg1_settings_groupBox_mask_appearance)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_2.setBaseSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pg1_settings_all_masks_color_button = QtWidgets.QPushButton(self.frame_2)
        self.pg1_settings_all_masks_color_button.setStyleSheet(
            "background-color: rgb(0, 0, 255);"
        )
        self.pg1_settings_all_masks_color_button.setText("")
        self.pg1_settings_all_masks_color_button.setObjectName(
            "pg1_settings_all_masks_color_button"
        )
        self.horizontalLayout_8.addWidget(self.pg1_settings_all_masks_color_button)
        self.pg1_settings_all_masks_color_width_label = QtWidgets.QLabel(self.frame_2)
        self.pg1_settings_all_masks_color_width_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg1_settings_all_masks_color_width_label.setObjectName(
            "pg1_settings_all_masks_color_width_label"
        )
        self.horizontalLayout_8.addWidget(self.pg1_settings_all_masks_color_width_label)
        self.pg1_settings_all_masks_color_width_spibox = QtWidgets.QSpinBox(
            self.frame_2
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_all_masks_color_width_spibox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_all_masks_color_width_spibox.setSizePolicy(sizePolicy)
        self.pg1_settings_all_masks_color_width_spibox.setFrame(True)
        self.pg1_settings_all_masks_color_width_spibox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg1_settings_all_masks_color_width_spibox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.pg1_settings_all_masks_color_width_spibox.setKeyboardTracking(False)
        self.pg1_settings_all_masks_color_width_spibox.setMinimum(1)
        self.pg1_settings_all_masks_color_width_spibox.setMaximum(30)
        self.pg1_settings_all_masks_color_width_spibox.setProperty("value", 2)
        self.pg1_settings_all_masks_color_width_spibox.setObjectName(
            "pg1_settings_all_masks_color_width_spibox"
        )
        self.horizontalLayout_8.addWidget(
            self.pg1_settings_all_masks_color_width_spibox
        )
        self.gridLayout_21.addWidget(self.frame_2, 3, 1, 1, 2)
        self.frame = QtWidgets.QFrame(self.pg1_settings_groupBox_mask_appearance)
        self.frame.setMinimumSize(QtCore.QSize(0, 35))
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pg1_settings_selected_mask_color_button = QtWidgets.QPushButton(self.frame)
        self.pg1_settings_selected_mask_color_button.setStyleSheet(
            "background-color: rgb(255, 0, 0);"
        )
        self.pg1_settings_selected_mask_color_button.setText("")
        self.pg1_settings_selected_mask_color_button.setObjectName(
            "pg1_settings_selected_mask_color_button"
        )
        self.horizontalLayout_7.addWidget(self.pg1_settings_selected_mask_color_button)
        self.pg1_settings_selected_mask_color_width_label = QtWidgets.QLabel(self.frame)
        self.pg1_settings_selected_mask_color_width_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg1_settings_selected_mask_color_width_label.setObjectName(
            "pg1_settings_selected_mask_color_width_label"
        )
        self.horizontalLayout_7.addWidget(
            self.pg1_settings_selected_mask_color_width_label
        )
        self.pg1_settings_selected_mask_color_width_spibox = QtWidgets.QSpinBox(
            self.frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_selected_mask_color_width_spibox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_selected_mask_color_width_spibox.setSizePolicy(sizePolicy)
        self.pg1_settings_selected_mask_color_width_spibox.setFrame(True)
        self.pg1_settings_selected_mask_color_width_spibox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg1_settings_selected_mask_color_width_spibox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.pg1_settings_selected_mask_color_width_spibox.setKeyboardTracking(False)
        self.pg1_settings_selected_mask_color_width_spibox.setMinimum(1)
        self.pg1_settings_selected_mask_color_width_spibox.setMaximum(30)
        self.pg1_settings_selected_mask_color_width_spibox.setObjectName(
            "pg1_settings_selected_mask_color_width_spibox"
        )
        self.horizontalLayout_7.addWidget(
            self.pg1_settings_selected_mask_color_width_spibox
        )
        self.gridLayout_21.addWidget(self.frame, 6, 1, 1, 2)
        self.pg1_settings_mask_opasity_spinbox = QtWidgets.QSpinBox(
            self.pg1_settings_groupBox_mask_appearance
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_mask_opasity_spinbox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_mask_opasity_spinbox.setSizePolicy(sizePolicy)
        self.pg1_settings_mask_opasity_spinbox.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.pg1_settings_mask_opasity_spinbox.setWrapping(False)
        self.pg1_settings_mask_opasity_spinbox.setFrame(True)
        self.pg1_settings_mask_opasity_spinbox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg1_settings_mask_opasity_spinbox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        self.pg1_settings_mask_opasity_spinbox.setAccelerated(False)
        self.pg1_settings_mask_opasity_spinbox.setKeyboardTracking(False)
        self.pg1_settings_mask_opasity_spinbox.setMaximum(100)
        self.pg1_settings_mask_opasity_spinbox.setProperty("value", 75)
        self.pg1_settings_mask_opasity_spinbox.setObjectName(
            "pg1_settings_mask_opasity_spinbox"
        )
        self.gridLayout_21.addWidget(self.pg1_settings_mask_opasity_spinbox, 2, 2, 1, 1)
        self.gridLayout_12.addWidget(
            self.pg1_settings_groupBox_mask_appearance, 3, 0, 1, 2
        )
        self.verticalLayout_5.addWidget(self.mask_contrast_brightness_btn_widget)
        self.scrollArea_analysis_tools.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea_analysis_tools)

        self.retranslateUi(pg1_settings_widget)
        QtCore.QMetaObject.connectSlotsByName(pg1_settings_widget)

    def retranslateUi(self, pg1_settings_widget):
        _translate = QtCore.QCoreApplication.translate
        pg1_settings_widget.setWindowTitle(_translate("pg1_settings_widget", "Form"))
        self.pg1_MaskAttributes_groupBox_ToolBox.setTitle(
            _translate("pg1_settings_widget", "Mask Attributes")
        )
        self.pg1_MaskAttributes_ApplyToEmpty.setText(
            _translate("pg1_settings_widget", "Apply To Empty")
        )
        self.pg1_MaskAttributes_ApplyToAllImages.setText(
            _translate("pg1_settings_widget", "Apply To All Images")
        )
        self.pg1_Maskshandler_groupBox_ToolBox.setTitle(
            _translate("pg1_settings_widget", "MasksHandler")
        )
        self.pg1_Maskshandler_DeleteAll_button.setText(
            _translate("pg1_settings_widget", "Delete all masks")
        )
        self.pg1_Maskshandler_DeleteAllPolygon_button.setText(
            _translate("pg1_settings_widget", "Delete All Polygon")
        )
        self.pg1_Maskshandler_DeleteAllBit_button.setText(
            _translate("pg1_settings_widget", "--")
        )
        self.pg1_settings_lasso_Render.setText(
            _translate("pg1_settings_widget", "Rerender")
        )
        self.pg1_channels_groupBox_ToolBox.setTitle(
            _translate("pg1_settings_widget", "Channels")
        )
        self.pg1_green_channel_button_visual.setText(
            _translate("pg1_settings_widget", "G")
        )
        self.pg1_red_channel_button_visual.setText(
            _translate("pg1_settings_widget", "R")
        )
        self.pg1_blue_channel_button_visual.setText(
            _translate("pg1_settings_widget", "B")
        )
        self.labeActiveChannelsLabel.setText(
            _translate("pg1_settings_widget", "Active Channels:")
        )
        self.pg1_settings_groupBox_ToolBox.setTitle(
            _translate("pg1_settings_widget", "ToolBox")
        )
        self.pg1_settings_lasso_remove_button.setText(
            _translate("pg1_settings_widget", "Lasso -")
        )
        self.pg1_settings_lasso_plus_button.setText(
            _translate("pg1_settings_widget", "Lasso +")
        )
        self.pg1_settings_poly_add_button.setText(
            _translate("pg1_settings_widget", "Poly add")
        )
        self.pg1_settings_poly_remove_button.setText(
            _translate("pg1_settings_widget", "Poly remove")
        )
        self.pg1_settings_groupBox_brightness_contrast.setTitle(
            _translate("pg1_settings_widget", "Visual Brighness Contrast")
        )
        self.pg1_settings_ContrastAffectsNN_label.setText(
            _translate("pg1_settings_widget", "Contrast affects NN")
        )
        self.pg1_settings_brightness_label.setText(
            _translate("pg1_settings_widget", "Brightness")
        )
        self.pg1_settings_contras_label.setText(
            _translate("pg1_settings_widget", "Contrast")
        )
        self.pg1_settings_groupBox_mask_appearance.setTitle(
            _translate("pg1_settings_widget", "APEARANCE")
        )
        self.pg1_settings_mask_opasity_label.setText(
            _translate("pg1_settings_widget", "Masks Opacity")
        )
        self.pg1_settings_mask_visibility_label.setText(
            _translate("pg1_settings_widget", "Mask Visibility")
        )
        self.pg1_settings_all_masks_color_label.setText(
            _translate("pg1_settings_widget", "All masks")
        )
        self.pg1_settings_selected_mask_color_label.setText(
            _translate("pg1_settings_widget", "Selected mask")
        )
        self.pg1_settings_all_masks_color_width_label.setText(
            _translate("pg1_settings_widget", "Width ")
        )
        self.pg1_settings_selected_mask_color_width_label.setText(
            _translate("pg1_settings_widget", "Width ")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    pg1_settings_widget = QtWidgets.QWidget()
    ui = Ui_pg1_settings_widget()
    ui.setupUi(pg1_settings_widget)
    pg1_settings_widget.show()
    sys.exit(app.exec())
