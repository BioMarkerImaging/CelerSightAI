# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\backup_work_old - Copy\pg1_widget_mask_settings.ui'
#
# Created by: PyQt6 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_pg1_settings_widget(object):
    def setup(self, pg1_settings_widget):
        pg1_settings_widget.setObjectName("pg1_settings_widget")
        pg1_settings_widget.resize(281, 638)

        self.horizontalLayout = QtWidgets.QHBoxLayout(pg1_settings_widget)
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
        self.scrollArea_analysis_tools.setWidgetResizable(True)
        self.scrollArea_analysis_tools.setObjectName("scrollArea_analysis_tools")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 242, 718))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mask_contrast_brightness_btn_widget = QtWidgets.QWidget(
            self.scrollAreaWidgetContents_2
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mask_contrast_brightness_btn_widget.sizePolicy().hasHeightForWidth()
        )
        self.mask_contrast_brightness_btn_widget.setSizePolicy(sizePolicy)
        self.mask_contrast_brightness_btn_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.mask_contrast_brightness_btn_widget.setMaximumSize(
            QtCore.QSize(200, 16777215)
        )

        self.mask_contrast_brightness_btn_widget.setObjectName(
            "mask_contrast_brightness_btn_widget"
        )
        self.gridLayout_12 = QtWidgets.QGridLayout(
            self.mask_contrast_brightness_btn_widget
        )
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_12.addItem(spacerItem, 4, 0, 1, 1)
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
        self.pg1_settings_groupBox_ToolBox.setMinimumSize(QtCore.QSize(200, 99))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_groupBox_ToolBox.setFont(font)
        self.pg1_settings_groupBox_ToolBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
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
        self.gridLayout_GrouBox_ToolBox_2.setContentsMargins(9, 15, 9, 15)
        self.gridLayout_GrouBox_ToolBox_2.setHorizontalSpacing(9)
        self.gridLayout_GrouBox_ToolBox_2.setVerticalSpacing(7)
        self.gridLayout_GrouBox_ToolBox_2.setObjectName("gridLayout_GrouBox_ToolBox_2")
        self.frame_5 = QtWidgets.QFrame(self.pg1_settings_groupBox_ToolBox)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setHorizontalSpacing(5)
        self.gridLayout_17.setVerticalSpacing(0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.pg1_settings_lasso_plus_button = QtWidgets.QPushButton(self.frame_5)
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
        self.gridLayout_17.addWidget(self.pg1_settings_lasso_plus_button, 0, 0, 1, 1)
        self.pg1_settings_lasso_remove_button = QtWidgets.QPushButton(self.frame_5)
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
        self.gridLayout_17.addWidget(self.pg1_settings_lasso_remove_button, 0, 1, 1, 1)
        self.gridLayout_GrouBox_ToolBox_2.addWidget(self.frame_5, 2, 0, 1, 2)
        self.frame_3 = QtWidgets.QFrame(self.pg1_settings_groupBox_ToolBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setHorizontalSpacing(5)
        self.gridLayout_15.setVerticalSpacing(0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.pg1_settings_poly_add_button = QtWidgets.QPushButton(self.frame_3)
        self.pg1_settings_poly_add_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
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
        font.setPointSize(9)
        self.pg1_settings_poly_add_button.setFont(font)
        self.pg1_settings_poly_add_button.setStyleSheet(
            "QPushButton:{\n"
            "color: rgb(255, 255, 255);\n"
            "    background-color: rgb(0, 85, 255);\n"
            "}"
        )
        self.pg1_settings_poly_add_button.setObjectName("pg1_settings_poly_add_button")
        self.gridLayout_15.addWidget(self.pg1_settings_poly_add_button, 0, 0, 1, 1)
        self.pg1_settings_poly_remove_button = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
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
        font.setPointSize(9)
        self.pg1_settings_poly_remove_button.setFont(font)
        self.pg1_settings_poly_remove_button.setObjectName(
            "pg1_settings_poly_remove_button"
        )
        self.gridLayout_15.addWidget(self.pg1_settings_poly_remove_button, 0, 1, 1, 1)
        self.gridLayout_GrouBox_ToolBox_2.addWidget(self.frame_3, 1, 0, 1, 2)
        self.gridLayout_12.addWidget(self.pg1_settings_groupBox_ToolBox, 0, 0, 1, 1)
        self.pg1_settings_groupBox_brightness_contrast = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_groupBox_brightness_contrast.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_groupBox_brightness_contrast.setSizePolicy(sizePolicy)
        self.pg1_settings_groupBox_brightness_contrast.setMinimumSize(
            QtCore.QSize(0, 185)
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
        self.gridLayout_18.setContentsMargins(9, 14, 9, 15)
        self.gridLayout_18.setHorizontalSpacing(10)
        self.gridLayout_18.setVerticalSpacing(11)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.pg1_settings_adjust_brightness_sliders_label = QtWidgets.QLabel(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_adjust_brightness_sliders_label.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_adjust_brightness_sliders_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg1_settings_adjust_brightness_sliders_label.setFont(font)
        self.pg1_settings_adjust_brightness_sliders_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.pg1_settings_adjust_brightness_sliders_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg1_settings_adjust_brightness_sliders_label.setObjectName(
            "pg1_settings_adjust_brightness_sliders_label"
        )
        self.gridLayout_18.addWidget(
            self.pg1_settings_adjust_brightness_sliders_label, 1, 0, 1, 1
        )
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
        self.gridLayout_18.addWidget(self.pg1_settings_contras_label, 4, 0, 1, 1)
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
        self.pg1_settings_contras_slider.setMinimum(-50)
        self.pg1_settings_contras_slider.setMaximum(50)
        self.pg1_settings_contras_slider.setPageStep(2)
        self.pg1_settings_contras_slider.setProperty("value", 0)
        self.pg1_settings_contras_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.pg1_settings_contras_slider.setObjectName("pg1_settings_contras_slider")
        self.gridLayout_18.addWidget(self.pg1_settings_contras_slider, 5, 0, 1, 1)
        self.pg1_settings_adjust_brightness_sliders_checkbox = QtWidgets.QCheckBox(
            self.pg1_settings_groupBox_brightness_contrast
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_adjust_brightness_sliders_checkbox.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_adjust_brightness_sliders_checkbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pg1_settings_adjust_brightness_sliders_checkbox.setFont(font)
        self.pg1_settings_adjust_brightness_sliders_checkbox.setStyleSheet("")
        self.pg1_settings_adjust_brightness_sliders_checkbox.setText("")
        self.pg1_settings_adjust_brightness_sliders_checkbox.setIconSize(
            QtCore.QSize(16, 16)
        )
        self.pg1_settings_adjust_brightness_sliders_checkbox.setCheckable(True)
        self.pg1_settings_adjust_brightness_sliders_checkbox.setChecked(False)
        self.pg1_settings_adjust_brightness_sliders_checkbox.setObjectName(
            "pg1_settings_adjust_brightness_sliders_checkbox"
        )
        self.gridLayout_18.addWidget(
            self.pg1_settings_adjust_brightness_sliders_checkbox, 1, 1, 1, 1
        )
        self.pg1_settings_brightness_slider = QtWidgets.QSlider(
            self.pg1_settings_groupBox_brightness_contrast
        )
        self.pg1_settings_brightness_slider.setStyleSheet("")
        self.pg1_settings_brightness_slider.setMinimum(-255)
        self.pg1_settings_brightness_slider.setMaximum(255)
        self.pg1_settings_brightness_slider.setPageStep(5)
        self.pg1_settings_brightness_slider.setProperty("value", 0)
        self.pg1_settings_brightness_slider.setOrientation(
            QtCore.Qt.Orientation.Horizontal
        )
        self.pg1_settings_brightness_slider.setInvertedAppearance(False)
        self.pg1_settings_brightness_slider.setObjectName(
            "pg1_settings_brightness_slider"
        )
        self.gridLayout_18.addWidget(self.pg1_settings_brightness_slider, 3, 0, 1, 1)
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
        self.gridLayout_18.addWidget(self.spinBox_Theta_3, 5, 1, 1, 1)
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
        self.gridLayout_18.addWidget(self.spinBox_Phi_3, 3, 1, 1, 1)
        self.gridLayout_12.addWidget(
            self.pg1_settings_groupBox_brightness_contrast, 1, 0, 1, 1
        )
        self.pg1_settings_groupBox_mask_appearance = QtWidgets.QGroupBox(
            self.mask_contrast_brightness_btn_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg1_settings_groupBox_mask_appearance.sizePolicy().hasHeightForWidth()
        )
        self.pg1_settings_groupBox_mask_appearance.setSizePolicy(sizePolicy)
        self.pg1_settings_groupBox_mask_appearance.setMinimumSize(QtCore.QSize(0, 109))
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
        self.gridLayout_21.setContentsMargins(9, 14, 9, 15)
        self.gridLayout_21.setHorizontalSpacing(10)
        self.gridLayout_21.setVerticalSpacing(11)
        self.gridLayout_21.setObjectName("gridLayout_21")
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
        self.gridLayout_21.addWidget(self.pg1_settings_mask_opasity_slider, 3, 0, 1, 1)
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
        self.gridLayout_21.addWidget(self.pg1_settings_mask_opasity_spinbox, 3, 1, 1, 1)
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
            self.pg1_settings_all_masks_color_label, 4, 0, 1, 2
        )
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
        self.gridLayout_21.addWidget(self.frame, 9, 0, 2, 2)
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
        self.pg1_settings_all_masks_color_width_spibox.setObjectName(
            "pg1_settings_all_masks_color_width_spibox"
        )
        self.horizontalLayout_8.addWidget(
            self.pg1_settings_all_masks_color_width_spibox
        )
        self.gridLayout_21.addWidget(self.frame_2, 5, 0, 1, 2)
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
            self.pg1_settings_selected_mask_color_label, 7, 0, 1, 1
        )
        self.gridLayout_12.addWidget(
            self.pg1_settings_groupBox_mask_appearance, 3, 0, 1, 1
        )
        self.verticalLayout_5.addWidget(self.mask_contrast_brightness_btn_widget)
        self.scrollArea_analysis_tools.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea_analysis_tools)

        # self.retranslateUi(pg1_settings_widget)
        #     QtCore.QMetaObject.connectSlotsByName(pg1_settings_widget)

        # def retranslateUi(self, pg1_settings_widget):
        pg1_settings_widget.setStyleSheet(
            """

QScrollArea{
background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #3e465a, stop: 0.1 #3e4659, stop: 0.5 #3e4659, stop: 0.9 #3e4659, stop: 1 #3e465a);
}

"""
        )
        _translate = QtCore.QCoreApplication.translate
        # pg1_settings_widget.setWindowTitle(_translate("pg1_settings_widget", "Form"))
        self.pg1_settings_groupBox_ToolBox.setTitle(
            _translate("pg1_settings_widget", "ToolBox")
        )
        self.pg1_settings_lasso_plus_button.setText(
            _translate("pg1_settings_widget", "Lasso +")
        )
        self.pg1_settings_lasso_remove_button.setText(
            _translate("pg1_settings_widget", "Lasso -")
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
        self.pg1_settings_adjust_brightness_sliders_label.setText(
            _translate("pg1_settings_widget", "Brigtness Sliders")
        )
        self.pg1_settings_contras_label.setText(
            _translate("pg1_settings_widget", "Contrast")
        )
        self.pg1_settings_brightness_label.setText(
            _translate("pg1_settings_widget", "Brightness")
        )
        self.pg1_settings_groupBox_mask_appearance.setTitle(
            _translate("pg1_settings_widget", "APEARANCE")
        )
        self.pg1_settings_mask_visibility_label.setText(
            _translate("pg1_settings_widget", "Mask Visibility")
        )
        self.pg1_settings_mask_opasity_label.setText(
            _translate("pg1_settings_widget", "Masks Opacity")
        )
        self.pg1_settings_all_masks_color_label.setText(
            _translate("pg1_settings_widget", "All masks")
        )
        self.pg1_settings_selected_mask_color_width_label.setText(
            _translate("pg1_settings_widget", "Width ")
        )
        self.pg1_settings_all_masks_color_width_label.setText(
            _translate("pg1_settings_widget", "Width ")
        )
        self.pg1_settings_selected_mask_color_label.setText(
            _translate("pg1_settings_widget", "Selected mask")
        )


if __name__ == "__main__":
    pass
