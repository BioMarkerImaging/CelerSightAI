# ../celer_sight_ai/UiAssets/violin_plot_settings_widget.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(376, 201)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pg_2_violinplot_plot_settings_1 = QtWidgets.QFrame(parent=Form)
        self.pg_2_violinplot_plot_settings_1.setObjectName(
            "pg_2_violinplot_plot_settings_1"
        )
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(
            self.pg_2_violinplot_plot_settings_1
        )
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pg_2_violinplot_plot_settings_1_left = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1
        )
        self.pg_2_violinplot_plot_settings_1_left.setObjectName(
            "pg_2_violinplot_plot_settings_1_left"
        )
        self.verticalLayout = QtWidgets.QVBoxLayout(
            self.pg_2_violinplot_plot_settings_1_left
        )
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pg2_graph_violinplot_pallete_style_frame = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_left
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
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_pallete_style_frame
        )
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pg2_graph_pallete_style_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_violinplot_pallete_style_frame
        )
        self.pg2_graph_pallete_style_label_violinplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_pallete_style_label_violinplot.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_pallete_style_label_violinplot.setFont(font)
        self.pg2_graph_pallete_style_label_violinplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_pallete_style_label_violinplot.setObjectName(
            "pg2_graph_pallete_style_label_violinplot"
        )
        self.horizontalLayout_11.addWidget(
            self.pg2_graph_pallete_style_label_violinplot
        )
        self.pg_2_graph_violinplot_pallete_style_combobox = QtWidgets.QComboBox(
            parent=self.pg2_graph_violinplot_pallete_style_frame
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setMinimumSize(
            QtCore.QSize(75, 0)
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setMaximumSize(
            QtCore.QSize(75, 16777215)
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setObjectName(
            "pg_2_graph_violinplot_pallete_style_combobox"
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.pg_2_graph_violinplot_pallete_style_combobox.addItem("")
        self.horizontalLayout_11.addWidget(
            self.pg_2_graph_violinplot_pallete_style_combobox
        )
        self.verticalLayout.addWidget(self.pg2_graph_violinplot_pallete_style_frame)
        self.pg_2_custom_color_graph_frame_violinplot = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_left
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.pg_2_custom_color_graph_frame_violinplot
        )
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pg2_graph_color_violinplot = QtWidgets.QLabel(
            parent=self.pg_2_custom_color_graph_frame_violinplot
        )
        self.pg2_graph_color_violinplot.setMinimumSize(QtCore.QSize(0, 0))
        self.pg2_graph_color_violinplot.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_color_violinplot.setFont(font)
        self.pg2_graph_color_violinplot.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_color_violinplot.setObjectName("pg2_graph_color_violinplot")
        self.horizontalLayout_2.addWidget(self.pg2_graph_color_violinplot)
        self.pg_2_graph_colors_pallete_2_violinplot = QtWidgets.QPushButton(
            parent=self.pg_2_custom_color_graph_frame_violinplot
        )
        self.pg_2_graph_colors_pallete_2_violinplot.setMinimumSize(QtCore.QSize(60, 0))
        self.pg_2_graph_colors_pallete_2_violinplot.setMaximumSize(
            QtCore.QSize(60, 16777215)
        )
        self.pg_2_graph_colors_pallete_2_violinplot.setObjectName(
            "pg_2_graph_colors_pallete_2_violinplot"
        )
        self.horizontalLayout_2.addWidget(self.pg_2_graph_colors_pallete_2_violinplot)
        self.verticalLayout.addWidget(self.pg_2_custom_color_graph_frame_violinplot)
        self.pg2_graph_border_width_frame_violinplot_2 = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_left
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
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(
            self.pg2_graph_border_width_frame_violinplot_2
        )
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pg2_graph_border_width_label_violinplot_2 = QtWidgets.QLabel(
            parent=self.pg2_graph_border_width_frame_violinplot_2
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
        self.horizontalLayout_10.addWidget(
            self.pg2_graph_border_width_label_violinplot_2
        )
        self.pg2_graph_border_width_spinbox_violinplot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_border_width_frame_violinplot_2
        )
        self.pg2_graph_border_width_spinbox_violinplot.setMinimumSize(
            QtCore.QSize(65, 0)
        )
        self.pg2_graph_border_width_spinbox_violinplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_border_width_spinbox_violinplot.setMinimum(0)
        self.pg2_graph_border_width_spinbox_violinplot.setMaximum(100)
        self.pg2_graph_border_width_spinbox_violinplot.setProperty("value", 100)
        self.pg2_graph_border_width_spinbox_violinplot.setObjectName(
            "pg2_graph_border_width_spinbox_violinplot"
        )
        self.horizontalLayout_10.addWidget(
            self.pg2_graph_border_width_spinbox_violinplot
        )
        self.verticalLayout.addWidget(self.pg2_graph_border_width_frame_violinplot_2)
        self.pg2_graph_violinplot_orienation_frame = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_left
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
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_orienation_frame
        )
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pg2_graph_violinplot_orienation_label = QtWidgets.QLabel(
            parent=self.pg2_graph_violinplot_orienation_frame
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
        self.horizontalLayout_9.addWidget(self.pg2_graph_violinplot_orienation_label)
        self.pg2_graph_violinplot_orienation_combobox = QtWidgets.QComboBox(
            parent=self.pg2_graph_violinplot_orienation_frame
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
        self.horizontalLayout_9.addWidget(self.pg2_graph_violinplot_orienation_combobox)
        self.verticalLayout.addWidget(self.pg2_graph_violinplot_orienation_frame)
        self.pg2_graph_violinplot_saturation_frame = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_left
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.pg2_graph_violinplot_saturation_frame
        )
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pg2_graph_violinplot_saturation_label = QtWidgets.QLabel(
            parent=self.pg2_graph_violinplot_saturation_frame
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
        self.horizontalLayout_3.addWidget(self.pg2_graph_violinplot_saturation_label)
        self.pg2_graph_saturation_spinBox_violinplot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_violinplot_saturation_frame
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
        self.horizontalLayout_3.addWidget(self.pg2_graph_saturation_spinBox_violinplot)
        self.verticalLayout.addWidget(self.pg2_graph_violinplot_saturation_frame)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_7.addWidget(self.pg_2_violinplot_plot_settings_1_left)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_7.addItem(spacerItem1)
        self.pg_2_violinplot_plot_settings_1_right = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1
        )
        self.pg_2_violinplot_plot_settings_1_right.setObjectName(
            "pg_2_violinplot_plot_settings_1_right"
        )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.pg_2_violinplot_plot_settings_1_right
        )
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pg2_graph_index_frame_violinplot = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_right
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
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(
            self.pg2_graph_index_frame_violinplot
        )
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.pg2_graph_index_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_index_frame_violinplot
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_index_label_violinplot.setFont(font)
        self.pg2_graph_index_label_violinplot.setObjectName(
            "pg2_graph_index_label_violinplot"
        )
        self.horizontalLayout_12.addWidget(self.pg2_graph_index_label_violinplot)
        self.pg2_graph_index_combobox_violinplot = QtWidgets.QComboBox(
            parent=self.pg2_graph_index_frame_violinplot
        )
        self.pg2_graph_index_combobox_violinplot.setMinimumSize(QtCore.QSize(80, 0))
        self.pg2_graph_index_combobox_violinplot.setMaximumSize(
            QtCore.QSize(80, 16777215)
        )
        self.pg2_graph_index_combobox_violinplot.setObjectName(
            "pg2_graph_index_combobox_violinplot"
        )
        self.pg2_graph_index_combobox_violinplot.addItem("")
        self.horizontalLayout_12.addWidget(self.pg2_graph_index_combobox_violinplot)
        self.verticalLayout_2.addWidget(self.pg2_graph_index_frame_violinplot)
        self.pg_2_graph_border_color_frame_violinplot_pallete = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_right
        )
        self.pg_2_graph_border_color_frame_violinplot_pallete.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )
        self.pg_2_graph_border_color_frame_violinplot_pallete.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )
        self.pg_2_graph_border_color_frame_violinplot_pallete.setObjectName(
            "pg_2_graph_border_color_frame_violinplot_pallete"
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.pg_2_graph_border_color_frame_violinplot_pallete
        )
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pg2_graph_border_color_violinplot_pallete_label = QtWidgets.QLabel(
            parent=self.pg_2_graph_border_color_frame_violinplot_pallete
        )
        self.pg2_graph_border_color_violinplot_pallete_label.setMinimumSize(
            QtCore.QSize(0, 0)
        )
        self.pg2_graph_border_color_violinplot_pallete_label.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pg2_graph_border_color_violinplot_pallete_label.setFont(font)
        self.pg2_graph_border_color_violinplot_pallete_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.pg2_graph_border_color_violinplot_pallete_label.setObjectName(
            "pg2_graph_border_color_violinplot_pallete_label"
        )
        self.horizontalLayout.addWidget(
            self.pg2_graph_border_color_violinplot_pallete_label
        )
        self.pg2_graph_border_color_violinplot_pallete_button = QtWidgets.QPushButton(
            parent=self.pg_2_graph_border_color_frame_violinplot_pallete
        )
        self.pg2_graph_border_color_violinplot_pallete_button.setMinimumSize(
            QtCore.QSize(60, 0)
        )
        self.pg2_graph_border_color_violinplot_pallete_button.setMaximumSize(
            QtCore.QSize(60, 16777215)
        )
        self.pg2_graph_border_color_violinplot_pallete_button.setObjectName(
            "pg2_graph_border_color_violinplot_pallete_button"
        )
        self.horizontalLayout.addWidget(
            self.pg2_graph_border_color_violinplot_pallete_button
        )
        self.verticalLayout_2.addWidget(
            self.pg_2_graph_border_color_frame_violinplot_pallete
        )
        self.pg2_graph_border_width_frame_violinplot = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_right
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(
            self.pg2_graph_border_width_frame_violinplot
        )
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pg2_graph_border_width_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_border_width_frame_violinplot
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
        self.horizontalLayout_4.addWidget(self.pg2_graph_border_width_label_violinplot)
        self.pg2_graph_border_width_spinBox_violinplot = QtWidgets.QSpinBox(
            parent=self.pg2_graph_border_width_frame_violinplot
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMinimumSize(
            QtCore.QSize(65, 0)
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMaximumSize(
            QtCore.QSize(65, 16777215)
        )
        self.pg2_graph_border_width_spinBox_violinplot.setMinimum(0)
        self.pg2_graph_border_width_spinBox_violinplot.setMaximum(100)
        self.pg2_graph_border_width_spinBox_violinplot.setProperty("value", 100)
        self.pg2_graph_border_width_spinBox_violinplot.setObjectName(
            "pg2_graph_border_width_spinBox_violinplot"
        )
        self.horizontalLayout_4.addWidget(
            self.pg2_graph_border_width_spinBox_violinplot
        )
        self.verticalLayout_2.addWidget(self.pg2_graph_border_width_frame_violinplot)
        self.pg2_graph_cut_frame_violinplot = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_right
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
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(
            self.pg2_graph_cut_frame_violinplot
        )
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pg2_graph_cut_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_cut_frame_violinplot
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
        self.horizontalLayout_6.addWidget(self.pg2_graph_cut_label_violinplot)
        self.pg2_graph_cut_spinBox_vil = QtWidgets.QDoubleSpinBox(
            parent=self.pg2_graph_cut_frame_violinplot
        )
        self.pg2_graph_cut_spinBox_vil.setMinimumSize(QtCore.QSize(65, 0))
        self.pg2_graph_cut_spinBox_vil.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pg2_graph_cut_spinBox_vil.setDecimals(1)
        self.pg2_graph_cut_spinBox_vil.setSingleStep(0.1)
        self.pg2_graph_cut_spinBox_vil.setObjectName("pg2_graph_cut_spinBox_vil")
        self.horizontalLayout_6.addWidget(self.pg2_graph_cut_spinBox_vil)
        self.verticalLayout_2.addWidget(self.pg2_graph_cut_frame_violinplot)
        self.pg2_graph_scale_frame_violinplot = QtWidgets.QFrame(
            parent=self.pg_2_violinplot_plot_settings_1_right
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
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(
            self.pg2_graph_scale_frame_violinplot
        )
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pg2_graph_scale_label_violinplot = QtWidgets.QLabel(
            parent=self.pg2_graph_scale_frame_violinplot
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
        self.horizontalLayout_5.addWidget(self.pg2_graph_scale_label_violinplot)
        self.pg2_graph_scale_comboBox_violinplot = QtWidgets.QComboBox(
            parent=self.pg2_graph_scale_frame_violinplot
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
        self.horizontalLayout_5.addWidget(self.pg2_graph_scale_comboBox_violinplot)
        self.verticalLayout_2.addWidget(self.pg2_graph_scale_frame_violinplot)
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_7.addWidget(self.pg_2_violinplot_plot_settings_1_right)
        self.horizontalLayout_8.addWidget(self.pg_2_violinplot_plot_settings_1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pg2_graph_pallete_style_label_violinplot.setText(
            _translate("Form", "Palette")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            0, _translate("Form", "Custom")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            1, _translate("Form", "deep")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            2, _translate("Form", "muted")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            3, _translate("Form", "bright")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            4, _translate("Form", "dark")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            5, _translate("Form", "colorblind")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            6, _translate("Form", "Paired")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            7, _translate("Form", "BuGn")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            8, _translate("Form", "GnBu")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            9, _translate("Form", "OrRd")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            10, _translate("Form", "PuBu")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            11, _translate("Form", "YlGn")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            12, _translate("Form", "YlGnBu")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            13, _translate("Form", "YlOrBr")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            14, _translate("Form", "YlOrRd")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            15, _translate("Form", "BrBG")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            16, _translate("Form", "PiYG")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            17, _translate("Form", "PRGn")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            18, _translate("Form", "PuOr")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            19, _translate("Form", "RdBu")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            20, _translate("Form", "RdGy")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            21, _translate("Form", "RdYlBu")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            22, _translate("Form", "RdYlGn")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            23, _translate("Form", "Spectral")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            24, _translate("Form", "Blues_d")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            25, _translate("Form", "coolwarm")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            26, _translate("Form", "pastel")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            27, _translate("Form", "husl")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            28, _translate("Form", "Set1")
        )
        self.pg_2_graph_violinplot_pallete_style_combobox.setItemText(
            29, _translate("Form", "Set3")
        )
        self.pg2_graph_color_violinplot.setText(_translate("Form", "Color"))
        self.pg_2_graph_colors_pallete_2_violinplot.setText(
            _translate("Form", "Pallet")
        )
        self.pg2_graph_border_width_label_violinplot_2.setText(
            _translate("Form", "Width")
        )
        self.pg2_graph_violinplot_orienation_label.setText(
            _translate("Form", "Orientation")
        )
        self.pg2_graph_violinplot_orienation_combobox.setItemText(
            0, _translate("Form", "Vertical")
        )
        self.pg2_graph_violinplot_orienation_combobox.setItemText(
            1, _translate("Form", "Horizontal")
        )
        self.pg2_graph_violinplot_saturation_label.setText(
            _translate("Form", "Saturation")
        )
        self.pg2_graph_index_label_violinplot.setText(_translate("Form", "Index"))
        self.pg2_graph_index_combobox_violinplot.setItemText(
            0, _translate("Form", "All")
        )
        self.pg2_graph_border_color_violinplot_pallete_label.setText(
            _translate("Form", "Border Color")
        )
        self.pg2_graph_border_color_violinplot_pallete_button.setText(
            _translate("Form", "Pallet")
        )
        self.pg2_graph_border_width_label_violinplot.setText(
            _translate("Form", "Border width")
        )
        self.pg2_graph_cut_label_violinplot.setText(_translate("Form", "Cut"))
        self.pg2_graph_scale_label_violinplot.setText(_translate("Form", "Scale"))
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            0, _translate("Form", "area")
        )
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            1, _translate("Form", "count")
        )
        self.pg2_graph_scale_comboBox_violinplot.setItemText(
            2, _translate("Form", "width")
        )
