# ../celer_sight_ai/UiAssets/bax_plot_settings_widget.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(355, 222)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pg_2_box_plot_settings_1 = QtWidgets.QFrame(parent=Form)
        self.pg_2_box_plot_settings_1.setObjectName("pg_2_box_plot_settings_1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.pg_2_box_plot_settings_1)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pg_2_box_plot_settings_1_left = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1
        )
        self.pg_2_box_plot_settings_1_left.setObjectName(
            "pg_2_box_plot_settings_1_left"
        )
        self.verticalLayout = QtWidgets.QVBoxLayout(self.pg_2_box_plot_settings_1_left)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pg2_graph_boxplot_pallete_style_frame = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_left
        )
        self.pg2_graph_boxplot_pallete_style_frame.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_boxplot_pallete_style_frame.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_boxplot_pallete_style_frame.setObjectName(
            "pg2_graph_boxplot_pallete_style_frame"
        )
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(
            self.pg2_graph_boxplot_pallete_style_frame
        )
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pg2_graph_pallete_style_label_boxplot = QtWidgets.QLabel(
            parent=self.pg2_graph_boxplot_pallete_style_frame
        )
        self.pg2_graph_pallete_style_label_boxplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_pallete_style_label_boxplot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_pallete_style_label_boxplot.setFont(font)
        self.pg2_graph_pallete_style_label_boxplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_pallete_style_label_boxplot.setObjectName(
            "pg2_graph_pallete_style_label_boxplot"
        )
        self.horizontalLayout_11.addWidget(self.pg2_graph_pallete_style_label_boxplot)
        self.pg_2_graph_boxplot_pallete_style_combobox = QtWidgets.QComboBox(
            parent=self.pg2_graph_boxplot_pallete_style_frame
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setMinimumSize(
            QtCore.QSize(75, 0)
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setMaximumSize(
            QtCore.QSize(75, 16777215)
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setObjectName(
            "pg_2_graph_boxplot_pallete_style_combobox"
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_boxplot_pallete_style_combobox.addItem("")
        self.horizontalLayout_11.addWidget(
            self.pg_2_graph_boxplot_pallete_style_combobox
        )
        self.verticalLayout.addWidget(self.pg2_graph_boxplot_pallete_style_frame)
        self.pg_2_color_graph_frame_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_left
        )
        self.pg_2_color_graph_frame_box_plot.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_color_graph_frame_box_plot.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_color_graph_frame_box_plot.setObjectName(
            "pg_2_color_graph_frame_box_plot"
        )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.pg_2_color_graph_frame_box_plot
        )
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pg2_graph_color_box_plot = QtWidgets.QLabel(
            parent=self.pg_2_color_graph_frame_box_plot
        )
        self.pg2_graph_color_box_plot.setMinimumSize(QtCore.QSize(0, 20))
        self.pg2_graph_color_box_plot.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_color_box_plot.setFont(font)
        self.pg2_graph_color_box_plot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_color_box_plot.setObjectName("pg2_graph_color_box_plot")
        self.horizontalLayout_2.addWidget(self.pg2_graph_color_box_plot)
        self.pg_2_graph_colors_pallete_2_box_plot = QtWidgets.QPushButton(
            parent=self.pg_2_color_graph_frame_box_plot
        )
        self.pg_2_graph_colors_pallete_2_box_plot.setMinimumSize(QtCore.QSize(60, 0))
        self.pg_2_graph_colors_pallete_2_box_plot.setMaximumSize(
            QtCore.QSize(60, 16777215)
        )
        self.pg_2_graph_colors_pallete_2_box_plot.setObjectName(
            "pg_2_graph_colors_pallete_2_box_plot"
        )
        self.horizontalLayout_2.addWidget(self.pg_2_graph_colors_pallete_2_box_plot)
        self.verticalLayout.addWidget(self.pg_2_color_graph_frame_box_plot)
        self.pg_2_graph_width_frame_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_left
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.pg_2_graph_width_frame_box_plot
        )
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pg2_graph_width_label_box_plot = QtWidgets.QLabel(
            parent=self.pg_2_graph_width_frame_box_plot
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
        self.horizontalLayout.addWidget(self.pg2_graph_width_label_box_plot)
        self.pg2_graph_width_spinBox_box_plot = QtWidgets.QSpinBox(
            parent=self.pg_2_graph_width_frame_box_plot
        )
        self.pg2_graph_width_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_width_spinBox_box_plot.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_graph_width_spinBox_box_plot.setMaximum(100)
        self.pg2_graph_width_spinBox_box_plot.setObjectName(
            "pg2_graph_width_spinBox_box_plot"
        )
        self.horizontalLayout.addWidget(self.pg2_graph_width_spinBox_box_plot)
        self.verticalLayout.addWidget(self.pg_2_graph_width_frame_box_plot)
        self.pg2_graph_boxplot_orientation_frame = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_left
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
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(
            self.pg2_graph_boxplot_orientation_frame
        )
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pg2_graph_orientation_label_boxplot = QtWidgets.QLabel(
            parent=self.pg2_graph_boxplot_orientation_frame
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_orientation_label_boxplot.setFont(font)
        self.pg2_graph_orientation_label_boxplot.setObjectName(
            "pg2_graph_orientation_label_boxplot"
        )
        self.horizontalLayout_10.addWidget(self.pg2_graph_orientation_label_boxplot)
        self.pg_2_graph_boxplot_orientation_combobox = QtWidgets.QComboBox(
            parent=self.pg2_graph_boxplot_orientation_frame
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
        self.horizontalLayout_10.addWidget(self.pg_2_graph_boxplot_orientation_combobox)
        self.verticalLayout.addWidget(self.pg2_graph_boxplot_orientation_frame)
        self.pg2_graph_saturation_frame_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_left
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
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(
            self.pg2_graph_saturation_frame_box_plot
        )
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pg2_graph_saturation_label_box_plot = QtWidgets.QLabel(
            parent=self.pg2_graph_saturation_frame_box_plot
        )
        self.pg2_graph_saturation_label_box_plot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_saturation_label_box_plot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
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
        self.horizontalLayout_5.addWidget(self.pg2_graph_saturation_label_box_plot)
        self.pg2_graph_saturation_spinBox_box_plot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_saturation_frame_box_plot
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
        self.horizontalLayout_5.addWidget(self.pg2_graph_saturation_spinBox_box_plot)
        self.verticalLayout.addWidget(self.pg2_graph_saturation_frame_box_plot)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_7.addWidget(self.pg_2_box_plot_settings_1_left)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_7.addItem(spacerItem1)
        self.pg_2_box_plot_settings_1_right_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1
        )
        self.pg_2_box_plot_settings_1_right_box_plot.setObjectName(
            "pg_2_box_plot_settings_1_right_box_plot"
        )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pg2_graph_index_frame_boxplot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_right_box_plot
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
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(
            self.pg2_graph_index_frame_boxplot
        )
        self.horizontalLayout_9.setContentsMargins(0, 0, 11, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pg2_graph_index_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_index_frame_boxplot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_index_label_violinplot.setFont(font)
        self.pg2_graph_index_label_violinplot.setObjectName(
            "pg2_graph_index_label_violinplot"
        )
        self.horizontalLayout_9.addWidget(self.pg2_graph_index_label_violinplot)
        self.pg2_graph_index_combobox_boxplot = QtWidgets.QComboBox(
            parent=self.pg2_graph_index_frame_boxplot
        )
        self.pg2_graph_index_combobox_boxplot.setMinimumSize(QtCore.QSize(80, 0))
        self.pg2_graph_index_combobox_boxplot.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pg2_graph_index_combobox_boxplot.setObjectName(
            "pg2_graph_index_combobox_boxplot"
        )
        self.pg2_graph_index_combobox_boxplot.addItem("")
        self.horizontalLayout_9.addWidget(self.pg2_graph_index_combobox_boxplot)
        self.verticalLayout_2.addWidget(self.pg2_graph_index_frame_boxplot)
        self.pg_2_graph_border_color_frame_box_plot_2 = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_right_box_plot
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.pg_2_graph_border_color_frame_box_plot_2
        )
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pg2_graph_border_color_box_plot_2 = QtWidgets.QLabel(
            parent=self.pg_2_graph_border_color_frame_box_plot_2
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_border_color_box_plot_2.setFont(font)
        self.pg2_graph_border_color_box_plot_2.setObjectName(
            "pg2_graph_border_color_box_plot_2"
        )
        self.horizontalLayout_3.addWidget(self.pg2_graph_border_color_box_plot_2)
        self.pg_2_graph_colors_pallete_1_box_plot = QtWidgets.QPushButton(
            parent=self.pg_2_graph_border_color_frame_box_plot_2
        )
        self.pg_2_graph_colors_pallete_1_box_plot.setMinimumSize(QtCore.QSize(60, 0))
        self.pg_2_graph_colors_pallete_1_box_plot.setMaximumSize(
            QtCore.QSize(60, 16777215)
        )
        self.pg_2_graph_colors_pallete_1_box_plot.setObjectName(
            "pg_2_graph_colors_pallete_1_box_plot"
        )
        self.horizontalLayout_3.addWidget(self.pg_2_graph_colors_pallete_1_box_plot)
        self.verticalLayout_2.addWidget(self.pg_2_graph_border_color_frame_box_plot_2)
        self.pg2_graph_line_width_frame_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_right_box_plot
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(
            self.pg2_graph_line_width_frame_box_plot
        )
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pg2_graph_line_width_label_box_plot = QtWidgets.QLabel(
            parent=self.pg2_graph_line_width_frame_box_plot
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
        self.horizontalLayout_4.addWidget(self.pg2_graph_line_width_label_box_plot)
        self.pg2_graph_line_width_spinBox_box_plot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_line_width_frame_box_plot
        )
        self.pg2_graph_line_width_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_line_width_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_line_width_spinBox_box_plot.setMinimum(0)
        self.pg2_graph_line_width_spinBox_box_plot.setMaximum(100)
        self.pg2_graph_line_width_spinBox_box_plot.setProperty("value", 100)
        self.pg2_graph_line_width_spinBox_box_plot.setObjectName(
            "pg2_graph_line_width_spinBox_box_plot"
        )
        self.horizontalLayout_4.addWidget(self.pg2_graph_line_width_spinBox_box_plot)
        self.verticalLayout_2.addWidget(self.pg2_graph_line_width_frame_box_plot)
        self.pg2_graph_cap_size_frame_box_plot = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_right_box_plot
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
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(
            self.pg2_graph_cap_size_frame_box_plot
        )
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(7)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pg2_graph_cap_size_label_box_plot_box_plot = QtWidgets.QLabel(
            parent=self.pg2_graph_cap_size_frame_box_plot
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
        self.horizontalLayout_6.addWidget(
            self.pg2_graph_cap_size_label_box_plot_box_plot
        )
        self.pg2_graph_cap_size_spinBox_box_plot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_cap_size_frame_box_plot
        )
        self.pg2_graph_cap_size_spinBox_box_plot.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_cap_size_spinBox_box_plot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_cap_size_spinBox_box_plot.setMinimum(0)
        self.pg2_graph_cap_size_spinBox_box_plot.setMaximum(100)
        self.pg2_graph_cap_size_spinBox_box_plot.setProperty("value", 100)
        self.pg2_graph_cap_size_spinBox_box_plot.setObjectName(
            "pg2_graph_cap_size_spinBox_box_plot"
        )
        self.horizontalLayout_6.addWidget(self.pg2_graph_cap_size_spinBox_box_plot)
        self.verticalLayout_2.addWidget(self.pg2_graph_cap_size_frame_box_plot)
        self.pg2_graph_flier_size_frame_box_plot_2 = QtWidgets.QFrame(
            parent=self.pg_2_box_plot_settings_1_right_box_plot
        )
        self.pg2_graph_flier_size_frame_box_plot_2.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg2_graph_flier_size_frame_box_plot_2.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg2_graph_flier_size_frame_box_plot_2.setObjectName(
            "pg2_graph_flier_size_frame_box_plot_2"
        )
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(
            self.pg2_graph_flier_size_frame_box_plot_2
        )
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.pg2_graph_flier_size_label_box_plot_box_plot_2 = QtWidgets.QLabel(
            parent=self.pg2_graph_flier_size_frame_box_plot_2
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_flier_size_label_box_plot_box_plot_2.setFont(font)
        self.pg2_graph_flier_size_label_box_plot_box_plot_2.setObjectName(
            "pg2_graph_flier_size_label_box_plot_box_plot_2"
        )
        self.horizontalLayout_12.addWidget(
            self.pg2_graph_flier_size_label_box_plot_box_plot_2
        )
        self.pg2_graph_flier_size_spinBox_box_plot_2 = QtWidgets.QSpinBox(
            parent=self.pg2_graph_flier_size_frame_box_plot_2
        )
        self.pg2_graph_flier_size_spinBox_box_plot_2.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_flier_size_spinBox_box_plot_2.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_flier_size_spinBox_box_plot_2.setMaximum(100)
        self.pg2_graph_flier_size_spinBox_box_plot_2.setObjectName(
            "pg2_graph_flier_size_spinBox_box_plot_2"
        )
        self.horizontalLayout_12.addWidget(self.pg2_graph_flier_size_spinBox_box_plot_2)
        self.verticalLayout_2.addWidget(self.pg2_graph_flier_size_frame_box_plot_2)
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_7.addWidget(self.pg_2_box_plot_settings_1_right_box_plot)
        self.horizontalLayout_8.addWidget(self.pg_2_box_plot_settings_1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pg2_graph_pallete_style_label_boxplot.setText(
            _translate("Form", "Palette")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            0, _translate("Form", "Custom")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            1, _translate("Form", "deep")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            2, _translate("Form", "muted")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            3, _translate("Form", "bright")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            4, _translate("Form", "dark")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            5, _translate("Form", "colorblind")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            6, _translate("Form", "Paired")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            7, _translate("Form", "BuGn")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            8, _translate("Form", "GnBu")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            9, _translate("Form", "OrRd")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            10, _translate("Form", "PuBu")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            11, _translate("Form", "YlGn")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            12, _translate("Form", "YlGnBu")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            13, _translate("Form", "YlOrBr")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            14, _translate("Form", "YlOrRd")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            15, _translate("Form", "BrBG")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            16, _translate("Form", "PiYG")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            17, _translate("Form", "PRGn")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            18, _translate("Form", "PuOr")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            19, _translate("Form", "RdBu")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            20, _translate("Form", "RdGy")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            21, _translate("Form", "RdYlBu")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            22, _translate("Form", "RdYlGn")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            23, _translate("Form", "Spectral")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            24, _translate("Form", "Blues_d")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            25, _translate("Form", "coolwarm")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            26, _translate("Form", "pastel")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            27, _translate("Form", "husl")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            28, _translate("Form", "Set1")
        )
        self.pg_2_graph_boxplot_pallete_style_combobox.setItemText(
            29, _translate("Form", "Set3")
        )
        self.pg2_graph_color_box_plot.setText(_translate("Form", "Color"))
        self.pg_2_graph_colors_pallete_2_box_plot.setText(_translate("Form", "Pallet"))
        self.pg2_graph_width_label_box_plot.setText(_translate("Form", "Width"))
        self.pg2_graph_orientation_label_boxplot.setText(
            _translate("Form", "Orientation")
        )
        self.pg_2_graph_boxplot_orientation_combobox.setItemText(
            0, _translate("Form", "Vertical")
        )
        self.pg_2_graph_boxplot_orientation_combobox.setItemText(
            1, _translate("Form", "Horizontal")
        )
        self.pg2_graph_saturation_label_box_plot.setText(
            _translate("Form", "Saturation")
        )
        self.pg2_graph_index_label_violinplot.setText(_translate("Form", "Index"))
        self.pg2_graph_index_combobox_boxplot.setItemText(0, _translate("Form", "All"))
        self.pg2_graph_border_color_box_plot_2.setText(
            _translate("Form", "Border Color")
        )
        self.pg_2_graph_colors_pallete_1_box_plot.setText(_translate("Form", "Pallet"))
        self.pg2_graph_line_width_label_box_plot.setText(
            _translate("Form", "Border width")
        )
        self.pg2_graph_cap_size_label_box_plot_box_plot.setText(
            _translate("Form", "Cap size")
        )
        self.pg2_graph_flier_size_label_box_plot_box_plot_2.setText(
            _translate("Form", "Flier Size")
        )