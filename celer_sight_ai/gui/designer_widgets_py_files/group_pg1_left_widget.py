# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\backup_work_old - Copy\EasyFluo\UiAssets\group_pg1_left_widget.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(270, 1072)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.group_pg1_left = QtWidgets.QFrame(Form)
        self.group_pg1_left.setMaximumSize(QtCore.QSize(300, 16777215))
        self.group_pg1_left.setStyleSheet("")
        self.group_pg1_left.setObjectName("group_pg1_left")
        self.gridLayout = QtWidgets.QGridLayout(self.group_pg1_left)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.AddRNAiFrames = QtWidgets.QFrame(self.group_pg1_left)
        self.AddRNAiFrames.setMaximumSize(QtCore.QSize(16777215, 370))
        self.AddRNAiFrames.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.AddRNAiFrames.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.AddRNAiFrames.setObjectName("AddRNAiFrames")
        self.gridLayout_2AddRNAibtnframe = QtWidgets.QGridLayout(self.AddRNAiFrames)
        self.gridLayout_2AddRNAibtnframe.setObjectName("gridLayout_2AddRNAibtnframe")
        self.initialize_analysis_button = QtWidgets.QPushButton(self.AddRNAiFrames)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.initialize_analysis_button.sizePolicy().hasHeightForWidth()
        )
        self.initialize_analysis_button.setSizePolicy(sizePolicy)
        self.initialize_analysis_button.setMinimumSize(QtCore.QSize(120, 120))
        self.initialize_analysis_button.setMaximumSize(QtCore.QSize(120, 120))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush
        )
        self.initialize_analysis_button.setPalette(palette)
        self.initialize_analysis_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.initialize_analysis_button.setStyleSheet("")
        self.initialize_analysis_button.setText("")
        self.initialize_analysis_button.setObjectName("initialize_btn")
        self.gridLayout_2AddRNAibtnframe.addWidget(
            self.initialize_analysis_button, 2, 0, 1, 1
        )
        self.add_images_btn = QtWidgets.QPushButton(self.AddRNAiFrames)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.add_images_btn.sizePolicy().hasHeightForWidth()
        )
        self.add_images_btn.setSizePolicy(sizePolicy)
        self.add_images_btn.setMinimumSize(QtCore.QSize(120, 120))
        self.add_images_btn.setMaximumSize(QtCore.QSize(120, 120))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush
        )
        self.add_images_btn.setPalette(palette)
        font = QtGui.QFont()
        self.add_images_btn.setFont(font)
        self.add_images_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.add_images_btn.setStyleSheet("")
        self.add_images_btn.setText("")
        self.add_images_btn.setIconSize(QtCore.QSize(40, 40))
        self.add_images_btn.setCheckable(True)
        self.add_images_btn.setObjectName("add_images_btn")
        self.gridLayout_2AddRNAibtnframe.addWidget(self.add_images_btn, 0, 0, 1, 1)
        self.get_roi_ai_button = QtWidgets.QPushButton(self.AddRNAiFrames)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.get_roi_ai_button.sizePolicy().hasHeightForWidth()
        )
        self.get_roi_ai_button.setSizePolicy(sizePolicy)
        self.get_roi_ai_button.setMinimumSize(QtCore.QSize(120, 120))
        self.get_roi_ai_button.setMaximumSize(QtCore.QSize(120, 120))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush
        )
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.Spread.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush
        )
        self.get_roi_ai_button.setPalette(palette)
        font = QtGui.QFont()
        self.get_roi_ai_button.setFont(font)
        self.get_roi_ai_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.get_roi_ai_button.setText("")
        self.get_roi_ai_button.setObjectName("replicate_btn")
        self.gridLayout_2AddRNAibtnframe.addWidget(self.get_roi_ai_button, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.AddRNAiFrames, 0, 0, 1, 1)
        self.frame_RNAi_list = QtWidgets.QFrame(self.group_pg1_left)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_RNAi_list.sizePolicy().hasHeightForWidth()
        )
        self.frame_RNAi_list.setSizePolicy(sizePolicy)
        self.frame_RNAi_list.setMinimumSize(QtCore.QSize(135, 300))
        self.frame_RNAi_list.setStyleSheet(
            "QGroupBox {\n"
            "\n"
            "    border: 1px solid gray;\n"
            "    border-color: #FF17365D;\n"
            "    margin-top: 0px;\n"
            "    font-size: 12px;\n"
            "    border-bottom-left-radius: 15px;\n"
            "    border-bottom-right-radius: 15px;\n"
            "    border-top-color: rgba(255, 255, 255,0);\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    border-top-color: rgb(255, 255, 255);\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top left;\n"
            "    border-top-left-radius: 15px;\n"
            "    border-top-right-radius:15px;\n"
            "    padding: 2px 10px;\n"
            "    background-color: #FF17365D;\n"
            "    color: rgb(255, 255, 255);\n"
            "}"
        )
        self.frame_RNAi_list.setObjectName("frame_RNAi_list")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_RNAi_list)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.RNAiListFramepg1Left = QtWidgets.QFrame(self.frame_RNAi_list)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.RNAiListFramepg1Left.sizePolicy().hasHeightForWidth()
        )
        self.RNAiListFramepg1Left.setSizePolicy(sizePolicy)
        self.RNAiListFramepg1Left.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.RNAiListFramepg1Left.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.RNAiListFramepg1Left.setObjectName("RNAiListFramepg1Left")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.RNAiListFramepg1Left)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            15,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.up_button_list = QtWidgets.QPushButton(self.RNAiListFramepg1Left)
        self.up_button_list.setMinimumSize(QtCore.QSize(30, 30))
        self.up_button_list.setMaximumSize(QtCore.QSize(30, 30))
        self.up_button_list.setText("")
        self.up_button_list.setObjectName("up_button_list")
        self.gridLayout_2.addWidget(self.up_button_list, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            13,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.down_button_list = QtWidgets.QPushButton(self.RNAiListFramepg1Left)
        self.down_button_list.setMinimumSize(QtCore.QSize(30, 30))
        self.down_button_list.setMaximumSize(QtCore.QSize(30, 30))
        self.down_button_list.setText("")
        self.down_button_list.setObjectName("down_button_list")
        self.gridLayout_2.addWidget(self.down_button_list, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_2.addItem(spacerItem2, 0, 4, 1, 1)
        self.delete_button_list = QtWidgets.QPushButton(self.RNAiListFramepg1Left)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.delete_button_list.sizePolicy().hasHeightForWidth()
        )
        self.delete_button_list.setSizePolicy(sizePolicy)
        self.delete_button_list.setMinimumSize(QtCore.QSize(30, 30))
        self.delete_button_list.setMaximumSize(QtCore.QSize(30, 30))
        self.delete_button_list.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.delete_button_list.setText("")
        self.delete_button_list.setObjectName("delete_button_list")
        self.gridLayout_2.addWidget(self.delete_button_list, 0, 5, 1, 1)
        self.verticalLayout.addWidget(self.RNAiListFramepg1Left)
        self.RNAi_list = QtWidgets.QListWidget(self.frame_RNAi_list)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RNAi_list.sizePolicy().hasHeightForWidth())
        self.RNAi_list.setSizePolicy(sizePolicy)
        self.RNAi_list.setMinimumSize(QtCore.QSize(100, 0))
        self.RNAi_list.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.RNAi_list.setDragDropMode(
            QtWidgets.QAbstractItemView.DragDropMode.InternalMove
        )
        self.RNAi_list.setObjectName("RNAi_list")
        self.verticalLayout.addWidget(self.RNAi_list)
        self.frae_RNAi_list_buttons = QtWidgets.QFrame(self.frame_RNAi_list)
        self.frae_RNAi_list_buttons.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frae_RNAi_list_buttons.sizePolicy().hasHeightForWidth()
        )
        self.frae_RNAi_list_buttons.setSizePolicy(sizePolicy)
        self.frae_RNAi_list_buttons.setMinimumSize(QtCore.QSize(30, 0))
        self.frae_RNAi_list_buttons.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frae_RNAi_list_buttons.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frae_RNAi_list_buttons.setLineWidth(0)
        self.frae_RNAi_list_buttons.setObjectName("frae_RNAi_list_buttons")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frae_RNAi_list_buttons)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.frae_RNAi_list_buttons)
        self.gridLayout.addWidget(self.frame_RNAi_list, 3, 0, 1, 1)
        self.frame_mask_generation = QtWidgets.QFrame(self.group_pg1_left)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_mask_generation.sizePolicy().hasHeightForWidth()
        )
        self.frame_mask_generation.setSizePolicy(sizePolicy)
        self.frame_mask_generation.setMinimumSize(QtCore.QSize(20, 60))
        self.frame_mask_generation.setMaximumSize(QtCore.QSize(255, 16777215))
        self.frame_mask_generation.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mask_generation.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_mask_generation.setObjectName("frame_mask_generation")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_mask_generation)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.mask_generation = QtWidgets.QLabel(self.frame_mask_generation)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mask_generation.setFont(font)
        self.mask_generation.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.mask_generation.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.mask_generation.setObjectName("mask_generation")
        self.gridLayout_5.addWidget(self.mask_generation, 0, 0, 1, 1)
        self.comboBox_for_mask_generation = QtWidgets.QComboBox(
            self.frame_mask_generation
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_for_mask_generation.setFont(font)
        self.comboBox_for_mask_generation.setObjectName("comboBox_for_mask_generation")
        self.comboBox_for_mask_generation.addItem("")
        self.comboBox_for_mask_generation.addItem("")
        self.gridLayout_5.addWidget(self.comboBox_for_mask_generation, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_mask_generation, 2, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.group_pg1_left)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.mask_generation.setText(_translate("Form", "Masks Generation"))
        self.comboBox_for_mask_generation.setItemText(0, _translate("Form", "Assisted"))
        self.comboBox_for_mask_generation.setItemText(
            1, _translate("Form", "Standalone")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
