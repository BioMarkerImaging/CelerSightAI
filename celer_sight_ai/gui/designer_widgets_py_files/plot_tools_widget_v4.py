# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\manos\Documents\topfluov2\UiAssets\plot_tools_widget_v4.ui'
#
# Created by: PyQt6 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Plot_tools_widget(object):
    def setupUi(self, Plot_tools_widget):
        Plot_tools_widget.setObjectName("Plot_tools_widget")
        Plot_tools_widget.resize(1201, 1266)
        Plot_tools_widget.setStyleSheet(
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
            "QGroupBox {\n"
            "            border: 1px solid;\n"
            "            border-color: rgb(20, 20, 20);\n"
            "            margin-top: 20px;\n"
            "            border-top-left-radius: 15px;\n"
            "            border-top-right-radius:15px;\n"
            "            border-bottom-left-radius: 15px;\n"
            "            border-bottom-right-radius: 15px;\n"
            "            background-color: rgb(90, 90, 90);\n"
            "        }\n"
            "QGroupBox::title {\n"
            "            font-size: 12px;\n"
            "            border-top-color: rgb(255, 255, 255);\n"
            "            subcontrol-origin: margin;\n"
            "            subcontrol-position: top left;\n"
            "            border-top-left-radius: 15px;\n"
            "            border-top-right-radius:15px;\n"
            "            padding: 2px 10px;\n"
            "            background-color: rgba(255, 255, 255,0);\n"
            "            color:rgba(255, 255, 255,220);\n"
            "}\n"
            "\n"
            "\n"
            "QPushButton {\n"
            "\n"
            "    font-size: 12px;\n"
            "    border-radius: 5px;\n"
            "\n"
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(Plot_tools_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter_3 = QtWidgets.QSplitter(Plot_tools_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setMinimumSize(QtCore.QSize(21, 479))
        self.splitter_3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.pg_2_widget_graph_visualizer = QtWidgets.QWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_widget_graph_visualizer.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_widget_graph_visualizer.setSizePolicy(sizePolicy)
        self.pg_2_widget_graph_visualizer.setMinimumSize(QtCore.QSize(60, 364))
        self.pg_2_widget_graph_visualizer.setStyleSheet("")
        self.pg_2_widget_graph_visualizer.setObjectName("pg_2_widget_graph_visualizer")
        self.pg_2_gridLayout_8 = QtWidgets.QGridLayout(
            self.pg_2_widget_graph_visualizer
        )
        self.pg_2_gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pg_2_gridLayout_8.setObjectName("pg_2_gridLayout_8")
        self.widget_graph_visualizer_scroll_area_2 = QtWidgets.QScrollArea(
            self.pg_2_widget_graph_visualizer
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_graph_visualizer_scroll_area_2.sizePolicy().hasHeightForWidth()
        )
        self.widget_graph_visualizer_scroll_area_2.setSizePolicy(sizePolicy)
        self.widget_graph_visualizer_scroll_area_2.setMinimumSize(QtCore.QSize(600, 0))
        self.widget_graph_visualizer_scroll_area_2.setWidgetResizable(True)
        self.widget_graph_visualizer_scroll_area_2.setObjectName(
            "widget_graph_visualizer_scroll_area_2"
        )
        self.widget_graph_visualizer_scroll_area_2_contents = QtWidgets.QWidget()
        self.widget_graph_visualizer_scroll_area_2_contents.setGeometry(
            QtCore.QRect(0, 0, 656, 2099)
        )
        self.widget_graph_visualizer_scroll_area_2_contents.setObjectName(
            "widget_graph_visualizer_scroll_area_2_contents"
        )
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents = (
            QtWidgets.QGridLayout(self.widget_graph_visualizer_scroll_area_2_contents)
        )
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.setObjectName(
            "gridLayoutwidget_graph_visualizer_scroll_area_2_contents"
        )
        self.groupBoxOfGraphTypes = QtWidgets.QGroupBox(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBoxOfGraphTypes.sizePolicy().hasHeightForWidth()
        )
        self.groupBoxOfGraphTypes.setSizePolicy(sizePolicy)
        self.groupBoxOfGraphTypes.setMaximumSize(QtCore.QSize(16777215, 205))
        self.groupBoxOfGraphTypes.setObjectName("groupBoxOfGraphTypes")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2 = (
            QtWidgets.QGridLayout(self.groupBoxOfGraphTypes)
        )
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.setContentsMargins(
            6, 20, 6, 6
        )
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.setSpacing(6)
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.setObjectName(
            "widget_graph_visualizer_scroll_area_2_contents_grid_layout_2"
        )
        self.pg2_graph_order = QtWidgets.QLabel(self.groupBoxOfGraphTypes)
        self.pg2_graph_order.setMinimumSize(QtCore.QSize(0, 23))
        self.pg2_graph_order.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg2_graph_order.setFont(font)
        self.pg2_graph_order.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_order.setObjectName("pg2_graph_order")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_graph_order, 1, 1, 1, 3
        )
        self.pg2_add_plot_button = QtWidgets.QPushButton(self.groupBoxOfGraphTypes)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_add_plot_button.sizePolicy().hasHeightForWidth()
        )
        self.pg2_add_plot_button.setSizePolicy(sizePolicy)
        self.pg2_add_plot_button.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.pg2_add_plot_button.setFont(font)
        self.pg2_add_plot_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.pg2_add_plot_button.setObjectName("pg2_add_plot_button")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_add_plot_button, 2, 0, 1, 1
        )
        self.pg2_remove_plot_button = QtWidgets.QPushButton(self.groupBoxOfGraphTypes)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_remove_plot_button.sizePolicy().hasHeightForWidth()
        )
        self.pg2_remove_plot_button.setSizePolicy(sizePolicy)
        self.pg2_remove_plot_button.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_remove_plot_button.setFont(font)
        self.pg2_remove_plot_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.pg2_remove_plot_button.setObjectName("pg2_remove_plot_button")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_remove_plot_button, 3, 0, 1, 1
        )
        self.pg2_graph_type_comboBox = QtWidgets.QComboBox(self.groupBoxOfGraphTypes)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pg2_graph_type_comboBox.setFont(font)
        self.pg2_graph_type_comboBox.setObjectName("pg2_graph_type_comboBox")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.pg2_graph_type_comboBox.addItem("")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_graph_type_comboBox, 0, 1, 1, 3
        )
        self.pg2_graph_type = QtWidgets.QLabel(self.groupBoxOfGraphTypes)
        self.pg2_graph_type.setMinimumSize(QtCore.QSize(0, 28))
        self.pg2_graph_type.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg2_graph_type.setFont(font)
        self.pg2_graph_type.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.pg2_graph_type.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_type.setObjectName("pg2_graph_type")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_graph_type, 0, 0, 1, 1
        )
        self.pg2_graphs_view = QtWidgets.QListWidget(self.groupBoxOfGraphTypes)
        self.pg2_graphs_view.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.pg2_graphs_view.setDragEnabled(True)
        self.pg2_graphs_view.setDragDropMode(
            QtWidgets.QAbstractItemView.DragDropMode.InternalMove
        )
        self.pg2_graphs_view.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.pg2_graphs_view.setFlow(QtWidgets.QListView.Flow.TopToBottom)
        self.pg2_graphs_view.setObjectName("pg2_graphs_view")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_2.addWidget(
            self.pg2_graphs_view, 2, 1, 2, 3
        )
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.groupBoxOfGraphTypes, 3, 0, 1, 1
        )
        self.groupBox_ErrorBarsPg2 = QtWidgets.QGroupBox(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_ErrorBarsPg2.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_ErrorBarsPg2.setSizePolicy(sizePolicy)
        self.groupBox_ErrorBarsPg2.setMaximumSize(QtCore.QSize(16777215, 472))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_ErrorBarsPg2.setFont(font)
        self.groupBox_ErrorBarsPg2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.groupBox_ErrorBarsPg2.setObjectName("groupBox_ErrorBarsPg2")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_ErrorBarsPg2)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.pg_2_errorbar_basic_settings = QtWidgets.QGroupBox(
            self.groupBox_ErrorBarsPg2
        )
        self.pg_2_errorbar_basic_settings.setObjectName("pg_2_errorbar_basic_settings")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.pg_2_errorbar_basic_settings)
        self.gridLayout_22.setContentsMargins(13, 20, 8, 10)
        self.gridLayout_22.setObjectName("gridLayout_22")
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_22.addItem(spacerItem, 1, 2, 1, 1)
        self.pg_2_error_bar_botom_style_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_botom_style_combobox.setObjectName(
            "pg_2_error_bar_botom_style_combobox"
        )
        self.pg_2_error_bar_botom_style_combobox.addItem("")
        self.pg_2_error_bar_botom_style_combobox.addItem("")
        self.pg_2_error_bar_botom_style_combobox.addItem("")
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_botom_style_combobox, 5, 1, 1, 1
        )
        self.pg_2_error_bar_top_thickness_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_top_thickness_combobox.setObjectName(
            "pg_2_error_bar_top_thickness_combobox"
        )
        self.pg_2_error_bar_top_thickness_combobox.addItem("")
        self.pg_2_error_bar_top_thickness_combobox.addItem("")
        self.pg_2_error_bar_top_thickness_combobox.addItem("")
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_top_thickness_combobox, 1, 1, 1, 1
        )
        self.pg_2_error_bar_opacity_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_opacity_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_opacity_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_opacity_label.setFont(font)
        self.pg_2_error_bar_opacity_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_opacity_label.setObjectName("pg_2_error_bar_opacity_label")
        self.gridLayout_22.addWidget(self.pg_2_error_bar_opacity_label, 0, 3, 1, 1)
        self.pg_2_error_bar_botom_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_botom_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_botom_style_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_botom_style_label.setFont(font)
        self.pg_2_error_bar_botom_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_botom_style_label.setObjectName(
            "pg_2_error_bar_botom_style_label"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_botom_style_label, 5, 0, 1, 1)
        self.pg_2_error_bar_opacity_spinBox = QtWidgets.QSpinBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_opacity_spinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg_2_error_bar_opacity_spinBox.setMinimum(0)
        self.pg_2_error_bar_opacity_spinBox.setMaximum(100)
        self.pg_2_error_bar_opacity_spinBox.setProperty("value", 100)
        self.pg_2_error_bar_opacity_spinBox.setObjectName(
            "pg_2_error_bar_opacity_spinBox"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_opacity_spinBox, 0, 4, 1, 1)
        self.pg_2_error_bar_line_width_spinbox = QtWidgets.QSpinBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_line_width_spinbox.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg_2_error_bar_line_width_spinbox.setMinimum(1)
        self.pg_2_error_bar_line_width_spinbox.setMaximum(100)
        self.pg_2_error_bar_line_width_spinbox.setProperty("value", 2)
        self.pg_2_error_bar_line_width_spinbox.setObjectName(
            "pg_2_error_bar_line_width_spinbox"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_line_width_spinbox, 8, 1, 1, 1)
        self.pg_2_error_bar_line_width_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_line_width_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_line_width_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_line_width_label.setFont(font)
        self.pg_2_error_bar_line_width_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_line_width_label.setObjectName(
            "pg_2_error_bar_line_width_label"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_line_width_label, 8, 0, 1, 1)
        self.pg_2_error_bar_cap_thickness_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_thickness_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_cap_thickness_label.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_cap_thickness_label.setFont(font)
        self.pg_2_error_bar_cap_thickness_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_cap_thickness_label.setObjectName(
            "pg_2_error_bar_cap_thickness_label"
        )
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_cap_thickness_label, 8, 3, 1, 1
        )
        self.pg_2_error_bar_color_button = QtWidgets.QPushButton(
            self.pg_2_errorbar_basic_settings
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_error_bar_color_button.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_error_bar_color_button.setSizePolicy(sizePolicy)
        self.pg_2_error_bar_color_button.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n" "border-radius: 5px;"
        )
        self.pg_2_error_bar_color_button.setText("")
        self.pg_2_error_bar_color_button.setObjectName("pg_2_error_bar_color_button")
        self.gridLayout_22.addWidget(self.pg_2_error_bar_color_button, 1, 4, 1, 1)
        self.pg_2_error_bar_cap_size_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_size_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_cap_size_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_cap_size_label.setFont(font)
        self.pg_2_error_bar_cap_size_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_cap_size_label.setObjectName(
            "pg_2_error_bar_cap_size_label"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_cap_size_label, 5, 3, 1, 1)
        self.pg_2_error_bar_top_thickness_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_top_thickness_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_top_thickness_label.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_top_thickness_label.setFont(font)
        self.pg_2_error_bar_top_thickness_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_top_thickness_label.setObjectName(
            "pg_2_error_bar_top_thickness_label"
        )
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_top_thickness_label, 1, 0, 1, 1
        )
        self.pg_2_error_bar_cap_thickness_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_thickness_combobox.setMinimumSize(QtCore.QSize(80, 0))
        self.pg_2_error_bar_cap_thickness_combobox.setObjectName(
            "pg_2_error_bar_cap_thickness_combobox"
        )
        self.pg_2_error_bar_cap_thickness_combobox.addItem("")
        self.pg_2_error_bar_cap_thickness_combobox.addItem("")
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_cap_thickness_combobox, 0, 1, 1, 1
        )
        self.pg_2_error_bar_cap_size_spinBox = QtWidgets.QSpinBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_size_spinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg_2_error_bar_cap_size_spinBox.setMinimum(0)
        self.pg_2_error_bar_cap_size_spinBox.setMaximum(10000)
        self.pg_2_error_bar_cap_size_spinBox.setProperty("value", 5)
        self.pg_2_error_bar_cap_size_spinBox.setObjectName(
            "pg_2_error_bar_cap_size_spinBox"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_cap_size_spinBox, 5, 4, 1, 1)
        self.pg_2_error_bar_cap_thickness_spinBox = QtWidgets.QSpinBox(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_thickness_spinBox.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg_2_error_bar_cap_thickness_spinBox.setMinimum(0)
        self.pg_2_error_bar_cap_thickness_spinBox.setMaximum(10000)
        self.pg_2_error_bar_cap_thickness_spinBox.setProperty("value", 2)
        self.pg_2_error_bar_cap_thickness_spinBox.setObjectName(
            "pg_2_error_bar_cap_thickness_spinBox"
        )
        self.gridLayout_22.addWidget(
            self.pg_2_error_bar_cap_thickness_spinBox, 8, 4, 1, 1
        )
        self.pg_2_error_bar_color_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_color_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_color_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_color_label.setFont(font)
        self.pg_2_error_bar_color_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_color_label.setObjectName("pg_2_error_bar_color_label")
        self.gridLayout_22.addWidget(self.pg_2_error_bar_color_label, 1, 3, 1, 1)
        self.pg_2_error_bar_cap_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_basic_settings
        )
        self.pg_2_error_bar_cap_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_error_bar_cap_style_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_error_bar_cap_style_label.setFont(font)
        self.pg_2_error_bar_cap_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_error_bar_cap_style_label.setObjectName(
            "pg_2_error_bar_cap_style_label"
        )
        self.gridLayout_22.addWidget(self.pg_2_error_bar_cap_style_label, 0, 0, 1, 1)
        self.verticalLayout_14.addWidget(self.pg_2_errorbar_basic_settings)
        self.pg_2_errorbar_extra_settings = QtWidgets.QGroupBox(
            self.groupBox_ErrorBarsPg2
        )
        self.pg_2_errorbar_extra_settings.setObjectName("pg_2_errorbar_extra_settings")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.pg_2_errorbar_extra_settings)
        self.gridLayout_23.setContentsMargins(13, 8, 8, 10)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.pg_2_errorbar_dashed_line_style_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_extra_settings
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorbar_dashed_line_style_combobox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorbar_dashed_line_style_combobox.setSizePolicy(sizePolicy)
        self.pg_2_errorbar_dashed_line_style_combobox.setObjectName(
            "pg_2_errorbar_dashed_line_style_combobox"
        )
        self.pg_2_errorbar_dashed_line_style_combobox.addItem("")
        self.pg_2_errorbar_dashed_line_style_combobox.addItem("")
        self.pg_2_errorbar_dashed_line_style_combobox.addItem("")
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_line_style_combobox, 6, 1, 1, 1
        )
        self.pg_2_errorbar_dashed_line_separation_label = QtWidgets.QLabel(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_dashed_line_separation_label.setMinimumSize(
            QtCore.QSize(0, 20)
        )
        self.pg_2_errorbar_dashed_line_separation_label.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorbar_dashed_line_separation_label.setFont(font)
        self.pg_2_errorbar_dashed_line_separation_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_errorbar_dashed_line_separation_label.setObjectName(
            "pg_2_errorbar_dashed_line_separation_label"
        )
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_line_separation_label, 7, 0, 1, 1
        )
        self.pg_2_errorbar_dashed_line_separation_combobox = QtWidgets.QSpinBox(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_dashed_line_separation_combobox.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg_2_errorbar_dashed_line_separation_combobox.setMinimum(1)
        self.pg_2_errorbar_dashed_line_separation_combobox.setMaximum(10000)
        self.pg_2_errorbar_dashed_line_separation_combobox.setProperty("value", 5)
        self.pg_2_errorbar_dashed_line_separation_combobox.setObjectName(
            "pg_2_errorbar_dashed_line_separation_combobox"
        )
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_line_separation_combobox, 7, 1, 1, 1
        )
        self.pg_2_errorbar_join_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_join_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_errorbar_join_style_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorbar_join_style_label.setFont(font)
        self.pg_2_errorbar_join_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_errorbar_join_style_label.setObjectName(
            "pg_2_errorbar_join_style_label"
        )
        self.gridLayout_23.addWidget(self.pg_2_errorbar_join_style_label, 1, 0, 1, 1)
        self.pg_2_errorbar_join_style_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_extra_settings
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorbar_join_style_combobox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorbar_join_style_combobox.setSizePolicy(sizePolicy)
        self.pg_2_errorbar_join_style_combobox.setObjectName(
            "pg_2_errorbar_join_style_combobox"
        )
        self.pg_2_errorbar_join_style_combobox.addItem("")
        self.pg_2_errorbar_join_style_combobox.addItem("")
        self.pg_2_errorbar_join_style_combobox.addItem("")
        self.gridLayout_23.addWidget(self.pg_2_errorbar_join_style_combobox, 1, 1, 1, 1)
        self.pg_2_errorbar_dashed_cap_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_dashed_cap_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_errorbar_dashed_cap_style_label.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorbar_dashed_cap_style_label.setFont(font)
        self.pg_2_errorbar_dashed_cap_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_errorbar_dashed_cap_style_label.setObjectName(
            "pg_2_errorbar_dashed_cap_style_label"
        )
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_cap_style_label, 5, 0, 1, 1
        )
        self.pg_2_errorbar_line_style_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_extra_settings
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorbar_line_style_combobox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorbar_line_style_combobox.setSizePolicy(sizePolicy)
        self.pg_2_errorbar_line_style_combobox.setMinimumSize(QtCore.QSize(80, 0))
        self.pg_2_errorbar_line_style_combobox.setObjectName(
            "pg_2_errorbar_line_style_combobox"
        )
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.pg_2_errorbar_line_style_combobox.addItem("")
        self.gridLayout_23.addWidget(self.pg_2_errorbar_line_style_combobox, 0, 1, 1, 1)
        self.pg_2_errorbar_dashed_cap_style_combobox = QtWidgets.QComboBox(
            self.pg_2_errorbar_extra_settings
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorbar_dashed_cap_style_combobox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorbar_dashed_cap_style_combobox.setSizePolicy(sizePolicy)
        self.pg_2_errorbar_dashed_cap_style_combobox.setObjectName(
            "pg_2_errorbar_dashed_cap_style_combobox"
        )
        self.pg_2_errorbar_dashed_cap_style_combobox.addItem("")
        self.pg_2_errorbar_dashed_cap_style_combobox.addItem("")
        self.pg_2_errorbar_dashed_cap_style_combobox.addItem("")
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_cap_style_combobox, 5, 1, 1, 1
        )
        self.pg_2_errorbar_dashed_line_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_dashed_line_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_errorbar_dashed_line_style_label.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorbar_dashed_line_style_label.setFont(font)
        self.pg_2_errorbar_dashed_line_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_errorbar_dashed_line_style_label.setObjectName(
            "pg_2_errorbar_dashed_line_style_label"
        )
        self.gridLayout_23.addWidget(
            self.pg_2_errorbar_dashed_line_style_label, 6, 0, 1, 1
        )
        self.pg_2_errorbar_line_style_label = QtWidgets.QLabel(
            self.pg_2_errorbar_extra_settings
        )
        self.pg_2_errorbar_line_style_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg_2_errorbar_line_style_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorbar_line_style_label.setFont(font)
        self.pg_2_errorbar_line_style_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_errorbar_line_style_label.setObjectName(
            "pg_2_errorbar_line_style_label"
        )
        self.gridLayout_23.addWidget(self.pg_2_errorbar_line_style_label, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            7,
            3,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_23.addItem(spacerItem1, 1, 2, 1, 1)
        self.verticalLayout_14.addWidget(self.pg_2_errorbar_extra_settings)
        self.pg_2_dimentions_gridLayout = QtWidgets.QGridLayout()
        self.pg_2_dimentions_gridLayout.setObjectName("pg_2_dimentions_gridLayout")
        self.max_width_label = QtWidgets.QLabel(self.groupBox_ErrorBarsPg2)
        self.max_width_label.setMinimumSize(QtCore.QSize(0, 20))
        self.max_width_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.max_width_label.setFont(font)
        self.max_width_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.max_width_label.setObjectName("max_width_label")
        self.pg_2_dimentions_gridLayout.addWidget(self.max_width_label, 4, 0, 1, 1)
        self.min_height_label = QtWidgets.QLabel(self.groupBox_ErrorBarsPg2)
        self.min_height_label.setMinimumSize(QtCore.QSize(0, 20))
        self.min_height_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.min_height_label.setFont(font)
        self.min_height_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.min_height_label.setObjectName("min_height_label")
        self.pg_2_dimentions_gridLayout.addWidget(self.min_height_label, 1, 0, 1, 1)
        self.pg2_resolution_spinBox = QtWidgets.QSpinBox(self.groupBox_ErrorBarsPg2)
        self.pg2_resolution_spinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_resolution_spinBox.setMinimum(1)
        self.pg2_resolution_spinBox.setMaximum(2000)
        self.pg2_resolution_spinBox.setProperty("value", 300)
        self.pg2_resolution_spinBox.setObjectName("pg2_resolution_spinBox")
        self.pg_2_dimentions_gridLayout.addWidget(
            self.pg2_resolution_spinBox, 4, 1, 1, 1
        )
        self.min_height_label_spinBox = QtWidgets.QSpinBox(self.groupBox_ErrorBarsPg2)
        self.min_height_label_spinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.min_height_label_spinBox.setMinimum(1)
        self.min_height_label_spinBox.setMaximum(8000)
        self.min_height_label_spinBox.setProperty("value", 400)
        self.min_height_label_spinBox.setObjectName("min_height_label_spinBox")
        self.pg_2_dimentions_gridLayout.addWidget(
            self.min_height_label_spinBox, 1, 1, 1, 1
        )
        self.max_height_label = QtWidgets.QLabel(self.groupBox_ErrorBarsPg2)
        self.max_height_label.setMinimumSize(QtCore.QSize(0, 20))
        self.max_height_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.max_height_label.setFont(font)
        self.max_height_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.max_height_label.setObjectName("max_height_label")
        self.pg_2_dimentions_gridLayout.addWidget(self.max_height_label, 2, 0, 1, 1)
        self.max_height_label_spinBox = QtWidgets.QSpinBox(self.groupBox_ErrorBarsPg2)
        self.max_height_label_spinBox.setMaximumSize(QtCore.QSize(65, 16777215))
        self.max_height_label_spinBox.setMinimum(1)
        self.max_height_label_spinBox.setMaximum(8000)
        self.max_height_label_spinBox.setProperty("value", 400)
        self.max_height_label_spinBox.setObjectName("max_height_label_spinBox")
        self.pg_2_dimentions_gridLayout.addWidget(
            self.max_height_label_spinBox, 2, 1, 1, 1
        )
        self.min_width_label = QtWidgets.QLabel(self.groupBox_ErrorBarsPg2)
        self.min_width_label.setMinimumSize(QtCore.QSize(0, 20))
        self.min_width_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.min_width_label.setFont(font)
        self.min_width_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.min_width_label.setObjectName("min_width_label")
        self.pg_2_dimentions_gridLayout.addWidget(self.min_width_label, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.pg_2_dimentions_gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.dimations_comboBox = QtWidgets.QComboBox(self.groupBox_ErrorBarsPg2)
        self.dimations_comboBox.setObjectName("dimations_comboBox")
        self.dimations_comboBox.addItem("")
        self.dimations_comboBox.addItem("")
        self.dimations_comboBox.addItem("")
        self.pg_2_dimentions_gridLayout.addWidget(self.dimations_comboBox, 0, 1, 1, 1)
        self.verticalLayout_14.addLayout(self.pg_2_dimentions_gridLayout)
        self.brokenaxis_frame = QtWidgets.QFrame(self.groupBox_ErrorBarsPg2)
        self.brokenaxis_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.brokenaxis_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.brokenaxis_frame.setObjectName("brokenaxis_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.brokenaxis_frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.brokenaxis_label = QtWidgets.QLabel(self.brokenaxis_frame)
        self.brokenaxis_label.setObjectName("brokenaxis_label")
        self.gridLayout_5.addWidget(self.brokenaxis_label, 0, 0, 1, 1)
        self.brokenaxis_x_checkBox = QtWidgets.QCheckBox(self.brokenaxis_frame)
        self.brokenaxis_x_checkBox.setText("")
        self.brokenaxis_x_checkBox.setObjectName("brokenaxis_x_checkBox")
        self.gridLayout_5.addWidget(self.brokenaxis_x_checkBox, 2, 1, 1, 1)
        self.brokenaxis_y_label = QtWidgets.QLabel(self.brokenaxis_frame)
        self.brokenaxis_y_label.setEnabled(True)
        self.brokenaxis_y_label.setObjectName("brokenaxis_y_label")
        self.gridLayout_5.addWidget(self.brokenaxis_y_label, 2, 0, 1, 1)
        self.brokenaxis_y_checkBox = QtWidgets.QCheckBox(self.brokenaxis_frame)
        self.brokenaxis_y_checkBox.setText("")
        self.brokenaxis_y_checkBox.setObjectName("brokenaxis_y_checkBox")
        self.gridLayout_5.addWidget(self.brokenaxis_y_checkBox, 3, 1, 1, 1)
        self.brokenaxis_x_label = QtWidgets.QLabel(self.brokenaxis_frame)
        self.brokenaxis_x_label.setObjectName("brokenaxis_x_label")
        self.gridLayout_5.addWidget(self.brokenaxis_x_label, 3, 0, 1, 1)
        self.brokenaxis_y_spinBox = QtWidgets.QSpinBox(self.brokenaxis_frame)
        self.brokenaxis_y_spinBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.brokenaxis_y_spinBox.setObjectName("brokenaxis_y_spinBox")
        self.gridLayout_5.addWidget(self.brokenaxis_y_spinBox, 2, 2, 1, 1)
        self.brokenaxis_x_spinBox = QtWidgets.QSpinBox(self.brokenaxis_frame)
        self.brokenaxis_x_spinBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.brokenaxis_x_spinBox.setObjectName("brokenaxis_x_spinBox")
        self.gridLayout_5.addWidget(self.brokenaxis_x_spinBox, 3, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout_5.addItem(spacerItem3, 2, 3, 1, 1)
        self.verticalLayout_14.addWidget(self.brokenaxis_frame)
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.groupBox_ErrorBarsPg2, 5, 0, 1, 1
        )
        self.pg2_general_attributes_groupBox = QtWidgets.QGroupBox(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_general_attributes_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.pg2_general_attributes_groupBox.setSizePolicy(sizePolicy)
        self.pg2_general_attributes_groupBox.setMaximumSize(QtCore.QSize(16777215, 420))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pg2_general_attributes_groupBox.setFont(font)
        self.pg2_general_attributes_groupBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg2_general_attributes_groupBox.setObjectName(
            "pg2_general_attributes_groupBox"
        )
        self.pg_2_title_groupbox_gridLayout = QtWidgets.QGridLayout(
            self.pg2_general_attributes_groupBox
        )
        self.pg_2_title_groupbox_gridLayout.setContentsMargins(-1, 20, -1, -1)
        self.pg_2_title_groupbox_gridLayout.setObjectName(
            "pg_2_title_groupbox_gridLayout"
        )
        self.pg2_graph_x_axis_label = QtWidgets.QLabel(
            self.pg2_general_attributes_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_graph_x_axis_label.sizePolicy().hasHeightForWidth()
        )
        self.pg2_graph_x_axis_label.setSizePolicy(sizePolicy)
        self.pg2_graph_x_axis_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_x_axis_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pg2_graph_x_axis_label.setFont(font)
        self.pg2_graph_x_axis_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_x_axis_label.setObjectName("pg2_graph_x_axis_label")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg2_graph_x_axis_label, 3, 0, 1, 1
        )
        self.pg_2_Title_textedit = QtWidgets.QTextEdit(
            self.pg2_general_attributes_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_Title_textedit.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_Title_textedit.setSizePolicy(sizePolicy)
        self.pg_2_Title_textedit.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg_2_Title_textedit.setFont(font)
        self.pg_2_Title_textedit.setStyleSheet("color: rgb(255, 255, 255);")
        self.pg_2_Title_textedit.setObjectName("pg_2_Title_textedit")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_Title_textedit, 1, 0, 1, 2
        )
        self.pg2_graph_title = QtWidgets.QLabel(self.pg2_general_attributes_groupBox)
        self.pg2_graph_title.setMinimumSize(QtCore.QSize(0, 17))
        self.pg2_graph_title.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pg2_graph_title.setFont(font)
        self.pg2_graph_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_title.setObjectName("pg2_graph_title")
        self.pg_2_title_groupbox_gridLayout.addWidget(self.pg2_graph_title, 0, 0, 1, 2)
        self.pg_2_x_axis_textedit = QtWidgets.QTextEdit(
            self.pg2_general_attributes_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_x_axis_textedit.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_x_axis_textedit.setSizePolicy(sizePolicy)
        self.pg_2_x_axis_textedit.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg_2_x_axis_textedit.setFont(font)
        self.pg_2_x_axis_textedit.setStyleSheet("color: rgb(255, 255, 255);")
        self.pg_2_x_axis_textedit.setObjectName("pg_2_x_axis_textedit")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_x_axis_textedit, 4, 0, 1, 1
        )
        self.pg_2_y_axis_textedit_2 = QtWidgets.QTextEdit(
            self.pg2_general_attributes_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_y_axis_textedit_2.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_y_axis_textedit_2.setSizePolicy(sizePolicy)
        self.pg_2_y_axis_textedit_2.setMaximumSize(QtCore.QSize(100000, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg_2_y_axis_textedit_2.setFont(font)
        self.pg_2_y_axis_textedit_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.pg_2_y_axis_textedit_2.setObjectName("pg_2_y_axis_textedit_2")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg_2_y_axis_textedit_2, 4, 1, 1, 1
        )
        self.pg2_graph_y_axis_label = QtWidgets.QLabel(
            self.pg2_general_attributes_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_graph_y_axis_label.sizePolicy().hasHeightForWidth()
        )
        self.pg2_graph_y_axis_label.setSizePolicy(sizePolicy)
        self.pg2_graph_y_axis_label.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_y_axis_label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pg2_graph_y_axis_label.setFont(font)
        self.pg2_graph_y_axis_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_y_axis_label.setObjectName("pg2_graph_y_axis_label")
        self.pg_2_title_groupbox_gridLayout.addWidget(
            self.pg2_graph_y_axis_label, 3, 1, 1, 1
        )
        self.label = QtWidgets.QLabel(self.pg2_general_attributes_groupBox)
        self.label.setObjectName("label")
        self.pg_2_title_groupbox_gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.pg2_general_attributes_groupBox)
        self.comboBox.setObjectName("comboBox")
        self.pg_2_title_groupbox_gridLayout.addWidget(self.comboBox, 5, 1, 1, 1)
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.pg2_general_attributes_groupBox, 2, 0, 1, 1
        )
        self.pg_2_graph_colors_groupBox = QtWidgets.QGroupBox(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_graph_colors_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_graph_colors_groupBox.setSizePolicy(sizePolicy)
        self.pg_2_graph_colors_groupBox.setMaximumSize(QtCore.QSize(16777215, 2000))
        self.pg_2_graph_colors_groupBox.setObjectName("pg_2_graph_colors_groupBox")
        self.pg_2_gridLayout_16 = QtWidgets.QGridLayout(self.pg_2_graph_colors_groupBox)
        self.pg_2_gridLayout_16.setContentsMargins(-1, 20, -1, -1)
        self.pg_2_gridLayout_16.setHorizontalSpacing(7)
        self.pg_2_gridLayout_16.setVerticalSpacing(6)
        self.pg_2_gridLayout_16.setObjectName("pg_2_gridLayout_16")
        self.pg_2_graph_colors_groupBox_gridLayout = QtWidgets.QGridLayout()
        self.pg_2_graph_colors_groupBox_gridLayout.setObjectName(
            "pg_2_graph_colors_groupBox_gridLayout"
        )
        self.pg2_graph_visulaizer_pallets = QtWidgets.QPushButton(
            self.pg_2_graph_colors_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_graph_visulaizer_pallets.sizePolicy().hasHeightForWidth()
        )
        self.pg2_graph_visulaizer_pallets.setSizePolicy(sizePolicy)
        self.pg2_graph_visulaizer_pallets.setMinimumSize(QtCore.QSize(50, 0))
        self.pg2_graph_visulaizer_pallets.setObjectName("pg2_graph_visulaizer_pallets")
        self.pg_2_graph_colors_groupBox_gridLayout.addWidget(
            self.pg2_graph_visulaizer_pallets, 0, 0, 1, 1
        )
        self.pg2_graph_visulaizer_hide_item = QtWidgets.QPushButton(
            self.pg_2_graph_colors_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_graph_visulaizer_hide_item.sizePolicy().hasHeightForWidth()
        )
        self.pg2_graph_visulaizer_hide_item.setSizePolicy(sizePolicy)
        self.pg2_graph_visulaizer_hide_item.setMinimumSize(QtCore.QSize(50, 0))
        self.pg2_graph_visulaizer_hide_item.setObjectName(
            "pg2_graph_visulaizer_hide_item"
        )
        self.pg_2_graph_colors_groupBox_gridLayout.addWidget(
            self.pg2_graph_visulaizer_hide_item, 1, 0, 1, 1
        )
        self.pg2_graph_visulaizer_move_down = QtWidgets.QPushButton(
            self.pg_2_graph_colors_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_graph_visulaizer_move_down.sizePolicy().hasHeightForWidth()
        )
        self.pg2_graph_visulaizer_move_down.setSizePolicy(sizePolicy)
        self.pg2_graph_visulaizer_move_down.setMinimumSize(QtCore.QSize(50, 0))
        self.pg2_graph_visulaizer_move_down.setText("")
        self.pg2_graph_visulaizer_move_down.setObjectName(
            "pg2_graph_visulaizer_move_down"
        )
        self.pg_2_graph_colors_groupBox_gridLayout.addWidget(
            self.pg2_graph_visulaizer_move_down, 2, 0, 1, 1
        )
        self.pg_2_graph_colors_groupBox_listWidget = QtWidgets.QListWidget(
            self.pg_2_graph_colors_groupBox
        )
        self.pg_2_graph_colors_groupBox_listWidget.setObjectName(
            "pg_2_graph_colors_groupBox_listWidget"
        )
        self.pg_2_graph_colors_groupBox_gridLayout.addWidget(
            self.pg_2_graph_colors_groupBox_listWidget, 0, 3, 3, 1
        )
        self.pg_2_gridLayout_16.addLayout(
            self.pg_2_graph_colors_groupBox_gridLayout, 0, 0, 1, 1
        )
        self.pg_2_general_colors = QtWidgets.QFrame(self.pg_2_graph_colors_groupBox)
        self.pg_2_general_colors.setObjectName("pg_2_general_colors")
        self.pg_2_graph_colors_btns_verticalLayout = QtWidgets.QVBoxLayout(
            self.pg_2_general_colors
        )
        self.pg_2_graph_colors_btns_verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.pg_2_graph_colors_btns_verticalLayout.setSpacing(6)
        self.pg_2_graph_colors_btns_verticalLayout.setObjectName(
            "pg_2_graph_colors_btns_verticalLayout"
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm = QtWidgets.QFrame(
            self.pg_2_general_colors
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm.setMinimumSize(QtCore.QSize(0, 48))
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm.setObjectName(
            "pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm"
        )
        self.plotwidtget_gridLayout_7 = QtWidgets.QGridLayout(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm
        )
        self.plotwidtget_gridLayout_7.setObjectName("plotwidtget_gridLayout_7")
        self.pg_2_swarmplot_plot_settings_1 = QtWidgets.QFrame(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm
        )
        self.pg_2_swarmplot_plot_settings_1.setObjectName(
            "pg_2_swarmplot_plot_settings_1"
        )
        self.horizontalLayout_67 = QtWidgets.QHBoxLayout(
            self.pg_2_swarmplot_plot_settings_1
        )
        self.horizontalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_67.setObjectName("horizontalLayout_67")
        self.pg_2_swarmplot_settings_1_left = QtWidgets.QFrame(
            self.pg_2_swarmplot_plot_settings_1
        )
        self.pg_2_swarmplot_settings_1_left.setObjectName(
            "pg_2_swarmplot_settings_1_left"
        )
        self.pg2Layout_verticalLayout_18 = QtWidgets.QVBoxLayout(
            self.pg_2_swarmplot_settings_1_left
        )
        self.pg2Layout_verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_18.setObjectName("pg2Layout_verticalLayout_18")
        self.pg2_graph_swarmplot_pallete_style_frame = QtWidgets.QFrame(
            self.pg_2_swarmplot_settings_1_left
        )
        self.pg2_graph_swarmplot_pallete_style_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_swarmplot_pallete_style_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_swarmplot_pallete_style_frame.setObjectName(
            "pg2_graph_swarmplot_pallete_style_frame"
        )
        self.horizontalLayout_68 = QtWidgets.QHBoxLayout(
            self.pg2_graph_swarmplot_pallete_style_frame
        )
        self.horizontalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_68.setObjectName("horizontalLayout_68")
        self.pg2Layout_verticalLayout_18.addWidget(
            self.pg2_graph_swarmplot_pallete_style_frame
        )
        self.pg_2_graph_border_color_frame_swarmplot_plot = QtWidgets.QFrame(
            self.pg_2_swarmplot_settings_1_left
        )
        self.pg_2_graph_border_color_frame_swarmplot_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_graph_border_color_frame_swarmplot_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_graph_border_color_frame_swarmplot_plot.setObjectName(
            "pg_2_graph_border_color_frame_swarmplot_plot"
        )
        self.horizontalLayout_70 = QtWidgets.QHBoxLayout(
            self.pg_2_graph_border_color_frame_swarmplot_plot
        )
        self.horizontalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_70.setObjectName("horizontalLayout_70")
        self.pg2Layout_verticalLayout_18.addWidget(
            self.pg_2_graph_border_color_frame_swarmplot_plot
        )
        self.pg2_graph_border_width_frame_swarmplot = QtWidgets.QFrame(
            self.pg_2_swarmplot_settings_1_left
        )
        self.pg2_graph_border_width_frame_swarmplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_border_width_frame_swarmplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_border_width_frame_swarmplot.setObjectName(
            "pg2_graph_border_width_frame_swarmplot"
        )
        self.horizontalLayout_71 = QtWidgets.QHBoxLayout(
            self.pg2_graph_border_width_frame_swarmplot
        )
        self.horizontalLayout_71.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_71.setSpacing(7)
        self.horizontalLayout_71.setObjectName("horizontalLayout_71")
        self.pg2_graph_border_width_label_swarmplot = QtWidgets.QLabel(
            self.pg2_graph_border_width_frame_swarmplot
        )
        self.pg2_graph_border_width_label_swarmplot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_border_width_label_swarmplot.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_border_width_label_swarmplot.setFont(font)
        self.pg2_graph_border_width_label_swarmplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_border_width_label_swarmplot.setObjectName(
            "pg2_graph_border_width_label_swarmplot"
        )
        self.horizontalLayout_71.addWidget(self.pg2_graph_border_width_label_swarmplot)
        self.pg2_graph_border_width_spinBox_swarmplot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_border_width_frame_swarmplot
        )
        self.pg2_graph_border_width_spinBox_swarmplot.setMinimumSize(
            QtCore.QSize(65, 0)
        )
        self.pg2_graph_border_width_spinBox_swarmplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_border_width_spinBox_swarmplot.setProperty("value", 0.5)
        self.pg2_graph_border_width_spinBox_swarmplot.setObjectName(
            "pg2_graph_border_width_spinBox_swarmplot"
        )
        self.horizontalLayout_71.addWidget(
            self.pg2_graph_border_width_spinBox_swarmplot
        )
        self.pg2Layout_verticalLayout_18.addWidget(
            self.pg2_graph_border_width_frame_swarmplot
        )
        spacerItem4 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_18.addItem(spacerItem4)
        self.horizontalLayout_67.addWidget(self.pg_2_swarmplot_settings_1_left)
        spacerItem5 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_67.addItem(spacerItem5)
        self.pg_2_settings_1_right_swarmplot_plot = QtWidgets.QFrame(
            self.pg_2_swarmplot_plot_settings_1
        )
        self.pg_2_settings_1_right_swarmplot_plot.setObjectName(
            "pg_2_settings_1_right_swarmplot_plot"
        )
        self.pg2Layout_verticalLayout_19 = QtWidgets.QVBoxLayout(
            self.pg_2_settings_1_right_swarmplot_plot
        )
        self.pg2Layout_verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_19.setObjectName("pg2Layout_verticalLayout_19")
        self.pg2_graph_index_frame_swarmplot_2 = QtWidgets.QFrame(
            self.pg_2_settings_1_right_swarmplot_plot
        )
        self.pg2_graph_index_frame_swarmplot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_index_frame_swarmplot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_index_frame_swarmplot_2.setObjectName(
            "pg2_graph_index_frame_swarmplot_2"
        )
        self.horizontalLayout_72 = QtWidgets.QHBoxLayout(
            self.pg2_graph_index_frame_swarmplot_2
        )
        self.horizontalLayout_72.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_72.setObjectName("horizontalLayout_72")
        self.pg2Layout_verticalLayout_19.addWidget(
            self.pg2_graph_index_frame_swarmplot_2
        )
        self.pg2_graph_size_frame_swarmplot = QtWidgets.QFrame(
            self.pg_2_settings_1_right_swarmplot_plot
        )
        self.pg2_graph_size_frame_swarmplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_size_frame_swarmplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_size_frame_swarmplot.setObjectName(
            "pg2_graph_size_frame_swarmplot"
        )
        self.horizontalLayout_73 = QtWidgets.QHBoxLayout(
            self.pg2_graph_size_frame_swarmplot
        )
        self.horizontalLayout_73.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_73.setSpacing(0)
        self.horizontalLayout_73.setObjectName("horizontalLayout_73")
        self.pg2_graph_size_label_swarmplot = QtWidgets.QLabel(
            self.pg2_graph_size_frame_swarmplot
        )
        self.pg2_graph_size_label_swarmplot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_size_label_swarmplot.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_size_label_swarmplot.setFont(font)
        self.pg2_graph_size_label_swarmplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_size_label_swarmplot.setObjectName(
            "pg2_graph_size_label_swarmplot"
        )
        self.horizontalLayout_73.addWidget(self.pg2_graph_size_label_swarmplot)
        self.pg2_graph_size_spinBox_swarmplot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_size_frame_swarmplot
        )
        self.pg2_graph_size_spinBox_swarmplot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_size_spinBox_swarmplot.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_graph_size_spinBox_swarmplot.setProperty("value", 3.0)
        self.pg2_graph_size_spinBox_swarmplot.setObjectName(
            "pg2_graph_size_spinBox_swarmplot"
        )
        self.horizontalLayout_73.addWidget(self.pg2_graph_size_spinBox_swarmplot)
        self.pg2Layout_verticalLayout_19.addWidget(self.pg2_graph_size_frame_swarmplot)
        self.pg2_graph_orientaitno_frame_swarmplot = QtWidgets.QFrame(
            self.pg_2_settings_1_right_swarmplot_plot
        )
        self.pg2_graph_orientaitno_frame_swarmplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_orientaitno_frame_swarmplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_orientaitno_frame_swarmplot.setObjectName(
            "pg2_graph_orientaitno_frame_swarmplot"
        )
        self.horizontalLayout_74 = QtWidgets.QHBoxLayout(
            self.pg2_graph_orientaitno_frame_swarmplot
        )
        self.horizontalLayout_74.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_74.setObjectName("horizontalLayout_74")
        self.pg2_graph_orientation_label_swarmplot = QtWidgets.QLabel(
            self.pg2_graph_orientaitno_frame_swarmplot
        )
        self.pg2_graph_orientation_label_swarmplot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_orientation_label_swarmplot.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_orientation_label_swarmplot.setFont(font)
        self.pg2_graph_orientation_label_swarmplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_orientation_label_swarmplot.setObjectName(
            "pg2_graph_orientation_label_swarmplot"
        )
        self.horizontalLayout_74.addWidget(self.pg2_graph_orientation_label_swarmplot)
        self.pg2_graph_orientaitno_combobox_swarmplot = QtWidgets.QComboBox(
            self.pg2_graph_orientaitno_frame_swarmplot
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.setMinimumSize(
            QtCore.QSize(80, 0)
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.setObjectName(
            "pg2_graph_orientaitno_combobox_swarmplot"
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.addItem("")
        self.pg2_graph_orientaitno_combobox_swarmplot.addItem("")
        self.horizontalLayout_74.addWidget(
            self.pg2_graph_orientaitno_combobox_swarmplot
        )
        self.pg2Layout_verticalLayout_19.addWidget(
            self.pg2_graph_orientaitno_frame_swarmplot
        )
        spacerItem6 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_19.addItem(spacerItem6)
        self.horizontalLayout_67.addWidget(self.pg_2_settings_1_right_swarmplot_plot)
        self.plotwidtget_gridLayout_7.addWidget(
            self.pg_2_swarmplot_plot_settings_1, 0, 0, 1, 1
        )
        self.pg_2_graph_colors_btns_verticalLayout.addWidget(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Swarm
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot = QtWidgets.QWidget(
            self.pg_2_general_colors
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot.setMinimumSize(QtCore.QSize(0, 48))
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot.setObjectName(
            "pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot"
        )
        self.plotwidtget_gridLayout_6 = QtWidgets.QGridLayout(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot
        )
        self.plotwidtget_gridLayout_6.setObjectName("plotwidtget_gridLayout_6")
        self.pg_2_graph_colors_btns_verticalLayout.addWidget(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Dot
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin = QtWidgets.QFrame(
            self.pg_2_general_colors
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin.setMinimumSize(
            QtCore.QSize(0, 48)
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin.setObjectName(
            "pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin"
        )
        self.plotwidtget_gridLayout_2 = QtWidgets.QGridLayout(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin
        )
        self.plotwidtget_gridLayout_2.setObjectName("plotwidtget_gridLayout_2")
        self.pg_2_violinplot_plot_settings = QtWidgets.QFrame(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin
        )
        self.pg_2_violinplot_plot_settings.setObjectName(
            "pg_2_violinplot_plot_settings"
        )
        self.horizontalLayout_56 = QtWidgets.QHBoxLayout(
            self.pg_2_violinplot_plot_settings
        )
        self.horizontalLayout_56.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")
        self.pg_2_violinplot_plot_settings_1_left = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings
        )
        self.pg_2_violinplot_plot_settings_1_left.setObjectName(
            "pg_2_violinplot_plot_settings_1_left"
        )
        self.pg2Layout_verticalLayout_16 = QtWidgets.QVBoxLayout(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2Layout_verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_16.setObjectName("pg2Layout_verticalLayout_16")
        self.pg2_graph_violinplot_pallete_style_frame = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2_graph_violinplot_pallete_style_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_violinplot_pallete_style_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_violinplot_pallete_style_frame.setObjectName(
            "pg2_graph_violinplot_pallete_style_frame"
        )
        self.horizontalLayout_57 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_pallete_style_frame
        )
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg2_graph_violinplot_pallete_style_frame
        )
        self.pg_2_custom_color_graph_frame_violinplot = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg_2_custom_color_graph_frame_violinplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_custom_color_graph_frame_violinplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_custom_color_graph_frame_violinplot.setObjectName(
            "pg_2_custom_color_graph_frame_violinplot"
        )
        self.horizontalLayout_58 = QtWidgets.QHBoxLayout(
            self.pg_2_custom_color_graph_frame_violinplot
        )
        self.horizontalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_58.setObjectName("horizontalLayout_58")
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg_2_custom_color_graph_frame_violinplot
        )
        self.pg2_graph_border_width_frame_violinplot = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2_graph_border_width_frame_violinplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_border_width_frame_violinplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_border_width_frame_violinplot.setObjectName(
            "pg2_graph_border_width_frame_violinplot"
        )
        self.horizontalLayout_59 = QtWidgets.QHBoxLayout(
            self.pg2_graph_border_width_frame_violinplot
        )
        self.horizontalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_59.setSpacing(0)
        self.horizontalLayout_59.setObjectName("horizontalLayout_59")
        self.pg2_graph_border_width_label_violinplot = QtWidgets.QLabel(
            self.pg2_graph_border_width_frame_violinplot
        )
        self.pg2_graph_border_width_label_violinplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_border_width_label_violinplot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_border_width_label_violinplot.setFont(font)
        self.pg2_graph_border_width_label_violinplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_border_width_label_violinplot.setObjectName(
            "pg2_graph_border_width_label_violinplot"
        )
        self.horizontalLayout_59.addWidget(self.pg2_graph_border_width_label_violinplot)
        self.pg2_graph_just_width_spinbox_violinplot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_border_width_frame_violinplot
        )
        self.pg2_graph_just_width_spinbox_violinplot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_just_width_spinbox_violinplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_just_width_spinbox_violinplot.setMaximum(20.0)
        self.pg2_graph_just_width_spinbox_violinplot.setSingleStep(0.1)
        self.pg2_graph_just_width_spinbox_violinplot.setProperty("value", 0.4)
        self.pg2_graph_just_width_spinbox_violinplot.setObjectName(
            "pg2_graph_just_width_spinbox_violinplot"
        )
        self.horizontalLayout_59.addWidget(self.pg2_graph_just_width_spinbox_violinplot)
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg2_graph_border_width_frame_violinplot
        )
        self.pg2_graph_violinplot_orienation_frame = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2_graph_violinplot_orienation_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_violinplot_orienation_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_violinplot_orienation_frame.setObjectName(
            "pg2_graph_violinplot_orienation_frame"
        )
        self.horizontalLayout_60 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_orienation_frame
        )
        self.horizontalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")
        self.pg2_graph_violinplot_orienation_label = QtWidgets.QLabel(
            self.pg2_graph_violinplot_orienation_frame
        )
        self.pg2_graph_violinplot_orienation_label.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_violinplot_orienation_label.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_violinplot_orienation_label.setFont(font)
        self.pg2_graph_violinplot_orienation_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_violinplot_orienation_label.setObjectName(
            "pg2_graph_violinplot_orienation_label"
        )
        self.horizontalLayout_60.addWidget(self.pg2_graph_violinplot_orienation_label)
        self.pg2_graph_violinplot_orienation_combobox = QtWidgets.QComboBox(
            self.pg2_graph_violinplot_orienation_frame
        )
        self.pg2_graph_violinplot_orienation_combobox.setMinimumSize(
            QtCore.QSize(80, 0)
        )
        self.pg2_graph_violinplot_orienation_combobox.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg2_graph_violinplot_orienation_combobox.setObjectName(
            "pg2_graph_violinplot_orienation_combobox"
        )
        self.pg2_graph_violinplot_orienation_combobox.addItem("")
        self.pg2_graph_violinplot_orienation_combobox.addItem("")
        self.horizontalLayout_60.addWidget(
            self.pg2_graph_violinplot_orienation_combobox
        )
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg2_graph_violinplot_orienation_frame
        )
        self.pg2_graph_violinplot_saturation_frame = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2_graph_violinplot_saturation_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_violinplot_saturation_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_violinplot_saturation_frame.setObjectName(
            "pg2_graph_violinplot_saturation_frame"
        )
        self.horizontalLayout_61 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_saturation_frame
        )
        self.horizontalLayout_61.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")
        self.pg2_graph_violinplot_saturation_label = QtWidgets.QLabel(
            self.pg2_graph_violinplot_saturation_frame
        )
        self.pg2_graph_violinplot_saturation_label.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_violinplot_saturation_label.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_violinplot_saturation_label.setFont(font)
        self.pg2_graph_violinplot_saturation_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_violinplot_saturation_label.setObjectName(
            "pg2_graph_violinplot_saturation_label"
        )
        self.horizontalLayout_61.addWidget(self.pg2_graph_violinplot_saturation_label)
        self.pg2_graph_saturation_spinBox_violinplot = QtWidgets.QSpinBox(
            self.pg2_graph_violinplot_saturation_frame
        )
        self.pg2_graph_saturation_spinBox_violinplot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_saturation_spinBox_violinplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_saturation_spinBox_violinplot.setMaximum(100)
        self.pg2_graph_saturation_spinBox_violinplot.setProperty("value", 100)
        self.pg2_graph_saturation_spinBox_violinplot.setObjectName(
            "pg2_graph_saturation_spinBox_violinplot"
        )
        self.horizontalLayout_61.addWidget(self.pg2_graph_saturation_spinBox_violinplot)
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg2_graph_violinplot_saturation_frame
        )
        self.pg2_graph_violinplot_InnerVal_frame = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.pg2_graph_violinplot_InnerVal_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_violinplot_InnerVal_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_violinplot_InnerVal_frame.setObjectName(
            "pg2_graph_violinplot_InnerVal_frame"
        )
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_InnerVal_frame
        )
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout.setContentsMargins(
            0, 0, 0, 0
        )
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout.setSpacing(0)
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout.setObjectName(
            "pg2_graph_violinplot_Inner_frame_horizontalLayout"
        )
        self.pg2_graph_violinplot_Inner_label = QtWidgets.QLabel(
            self.pg2_graph_violinplot_InnerVal_frame
        )
        self.pg2_graph_violinplot_Inner_label.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_violinplot_Inner_label.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_violinplot_Inner_label.setFont(font)
        self.pg2_graph_violinplot_Inner_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg2_graph_violinplot_Inner_label.setObjectName(
            "pg2_graph_violinplot_Inner_label"
        )
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout.addWidget(
            self.pg2_graph_violinplot_Inner_label
        )
        self.pg2_graph_violinplot_InnerVal_combobox = QtWidgets.QComboBox(
            self.pg2_graph_violinplot_InnerVal_frame
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setMinimumSize(QtCore.QSize(80, 0))
        self.pg2_graph_violinplot_InnerVal_combobox.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setObjectName(
            "pg2_graph_violinplot_InnerVal_combobox"
        )
        self.pg2_graph_violinplot_InnerVal_combobox.addItem("")
        self.pg2_graph_violinplot_InnerVal_combobox.addItem("")
        self.pg2_graph_violinplot_InnerVal_combobox.addItem("")
        self.pg2_graph_violinplot_InnerVal_combobox.addItem("")
        self.pg2_graph_violinplot_InnerVal_combobox.addItem("")
        self.pg2_graph_violinplot_Inner_frame_horizontalLayout.addWidget(
            self.pg2_graph_violinplot_InnerVal_combobox
        )
        self.pg2Layout_verticalLayout_16.addWidget(
            self.pg2_graph_violinplot_InnerVal_frame
        )
        spacerItem7 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_16.addItem(spacerItem7)
        self.horizontalLayout_56.addWidget(self.pg_2_violinplot_plot_settings_1_left)
        spacerItem8 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_56.addItem(spacerItem8)
        self.pg_2_violinplot_plot_settings_1_right = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings
        )
        self.pg_2_violinplot_plot_settings_1_right.setObjectName(
            "pg_2_violinplot_plot_settings_1_right"
        )
        self.pg2Layout_verticalLayout_17 = QtWidgets.QVBoxLayout(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg2Layout_verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_17.setObjectName("pg2Layout_verticalLayout_17")
        self.pg2_graph_index_frame_violinplot = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg2_graph_index_frame_violinplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_index_frame_violinplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_index_frame_violinplot.setObjectName(
            "pg2_graph_index_frame_violinplot"
        )
        self.horizontalLayout_62 = QtWidgets.QHBoxLayout(
            self.pg2_graph_index_frame_violinplot
        )
        self.horizontalLayout_62.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_62.setObjectName("horizontalLayout_62")
        self.pg2Layout_verticalLayout_17.addWidget(
            self.pg2_graph_index_frame_violinplot
        )
        self.pg2_graph_border_width_frame_violinplot_2 = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg2_graph_border_width_frame_violinplot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_border_width_frame_violinplot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_border_width_frame_violinplot_2.setObjectName(
            "pg2_graph_border_width_frame_violinplot_2"
        )
        self.horizontalLayout_64 = QtWidgets.QHBoxLayout(
            self.pg2_graph_border_width_frame_violinplot_2
        )
        self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setObjectName("horizontalLayout_64")
        self.pg2_graph_border_width_label_violinplot_2 = QtWidgets.QLabel(
            self.pg2_graph_border_width_frame_violinplot_2
        )
        self.pg2_graph_border_width_label_violinplot_2.setMinimumSize(
            QtCore.QSize(0, 0)
        )
        self.pg2_graph_border_width_label_violinplot_2.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_border_width_label_violinplot_2.setFont(font)
        self.pg2_graph_border_width_label_violinplot_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_border_width_label_violinplot_2.setObjectName(
            "pg2_graph_border_width_label_violinplot_2"
        )
        self.horizontalLayout_64.addWidget(
            self.pg2_graph_border_width_label_violinplot_2
        )
        self.pg2_graph_border_width_spinBox_violinplot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_border_width_frame_violinplot_2
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMinimumSize(
            QtCore.QSize(65, 0)
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMaximum(30.0)
        self.pg2_graph_border_width_spinBox_violinplot.setSingleStep(0.5)
        self.pg2_graph_border_width_spinBox_violinplot.setProperty("value", 1.0)
        self.pg2_graph_border_width_spinBox_violinplot.setObjectName(
            "pg2_graph_border_width_spinBox_violinplot"
        )
        self.horizontalLayout_64.addWidget(
            self.pg2_graph_border_width_spinBox_violinplot
        )
        self.pg2Layout_verticalLayout_17.addWidget(
            self.pg2_graph_border_width_frame_violinplot_2
        )
        self.pg2_graph_cut_frame_violinplot = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg2_graph_cut_frame_violinplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_cut_frame_violinplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_cut_frame_violinplot.setObjectName(
            "pg2_graph_cut_frame_violinplot"
        )
        self.horizontalLayout_65 = QtWidgets.QHBoxLayout(
            self.pg2_graph_cut_frame_violinplot
        )
        self.horizontalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_65.setSpacing(0)
        self.horizontalLayout_65.setObjectName("horizontalLayout_65")
        self.pg2_graph_cut_label_violinplot = QtWidgets.QLabel(
            self.pg2_graph_cut_frame_violinplot
        )
        self.pg2_graph_cut_label_violinplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_cut_label_violinplot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_cut_label_violinplot.setFont(font)
        self.pg2_graph_cut_label_violinplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_cut_label_violinplot.setObjectName(
            "pg2_graph_cut_label_violinplot"
        )
        self.horizontalLayout_65.addWidget(self.pg2_graph_cut_label_violinplot)
        self.pg2_graph_cut_spinBox_vil = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_cut_frame_violinplot
        )
        self.pg2_graph_cut_spinBox_vil.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_cut_spinBox_vil.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_graph_cut_spinBox_vil.setDecimals(1)
        self.pg2_graph_cut_spinBox_vil.setSingleStep(0.1)
        self.pg2_graph_cut_spinBox_vil.setProperty("value", 3.0)
        self.pg2_graph_cut_spinBox_vil.setObjectName("pg2_graph_cut_spinBox_vil")
        self.horizontalLayout_65.addWidget(self.pg2_graph_cut_spinBox_vil)
        self.pg2Layout_verticalLayout_17.addWidget(self.pg2_graph_cut_frame_violinplot)
        self.pg2_graph_scale_frame_violinplot = QtWidgets.QFrame(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg2_graph_scale_frame_violinplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_scale_frame_violinplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_scale_frame_violinplot.setObjectName(
            "pg2_graph_scale_frame_violinplot"
        )
        self.horizontalLayout_66 = QtWidgets.QHBoxLayout(
            self.pg2_graph_scale_frame_violinplot
        )
        self.horizontalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        self.pg2_graph_scale_label_violinplot = QtWidgets.QLabel(
            self.pg2_graph_scale_frame_violinplot
        )
        self.pg2_graph_scale_label_violinplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_scale_label_violinplot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_scale_label_violinplot.setFont(font)
        self.pg2_graph_scale_label_violinplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_scale_label_violinplot.setObjectName(
            "pg2_graph_scale_label_violinplot"
        )
        self.horizontalLayout_66.addWidget(self.pg2_graph_scale_label_violinplot)
        self.pg2_graph_scale_comboBox_violinplot = QtWidgets.QComboBox(
            self.pg2_graph_scale_frame_violinplot
        )
        self.pg2_graph_scale_comboBox_violinplot.setMinimumSize(QtCore.QSize(70, 0))
        self.pg2_graph_scale_comboBox_violinplot.setMaximumSize(
            QtCore.QSize(70, 16777215)
        )
        self.pg2_graph_scale_comboBox_violinplot.setObjectName(
            "pg2_graph_scale_comboBox_violinplot"
        )
        self.pg2_graph_scale_comboBox_violinplot.addItem("")
        self.pg2_graph_scale_comboBox_violinplot.addItem("")
        self.pg2_graph_scale_comboBox_violinplot.addItem("")
        self.horizontalLayout_66.addWidget(self.pg2_graph_scale_comboBox_violinplot)
        self.pg2Layout_verticalLayout_17.addWidget(
            self.pg2_graph_scale_frame_violinplot
        )
        spacerItem9 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_17.addItem(spacerItem9)
        self.horizontalLayout_56.addWidget(self.pg_2_violinplot_plot_settings_1_right)
        self.plotwidtget_gridLayout_2.addWidget(
            self.pg_2_violinplot_plot_settings, 0, 0, 1, 1
        )
        self.pg_2_graph_colors_btns_verticalLayout.addWidget(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Violin
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar = QtWidgets.QFrame(
            self.pg_2_general_colors
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar.setMinimumSize(QtCore.QSize(0, 70))
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar.setObjectName(
            "pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar"
        )
        self.pg_2_plotwidtget_gridLayout = QtWidgets.QGridLayout(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar
        )
        self.pg_2_plotwidtget_gridLayout.setObjectName("pg_2_plotwidtget_gridLayout")
        self.pg_2_box_plot_settings_1 = QtWidgets.QFrame(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar
        )
        self.pg_2_box_plot_settings_1.setObjectName("pg_2_box_plot_settings_1")
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout(self.pg_2_box_plot_settings_1)
        self.horizontalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.pg_2_box_plot_settings_1_left_3 = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1
        )
        self.pg_2_box_plot_settings_1_left_3.setObjectName(
            "pg_2_box_plot_settings_1_left_3"
        )
        self.pg2Layout_verticalLayout_13 = QtWidgets.QVBoxLayout(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2Layout_verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_13.setObjectName("pg2Layout_verticalLayout_13")
        self.pg2_graph_barplot_pallete_style_frame = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2_graph_barplot_pallete_style_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_barplot_pallete_style_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_barplot_pallete_style_frame.setObjectName(
            "pg2_graph_barplot_pallete_style_frame"
        )
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout(
            self.pg2_graph_barplot_pallete_style_frame
        )
        self.horizontalLayout_46.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_46.setSpacing(0)
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.pg2Layout_verticalLayout_13.addWidget(
            self.pg2_graph_barplot_pallete_style_frame
        )
        self.pg2_graph_saturation_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2_graph_saturation_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_saturation_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_saturation_frame_box_plot.setObjectName(
            "pg2_graph_saturation_frame_box_plot"
        )
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout(
            self.pg2_graph_saturation_frame_box_plot
        )
        self.horizontalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_49.setSpacing(0)
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.pg2_graph_saturation_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_saturation_frame_box_plot
        )
        self.pg2_graph_saturation_label_box_plot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_saturation_label_box_plot.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_saturation_label_box_plot.setFont(font)
        self.pg2_graph_saturation_label_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_saturation_label_box_plot.setObjectName(
            "pg2_graph_saturation_label_box_plot"
        )
        self.horizontalLayout_49.addWidget(self.pg2_graph_saturation_label_box_plot)
        self.pg2_graph_saturation_spinBox_box_plot = QtWidgets.QSpinBox(
            self.pg2_graph_saturation_frame_box_plot
        )
        self.pg2_graph_saturation_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_saturation_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_saturation_spinBox_box_plot.setMinimum(0)
        self.pg2_graph_saturation_spinBox_box_plot.setMaximum(100)
        self.pg2_graph_saturation_spinBox_box_plot.setProperty("value", 100)
        self.pg2_graph_saturation_spinBox_box_plot.setObjectName(
            "pg2_graph_saturation_spinBox_box_plot"
        )
        self.horizontalLayout_49.addWidget(self.pg2_graph_saturation_spinBox_box_plot)
        self.pg2Layout_verticalLayout_13.addWidget(
            self.pg2_graph_saturation_frame_box_plot
        )
        self.pg2_graph_orientaitno_frame_barplot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2_graph_orientaitno_frame_barplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_orientaitno_frame_barplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_orientaitno_frame_barplot.setObjectName(
            "pg2_graph_orientaitno_frame_barplot"
        )
        self.horizontalLayout_50 = QtWidgets.QHBoxLayout(
            self.pg2_graph_orientaitno_frame_barplot
        )
        self.horizontalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_50.setSpacing(0)
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.pg2_graph_orientation_label_barplot = QtWidgets.QLabel(
            self.pg2_graph_orientaitno_frame_barplot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_orientation_label_barplot.setFont(font)
        self.pg2_graph_orientation_label_barplot.setObjectName(
            "pg2_graph_orientation_label_barplot"
        )
        self.horizontalLayout_50.addWidget(self.pg2_graph_orientation_label_barplot)
        self.pg2_graph_orientaitno_combobox_barplot = QtWidgets.QComboBox(
            self.pg2_graph_orientaitno_frame_barplot
        )
        self.pg2_graph_orientaitno_combobox_barplot.setMinimumSize(QtCore.QSize(80, 0))
        self.pg2_graph_orientaitno_combobox_barplot.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg2_graph_orientaitno_combobox_barplot.setObjectName(
            "pg2_graph_orientaitno_combobox_barplot"
        )
        self.pg2_graph_orientaitno_combobox_barplot.addItem("")
        self.pg2_graph_orientaitno_combobox_barplot.addItem("")
        self.horizontalLayout_50.addWidget(self.pg2_graph_orientaitno_combobox_barplot)
        self.pg2Layout_verticalLayout_13.addWidget(
            self.pg2_graph_orientaitno_frame_barplot
        )
        self.pg2_graph_bar_width_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2_graph_bar_width_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_bar_width_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_bar_width_frame_box_plot.setObjectName(
            "pg2_graph_bar_width_frame_box_plot"
        )
        self.horizontalLayout_86 = QtWidgets.QHBoxLayout(
            self.pg2_graph_bar_width_frame_box_plot
        )
        self.horizontalLayout_86.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_86.setSpacing(0)
        self.horizontalLayout_86.setObjectName("horizontalLayout_86")
        self.pg2_graph_bar_width_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_bar_width_frame_box_plot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_bar_width_label_box_plot.setFont(font)
        self.pg2_graph_bar_width_label_box_plot.setObjectName(
            "pg2_graph_bar_width_label_box_plot"
        )
        self.horizontalLayout_86.addWidget(self.pg2_graph_bar_width_label_box_plot)
        self.pg2_graph_bar_width_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_bar_width_frame_box_plot
        )
        self.pg2_graph_bar_width_spinBox_box_plot.setMinimumSize(QtCore.QSize(50, 0))
        self.pg2_graph_bar_width_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(50, 16777215)
        )
        self.pg2_graph_bar_width_spinBox_box_plot.setDecimals(1)
        self.pg2_graph_bar_width_spinBox_box_plot.setMaximum(20.0)
        self.pg2_graph_bar_width_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_bar_width_spinBox_box_plot.setProperty("value", 0.8)
        self.pg2_graph_bar_width_spinBox_box_plot.setObjectName(
            "pg2_graph_bar_width_spinBox_box_plot"
        )
        self.horizontalLayout_86.addWidget(self.pg2_graph_bar_width_spinBox_box_plot)
        self.pg2Layout_verticalLayout_13.addWidget(
            self.pg2_graph_bar_width_frame_box_plot
        )
        self.pg2_graph_bar_borderwidth_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left_3
        )
        self.pg2_graph_bar_borderwidth_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_bar_borderwidth_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_bar_borderwidth_frame_box_plot.setObjectName(
            "pg2_graph_bar_borderwidth_frame_box_plot"
        )
        self.horizontalLayout_75 = QtWidgets.QHBoxLayout(
            self.pg2_graph_bar_borderwidth_frame_box_plot
        )
        self.horizontalLayout_75.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_75.setSpacing(0)
        self.horizontalLayout_75.setObjectName("horizontalLayout_75")
        self.pg2_graph_bar_borderwidth_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_bar_borderwidth_frame_box_plot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_bar_borderwidth_label_box_plot.setFont(font)
        self.pg2_graph_bar_borderwidth_label_box_plot.setObjectName(
            "pg2_graph_bar_borderwidth_label_box_plot"
        )
        self.horizontalLayout_75.addWidget(
            self.pg2_graph_bar_borderwidth_label_box_plot
        )
        self.pg2_graph_bar_borderwidth_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_bar_borderwidth_frame_box_plot
        )
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setMinimumSize(
            QtCore.QSize(50, 0)
        )
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(50, 16777215)
        )
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setDecimals(1)
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setMaximum(20.0)
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setProperty("value", 0.1)
        self.pg2_graph_bar_borderwidth_spinBox_box_plot.setObjectName(
            "pg2_graph_bar_borderwidth_spinBox_box_plot"
        )
        self.horizontalLayout_75.addWidget(
            self.pg2_graph_bar_borderwidth_spinBox_box_plot
        )
        self.pg2Layout_verticalLayout_13.addWidget(
            self.pg2_graph_bar_borderwidth_frame_box_plot
        )
        spacerItem10 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_13.addItem(spacerItem10)
        self.horizontalLayout_45.addWidget(self.pg_2_box_plot_settings_1_left_3)
        spacerItem11 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_45.addItem(spacerItem11)
        self.pg_2_box_plot_settings_1_right_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1
        )
        self.pg_2_box_plot_settings_1_right_box_plot.setObjectName(
            "pg_2_box_plot_settings_1_right_box_plot"
        )
        self.pg2Layout_verticalLayout_15 = QtWidgets.QVBoxLayout(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg2Layout_verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_15.setObjectName("pg2Layout_verticalLayout_15")
        self.pg2_graph_bar_errwidth_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg2_graph_bar_errwidth_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_bar_errwidth_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_bar_errwidth_frame_box_plot.setObjectName(
            "pg2_graph_bar_errwidth_frame_box_plot"
        )
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout(
            self.pg2_graph_bar_errwidth_frame_box_plot
        )
        self.horizontalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_53.setSpacing(0)
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.pg2_graph_bar_errwidth_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_bar_errwidth_frame_box_plot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_bar_errwidth_label_box_plot.setFont(font)
        self.pg2_graph_bar_errwidth_label_box_plot.setObjectName(
            "pg2_graph_bar_errwidth_label_box_plot"
        )
        self.horizontalLayout_53.addWidget(self.pg2_graph_bar_errwidth_label_box_plot)
        self.pg2_graph_bar_errwidth_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_bar_errwidth_frame_box_plot
        )
        self.pg2_graph_bar_errwidth_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_bar_errwidth_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_bar_errwidth_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_bar_errwidth_spinBox_box_plot.setProperty("value", 0.2)
        self.pg2_graph_bar_errwidth_spinBox_box_plot.setObjectName(
            "pg2_graph_bar_errwidth_spinBox_box_plot"
        )
        self.horizontalLayout_53.addWidget(self.pg2_graph_bar_errwidth_spinBox_box_plot)
        self.pg2Layout_verticalLayout_15.addWidget(
            self.pg2_graph_bar_errwidth_frame_box_plot
        )
        self.pg2_graph_bar_ci_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg2_graph_bar_ci_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_bar_ci_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_bar_ci_frame_box_plot.setObjectName(
            "pg2_graph_bar_ci_frame_box_plot"
        )
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout(
            self.pg2_graph_bar_ci_frame_box_plot
        )
        self.horizontalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.pg2_graph_bar_ci_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_bar_ci_frame_box_plot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_bar_ci_label_box_plot.setFont(font)
        self.pg2_graph_bar_ci_label_box_plot.setObjectName(
            "pg2_graph_bar_ci_label_box_plot"
        )
        self.horizontalLayout_54.addWidget(self.pg2_graph_bar_ci_label_box_plot)
        self.pg2_graph_bar_ci_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_bar_ci_frame_box_plot
        )
        self.pg2_graph_bar_ci_spinBox_box_plot.setMinimumSize(QtCore.QSize(50, 0))
        self.pg2_graph_bar_ci_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(50, 16777215)
        )
        self.pg2_graph_bar_ci_spinBox_box_plot.setDecimals(1)
        self.pg2_graph_bar_ci_spinBox_box_plot.setMaximum(1.0)
        self.pg2_graph_bar_ci_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_bar_ci_spinBox_box_plot.setProperty("value", 1.0)
        self.pg2_graph_bar_ci_spinBox_box_plot.setObjectName(
            "pg2_graph_bar_ci_spinBox_box_plot"
        )
        self.horizontalLayout_54.addWidget(self.pg2_graph_bar_ci_spinBox_box_plot)
        self.pg2Layout_verticalLayout_15.addWidget(self.pg2_graph_bar_ci_frame_box_plot)
        self.pg2_graph_flier_size_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg2_graph_flier_size_frame_box_plot.setStyleSheet("")
        self.pg2_graph_flier_size_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_flier_size_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_flier_size_frame_box_plot.setObjectName(
            "pg2_graph_flier_size_frame_box_plot"
        )
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout(
            self.pg2_graph_flier_size_frame_box_plot
        )
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.pg2_graph_flier_size_label_box_plot_box_plot = QtWidgets.QLabel(
            self.pg2_graph_flier_size_frame_box_plot
        )
        self.pg2_graph_flier_size_label_box_plot_box_plot.setMinimumSize(
            QtCore.QSize(0, 0)
        )
        self.pg2_graph_flier_size_label_box_plot_box_plot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_flier_size_label_box_plot_box_plot.setFont(font)
        self.pg2_graph_flier_size_label_box_plot_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_flier_size_label_box_plot_box_plot.setObjectName(
            "pg2_graph_flier_size_label_box_plot_box_plot"
        )
        self.horizontalLayout_55.addWidget(
            self.pg2_graph_flier_size_label_box_plot_box_plot
        )
        self.pg2_graph_flier_size_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_flier_size_frame_box_plot
        )
        self.pg2_graph_flier_size_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_flier_size_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_flier_size_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_flier_size_spinBox_box_plot.setProperty("value", 0.1)
        self.pg2_graph_flier_size_spinBox_box_plot.setObjectName(
            "pg2_graph_flier_size_spinBox_box_plot"
        )
        self.horizontalLayout_55.addWidget(self.pg2_graph_flier_size_spinBox_box_plot)
        self.pg2Layout_verticalLayout_15.addWidget(
            self.pg2_graph_flier_size_frame_box_plot
        )
        self.pg_2_errorBars_barPlot_bool_checkBox = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg_2_errorBars_barPlot_bool_checkBox.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_errorBars_barPlot_bool_checkBox.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_errorBars_barPlot_bool_checkBox.setObjectName(
            "pg_2_errorBars_barPlot_bool_checkBox"
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.pg_2_errorBars_barPlot_bool_checkBox
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2.setContentsMargins(
            0, 0, 0, 0
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2.setSpacing(0)
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2.setObjectName(
            "pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2"
        )
        self.pg_2_errorBars_barPlot_bool_label = QtWidgets.QLabel(
            self.pg_2_errorBars_barPlot_bool_checkBox
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorBars_barPlot_bool_label.setFont(font)
        self.pg_2_errorBars_barPlot_bool_label.setObjectName(
            "pg_2_errorBars_barPlot_bool_label"
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2.addWidget(
            self.pg_2_errorBars_barPlot_bool_label
        )
        self.pg_2_errorBars_barPlot_bool_checkBox_2 = QtWidgets.QCheckBox(
            self.pg_2_errorBars_barPlot_bool_checkBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorBars_barPlot_bool_checkBox_2.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorBars_barPlot_bool_checkBox_2.setSizePolicy(sizePolicy)
        self.pg_2_errorBars_barPlot_bool_checkBox_2.setMinimumSize(QtCore.QSize(41, 0))
        self.pg_2_errorBars_barPlot_bool_checkBox_2.setText("")
        self.pg_2_errorBars_barPlot_bool_checkBox_2.setChecked(True)
        self.pg_2_errorBars_barPlot_bool_checkBox_2.setObjectName(
            "pg_2_errorBars_barPlot_bool_checkBox_2"
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout_2.addWidget(
            self.pg_2_errorBars_barPlot_bool_checkBox_2
        )
        self.pg2Layout_verticalLayout_15.addWidget(
            self.pg_2_errorBars_barPlot_bool_checkBox
        )
        spacerItem12 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_15.addItem(spacerItem12)
        self.horizontalLayout_45.addWidget(self.pg_2_box_plot_settings_1_right_box_plot)
        self.pg_2_plotwidtget_gridLayout.addWidget(
            self.pg_2_box_plot_settings_1, 0, 0, 1, 1
        )
        self.pg_2_graph_colors_btns_verticalLayout.addWidget(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Bar
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box = QtWidgets.QFrame(
            self.pg_2_general_colors
        )
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box.setMinimumSize(QtCore.QSize(0, 42))
        self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box.setObjectName(
            "pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box"
        )
        self.plotwidtget_gridLayout_9 = QtWidgets.QGridLayout(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box
        )
        self.plotwidtget_gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.plotwidtget_gridLayout_9.setObjectName("plotwidtget_gridLayout_9")
        self.pg_2_box_plot_settings = QtWidgets.QFrame(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box
        )
        self.pg_2_box_plot_settings.setObjectName("pg_2_box_plot_settings")
        self.horizontalLayout_76 = QtWidgets.QHBoxLayout(self.pg_2_box_plot_settings)
        self.horizontalLayout_76.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.pg_2_box_plot_settings_1_left = QtWidgets.QFrame(
            self.pg_2_box_plot_settings
        )
        self.pg_2_box_plot_settings_1_left.setObjectName(
            "pg_2_box_plot_settings_1_left"
        )
        self.pg2Layout_verticalLayout_20 = QtWidgets.QVBoxLayout(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg2Layout_verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_20.setObjectName("pg2Layout_verticalLayout_20")
        self.pg2_graph_boxplot_pallete_style_frame_ = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg2_graph_boxplot_pallete_style_frame_.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_boxplot_pallete_style_frame_.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_boxplot_pallete_style_frame_.setObjectName(
            "pg2_graph_boxplot_pallete_style_frame_"
        )
        self.horizontalLayout_77 = QtWidgets.QHBoxLayout(
            self.pg2_graph_boxplot_pallete_style_frame_
        )
        self.horizontalLayout_77.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_77.setObjectName("horizontalLayout_77")
        self.pg2Layout_verticalLayout_20.addWidget(
            self.pg2_graph_boxplot_pallete_style_frame_
        )
        self.pg_2_color_graph_frame_box_plot_2 = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg_2_color_graph_frame_box_plot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_color_graph_frame_box_plot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_color_graph_frame_box_plot_2.setObjectName(
            "pg_2_color_graph_frame_box_plot_2"
        )
        self.horizontalLayout_78 = QtWidgets.QHBoxLayout(
            self.pg_2_color_graph_frame_box_plot_2
        )
        self.horizontalLayout_78.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_78.setObjectName("horizontalLayout_78")
        self.pg2Layout_verticalLayout_20.addWidget(
            self.pg_2_color_graph_frame_box_plot_2
        )
        self.pg_2_graph_width_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg_2_graph_width_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_graph_width_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_graph_width_frame_box_plot.setObjectName(
            "pg_2_graph_width_frame_box_plot"
        )
        self.horizontalLayout_79 = QtWidgets.QHBoxLayout(
            self.pg_2_graph_width_frame_box_plot
        )
        self.horizontalLayout_79.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_79.setObjectName("horizontalLayout_79")
        self.pg2_graph_width_label_box_plot = QtWidgets.QLabel(
            self.pg_2_graph_width_frame_box_plot
        )
        self.pg2_graph_width_label_box_plot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_width_label_box_plot.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_width_label_box_plot.setFont(font)
        self.pg2_graph_width_label_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_width_label_box_plot.setObjectName(
            "pg2_graph_width_label_box_plot"
        )
        self.horizontalLayout_79.addWidget(self.pg2_graph_width_label_box_plot)
        self.pg2_graph_width_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg_2_graph_width_frame_box_plot
        )
        self.pg2_graph_width_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_width_spinBox_box_plot.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_graph_width_spinBox_box_plot.setProperty("value", 0.15)
        self.pg2_graph_width_spinBox_box_plot.setObjectName(
            "pg2_graph_width_spinBox_box_plot"
        )
        self.horizontalLayout_79.addWidget(self.pg2_graph_width_spinBox_box_plot)
        self.pg2Layout_verticalLayout_20.addWidget(self.pg_2_graph_width_frame_box_plot)
        self.pg2_graph_boxplot_orientation_frame = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg2_graph_boxplot_orientation_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_boxplot_orientation_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_boxplot_orientation_frame.setObjectName(
            "pg2_graph_boxplot_orientation_frame"
        )
        self.horizontalLayout_80 = QtWidgets.QHBoxLayout(
            self.pg2_graph_boxplot_orientation_frame
        )
        self.horizontalLayout_80.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_80.setSpacing(7)
        self.horizontalLayout_80.setObjectName("horizontalLayout_80")
        self.pg2_graph_orientation_label_boxplot = QtWidgets.QLabel(
            self.pg2_graph_boxplot_orientation_frame
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_orientation_label_boxplot.setFont(font)
        self.pg2_graph_orientation_label_boxplot.setObjectName(
            "pg2_graph_orientation_label_boxplot"
        )
        self.horizontalLayout_80.addWidget(self.pg2_graph_orientation_label_boxplot)
        self.pg_2_graph_boxplot_orientation_combobox = QtWidgets.QComboBox(
            self.pg2_graph_boxplot_orientation_frame
        )
        self.pg_2_graph_boxplot_orientation_combobox.setMinimumSize(QtCore.QSize(80, 0))
        self.pg_2_graph_boxplot_orientation_combobox.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg_2_graph_boxplot_orientation_combobox.setObjectName(
            "pg_2_graph_boxplot_orientation_combobox"
        )
        self.pg_2_graph_boxplot_orientation_combobox.addItem("")
        self.pg_2_graph_boxplot_orientation_combobox.addItem("")
        self.horizontalLayout_80.addWidget(self.pg_2_graph_boxplot_orientation_combobox)
        self.pg2Layout_verticalLayout_20.addWidget(
            self.pg2_graph_boxplot_orientation_frame
        )
        self.pg2_graph_saturation_frame_box_plot_2 = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_left
        )
        self.pg2_graph_saturation_frame_box_plot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_saturation_frame_box_plot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_saturation_frame_box_plot_2.setObjectName(
            "pg2_graph_saturation_frame_box_plot_2"
        )
        self.horizontalLayout_81 = QtWidgets.QHBoxLayout(
            self.pg2_graph_saturation_frame_box_plot_2
        )
        self.horizontalLayout_81.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_81.setSpacing(7)
        self.horizontalLayout_81.setObjectName("horizontalLayout_81")
        self.pg2_graph_saturation_label_box_plot_2 = QtWidgets.QLabel(
            self.pg2_graph_saturation_frame_box_plot_2
        )
        self.pg2_graph_saturation_label_box_plot_2.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_saturation_label_box_plot_2.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_saturation_label_box_plot_2.setFont(font)
        self.pg2_graph_saturation_label_box_plot_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_saturation_label_box_plot_2.setObjectName(
            "pg2_graph_saturation_label_box_plot_2"
        )
        self.horizontalLayout_81.addWidget(self.pg2_graph_saturation_label_box_plot_2)
        self.pg2_graph_saturation_spinBox_box_plot_2 = QtWidgets.QSpinBox(
            self.pg2_graph_saturation_frame_box_plot_2
        )
        self.pg2_graph_saturation_spinBox_box_plot_2.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_saturation_spinBox_box_plot_2.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_saturation_spinBox_box_plot_2.setMinimum(0)
        self.pg2_graph_saturation_spinBox_box_plot_2.setMaximum(100)
        self.pg2_graph_saturation_spinBox_box_plot_2.setProperty("value", 100)
        self.pg2_graph_saturation_spinBox_box_plot_2.setObjectName(
            "pg2_graph_saturation_spinBox_box_plot_2"
        )
        self.horizontalLayout_81.addWidget(self.pg2_graph_saturation_spinBox_box_plot_2)
        self.pg2Layout_verticalLayout_20.addWidget(
            self.pg2_graph_saturation_frame_box_plot_2
        )
        spacerItem13 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_20.addItem(spacerItem13)
        self.horizontalLayout_76.addWidget(self.pg_2_box_plot_settings_1_left)
        spacerItem14 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_76.addItem(spacerItem14)
        self.pg_2_box_plot_settings_1_right_box_plot_2 = QtWidgets.QFrame(
            self.pg_2_box_plot_settings
        )
        self.pg_2_box_plot_settings_1_right_box_plot_2.setObjectName(
            "pg_2_box_plot_settings_1_right_box_plot_2"
        )
        self.pg2Layout_verticalLayout_21 = QtWidgets.QVBoxLayout(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg2Layout_verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.pg2Layout_verticalLayout_21.setObjectName("pg2Layout_verticalLayout_21")
        self.pg2_graph_index_frame_boxplot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg2_graph_index_frame_boxplot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_index_frame_boxplot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_index_frame_boxplot.setObjectName(
            "pg2_graph_index_frame_boxplot"
        )
        self.horizontalLayout_82 = QtWidgets.QHBoxLayout(
            self.pg2_graph_index_frame_boxplot
        )
        self.horizontalLayout_82.setContentsMargins(0, 0, 11, 0)
        self.horizontalLayout_82.setObjectName("horizontalLayout_82")
        self.pg2Layout_verticalLayout_21.addWidget(self.pg2_graph_index_frame_boxplot)
        self.pg_2_graph_border_color_frame_box_plot_2 = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg_2_graph_border_color_frame_box_plot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_graph_border_color_frame_box_plot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_graph_border_color_frame_box_plot_2.setObjectName(
            "pg_2_graph_border_color_frame_box_plot_2"
        )
        self.horizontalLayout_83 = QtWidgets.QHBoxLayout(
            self.pg_2_graph_border_color_frame_box_plot_2
        )
        self.horizontalLayout_83.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_83.setObjectName("horizontalLayout_83")
        self.pg2Layout_verticalLayout_21.addWidget(
            self.pg_2_graph_border_color_frame_box_plot_2
        )
        self.pg2_graph_line_width_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg2_graph_line_width_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_line_width_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_line_width_frame_box_plot.setObjectName(
            "pg2_graph_line_width_frame_box_plot"
        )
        self.horizontalLayout_84 = QtWidgets.QHBoxLayout(
            self.pg2_graph_line_width_frame_box_plot
        )
        self.horizontalLayout_84.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_84.setSpacing(7)
        self.horizontalLayout_84.setObjectName("horizontalLayout_84")
        self.pg2_graph_line_width_label_box_plot = QtWidgets.QLabel(
            self.pg2_graph_line_width_frame_box_plot
        )
        self.pg2_graph_line_width_label_box_plot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_line_width_label_box_plot.setMaximumSize(
            QtCore.QSize(16777215, 10)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_line_width_label_box_plot.setFont(font)
        self.pg2_graph_line_width_label_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_line_width_label_box_plot.setObjectName(
            "pg2_graph_line_width_label_box_plot"
        )
        self.horizontalLayout_84.addWidget(self.pg2_graph_line_width_label_box_plot)
        self.pg2_graph_line_width_spinBox_box_plot = QtWidgets.QSpinBox(
            self.pg2_graph_line_width_frame_box_plot
        )
        self.pg2_graph_line_width_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_line_width_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_line_width_spinBox_box_plot.setMinimum(0)
        self.pg2_graph_line_width_spinBox_box_plot.setMaximum(100)
        self.pg2_graph_line_width_spinBox_box_plot.setProperty("value", 2)
        self.pg2_graph_line_width_spinBox_box_plot.setObjectName(
            "pg2_graph_line_width_spinBox_box_plot"
        )
        self.horizontalLayout_84.addWidget(self.pg2_graph_line_width_spinBox_box_plot)
        self.pg2Layout_verticalLayout_21.addWidget(
            self.pg2_graph_line_width_frame_box_plot
        )
        self.pg2_graph_cap_size_frame_box_plot = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg2_graph_cap_size_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_cap_size_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_cap_size_frame_box_plot.setObjectName(
            "pg2_graph_cap_size_frame_box_plot"
        )
        self.horizontalLayout_85 = QtWidgets.QHBoxLayout(
            self.pg2_graph_cap_size_frame_box_plot
        )
        self.horizontalLayout_85.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_85.setSpacing(7)
        self.horizontalLayout_85.setObjectName("horizontalLayout_85")
        self.pg2_graph_cap_size_label_box_plot_box_plot = QtWidgets.QLabel(
            self.pg2_graph_cap_size_frame_box_plot
        )
        self.pg2_graph_cap_size_label_box_plot_box_plot.setMinimumSize(
            QtCore.QSize(0, 0)
        )
        self.pg2_graph_cap_size_label_box_plot_box_plot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_cap_size_label_box_plot_box_plot.setFont(font)
        self.pg2_graph_cap_size_label_box_plot_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.pg2_graph_cap_size_label_box_plot_box_plot.setObjectName(
            "pg2_graph_cap_size_label_box_plot_box_plot"
        )
        self.horizontalLayout_85.addWidget(
            self.pg2_graph_cap_size_label_box_plot_box_plot
        )
        self.pg2_graph_cap_size_spinBox_box_plot = QtWidgets.QDoubleSpinBox(
            self.pg2_graph_cap_size_frame_box_plot
        )
        self.pg2_graph_cap_size_spinBox_box_plot.setDecimals(1)
        self.pg2_graph_cap_size_spinBox_box_plot.setSingleStep(0.1)
        self.pg2_graph_cap_size_spinBox_box_plot.setProperty("value", 1.0)
        self.pg2_graph_cap_size_spinBox_box_plot.setObjectName(
            "pg2_graph_cap_size_spinBox_box_plot"
        )
        self.horizontalLayout_85.addWidget(self.pg2_graph_cap_size_spinBox_box_plot)
        self.pg2Layout_verticalLayout_21.addWidget(
            self.pg2_graph_cap_size_frame_box_plot
        )
        self.pg2_boxPlot_bool_frame = QtWidgets.QFrame(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.pg2_boxPlot_bool_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.pg2_boxPlot_bool_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.pg2_boxPlot_bool_frame.setObjectName("pg2_boxPlot_bool_frame")
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout = QtWidgets.QHBoxLayout(
            self.pg2_boxPlot_bool_frame
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout.setContentsMargins(
            0, 0, 0, 0
        )
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout.setSpacing(0)
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout.setObjectName(
            "pg_2_frameBoxPlot_errorbarsBool_horizontalLayout"
        )
        self.pg_2_errorBars_bool_label = QtWidgets.QLabel(self.pg2_boxPlot_bool_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg_2_errorBars_bool_label.setFont(font)
        self.pg_2_errorBars_bool_label.setObjectName("pg_2_errorBars_bool_label")
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout.addWidget(
            self.pg_2_errorBars_bool_label
        )
        self.pg_2_errorBars_bool_checkBox = QtWidgets.QCheckBox(
            self.pg2_boxPlot_bool_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_errorBars_bool_checkBox.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_errorBars_bool_checkBox.setSizePolicy(sizePolicy)
        self.pg_2_errorBars_bool_checkBox.setMinimumSize(QtCore.QSize(41, 0))
        self.pg_2_errorBars_bool_checkBox.setText("")
        self.pg_2_errorBars_bool_checkBox.setChecked(True)
        self.pg_2_errorBars_bool_checkBox.setObjectName("pg_2_errorBars_bool_checkBox")
        self.pg_2_frameBoxPlot_errorbarsBool_horizontalLayout.addWidget(
            self.pg_2_errorBars_bool_checkBox
        )
        self.pg2Layout_verticalLayout_21.addWidget(self.pg2_boxPlot_bool_frame)
        spacerItem15 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.pg2Layout_verticalLayout_21.addItem(spacerItem15)
        self.horizontalLayout_76.addWidget(
            self.pg_2_box_plot_settings_1_right_box_plot_2
        )
        self.plotwidtget_gridLayout_9.addWidget(self.pg_2_box_plot_settings, 0, 0, 1, 1)
        self.pg_2_graph_colors_btns_verticalLayout.addWidget(
            self.pg_2_REPLACE_WITH_SPECIFIC_WIDGET_Box
        )
        self.pg_2_gridLayout_16.addWidget(self.pg_2_general_colors, 1, 0, 1, 1)
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.pg_2_graph_colors_groupBox, 4, 0, 1, 1
        )
        self.frame = QtWidgets.QFrame(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setObjectName("frame")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1 = (
            QtWidgets.QGridLayout(self.frame)
        )
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.setSpacing(0)
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.setObjectName(
            "widget_graph_visualizer_scroll_area_2_contents_grid_layout_1"
        )
        self.pg2_load_preset_btn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_load_preset_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_load_preset_btn.setSizePolicy(sizePolicy)
        self.pg2_load_preset_btn.setMinimumSize(QtCore.QSize(50, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_load_preset_btn.setFont(font)
        self.pg2_load_preset_btn.setObjectName("pg2_load_preset_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.addWidget(
            self.pg2_load_preset_btn, 0, 0, 1, 1
        )
        self.pg2_save_preset_btn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_save_preset_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_save_preset_btn.setSizePolicy(sizePolicy)
        self.pg2_save_preset_btn.setMinimumSize(QtCore.QSize(50, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_save_preset_btn.setFont(font)
        self.pg2_save_preset_btn.setObjectName("pg2_save_preset_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.addWidget(
            self.pg2_save_preset_btn, 0, 1, 1, 1
        )
        self.pg2_save_as_preset_btn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_save_as_preset_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_save_as_preset_btn.setSizePolicy(sizePolicy)
        self.pg2_save_as_preset_btn.setMinimumSize(QtCore.QSize(50, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_save_as_preset_btn.setFont(font)
        self.pg2_save_as_preset_btn.setObjectName("pg2_save_as_preset_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.addWidget(
            self.pg2_save_as_preset_btn, 1, 0, 1, 1
        )
        self.pg2_clear_preset_btn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_clear_preset_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_clear_preset_btn.setSizePolicy(sizePolicy)
        self.pg2_clear_preset_btn.setMinimumSize(QtCore.QSize(50, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_clear_preset_btn.setFont(font)
        self.pg2_clear_preset_btn.setObjectName("pg2_clear_preset_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_grid_layout_1.addWidget(
            self.pg2_clear_preset_btn, 1, 1, 1, 1
        )
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.frame, 0, 0, 1, 1
        )
        self.pg_2_plot_parameteres_scrollArea = QtWidgets.QScrollArea(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_plot_parameteres_scrollArea.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_plot_parameteres_scrollArea.setSizePolicy(sizePolicy)
        self.pg_2_plot_parameteres_scrollArea.setMinimumSize(QtCore.QSize(0, 120))
        self.pg_2_plot_parameteres_scrollArea.setMaximumSize(
            QtCore.QSize(16777215, 120)
        )
        self.pg_2_plot_parameteres_scrollArea.setStyleSheet("")
        self.pg_2_plot_parameteres_scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.pg_2_plot_parameteres_scrollArea.setWidgetResizable(True)
        self.pg_2_plot_parameteres_scrollArea.setObjectName(
            "pg_2_plot_parameteres_scrollArea"
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.pg_2_plot_parameteres_scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, 636, 120)
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContents.setMinimumSize(
            QtCore.QSize(0, 120)
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContents.setMaximumSize(
            QtCore.QSize(16777215, 120)
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContents.setStyleSheet(
            "QWidget#pg_2_plot_parameteres_scrollAreaWidgetContents{\n"
            "border-radius: 5px; \n"
            "background-color: rgb(120, 120,120);\n"
            "\n"
            "}"
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContents.setObjectName(
            "pg_2_plot_parameteres_scrollAreaWidgetContents"
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2 = (
            QtWidgets.QHBoxLayout(self.pg_2_plot_parameteres_scrollAreaWidgetContents)
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2.setContentsMargins(
            0, 7, 0, 13
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2.setSpacing(
            3
        )
        self.pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2.setObjectName(
            "pg_2_plot_parameteres_scrollAreaWidgetContentshorizontalLayout_2"
        )
        self.pg_2_plot_parameteres_scrollArea.setWidget(
            self.pg_2_plot_parameteres_scrollAreaWidgetContents
        )
        self.gridLayoutwidget_graph_visualizer_scroll_area_2_contents.addWidget(
            self.pg_2_plot_parameteres_scrollArea, 1, 0, 1, 1
        )
        self.widget_graph_visualizer_scroll_area_2.setWidget(
            self.widget_graph_visualizer_scroll_area_2_contents
        )
        self.pg_2_gridLayout_8.addWidget(
            self.widget_graph_visualizer_scroll_area_2, 1, 0, 1, 1
        )
        self.pg_2_PlotParameteres_label = QtWidgets.QLabel(
            self.pg_2_widget_graph_visualizer
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_PlotParameteres_label.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_PlotParameteres_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.pg_2_PlotParameteres_label.setFont(font)
        self.pg_2_PlotParameteres_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.pg_2_PlotParameteres_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg_2_PlotParameteres_label.setObjectName("pg_2_PlotParameteres_label")
        self.pg_2_gridLayout_8.addWidget(self.pg_2_PlotParameteres_label, 0, 0, 1, 1)
        self.FrameOfOutPutButtons = QtWidgets.QFrame(self.pg_2_widget_graph_visualizer)
        self.FrameOfOutPutButtons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.FrameOfOutPutButtons.setObjectName("FrameOfOutPutButtons")
        self.widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1 = (
            QtWidgets.QHBoxLayout(self.FrameOfOutPutButtons)
        )
        self.widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1.setObjectName(
            "widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1"
        )
        self.pg2_plot_btn = QtWidgets.QPushButton(self.FrameOfOutPutButtons)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pg2_plot_btn.sizePolicy().hasHeightForWidth())
        self.pg2_plot_btn.setSizePolicy(sizePolicy)
        self.pg2_plot_btn.setMinimumSize(QtCore.QSize(40, 44))
        self.pg2_plot_btn.setObjectName("pg2_plot_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1.addWidget(
            self.pg2_plot_btn
        )
        self.pg2_savegraph_btn = QtWidgets.QPushButton(self.FrameOfOutPutButtons)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_savegraph_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_savegraph_btn.setSizePolicy(sizePolicy)
        self.pg2_savegraph_btn.setMinimumSize(QtCore.QSize(40, 44))
        self.pg2_savegraph_btn.setObjectName("pg2_savegraph_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1.addWidget(
            self.pg2_savegraph_btn
        )
        self.pg2_clear_btn = QtWidgets.QPushButton(self.FrameOfOutPutButtons)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg2_clear_btn.sizePolicy().hasHeightForWidth()
        )
        self.pg2_clear_btn.setSizePolicy(sizePolicy)
        self.pg2_clear_btn.setMinimumSize(QtCore.QSize(40, 44))
        self.pg2_clear_btn.setObjectName("pg2_clear_btn")
        self.widget_graph_visualizer_scroll_area_2_contents_horizontal_layout_1.addWidget(
            self.pg2_clear_btn
        )
        self.pg_2_gridLayout_8.addWidget(self.FrameOfOutPutButtons, 2, 0, 1, 1)
        self.statistical_analysis_widget = QtWidgets.QWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.statistical_analysis_widget.sizePolicy().hasHeightForWidth()
        )
        self.statistical_analysis_widget.setSizePolicy(sizePolicy)
        self.statistical_analysis_widget.setObjectName("statistical_analysis_widget")
        self.statistical_analysis_widget_grid = QtWidgets.QGridLayout(
            self.statistical_analysis_widget
        )
        self.statistical_analysis_widget_grid.setContentsMargins(0, 0, 0, 0)
        self.statistical_analysis_widget_grid.setObjectName(
            "statistical_analysis_widget_grid"
        )
        self.pg_2_scrollArea_rightside = QtWidgets.QScrollArea(
            self.statistical_analysis_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_scrollArea_rightside.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_scrollArea_rightside.setSizePolicy(sizePolicy)
        self.pg_2_scrollArea_rightside.setWidgetResizable(True)
        self.pg_2_scrollArea_rightside.setObjectName("pg_2_scrollArea_rightside")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 448, 1200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.pg_2_gridLayout_20 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.pg_2_gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.pg_2_gridLayout_20.setSpacing(6)
        self.pg_2_gridLayout_20.setObjectName("pg_2_gridLayout_20")
        self.statistical_analysis_scroll_Area = QtWidgets.QScrollArea(
            self.scrollAreaWidgetContents
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.statistical_analysis_scroll_Area.sizePolicy().hasHeightForWidth()
        )
        self.statistical_analysis_scroll_Area.setSizePolicy(sizePolicy)
        self.statistical_analysis_scroll_Area.setMinimumSize(QtCore.QSize(0, 1200))
        self.statistical_analysis_scroll_Area.setWidgetResizable(True)
        self.statistical_analysis_scroll_Area.setObjectName(
            "statistical_analysis_scroll_Area"
        )
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 446, 1198))
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pg_2_statistical_analysis_groupBox = QtWidgets.QGroupBox(
            self.scrollAreaWidgetContents_7
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pg_2_statistical_analysis_groupBox.setFont(font)
        self.pg_2_statistical_analysis_groupBox.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg_2_statistical_analysis_groupBox.setObjectName(
            "pg_2_statistical_analysis_groupBox"
        )
        self.pg_2_gridLayout_3 = QtWidgets.QGridLayout(
            self.pg_2_statistical_analysis_groupBox
        )
        self.pg_2_gridLayout_3.setContentsMargins(-1, 20, -1, -1)
        self.pg_2_gridLayout_3.setObjectName("pg_2_gridLayout_3")
        self.pg_2_CollumnAnalysis_text = QtWidgets.QLabel(
            self.pg_2_statistical_analysis_groupBox
        )
        self.pg_2_CollumnAnalysis_text.setMinimumSize(QtCore.QSize(0, 28))
        self.pg_2_CollumnAnalysis_text.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pg_2_CollumnAnalysis_text.setFont(font)
        self.pg_2_CollumnAnalysis_text.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg_2_CollumnAnalysis_text.setObjectName("pg_2_CollumnAnalysis_text")
        self.pg_2_gridLayout_3.addWidget(self.pg_2_CollumnAnalysis_text, 0, 0, 1, 1)
        self.pg_2_statisticalAnalysis_combobox = QtWidgets.QComboBox(
            self.pg_2_statistical_analysis_groupBox
        )
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pg_2_statisticalAnalysis_combobox.setFont(font)
        self.pg_2_statisticalAnalysis_combobox.setObjectName(
            "pg_2_statisticalAnalysis_combobox"
        )
        self.pg_2_statisticalAnalysis_combobox.addItem("")
        self.pg_2_statisticalAnalysis_combobox.addItem("")
        self.pg_2_statisticalAnalysis_combobox.addItem("")
        self.pg_2_gridLayout_3.addWidget(
            self.pg_2_statisticalAnalysis_combobox, 0, 1, 1, 1
        )
        self.pg_2_textBrowser = QtWidgets.QTextBrowser(
            self.pg_2_statistical_analysis_groupBox
        )
        self.pg_2_textBrowser.setObjectName("pg_2_textBrowser")
        self.pg_2_gridLayout_3.addWidget(self.pg_2_textBrowser, 1, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.pg_2_statistical_analysis_groupBox)
        self.Annotations_GroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_7)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Annotations_GroupBox.setFont(font)
        self.Annotations_GroupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Annotations_GroupBox.setObjectName("Annotations_GroupBox")
        self.pg_2_gridLayout_4 = QtWidgets.QGridLayout(self.Annotations_GroupBox)
        self.pg_2_gridLayout_4.setObjectName("pg_2_gridLayout_4")
        self.pg_2_statistical_analysis_source_frame = QtWidgets.QFrame(
            self.Annotations_GroupBox
        )
        self.pg_2_statistical_analysis_source_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_statistical_analysis_source_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_statistical_analysis_source_frame.setObjectName(
            "pg_2_statistical_analysis_source_frame"
        )
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.pg_2_statistical_analysis_source_frame
        )
        self.verticalLayout_4.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pg_2_Source_Data_btn = QtWidgets.QPushButton(
            self.pg_2_statistical_analysis_source_frame
        )
        self.pg_2_Source_Data_btn.setObjectName("pg_2_Source_Data_btn")
        self.verticalLayout_4.addWidget(self.pg_2_Source_Data_btn)
        self.pg_2_Destination_Data_btn = QtWidgets.QPushButton(
            self.pg_2_statistical_analysis_source_frame
        )
        self.pg_2_Destination_Data_btn.setObjectName("pg_2_Destination_Data_btn")
        self.verticalLayout_4.addWidget(self.pg_2_Destination_Data_btn)
        self.pg_2_Add_Link_btn = QtWidgets.QPushButton(
            self.pg_2_statistical_analysis_source_frame
        )
        self.pg_2_Add_Link_btn.setObjectName("pg_2_Add_Link_btn")
        self.verticalLayout_4.addWidget(self.pg_2_Add_Link_btn)
        self.pg_2_gridLayout_4.addWidget(
            self.pg_2_statistical_analysis_source_frame, 0, 0, 1, 1
        )
        self.Pg2_Annotatations_listView = QtWidgets.QListView(self.Annotations_GroupBox)
        self.Pg2_Annotatations_listView.setObjectName("Pg2_Annotatations_listView")
        self.pg_2_gridLayout_4.addWidget(self.Pg2_Annotatations_listView, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.Annotations_GroupBox)
        self.statistical_analysis_scroll_Area.setWidget(self.scrollAreaWidgetContents_7)
        self.pg_2_gridLayout_20.addWidget(
            self.statistical_analysis_scroll_Area, 0, 0, 1, 1
        )
        self.pg_2_scrollArea_rightside.setWidget(self.scrollAreaWidgetContents)
        self.statistical_analysis_widget_grid.addWidget(
            self.pg_2_scrollArea_rightside, 1, 0, 1, 1
        )
        self.pg_2_StatisticalAnalaysis_label = QtWidgets.QLabel(
            self.statistical_analysis_widget
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pg_2_StatisticalAnalaysis_label.sizePolicy().hasHeightForWidth()
        )
        self.pg_2_StatisticalAnalaysis_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.pg_2_StatisticalAnalaysis_label.setFont(font)
        self.pg_2_StatisticalAnalaysis_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.pg_2_StatisticalAnalaysis_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.pg_2_StatisticalAnalaysis_label.setObjectName(
            "pg_2_StatisticalAnalaysis_label"
        )
        self.statistical_analysis_widget_grid.addWidget(
            self.pg_2_StatisticalAnalaysis_label, 0, 0, 1, 1
        )
        self.horizontalLayout.addWidget(self.splitter_3)

        self.retranslateUi(Plot_tools_widget)
        QtCore.QMetaObject.connectSlotsByName(Plot_tools_widget)

    def retranslateUi(self, Plot_tools_widget):
        _translate = QtCore.QCoreApplication.translate
        Plot_tools_widget.setWindowTitle(_translate("Plot_tools_widget", "Form"))
        self.pg2_graph_order.setText(_translate("Plot_tools_widget", "Graph Order"))
        self.pg2_add_plot_button.setText(_translate("Plot_tools_widget", "Add Plot"))
        self.pg2_remove_plot_button.setText(
            _translate("Plot_tools_widget", "Remove Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            0, _translate("Plot_tools_widget", "Box Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            1, _translate("Plot_tools_widget", "Bar Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            2, _translate("Plot_tools_widget", "Dot Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            3, _translate("Plot_tools_widget", "Violin Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            4, _translate("Plot_tools_widget", "Histogram Pot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            5, _translate("Plot_tools_widget", "Strip Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            6, _translate("Plot_tools_widget", "Swarm Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            7, _translate("Plot_tools_widget", "Density Plot")
        )
        self.pg2_graph_type_comboBox.setItemText(
            8, _translate("Plot_tools_widget", "Cross Bar Plot")
        )
        self.pg2_graph_type.setText(_translate("Plot_tools_widget", "Graph Type: "))
        self.groupBox_ErrorBarsPg2.setTitle(
            _translate("Plot_tools_widget", "Error bars")
        )
        self.pg_2_errorbar_basic_settings.setTitle(
            _translate("Plot_tools_widget", "Basic")
        )
        self.pg_2_error_bar_botom_style_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Left & Right")
        )
        self.pg_2_error_bar_botom_style_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Left")
        )
        self.pg_2_error_bar_botom_style_combobox.setItemText(
            2, _translate("Plot_tools_widget", "Right")
        )
        self.pg_2_error_bar_top_thickness_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Left & Right")
        )
        self.pg_2_error_bar_top_thickness_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Left")
        )
        self.pg_2_error_bar_top_thickness_combobox.setItemText(
            2, _translate("Plot_tools_widget", "Right")
        )
        self.pg_2_error_bar_opacity_label.setText(
            _translate("Plot_tools_widget", "Opacity")
        )
        self.pg_2_error_bar_botom_style_label.setText(
            _translate("Plot_tools_widget", "Botom Style")
        )
        self.pg_2_error_bar_line_width_label.setText(
            _translate("Plot_tools_widget", "Line Width")
        )
        self.pg_2_error_bar_cap_thickness_label.setText(
            _translate("Plot_tools_widget", "Cap Thickness")
        )
        self.pg_2_error_bar_cap_size_label.setText(
            _translate("Plot_tools_widget", "Cap Size")
        )
        self.pg_2_error_bar_top_thickness_label.setText(
            _translate("Plot_tools_widget", "Top Style")
        )
        self.pg_2_error_bar_cap_thickness_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Line")
        )
        self.pg_2_error_bar_cap_thickness_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Line & Edges")
        )
        self.pg_2_error_bar_color_label.setText(
            _translate("Plot_tools_widget", "Color")
        )
        self.pg_2_error_bar_cap_style_label.setText(
            _translate("Plot_tools_widget", "Cap Style")
        )
        self.pg_2_errorbar_extra_settings.setTitle(
            _translate("Plot_tools_widget", "Extra")
        )
        self.pg_2_errorbar_dashed_line_style_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Square")
        )
        self.pg_2_errorbar_dashed_line_style_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Round")
        )
        self.pg_2_errorbar_dashed_line_style_combobox.setItemText(
            2, _translate("Plot_tools_widget", "E. Square")
        )
        self.pg_2_errorbar_dashed_line_separation_label.setText(
            _translate("Plot_tools_widget", "Dashed Line Separation")
        )
        self.pg_2_errorbar_join_style_label.setText(
            _translate("Plot_tools_widget", "Join Style")
        )
        self.pg_2_errorbar_join_style_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Triangle")
        )
        self.pg_2_errorbar_join_style_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Round")
        )
        self.pg_2_errorbar_join_style_combobox.setItemText(
            2, _translate("Plot_tools_widget", "Bevel")
        )
        self.pg_2_errorbar_dashed_cap_style_label.setText(
            _translate("Plot_tools_widget", "Dashed Cap Style")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            0, _translate("Plot_tools_widget", "None")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            1, _translate("Plot_tools_widget", "-")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            2, _translate("Plot_tools_widget", "--")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            3, _translate("Plot_tools_widget", "-.")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            4, _translate("Plot_tools_widget", ":")
        )
        self.pg_2_errorbar_line_style_combobox.setItemText(
            5, _translate("Plot_tools_widget", "...")
        )
        self.pg_2_errorbar_dashed_cap_style_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Square")
        )
        self.pg_2_errorbar_dashed_cap_style_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Round")
        )
        self.pg_2_errorbar_dashed_cap_style_combobox.setItemText(
            2, _translate("Plot_tools_widget", "Extended Square")
        )
        self.pg_2_errorbar_dashed_line_style_label.setText(
            _translate("Plot_tools_widget", "Dashed Line Style")
        )
        self.pg_2_errorbar_line_style_label.setText(
            _translate("Plot_tools_widget", "Line Style")
        )
        self.max_width_label.setText(
            _translate("Plot_tools_widget", "Resolution (dpi)")
        )
        self.min_height_label.setText(_translate("Plot_tools_widget", "Plot Height"))
        self.max_height_label.setText(_translate("Plot_tools_widget", "Plot Width"))
        self.min_width_label.setText(_translate("Plot_tools_widget", "Dimentions"))
        self.dimations_comboBox.setItemText(
            0, _translate("Plot_tools_widget", "Pixels")
        )
        self.dimations_comboBox.setItemText(
            1, _translate("Plot_tools_widget", "Inches")
        )
        self.dimations_comboBox.setItemText(2, _translate("Plot_tools_widget", "cm"))
        self.brokenaxis_label.setText(_translate("Plot_tools_widget", "Broken axis"))
        self.brokenaxis_y_label.setText(_translate("Plot_tools_widget", "Y axis"))
        self.brokenaxis_x_label.setText(_translate("Plot_tools_widget", "X axis"))
        self.pg2_general_attributes_groupBox.setTitle(
            _translate("Plot_tools_widget", "General attributes")
        )
        self.pg2_graph_x_axis_label.setText(
            _translate("Plot_tools_widget", "X axis label")
        )
        self.pg2_graph_title.setText(_translate("Plot_tools_widget", "Title"))
        self.pg2_graph_y_axis_label.setText(
            _translate("Plot_tools_widget", "Y axis label")
        )
        self.label.setText(_translate("Plot_tools_widget", "Theme"))
        self.pg_2_graph_colors_groupBox.setTitle(
            _translate("Plot_tools_widget", "Graph Colors")
        )
        self.pg2_graph_visulaizer_pallets.setText(
            _translate("Plot_tools_widget", "Pallets")
        )
        self.pg2_graph_visulaizer_hide_item.setText(
            _translate("Plot_tools_widget", "Colorblind\n" "Palletes")
        )
        self.pg2_graph_border_width_label_swarmplot.setText(
            _translate("Plot_tools_widget", "Border width")
        )
        self.pg2_graph_size_label_swarmplot.setText(
            _translate("Plot_tools_widget", "Size")
        )
        self.pg2_graph_orientation_label_swarmplot.setText(
            _translate("Plot_tools_widget", "Orientation")
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.setItemText(
            0, _translate("Plot_tools_widget", "Vertical")
        )
        self.pg2_graph_orientaitno_combobox_swarmplot.setItemText(
            1, _translate("Plot_tools_widget", "Horizontal")
        )
        self.pg2_graph_border_width_label_violinplot.setText(
            _translate("Plot_tools_widget", "Width")
        )
        self.pg2_graph_violinplot_orienation_label.setText(
            _translate("Plot_tools_widget", "Orientation")
        )
        self.pg2_graph_violinplot_orienation_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Vertical")
        )
        self.pg2_graph_violinplot_orienation_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Horizontal")
        )
        self.pg2_graph_violinplot_saturation_label.setText(
            _translate("Plot_tools_widget", "Saturation")
        )
        self.pg2_graph_violinplot_Inner_label.setText(
            _translate("Plot_tools_widget", "Inner")
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setItemText(
            0, _translate("Plot_tools_widget", "box")
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setItemText(
            1, _translate("Plot_tools_widget", "quartile")
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setItemText(
            2, _translate("Plot_tools_widget", "point")
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setItemText(
            3, _translate("Plot_tools_widget", "stick")
        )
        self.pg2_graph_violinplot_InnerVal_combobox.setItemText(
            4, _translate("Plot_tools_widget", "none")
        )
        self.pg2_graph_border_width_label_violinplot_2.setText(
            _translate("Plot_tools_widget", "Border width")
        )
        self.pg2_graph_cut_label_violinplot.setText(
            _translate("Plot_tools_widget", "Cut")
        )
        self.pg2_graph_scale_label_violinplot.setText(
            _translate("Plot_tools_widget", "Scale")
        )
        self.pg2_graph_scale_comboBox_violinplot.setCurrentText(
            _translate("Plot_tools_widget", "area")
        )
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            0, _translate("Plot_tools_widget", "area")
        )
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            1, _translate("Plot_tools_widget", "count")
        )
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            2, _translate("Plot_tools_widget", "width")
        )
        self.pg2_graph_saturation_label_box_plot.setText(
            _translate("Plot_tools_widget", "Saturation")
        )
        self.pg2_graph_orientation_label_barplot.setText(
            _translate("Plot_tools_widget", "Orientation")
        )
        self.pg2_graph_orientaitno_combobox_barplot.setItemText(
            0, _translate("Plot_tools_widget", "Vertical")
        )
        self.pg2_graph_orientaitno_combobox_barplot.setItemText(
            1, _translate("Plot_tools_widget", "Horizontal")
        )
        self.pg2_graph_bar_width_label_box_plot.setText(
            _translate("Plot_tools_widget", "Width")
        )
        self.pg2_graph_bar_borderwidth_label_box_plot.setText(
            _translate("Plot_tools_widget", "Border Width")
        )
        self.pg2_graph_bar_errwidth_label_box_plot.setText(
            _translate("Plot_tools_widget", "Error Width")
        )
        self.pg2_graph_bar_ci_label_box_plot.setText(
            _translate("Plot_tools_widget", "Opacity")
        )
        self.pg2_graph_flier_size_label_box_plot_box_plot.setText(
            _translate("Plot_tools_widget", "Cap size")
        )
        self.pg_2_errorBars_barPlot_bool_label.setText(
            _translate("Plot_tools_widget", "Error bars")
        )
        self.pg2_graph_width_label_box_plot.setText(
            _translate("Plot_tools_widget", "Width")
        )
        self.pg2_graph_orientation_label_boxplot.setText(
            _translate("Plot_tools_widget", "Orientation")
        )
        self.pg_2_graph_boxplot_orientation_combobox.setItemText(
            0, _translate("Plot_tools_widget", "Vertical")
        )
        self.pg_2_graph_boxplot_orientation_combobox.setItemText(
            1, _translate("Plot_tools_widget", "Horizontal")
        )
        self.pg2_graph_saturation_label_box_plot_2.setText(
            _translate("Plot_tools_widget", "Saturation")
        )
        self.pg2_graph_line_width_label_box_plot.setText(
            _translate("Plot_tools_widget", "Border width")
        )
        self.pg2_graph_cap_size_label_box_plot_box_plot.setText(
            _translate("Plot_tools_widget", "Flier size")
        )
        self.pg_2_errorBars_bool_label.setText(
            _translate("Plot_tools_widget", "Error bars")
        )
        self.pg2_load_preset_btn.setText(_translate("Plot_tools_widget", "Load Preset"))
        self.pg2_save_preset_btn.setText(_translate("Plot_tools_widget", "Save Preset"))
        self.pg2_save_as_preset_btn.setText(
            _translate("Plot_tools_widget", "Save Preset As")
        )
        self.pg2_clear_preset_btn.setText(_translate("Plot_tools_widget", "Clear"))
        self.pg_2_PlotParameteres_label.setText(
            _translate("Plot_tools_widget", "Plot Parameters ")
        )
        self.pg2_plot_btn.setText(_translate("Plot_tools_widget", "Plot"))
        self.pg2_savegraph_btn.setText(_translate("Plot_tools_widget", "Save graph"))
        self.pg2_clear_btn.setText(_translate("Plot_tools_widget", "Clear"))
        self.pg_2_statistical_analysis_groupBox.setTitle(
            _translate("Plot_tools_widget", "Statistical analysis")
        )
        self.pg_2_CollumnAnalysis_text.setText(
            _translate("Plot_tools_widget", "Collumn Analysis")
        )
        self.pg_2_statisticalAnalysis_combobox.setItemText(
            0, _translate("Plot_tools_widget", "t-test")
        )
        self.pg_2_statisticalAnalysis_combobox.setItemText(
            1, _translate("Plot_tools_widget", "One-way Anova")
        )
        self.pg_2_statisticalAnalysis_combobox.setItemText(
            2, _translate("Plot_tools_widget", "Two-way Anova")
        )
        self.Annotations_GroupBox.setTitle(
            _translate("Plot_tools_widget", "Annotations")
        )
        self.pg_2_Source_Data_btn.setText(
            _translate("Plot_tools_widget", "Source Data")
        )
        self.pg_2_Destination_Data_btn.setText(
            _translate("Plot_tools_widget", "Destination Data")
        )
        self.pg_2_Add_Link_btn.setText(_translate("Plot_tools_widget", "Add Link"))
        self.pg_2_StatisticalAnalaysis_label.setText(
            _translate("Plot_tools_widget", "Statistical Analysis")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Plot_tools_widget = QtWidgets.QWidget()
    ui = Ui_Plot_tools_widget()
    ui.setupUi(Plot_tools_widget)
    Plot_tools_widget.show()
    sys.exit(app.exec())
